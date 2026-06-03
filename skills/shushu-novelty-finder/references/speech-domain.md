# Speech Domain Guide

Use for speech, audio, and spoken dialogue research topics.

Subdirections: VAD, endpointing, turn-taking, interruption, backchannel, spoken dialogue, full-duplex interaction, speech agent evaluation.

Metrics: frame-level F1, event F1, latency, false alarm, miss rate, interruption accuracy, response timing, user-perceived naturalness.

Fake novelty patterns:

- mixing ASR, VAD, diarization, and dialogue timing without defining the task;
- evaluating only offline accuracy for a real-time problem;
- ignoring latency and endpoint delay;
- using private data without a reproducible benchmark plan;
- proposing a new model without error analysis.

Minimum baselines: rule-based endpointing, classical VAD, neural VAD, simple timing heuristic, recent turn-taking models when relevant.

Strong idea pattern: define a realistic real-time evaluation setting where timing, interruption, and response decision quality are measured separately.
