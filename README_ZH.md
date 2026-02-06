
基于 sherpa-onnx 和 funasr 预训练模型SenseVoiceSmall 的 wyoming stt server。

项目组合Wyoming 协议、Sherpa-ONNX 引擎 和 FunASR onnx模型。

## Environment
rpi5 8G

esp32-s3-box3b：负责语音采集

home assistant docker 2025.11.5

wyoming-funasr-onnx(RPi5)：负责 STT

Wyoming-Piper (RPi5)：负责 TTS

## Quick Start

1. 安装Python环境

2. 安装依赖项
   
   安装sherpa-onnx

   安装wyoming==1.8.0： wyoming协议

   安装numpy : 音频处理   

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

### 3.下载语音识别模型到本地 下载模型文件 Download model  

1. sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09 - SenseVoiceSmall FP32 onnx模型

SenseVoiceSmall 官方模型来源

https://k2-fsa.github.io/sherpa/onnx/sense-voice/index.html

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


FunASR 官方支持使用 funasr-export 工具将模型导出为 ONNX 格式

~~~
# 安装导出工具
pip install -U "funasr[export]"
# 导出模型
python -m funasr.export.export_model --model-name iic/SenseVoiceSmall --export-dir ./export --type onnx

~~~
