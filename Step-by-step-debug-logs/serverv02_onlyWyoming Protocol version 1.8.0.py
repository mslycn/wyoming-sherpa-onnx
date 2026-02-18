#!/usr/bin/env python3
"""
Wyoming Protocol ASR Server with Wyoming Protocol info
can connect to home assistant by Wyoming Protocol

Features:
- add return Wyoming Protocol info
"""
import asyncio
import logging

from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioStart, AudioChunk, AudioStop
from wyoming.event import Event
from wyoming.info import AsrModel, AsrProgram, Describe, Info
from wyoming.server import AsyncTcpServer, AsyncEventHandler

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_LOGGER = logging.getLogger("wyoming_stt")


class CustomSTTHandler(AsyncEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_buffer = bytearray()

    async def handle_event(self, event: Event) -> bool:
        if Describe.is_type(event.type):
            _LOGGER.info("Describe request received：Received Describe event from client")
        
            print(f'Describe request received：Received Describe event from client')

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
                  name="funasr-wyoming",
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

        if AudioStart.is_type(event.type):
            _LOGGER.info("AudioStart received")
            self.audio_buffer.clear()
            return True

        if AudioChunk.is_type(event.type):
            _LOGGER.info("AudioChunk received")
            chunk = AudioChunk.from_event(event)
            self.audio_buffer.extend(chunk.audio)
            return True

        if AudioStop.is_type(event.type):
            _LOGGER.info("AudioStop received. Processing...")
            result_text = "This is a dummy transcription"
            await self.write_event(Transcript(text=result_text).event())
            return True

        if Transcribe.is_type(event.type):
            _LOGGER.info("Transcribe received")
            # 如果你想在 Transcribe 时触发识别，可以在这里执行
            return True

        return True


async def main():
    server = AsyncTcpServer(host="0.0.0.0", port=10900)
    _LOGGER.info("Wyoming STT Server started on port 10900")

    await server.run(CustomSTTHandler)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
