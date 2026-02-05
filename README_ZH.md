
基于 sherpa-onnx 和 funasr 预训练模型SenseVoiceSmall 的 wyoming stt server。

项目组合Wyoming 协议、Sherpa-ONNX 引擎 和 FunASR 模型。


下载模型文件



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

### 下载模型文件
~~~
cd /funasr-wyoming-sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
~~~

source: https://k2-fsa.github.io/sherpa/onnx/sense-voice/pretrained.html#sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17

## Speed on rpi5 cpu
