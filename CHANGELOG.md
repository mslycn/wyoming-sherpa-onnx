20250206

发现识别准确率 不及 原生 funasr。经查，使用sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09模型，音频精度被转换成了8位。造成开火，成开活，等。

决定调整位FP32精度模型

sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09

run ok

https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/step2-server2-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.py


20250206

sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09

准确率低

int8 量化会将 32 位的浮点数压缩到 8 位，虽然速度飞快，但在中文这种同音词、近音词极多的语言里，会丢失音调的细微特征（这就是为什么“火”会变成“花”）。


20260205 

Hard-coded model dir for docker run test

不改动 server.py 的代码，在启动 Docker 时，把宿主机的模型目录“伪装”成server.py内的模型目录路径，直接测试。 run test ok  20260205

servery.py 直接使用 外部目录测试 MODEL_DIR = "/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09"

Hard-coded

run ok  20260205
直接将缩主机物理目录/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09 映射为docker 内的/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09  目录，进行测试
~~~
docker run -d \
  --name "funasr" \
  -v /funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09:/funasr-wyoming-sherpa-onnx/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09 \
  -p 10900:10900 \
  ghcr.io/mslycn/wyoming-funasr-onnx:main
~~~



error

- RuntimeError: No graph was found in protobuf

模型文件路径设置错误


run ok

源文件：https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/step1-server1-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.py
