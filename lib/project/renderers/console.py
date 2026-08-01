from project.statistics import ProjectStatistics
from project.diagnostic import ProjectDiagnostic
from pathlib import Path
from typing import Optional
from project.finding import Severity


class ConsoleRenderer:
    @staticmethod
    def render_statistics(stats: ProjectStatistics, base_path: Optional[Path] = None) -> str:
        lines = [
            "=== Project Statistics ===",
            f"Files:      {stats.files}",
            f"Functions:  {stats.functions}",
            f"Classes:    {stats.classes}",
            f"Imports:    {stats.imports}",
            f"Calls:      {stats.calls}",
        ]
        return "\n".join(lines)

    @staticmethod
    def render_diagnostics(diagnostic: ProjectDiagnostic, base_path: Optional[Path] = None) -> str:
        if not diagnostic.findings:
            return "No diagnostics."
        lines = ["\n=== Diagnostics ==="]
        for f in diagnostic.findings:
            file_str = str(f.file.relative_to(base_path)) if base_path and f.file else ""
            severity = f.severity.value.upper()
            lines.append(f"[{severity}] [{f.rule_id}] {file_str}: {f.message}")
        return "\n".join(lines)
