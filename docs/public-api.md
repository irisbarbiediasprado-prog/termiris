# Termiris — Public API Contract

## Core Models

### ProjectAnalysis
Imutable knowledge base of a project.

```python
@dataclass(frozen=True)
class ProjectAnalysis:
    files: tuple[SourceFileAnalysis, ...]
```

### SourceFileAnalysis

```python
@dataclass(frozen=True)
class SourceFileAnalysis:
    source: SourceFile
    index: AnalysisIndex
```

### SourceFile

```python
@dataclass(frozen=True)
class SourceFile:
    path: Path
    line_count: int
    size: int
```

### AnalysisIndex
Collection of extracted facts.

```python
@dataclass
class AnalysisIndex:
    functions: list[FunctionInfo]
    classes: list[ClassInfo]
    imports: list[ImportInfo]
    calls: list[CallInfo]
    comments: list[CommentInfo]
    exceptions: list[ExceptionInfo]
```

### ProjectFinding
Diagnostic finding with stable rule_id.

```python
@dataclass(frozen=True)
class ProjectFinding:
    rule_id: str
    message: str
    file: Path
    item: Any | None = None
```

## Rule IDs (canonical values)

Defined in `lib/project/rules/ids.py`:

| RuleId | Value |
|---|---|
| `RuleId.LEGACY_IMPORT` | `"legacy_import"` |
| `RuleId.LARGE_FILE` | `"large_file"` |
| `RuleId.LARGE_FUNCTION` | `"large_function"` |
| `RuleId.TODO_COMMENT` | `"todo_comment"` |
| `RuleId.BARE_EXCEPT` | `"bare_except"` |

## DiagnosticRule Contract

```python
class DiagnosticRule(ABC):
    @abstractmethod
    def run(self, analysis: ProjectAnalysis) -> Iterable[ProjectFinding]:
        ...
```

## Engines

- `StatisticsEngine.compute(analysis) -> ProjectStatistics`
- `ProjectDiagnosticEngine(rules).run(analysis) -> ProjectDiagnostic`

## Renderers

- `ConsoleRenderer.render_statistics(stats, base_path) -> str`
- `ConsoleRenderer.render_diagnostics(diagnostic, base_path) -> str`
