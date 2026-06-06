# Chinese-English Translation Mode

Use this reference when the user asks for 中英文互转, 翻译, translate, bilingual wording, academic polishing across Chinese and English, or conversion of research writing between Chinese and English.

## Routing

Default direction:

- Chinese source text -> English.
- English source text -> Chinese.
- Mixed source text -> translate the main prose into the target language requested by the user. If no target is stated, preserve technical English terms and translate the surrounding prose into the more useful research-writing language.

If the user asks for "中英文互转" but provides no source text, ask for the text and say the skill supports:

- Chinese -> English academic translation;
- English -> Chinese academic translation;
- bilingual side-by-side output;
- literal translation plus polished academic version;
- terminology table for important technical terms.

## Hard Rules

- Do not invent claims, citations, datasets, metrics, results, or limitations.
- Preserve paper titles, author names, URLs, DOIs, arXiv IDs, equations, code identifiers, dataset names, metric names, section numbers, markdown tables, and bullet structure unless the user explicitly asks to localize them.
- Preserve the strength of claims. Do not turn "may improve" into "significantly improves" or "preliminary evidence" into "proves".
- Preserve hedging and uncertainty, especially words such as may, might, likely, preliminary, suggests, limited, possible, unclear, 可能, 初步, 有限, 尚不明确.
- Keep terms consistent. Choose one translation for each key term and use it throughout.
- If a term has no stable Chinese equivalent, keep the English term with a short Chinese gloss on first use.
- If a Chinese term has several plausible English translations, pick the most research-standard one and optionally include the Chinese original in parentheses on first use.

## Academic Style Defaults

For Chinese -> English:

- Prefer concise conference-paper style.
- Use active voice when it improves clarity, but keep neutral academic tone.
- Translate "创新点" according to context: novelty, contribution, proposed idea, or innovation point.
- Translate "论文脉络" as paper lineage, research lineage, or literature lineage depending on context.
- Translate "合理性审查" as reasonableness audit, plausibility audit, or validity check depending on context.

For English -> Chinese:

- Prefer clear technical Chinese.
- Keep common technical terms in English if translation would reduce precision, for example RAG, baseline, benchmark, ablation, faithfulness, hallucination, retrieval, reranker.
- Use Chinese punctuation and sentence flow unless preserving quoted text or code.
- Avoid marketing-like wording. Keep claims testable and measured.

## Output Templates

### Simple translation

```markdown
Translation:
<translated text>
```

### Bilingual side-by-side

```markdown
| Source | Translation |
| --- | --- |
| <source sentence> | <translated sentence> |
```

### Literal + polished academic version

```markdown
Literal translation:
<faithful translation>

Polished academic version:
<more natural academic version>

Notes:
- <only include notes when there are ambiguous terms, claim-strength changes avoided, or terminology decisions>
```

### Terminology table

```markdown
| Source term | Translation | Note |
| --- | --- | --- |
| <term> | <term> | <why this translation was chosen> |
```

## When Combined With Research Analysis

If the user asks to translate and then analyze, translate first. Then continue with the requested research mode.

If the user asks only for translation, stop after the translation and any necessary terminology notes. Do not add literature review, novelty ideas, or reviewer critique.

If the user asks to polish a rebuttal or reviewer response, preserve the factual scope and make the tone firm, specific, and non-defensive.
