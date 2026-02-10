# wyoming-funasr-onnx

Wyoming protocol server for the funasr speech to text system.

Wyoming FunASR ONNX is a lightweight Speech-to-Text (STT) server that bridges FunASR ONNX models with the Wyoming protocol, enabling seamless integration with Home Assistant voice assistant.

It provides fast, local, and privacy-friendly speech recognition powered by FunASR ONNX models.

## Features

- Full Wyoming protocol compliance

- Non-Streaming WebSocket Server

- ASREngine: CPU-only version of sherpa-onnx

- Models: For Chinese users FunASR ONNX models->SenseVoiceSmall->sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09
  

## Prerequisites

- A Linux machine  with Docker and Docker Compose installed.
- A static local IP address for the host machine. 

## System Architecture

~~~
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  HA WebSocket   │    │  Wyoming protocol│    │   sherpa-onnx   │
│   Client        │◄──►│  ASR   Server    │◄──►│   Engine        │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ HAonnection      │    │  Model Files    │
                       │  Manager         │    │  • SenseVoice   │
                       │                  │    │  • Silero VAD   │
                       └──────────────────┘    └─────────────────┘

~~~

## Project structre
~~~
funasr-wyoming-funasr-onnx/
├── Dockerfile
├── requirements.txt
├── server.py
├── entrypoint.sh
├── models/
│   └── sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09
└── .github/
    └── workflows/
        └── docker-publish.yml

~~~

## How to use

step 1. Pull the Docker Image 
~~~
docker pull ghcr.io/mslycn/wyoming-funasr-onnx:latest
~~~

step 2. download pre-trained  model(SenseVoice)

Create Necessary Folders 

~~~
mkdir -p funasr-wyoming-sherpa-onnx
~~~

~~~
cd /funasr-wyoming-sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2

~~~

step 3.  Run the Container 

Docker run

~~~
docker run -d \
  --name wyoming-funasr-onnx \
  -p 10300:10300 \
  ghcr.io/mslycn/wyoming-funasr-onnx:latest

~~~

step 4. Integration with Home Assistant 

step 5. Voice Assistant


## Docker Image  Debug

~~~
docker pull ghcr.io/mslycn/wyoming-funasr-onnx:main
~~~

~~~
docker run -it -p 10300:10300 -v /path/to/local/data:/data ghcr.io/mslycn/wyoming-funasr-onnx:main \
    --model SenseVoiceSmall --language zh
~~~

~~~
docker run -d \
  --name "funasr" \
  -v /funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09:/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09 \
  -p 10900:10900 \
  ghcr.io/mslycn/wyoming-funasr-onnx:main
~~~


## Dockerfile

Install system dependencies

install the Python package sherpa-onnx
~~~
pip3 install sherpa-onnx sherpa-onnx-bin
~~~




useful links

Install the Python package sherpa-onnx 

https://k2-fsa.github.io/sherpa/onnx/python/install.html#method-1-from-pre-compiled-wheels-cpu-only

download model (sense-voice small)

https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models

https://k2-fsa.github.io/sherpa/onnx/sense-voice/index.html


https://github.com/mawwalker/stt-server

AudioChunk Event

https://github.com/ptbsare/sherpa-onnx-tts-stt

