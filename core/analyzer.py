"""Analyze scan results and produce actionable insights."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

THRESHOLDS = {
    "Downloads": 5,
    "SoftwareDistribution": 3,
    "Temp": 1,
}

ACTIONS = {
    "Downloads": "迁移",
    "SoftwareDistribution": "清理",
    "Temp": "清理",
}


@dataclass
class Insight:
    path: str
    size_gb: float
    suggestion: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "path": self.path,
            "size": f"{self.size_gb:.2f} GB",
            "suggestion": self.suggestion,
        }


def _match_rule(path: str) -> str | None:
    for key in THRESHOLDS:
        if key.lower() in path.lower():
            return key
    return None


def generate_insights(flat_results: Dict[str, int]) -> List[Dict[str, str]]:
    insights: List[Insight] = []
    for path, size in flat_results.items():
        rule = _match_rule(path)
        if not rule:
            continue
        size_gb = size / (1024 ** 3)
        if size_gb >= THRESHOLDS[rule]:
            suggestion = ACTIONS.get(rule, "清理")
            insights.append(Insight(path=path, size_gb=size_gb, suggestion=suggestion))
    return [insight.to_dict() for insight in insights]
