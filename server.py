
#!/usr/bin/env python3
"""
Wyoming Protocol Server Test

一个基于 Wyoming 协议 的语音转文字（STT）服务端脚本，使用阿里开源的 SenseVoiceSmall onnx模型。

step 1. Install sherpa-onnx
pip3 install sherpa-onnx

pip3 install numpy

pip3 install Wyoming

step 2. server.py

from funasr_onnx import SenseVoiceSmall

"""

import os
import asyncio
import io

import numpy as np
import logging
import datetime
import time
import re




# Wyoming protocol 1.8.0 imports
from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioStart, AudioChunk, AudioStop
from wyoming.event import Event
from wyoming.info import (
    AsrModel,
    AsrProgram,
    Attribution,
    Describe,
    Info,
)
from wyoming.server import AsyncTcpServer, AsyncEventHandler


# ---------------- 1. 日志设置 ----------------

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_LOGGER = logging.getLogger("wyoming-funasr-onnx")


import sherpa_onnx
_LOGGER.info(f"Sherpa-ONNX Version: {sherpa_onnx.__version__}")


# ---------------- 2. 初始化 Sherpa-ONNX----------------
# 在脚本启动时加载一次，确保响应速度
# --------------------------------
_LOGGER.info("%s - start excute sherpa-onnx" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])



# load model
start_model = time.time()

# 请确保路径指向你下载的模型文件夹
# /data/models
# MODEL_DIR = "/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09"
MODEL_DIR = "/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09"

def create_recognizer():
    _LOGGER.info(f"Loading Sherpa-ONNX model from {MODEL_DIR}")
    # 参数配置
    recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=f"{MODEL_DIR}/model.onnx",
        tokens=f"{MODEL_DIR}/tokens.txt",
        num_threads=4,      # 适配树莓派核心数

        debug=False,
    )
    return recognizer

# 全局初始化模型
recognizer = create_recognizer()

end_model = time.time()
load_time_ms = (end_model - start_model) * 1000
print(f'加载模型SenseVoiceSmall耗时 {load_time_ms:.2f} 毫秒')







