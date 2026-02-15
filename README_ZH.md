# Sherpa-ONNX wyoming协议语音识别服务器for home assistant

custom wyoming stt server for developer

基于 sherpa-onnx 和 funasr 预训练模型SenseVoiceSmall 的 wyoming stt server。

项目组合Wyoming 协议、Sherpa-ONNX 引擎 和 FunASR onnx模型。

## Prerequisites
Ensure you have home assistant installed on your machine (Linux) and that it is running. 

## Environment

~~~
ESP32-S3-Box3b   →   Wyoming stt server  →   sherpa-onnx   →   Home Assistant
        麦克风             STT服务器           语音转文字
                         （i am here）        （i use it）

~~~

Host ：rpi5 8G；Debain 12

HA   ：home assistant docker 2025.11.5

Satellite： esp32-s3-box3b，负责采集语音，检测唤醒词 (microWakeWord) + VAD。

STT Server：wyoming-funasr-onnx stt server：负责 STT;负责接收 HA传来的音频流；负责转为文本；负责输出文本；

  - 推理引擎 ：sherpa-onnx
  - 推理模型 ：SenseVoiceSmall ONNX
  - VAD     ：

## Quick Start

1. 安装Python环境

2. 安装依赖项
   
   安装sherpa-onnx: asr推理引擎

   安装wyoming==1.8.0： wyoming协议,Home Assistant 语音助手协议库

   安装numpy : 音频处理，stt server代码使用  

3. 下载语音识别模型到本地

SenseVoiceSmall FP32 onnx模型：sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09
   

5. 简易代码实现语音识别




sherpa-onnx 



output
~~~
2026-02-05 22:38:34.029 - Wyoming Sherpa-ONNX Server started on port 10900
2026-02-05 22:39:15.971 - AudioStart Event received. Processing...
2026-02-05 22:39:18.315 - AudioStop received. Processing...
2026-02-05 22:39:18.727 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:39:18.728 - 识别结果: 困火
2026-02-05 22:39:27.494 - AudioStart Event received. Processing...
2026-02-05 22:39:42.514 - AudioStop received. Processing...
2026-02-05 22:39:44.233 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:39:44.233 - 识别结果: 开火
2026-02-05 22:39:49.990 - AudioStart Event received. Processing...
2026-02-05 22:39:52.293 - AudioStop received. Processing...
2026-02-05 22:39:52.573 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:39:52.573 - 识别结果: 关火
2026-02-05 22:39:56.848 - AudioStart Event received. Processing...
2026-02-05 22:40:11.874 - AudioStop received. Processing...
2026-02-05 22:40:13.567 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:40:13.567 - 识别结果: 开火
2026-02-05 22:40:28.652 - AudioStart Event received. Processing...
2026-02-05 22:40:31.030 - AudioStop received. Processing...
2026-02-05 22:40:31.323 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:40:31.323 - 识别结果: 关火
2026-02-05 22:40:36.973 - AudioStart Event received. Processing...
2026-02-05 22:40:39.283 - AudioStop received. Processing...
2026-02-05 22:40:39.587 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:40:39.587 - 识别结果: 开火
2026-02-05 22:40:43.916 - AudioStart Event received. Processing...
2026-02-05 22:40:46.514 - AudioStop received. Processing...
2026-02-05 22:40:46.824 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:40:46.824 - 识别结果: 星期几
2026-02-05 22:40:53.770 - AudioStart Event received. Processing...
2026-02-05 22:40:56.086 - AudioStop received. Processing...
2026-02-05 22:40:56.421 - 过滤掉 SenseVoice 可能输出的情感/事件标签
2026-02-05 22:40:56.421 - 识别结果: 火开了吗


~~~


下载模型文件


## 准确率

优先保证准确率

准确率与模型精度有关

### 如何确认模型精度是 FP32
~~~
import onnx

model = onnx.load("model.onnx")
print(model.graph.input[0].type.tensor_type.elem_type)

~~~
output
~~~
1 = FP32

~~~

## Supported STT Models - RPi5 + sherpa-onnx + 中文模型可选模型 

~~~
SenseVoice Small

Paraformer
  sherpa-onnx-paraformer-zh
  sherpa-onnx-paraformer-zh-small

Zipformer
  sherpa-onnx-streaming-zipformer-fr-kroko

Whisper tiny/large
~~~

### 3.下载语音识别模型到本地 下载模型文件 Download model 

1. SenseVoice多语言语音理解模型分为：SenseVoice-Small、SenseVoice-Large
  
SenseVoice-Small   last updated:2024-09-26
   
https://www.modelscope.cn/models/iic/SenseVoiceSmall

Note

SenseVoice开源模型是多语言音频理解模型，具有包括语音识别、语种识别、语音情感识别，声学事件检测能力。

3. sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09 - SenseVoiceSmall FP32 onnx模型

SenseVoiceSmall 官方模型来源

https://k2-fsa.github.io/sherpa/onnx/sense-voice/index.html

Note

模型说明: SenseVoiceSmall 模型来自 FunAudioLLM/SenseVoice 项目，已转换为 ONNX 格式用于 sherpa-onnx

2.download

~~~
cd /funasr-wyoming-sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
~~~

