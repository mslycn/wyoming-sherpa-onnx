
基于 sherpa-onnx 和 funasr 预训练模型SenseVoiceSmall 的 wyoming stt server。

项目组合Wyoming 协议、Sherpa-ONNX 引擎 和 FunASR 模型。


下载模型文件


## 准确率

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

### 下载模型文件 Download model
~~~
cd /funasr-wyoming-sherpa-onnx

wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.tar.bz2
~~~

~~~
raspberrypi:/funasr-wyoming-sherpa-onnx# tree -L 2 ./sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09
./sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09
├── model.onnx
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

## Speed on rpi5 cpu

- 4 threads
