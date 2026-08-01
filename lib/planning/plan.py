from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DiagnosticOrigin:
    rule_id: str
    finding_id: str | None = None


@dataclass(frozen=True)
class IntentOrigin:
    source: str
    raw_intent: str | None = None


Origin = DiagnosticOrigin | IntentOrigin | None


@dataclass(frozen=True)
class PlanStep:
    goal: Any  # TODO: substituir por Goal quando os goals concretos existirem
    origin: Origin = None


@dataclass(frozen=True)
class Plan:
    steps: tuple[PlanStep, ...]
