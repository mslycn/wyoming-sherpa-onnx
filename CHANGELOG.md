

20250206

## 使用sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09模型  FP16 / INT8

sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09

准确率低

int8 量化会将 32 位的浮点数压缩到 8 位，虽然速度飞快，但在中文这种同音词、近音词极多的语言里，会丢失音调的细微特征（这就是为什么“火”会变成“花”）。


20260205 

## Hard-coded model dir for docker run test

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



## 20250207 调整为使用FP32精度模型

### Old
sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09

### New

sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09

发现识别准确率 不及 原生 funasr。经查，使用sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09模型，音频精度被转换成了8位。造成开火，成开活，等。

决定调整为FP32精度模型

sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09

run ok

https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/step2-server2-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.py

server.py

https://github.com/mslycn/wyoming-funasr-onnx/commit/a62a07064356108470b85c46d97993a6d6c99678

##  20260608  AudioChunk.is_type(event.type):  AudioChunk 处理函数中做vad检查

在 AudioChunk 阶段做 VAD 是解决“识别不准”和“响应慢”的方案。

在树莓派 5 上，使用 sherpa-onnx 官方支持的 Silero VAD。它是一个专门检测“人声”的轻量级深度学习模型。

推理引擎 ：sherpa-onnx

推理模型 ：SenseVoiceSmall ONNX 

VAD      : Silero VAD      





## 使用 sherpa-onnx 的端点检测 (Endpointing)  Silero VAD + 能量辅助

原理：每次收到 AudioChunk 时，都会实时检测音频。如果连续 500ms 没有人声，就提前结束录音并执行识别。

需要从 sherpa-onnx 仓库（https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models） 下载 silero_vad.onnx

~~~
cd /your/model/path
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
~~~

VAD 建议设置 500ms 到 800ms 的静音阈值。太短（比如 200ms）可能会在你说话停顿换气时误断。

内存占用：RPi5 8G 运行这两个模型（SenseVoice + Silero VAD）总共约占 1.5GB 左右内存



