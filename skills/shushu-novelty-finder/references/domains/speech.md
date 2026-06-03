# Domain Pack: Speech and Spoken Dialogue

Use this pack when the topic is speech, audio, spoken dialogue, VAD, endpointing, turn-taking, interruption, backchannel, or full-duplex interaction.

## Scope questions

Ask or infer:

- Is the target task VAD, endpointing, turn-taking prediction, interruption handling, backchannel detection, or full-duplex dialogue control?
- Is the input audio, transcript, multimodal signal, or streaming state?
- Is the output binary, multi-class, timestamp, policy action, or response timing?
- Is the setting offline benchmark or real-time interaction?
- Does the user have access to audio data and annotation resources?

## Common tasks

- voice activity detection;
- endpoint detection;
- turn-taking prediction;
- response timing prediction;
- interruption detection;
- backchannel detection;
- full-duplex dialogue policy;
- streaming speech agent evaluation.

## Common metrics

- frame-level precision, recall, F1;
- endpointing latency;
- false cutoff rate;
- false wait rate;
- turn prediction accuracy;
- interruption detection precision and recall;
- response timing delay;
- user-perceived smoothness;
- real-time factor.

## Common weak novelty

- only changing a threshold;
- testing one new model without streaming constraints;
- evaluating only clean offline audio;
- ignoring latency, false cutoff, and false wait;
- mixing ASR quality with turn-taking quality.

## Promising medium novelty

- benchmark realistic short utterances, pauses, noise, overlap, and incomplete speech;
- separate semantic completion from acoustic silence;
- evaluate real-time turn decisions rather than offline labels only;
- create a failure taxonomy for endpointing and turn-taking;
- compare transcript-only, audio-only, and audio-text settings.

## Strong novelty candidates

Strong ideas need proof, but possible directions include:

- a new task formulation for full-duplex turn control;
- a benchmark that changes model ranking under streaming constraints;
- a policy-level evaluation protocol for when a voice agent should speak, wait, or interrupt;
- a diagnostic framework separating VAD error, ASR error, semantic incompleteness, and dialogue policy error.

## Baseline reminders

Include:

- simple silence threshold baseline;
- WebRTC or common VAD baseline if applicable;
- transcript-only baseline;
- audio-only baseline;
- audio-text fusion baseline;
- streaming versus offline comparison;
- latency and real-time factor reporting.
