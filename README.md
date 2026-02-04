# wyoming-funasr-onnx

Wyoming protocol server for the funasr speech to text system.

## Features

Non-Streaming WebSocket Server

CPU-only version of sherpa-onnx

## Docker Image
~~~
docker run -it -p 10300:10300 -v /path/to/local/data:/data ghcr.io/mslycn/wyoming-funasr-onnx:main \
    --model SenseVoiceSmall --language zh
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
