# Complete real-paper example runs

Each child directory is a complete `full`-mode P0–P9 run. The examples use real canonical arXiv
papers and intentionally submit known-scooped mechanisms, so the correct collision/reviewer result
is `abandon`.

- `rag-known-scoop` — RAG / arXiv:2005.11401;
- `lora-known-scoop` — LoRA / arXiv:2106.09685;
- `clip-known-scoop` — CLIP / arXiv:2103.00020.

Every run includes the source PDF, extracted page text and hashes, claim ledger, lineage graph, gap,
idea, collision audit, independent reviewer audit, final Markdown report, report manifest, and
completed run state. Verify them without network access:

```bash
for run in examples/runs/*-known-scoop; do
  shushu next --run "$run"
done
```

To rebuild from the live arXiv PDFs, first remove only the example directory you intend to replace,
then run:

```bash
python scripts/build_real_example_runs.py --case rag-known-scoop
```

These regression controls demonstrate evidence-chain and rejection behavior. They are not
comparative-effectiveness results.
