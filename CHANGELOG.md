20260205 

Hard-coded model dir for docker run test

不改动 server.py 的代码，在启动 Docker 时，把宿主机的模型目录“伪装”成server.py内的模型目录路径，直接测试。 run test ok  20260205

servery.py 直接使用 外部目录测试 MODEL_DIR = "/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09"

Hard-coded

run ok  20260205

~~~
docker run -d \
  --name "funasr" \
  -v /funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09:/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09 \
  -p 10900:10900 \
  ghcr.io/mslycn/wyoming-funasr-onnx:main
~~~
