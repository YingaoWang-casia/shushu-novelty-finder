# Trend Matrix

Do not output only a list of papers. Convert papers into trends.

## Literature timeline format

```text
Stage:
Years:
Representative papers:
Main task framing:
Main methods:
Datasets and metrics:
What became saturated:
What remained weak:
```

## Trend matrix columns

```text
Time period | Representative papers | Task shift | Method shift | Dataset/metric shift | Open gap
```

## Required analysis axes

- Task definition: how the problem statement changed.
- Method route: what families of methods became dominant.
- Dataset: whether data is diverse, realistic, multilingual, multimodal, noisy, or domain-specific.
- Metric: whether metrics actually reflect real-world success.
- System setting: offline benchmark, online system, real-time system, edge device, multi-agent system, etc.
- Reproducibility: whether code, data, and evaluation scripts exist.

## Reviewer-style checks

Ask:

- Is the field solving the same task repeatedly with minor variants?
- Are papers sharing the same weak benchmark?
- Are reported gains meaningful or only incremental?
- Are there missing negative results?
- Is the apparent gap technically important or merely unattempted?
