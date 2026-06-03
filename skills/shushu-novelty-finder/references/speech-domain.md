# Speech Domain Guide

Use this guide for speech, audio, and spoken dialogue research topics. It helps prevent fake novelty by forcing the Skill to separate ASR, VAD, diarization, timing, and dialogue-policy claims.

## Subdirections

- VAD
- endpointing
- turn-taking
- interruption
- backchannel
- spoken dialogue
- full-duplex interaction
- speech agent evaluation

## Metrics

- frame-level F1
- event F1
- latency
- false alarm
- miss rate
- interruption accuracy
- response timing

## Fake Novelty

- mixing ASR, VAD, diarization, dialogue timing without defining task
- evaluating offline accuracy for real-time problem
- ignoring latency
- relying on private data without reproducible benchmark plan

## Minimum Baselines

- rule-based endpointing
- classical VAD
- neural VAD
- simple timing heuristic
- recent turn-taking models when relevant

## Scope-Lock Questions

Ask these when `speech turn-taking` or `speech agent evaluation` is too broad:

1. Is the task VAD, endpointing, turn-taking, interruption handling, backchannel prediction, or full-duplex response timing?
2. Is the evaluation offline, streaming, or real-time interactive?
3. Which latency budget matters: frame-level decision, endpoint delay, response delay, or user-perceived timing?
4. Are datasets public and reproducible, or private and only useful for a technical report?
5. Which baseline family is mandatory: rules, classical VAD, neural VAD, timing heuristic, or recent turn-taking model?

## Strong Idea Pattern

A stronger idea defines a realistic real-time evaluation setting where timing, interruption, and response decision quality are measured separately.

Required evidence:

- task boundary separated from ASR and diarization;
- latency and false-alarm metrics included;
- public benchmark or reproducible dataset plan;
- baseline suite covering rules, VAD, and timing heuristics;
- clear threat-to-validity discussion for private or synthetic data.