# ---------------- 3. 事件处理器 ----------------
class CustomSTTHandler(AsyncEventHandler):

    """
    Event handler for clients.
    Handle a single Wyoming TCP connection for ASR.

    Expects Describe? → Transcribe? → AudioStart → AudioChunk* → AudioStop,
    and responds with Info (optional) and a final Transcript.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_buffer = bytearray()

        self.processed = False
        # 1. 初始化 VAD (使用 sherpa_onnx 内置的 Silero VAD)
        # 需确保 MODEL_DIR 下有 silero_vad.onnx
 

        # ---add vad： step 1. 初始化 VAD 配置 (针对 1.12.23 API) ---
        vad_config = sherpa_onnx.VadModelConfig()
        # 必须逐项赋值给嵌套的 silero_vad 对象
        vad_config.silero_vad.model = f"{MODEL_DIR}/silero_vad.onnx"
        vad_config.silero_vad.min_speech_duration = 0.25  # 用户必须连续说话超过 0.25秒，VAD 才会把状态从 False 改为 True
        vad_config.silero_vad.min_silence_duration = 0.5  # 0.5秒静音即截断
        vad_config.silero_vad.window_size = 512
        
        vad_config.sample_rate = 16000
        vad_config.num_threads = 1
        
        # 实例化真正的检测器
        self.vad = sherpa_onnx.VoiceActivityDetector(vad_config, buffer_size_in_seconds=30)

        self.was_speaking = False

    async def handle_event(self, event: Event) -> bool:
        """Handle Wyoming protocol events"""

        # 这一行能让你看到客户端发出的每一个event
        # _LOGGER.info(f"Received event type: {event.type}")

        # 1. Handle service discovery 
        if Describe.is_type(event.type):
            _LOGGER.info("Describe request received：Received Describe event from client")
        
            
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - Describe request received：Received Describe event from ha client")
             # see:https://github.com/Johnson145/voxtral_wyoming/blob/main/src/voxtral_wyoming/server.py
            attribution = Attribution(
                 name="FunASR Wyoming",
                 url="https://github.com/mslycn/wyoming-funasr",
             )
            asr_model = AsrModel(
                  name="SenseVoiceSmall",
                  attribution=attribution,
                  installed=True,
                  description="Offline STT with FunASR SenseVoiceSmall",
                  version="1.0.0",
                  languages=["zh"],
             )
            asr_program = AsrProgram(
                  name="funasr-wyoming-sherpa_onnx",
                  attribution=attribution,
                  installed=True,
                  description="Wyoming-compatible FunASR STT service",
                  version="1.0.0",
                  models=[asr_model],
                  supports_transcript_streaming=False,
             )

   
            info = Info(asr=[asr_program])
            await self.write_event(info.event())
            return True

        # 2. Handle audio stream start
        if AudioStart.is_type(event.type):
            _LOGGER.info("AudioStart received")
 
            self.audio_buffer.clear()

            # add vad: step 2
            self.processed = False
            self.vad.reset()
 
            return True

        # 3. Handle audio data chunks
        if AudioChunk.is_type(event.type):
            chunk = AudioChunk.from_event(event)
            self.audio_buffer.extend(chunk.audio)

            #  如果音频特别长，每 3 秒打印一次状态，保持连接活跃
            if len(self.audio_buffer) % 48000 == 0:
                _LOGGER.info(f"AudioChunk Event received.正在接收音频... 已累积 {len(self.audio_buffer)/32000:.1f} 秒")

            # 转换音频供 VAD 检查
            audio_f32 = np.frombuffer(chunk.audio, dtype=np.int16).astype(np.float32) / 32768.0
            
            # 喂给 VAD
            self.vad.accept_waveform(audio_f32)      

            # --- 2. 检查语音结束点 (Endpoint) ---
            # 如果检测到说话已经开始，且现在检测到了结束点
            # if self.vad.is_speech_detected():
               # _LOGGER.info("VAD: 检测到检测到人声")
                # await self._process_audio()
                # 我们不再关闭连接，而是标记已处理。AudioStop 到达时会正常退出。
                # 或者直接 return False 强制客户端断开，看你需求。
     
              
                # 如果检测到用户停止说话，主动发送一个 AudioStop 事件来触发最终识别结果返回
                # await self.write_event(AudioStop().event())
           
            self.was_speaking = False

            currently_speaking = self.vad.is_speech_detected()

            _LOGGER.info(f"Speech State: {currently_speaking}")

            if self.vad.is_speech_detected():
                 if not self.was_speaking:
                      _LOGGER.info("Started speaking!")
                      self.was_speaking = True
            else:
                  if not currently_speaking and self.was_speaking:
                        _LOGGER.info("User stopped speaking.")
                        # This is where you would trigger your STT or GPT response
                        await self.write_event(AudioStop().event())
                        self.was_speaking = False
                        self.vad.reset()  # Optional: clear the buffer for the next sentence
  
            return True


 # ---------------- AudioStop (Optimized with NumPy) ----------------
        # 4. Handle audio stream end
        if AudioStop.is_type(event.type):
            _LOGGER.info(f"AudioStop Event received.Processing {len(self.audio_buffer)} bytes of audio...")
   

            if not self.audio_buffer:
                await self.write_event(Transcript(text="").event())
                return False

            try:
                # Direct NumPy conversion: Bytes -> Int16 -> Float32 Normalization
                audio = np.frombuffer(self.audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0

                # 推理过程            
                stream = recognizer.create_stream()
                stream.accept_waveform(16000, audio)
                recognizer.decode_stream(stream)
                
                res = stream.result.text

                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - 过滤掉 SenseVoice 可能输出的情感/事件标签")
                if res and len(res) > 0:
                    result_text = res

                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - 识别结果原文: {result_text}")
                    # Regex to strip emotional/event tags like <|HAPPY|>
                    result_text = re.sub(r'<\|.*?\|>', '', result_text).strip()
                else:
                    result_text = ""
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - 接收到的音频为空...")     
          
                _LOGGER.info(f"识别结果 Result: {result_text}")
               
                await self.write_event(Transcript(text=result_text).event())
                
            except Exception as e:
                _LOGGER.error(f"识别过程出错 Inference error: {e}", exc_info=True)
                
                await self.write_event(Transcript(text="").event())
            
            self.audio_buffer.clear()
            return False # Close session after transcription

        return True

        # Handle transcription requests
        if Transcribe.is_type(event.type):
            _LOGGER.info("Transcribe Event received.ha客户端请求识别为文字...")
  
            return True


async def main():
    server = AsyncTcpServer(host="0.0.0.0", port=10900)
    _LOGGER.info("Wyoming Sherpa-ONNX Server started on port 10900")
   
    await server.run(CustomSTTHandler)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