~~~
raspberrypi:/funasr-wyoming-sherpa-onnx# tree -L 2 ./sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09
./sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09
├── model.onnx  ← FP32
├── README.md
├── test_wavs
│   ├── en.wav
│   ├── ja.wav
│   ├── ko.wav
│   ├── yue-0.wav
│   ├── yue-10.wav
│   ├── yue-11.wav
│   ├── yue-12.wav
│   ├── yue-13.wav
│   ├── yue-14.wav
│   ├── yue-15.wav
│   ├── yue-16.wav
│   ├── yue-17.wav
│   ├── yue-1.wav
│   ├── yue-2.wav
│   ├── yue-3.wav
│   ├── yue-4.wav
│   ├── yue-5.wav
│   ├── yue-6.wav
│   ├── yue-7.wav
│   ├── yue-8.wav
│   ├── yue-9.wav
│   ├── yue.wav
│   └── zh.wav
└── tokens.txt

2 directories, 26 files

~~~

source: https://k2-fsa.github.io/sherpa/onnx/sense-voice/pretrained.html#sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17


流式模型 Zipformer 小米团队

### Docker

~~~
docker run --rm -m 4g ghcr.io/mslycn/funasr-wyoming:main
~~~


## Speed on rpi5 cpu

- 4 threads



## server.py

SenseVoiceSmall + sherpa-onnx 标准加载方式及完整最小可运行示例
~~~
import sherpa_onnx

recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
    model="./sense-voice/model.onnx",
    tokens="./sense-voice/tokens.txt",
    use_itn=True,
)

stream = recognizer.create_stream()

stream.accept_waveform(16000, samples)

recognizer.decode_stream(stream)

print(stream.result.text)
~~~

### sherpa-onnx VAD (Voice Activity Detection) 方案

AudioChunk.is_type(event.type):  做vad检查  - 优化点

单VAD检测方案 - VAD (Voice Activity Detection)

在 sherpa-onnx 框架下，在 AudioChunk 阶段做 VAD 检查是官方推荐的专业做法。

sherpa-onnx 内部已经集成了高性能的 Silero VAD（目前业界公认最准的 CPU 级 VAD 模型），直接调用 sherpa_onnx 的接口即可实现流式截断。

- 工作原理

~~~
AudioChunk
    ↓
用numpy转换为模型所要求的音频格式
    ↓
VAD 检测
    ↓
if speech:
    送入 ASR
else:
    丢弃

~~~

连续 N 帧静音 300ms 静音 → 结束一句话


在 AudioChunk 做 VAD 优点

极速响应：用户说完话（比如“开火”），服务端 VAD 检测到静音（例如 500ms），立刻启动推理。而不需要等 ESP32 那个不靠谱的 15 秒超时。

提升准确率：SenseVoice 等模型在处理带有长段噪音的音频时容易产生“幻觉”（如你遇到的“开火”变“快活”）。VAD 可以在喂给模型前就把末尾的垃圾噪音切掉。

节省资源：一旦检测到静音，立刻断开连接。

缺点：

is_speech_detected()容易受背景里微弱的电视声、风扇声干扰（Silero 有时太灵敏）

is_speech_detected()只检测“这一刻”有没有人在说话。is_speech_detected()是否检测到人声会随说话停顿、背景噪音让 VAD is_speech_detected()在 True 和 False快速切换。


### Endpoint detected - sherpa-onnx 端点检测 (Endpointing Detection) 方案 - 

sherpa-onnx 的端点检测 (Endpointing) Silero VAD + 能量辅助双保险方案

Endpoint Detection（端点检测）是判断一句话 什么时候开始， 判断一句话 什么时候结束，不是逐帧判断有没有语音。


- 工作原理



VAD + 能量的双保险方案：

端点检测 (Endpointing)：基于 VAD 的结果，结合时间规则。例如：“如果用户停止说话超过 0.8 秒，则判定为一句话结束”。

能量门限：强制要求声音必须有一定的“物理强度”，只有当你对着麦克风说话时才会被标记为 True。

关键技术点：

Endpoint Detection 是 sherpa-onnx 提供的能力

不是 SenseVoice 模型自己实现的



sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17模型 模型原始说明 https://k2-fsa.github.io/sherpa/onnx/sense-voice/pretrained.html#sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17

从modelscope 的镜像库下载：https://modelscope.cn/models/pengzhendong/sherpa-onnx-sense-voice-zh-en-ja-ko-yue

Download
~~~
cd /path/to/sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.tar.bz2
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.tar.bz2

~~~

Download silero-vad

Speech recognition from a microphone with VAD

~~~
silero_vad.onnx- exported： by k2-fsa https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
silero_vad v5： wget https://github.com/snakers4/silero-vad/raw/refs/tags/v5.0/files/silero_vad.onnx
~~~
source：https://k2-fsa.github.io/sherpa/onnx/vad/silero-vad.html#download-models-files

FunASR 官方支持使用 funasr-export 工具将模型导出为 ONNX 格式

~~~
# 安装导出工具
pip install -U "funasr[export]"
# 导出模型
python -m funasr.export.export_model --model-name iic/SenseVoiceSmall --export-dir ./export --type onnx

~~~

https://modelscope.cn/models/xiaowangge/sherpa-onnx-sense-voice-small

参考https://github.com/k2-fsa/sherpa-onnx/blob/master/scripts/sense-voice/export-onnx.py脚本，完成 onnx 模型导出

~~~
# 安装 ModelScope
pip install modelscope

# SDK 模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('xiaowangge/sherpa-onnx-sense-voice-small')

~~~



