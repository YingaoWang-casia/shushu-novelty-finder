# Literature Lineage Mode Example

This mode is for users who want to understand a direction before asking for paper ideas.

## Example Input

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first.

Direction:
organic reaction prediction + RAG + LLM reasoning

Please first梳理这个方向极度相似论文的整体脉络:
- group papers by historical stage or method route;
- list each important paper's concrete innovation points;
- explain task, input, output, datasets, metrics, and assumptions;
- mark what has become saturated and what remains open;
- do not propose ideas until the lineage and gap audit are complete.
```

## Example Output

```text
Scope And Task Map:
Research field: machine learning for organic reaction prediction.
Core task: predict reaction products from reactants, reagents, conditions, or retrieved evidence.
Subtasks: forward reaction prediction, retrosynthesis, reaction condition prediction, yield prediction, reaction reasoning, chemistry RAG.
Canonical input: reaction SMILES, reagent/condition text, reaction class, retrieved similar reactions, or chemistry documents.
Canonical output: product SMILES, reaction route, predicted condition, reasoning chain, or evidence-grounded answer.
Standard datasets: USPTO-50K, USPTO-MIT, Pistachio-style reaction records, task-specific chemistry RAG corpora.
Standard metrics: top-1/top-k exact match, invalid SMILES rate, fingerprint similarity, reaction-class accuracy, evidence relevance, faithfulness, expert judgment.
Typical baselines: template systems, Molecular Transformer, graph-to-sequence models, ChemFormer/T5Chem/ReactionT5, tool-augmented LLMs, RAG-based LLMs.
What counts as meaningful progress: not only higher exact match, but better OOD robustness, chemically faithful reasoning, evidence use, and metric validity.

Closest-Paper Clusters:

Cluster 1: Sequence-to-sequence reaction prediction
Why close: defines the standard forward reaction prediction formulation.
Representative papers: Molecular Transformer; T5Chem; ChemFormer.
Shared assumption: reaction prediction can be treated as molecular string translation.
What became saturated: high accuracy on common USPTO-style splits.
What remains open: mechanism explanation, OOD reaction classes, condition sensitivity.

Cluster 2: Structure-aware reaction prediction
Why close: tries to inject molecular graph structure into reaction modeling.
Representative papers: Graph2SMILES and related graph-to-sequence methods.
Shared assumption: graph structure should improve chemical validity over pure string modeling.
What became saturated: graph/SMILES hybrid encoders for standard tasks.
What remains open: whether structure-aware models produce faithful mechanistic explanations.

Cluster 3: Chemistry LLMs and tool-augmented agents
Why close: moves from single-task predictor to system-level chemistry assistant.
Representative papers: ChemCrow and related chemistry-agent systems.
Shared assumption: LLMs can orchestrate tools and domain knowledge.
What became saturated: wrapping existing tools with LLM planning.
What remains open: hallucination, tool-result interpretation, and evidence-grounded reasoning.

Cluster 4: Chemistry RAG and reasoning-powered reaction LLMs
Why close: directly overlaps with RAG + LLM reasoning for reaction prediction.
Representative papers: ChemRAG-style benchmarks; Reaction-Thinker-style RAG + CoT + RL systems.
Shared assumption: retrieved chemistry evidence can improve prediction and explanation.
What became saturated: simple "add RAG / add CoT" claims.
What remains open: retrieval quality, evidence faithfulness, counterfactual robustness, and benchmark validity.

Per-Paper Innovation Card:

Paper: Molecular Transformer
Year: 2019
Evidence status: verified if source was searched; otherwise mark partial.
Relationship to user direction: ancestor.
Task: forward reaction prediction.
Innovation point 1: formulates reaction prediction as sequence-to-sequence translation from reaction SMILES to product SMILES.
Innovation point 2: shows Transformer-based models can reach strong top-k accuracy on common reaction benchmarks.
Innovation point 3: introduces uncertainty-aware prediction analysis for chemical reaction outcomes.
What it solved: strong data-driven baseline for product prediction.
What it did not solve: faithful mechanism reasoning, evidence retrieval, and real-world condition dependence.
What idea space it blocks: "Transformer for reaction prediction" alone is no longer novel.
What idea space it leaves open: explainable, evidence-grounded, and OOD-robust reaction prediction.

Paper: Reaction-Thinker-style RAG + reasoning system
Year: recent / seed-paper dependent
Evidence status: verify exact venue and claims before using as support.
Relationship to user direction: closest prior.
Task: organic reaction prediction with retrieved similar reactions and LLM reasoning.
Innovation point 1: uses similar-case retrieval to provide reaction evidence.
Innovation point 2: creates or uses reaction chain-of-thought data for reasoning-powered prediction.
Innovation point 3: applies supervised tuning or reinforcement learning to improve product prediction and explanation.
What it solved: moves beyond black-box prediction toward RAG-enhanced reasoning.
What it did not solve: whether the reasoning is causally faithful to retrieved evidence.
What idea space it blocks: "RAG + CoT for reaction prediction" as a standalone contribution.
What idea space it leaves open: evidence-faithfulness auditing, mechanism-aware retrieval, and metric refinement.

Trend Matrix:
Time period | Representative papers | Task shift | Method shift | Dataset/metric shift | Saturated contribution | Open gap
Template era | expert systems | rule matching | templates | coverage/top-k | interpretable templates | template coverage
Seq2seq era | Molecular Transformer | SMILES translation | Transformer | USPTO exact match | high benchmark accuracy | black-box reasoning
Pretraining era | ChemFormer/T5Chem | multitask transfer | pretrained encoder-decoder | multi-task evaluation | model scaling and transfer | OOD and metric validity
Tool/RAG era | ChemCrow/ChemRAG | system + external evidence | tools/RAG/LLMs | task success + RAG metrics | tool wrapping and simple RAG | evidence faithfulness
Reasoning era | Reaction-Thinker-like systems | prediction + rationale | RAG + CoT + tuning/RL | exact match + similarity | RAG+CoT novelty | faithful reasoning and robust evaluation

Gap Audit:
Gap: generated reasoning may not be faithful to retrieved evidence.
Gap type: benchmark absence / inferred gap.
Supporting papers: RAG/reasoning systems that claim explanation but do not run counterfactual evidence tests.
Why this matters: a fluent rationale can mislead chemists if it is not causally tied to the prediction.
Why it may be a bad idea: expert annotation and mechanism labels may be expensive.
Confidence: medium until closest recent follow-up work is verified.

Lineage Verdict:
Most saturated idea: simply adding RAG or CoT to reaction prediction.
Most defensible gap: evidence-faithful and mechanism-aware reaction reasoning.
Most dangerous overlap risk: Reaction-Thinker-style systems already cover RAG + reasoning + tuning.
Best direction to continue: turn explainability into a falsifiable evidence-faithfulness benchmark and method.
What must be verified next: recent RAG reaction prediction papers and whether they already evaluate counterfactual evidence use.
```
