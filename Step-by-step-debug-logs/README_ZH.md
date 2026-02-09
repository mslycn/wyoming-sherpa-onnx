- step 01. 实现wyoming协议框架

  https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/serverv01_onlyWyoming%20Protocol%20version%201.8.0.py

- step 02.处理Describe Event，使其能被home assistant wyoming integration 添加 

https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/serverv02_onlyWyoming%20Protocol%20version%201.8.0.py

- step 1. 加载sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09模型，进行语音识别

step1-server1-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.py

sherpa-onnx + sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09 

run ok , 识别准确率欠佳


https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/step1-server1-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.py

- step 2. Use sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09 instead of sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09
  
改为加载sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09模型进行语音识别。用 FP32 的 model.onnx 提高识别率准确度

  step2-server1-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.py

sherpa-onnx + sherpa-onnx-sense-voice-zh-en-ja-ko-yue2025-09-09

run ok , 识别准确率较佳

https://github.com/mslycn/wyoming-funasr-onnx/blob/main/Step-by-step-debug-logs/step2-server2-sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09.py
