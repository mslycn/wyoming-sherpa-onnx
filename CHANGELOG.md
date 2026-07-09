Technical Log: Wyoming-Sherpa-ONNX Integration

## June 2026: Audio Chunk Management & Silero VAD Integration
Implementing VAD (Voice Activity Detection) during the AudioChunk phase is a highly effective strategy to address low recognition accuracy and slow response latencies.

~~~
Deployment Environment: Raspberry Pi 5 (8GB RAM)

Inference Engine: sherpa-onnx

Inference Model: SenseVoiceSmall ONNX (FP32/INT16 Precision)

VAD Model: Silero VAD (A lightweight, specialized deep learning model for human speech detection)

~~~

## February 22, 2026: Repository Maintenance

Refactoring Action: Renamed the local wrapper repository from wyoming-funasr-onnx to wyoming-sherpa-onnx to correctly match the underlying runtime dependency.

## February 7, 2025: Transition to Higher Precision Weights

Observed Issue: The downstream text output accuracy fell noticeably short of native FunASR server implementations. The INT8 quantization steps stripped necessary tonal characteristics crucial for tonal languages like Chinese, leading to critical homophone errors (e.g., mapping command tokens like "开火" [Kai Huo] into "开活" [Kai Huo]).

Remediation: Shifted system configuration to prioritize higher precision weights.

Target Asset Model Matrix: sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2025-09-09 (FP32 / INT16 Precision)

Reference Scripts: Step 2 High Precision Script Source | Commit a62a070

## February 6, 2025: Initial Quantization Evaluation

Initial Quantization Target Asset: sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09

Technical Constraint: INT8 quantization compresses standard 32-bit floating-point numbers into 8-bit integers. While processing speed scales up drastically, it sacrifices granular audio frequency data, leading to degraded word error rates on homophones and pitch inflections.
