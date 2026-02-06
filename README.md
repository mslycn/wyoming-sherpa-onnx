# wyoming-funasr-onnx

Wyoming protocol server for the funasr speech to text system.

Wyoming FunASR ONNX is a lightweight Speech-to-Text (STT) server that bridges FunASR ONNX models with the Wyoming protocol, enabling seamless integration with Home Assistant voice assistant.

It provides fast, local, and privacy-friendly speech recognition powered by FunASR ONNX models.

## Features

Non-Streaming WebSocket Server

CPU-only version of sherpa-onnx

Multilingual FunASR ONNX models： SenseVoice Small->sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09

## How to use

step 1. Docker pull
~~~

~~~

step 2. download pre-trained  model(SenseVoice)

step 3. Docker run
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
 install the Python package sherpa-onnx
~~~
pip3 install sherpa-onnx sherpa-onnx-bin
~~~




useful links

https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models

Install the Python package sherpa-onnx 

https://k2-fsa.github.io/sherpa/onnx/python/install.html#method-1-from-pre-compiled-wheels-cpu-only
