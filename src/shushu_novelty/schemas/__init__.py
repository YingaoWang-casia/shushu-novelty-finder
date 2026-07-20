"""Versioned public data contracts."""

from shushu_novelty.schemas.benchmark import BenchmarkReference, BenchmarkRun, BenchmarkSeed
from shushu_novelty.schemas.benchmark_adapter import BenchmarkAdapter, BenchmarkAdapterSet
from shushu_novelty.schemas.blind_evaluation import (
    BlindOutputAssignment,
    BlindOutputKey,
    BlindPairwiseAssignment,
    BlindPairwiseResponse,
    BlindResponseLock,
    BlindScalarResponse,
)
from shushu_novelty.schemas.claim import ClaimEvidence, EvidenceRef
from shushu_novelty.schemas.collision import (
    AxisOverlap,
    CollisionAudit,
    CollisionBatch,
    CollisionQueries,
    PriorComparison,
)
from shushu_novelty.schemas.evaluation import (
    CalibrationAssessment,
    EvaluationJudgment,
    EvidenceAssessment,
    IdeaQualityAssessment,
    LineageAssessment,
    PairwiseJudgment,
    RelationClassificationAssessment,
    RetrievalAssessment,
)
from shushu_novelty.schemas.fulltext import FullTextDocument, PageText
from shushu_novelty.schemas.gap import GapRecord
from shushu_novelty.schemas.idea import IdeaCandidate
from shushu_novelty.schemas.lineage import (
    LineageEdge,
    LineageGraph,
    LineageNode,
    SaturationRecord,
)
from shushu_novelty.schemas.paper import PaperRecord, Provenance
from shushu_novelty.schemas.report import ReportManifest
from shushu_novelty.schemas.retrieval import SearchManifest
from shushu_novelty.schemas.retrieval_benchmark import RetrievalBenchmarkTopic
from shushu_novelty.schemas.reviewer import (
    ReviewerAudit,
    ReviewerBatch,
    ReviewerObjection,
    RevisionRecord,
)
from shushu_novelty.schemas.run_state import PhaseRecord, RunState

SCHEMA_MODELS = {
    "benchmark": BenchmarkSeed,
    "benchmark-adapters": BenchmarkAdapterSet,
    "blind-output-assignment": BlindOutputAssignment,
    "blind-output-key": BlindOutputKey,
    "blind-pairwise-assignment": BlindPairwiseAssignment,
    "blind-pairwise-response": BlindPairwiseResponse,
    "blind-response-lock": BlindResponseLock,
    "blind-scalar-response": BlindScalarResponse,
    "paper": PaperRecord,
    "claim": ClaimEvidence,
    "collision": CollisionBatch,
    "evaluation-judgment": EvaluationJudgment,
    "pairwise-judgment": PairwiseJudgment,
    "fulltext": FullTextDocument,
    "gap": GapRecord,
    "idea": IdeaCandidate,
    "lineage": LineageGraph,
    "run-state": RunState,
    "search-manifest": SearchManifest,
    "retrieval-benchmark-topic": RetrievalBenchmarkTopic,
    "reviewer": ReviewerBatch,
    "report-manifest": ReportManifest,
}

__all__ = [
    "BenchmarkReference",
    "BenchmarkAdapter",
    "BenchmarkAdapterSet",
    "BenchmarkRun",
    "BenchmarkSeed",
    "BlindOutputAssignment",
    "BlindOutputKey",
    "BlindPairwiseAssignment",
    "BlindPairwiseResponse",
    "BlindResponseLock",
    "BlindScalarResponse",
    "ClaimEvidence",
    "AxisOverlap",
    "CollisionAudit",
    "CollisionBatch",
    "CollisionQueries",
    "CalibrationAssessment",
    "EvidenceRef",
    "EvidenceAssessment",
    "EvaluationJudgment",
    "FullTextDocument",
    "GapRecord",
    "IdeaCandidate",
    "IdeaQualityAssessment",
    "LineageAssessment",
    "LineageEdge",
    "LineageGraph",
    "LineageNode",
    "PaperRecord",
    "PageText",
    "PairwiseJudgment",
    "PhaseRecord",
    "Provenance",
    "PriorComparison",
    "ReviewerAudit",
    "ReviewerBatch",
    "ReviewerObjection",
    "RevisionRecord",
    "ReportManifest",
    "RelationClassificationAssessment",
    "RunState",
    "RetrievalAssessment",
    "SaturationRecord",
    "SearchManifest",
    "RetrievalBenchmarkTopic",
    "SCHEMA_MODELS",
]
