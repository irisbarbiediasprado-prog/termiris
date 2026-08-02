from planning.plan import Plan, PlanStep
from .operations import Operation, CreateSourceFileOperation
from .models import SourceFile


class Compiler:
    """Compilador de Plan para Operations.

    Não interpreta linguagem natural.
    Recebe intenções estruturadas (ou muito simples).
    """

    def compile(self, plan: Plan) -> tuple[Operation, ...]:
        operations = []
        for step in plan.steps:
            ops = self._compile_step(step)
            operations.extend(ops)
        return tuple(operations)

    def _compile_step(self, step: PlanStep) -> tuple[Operation, ...]:
        intent = step.goal

        # Intenção estruturada (futuro)
        if hasattr(intent, "source_file"):
            sf = intent.source_file
            if not sf.declarations and not sf.imports:
                raise ValueError(
                    f"SourceFile vazio não pode ser criado: {sf.path}"
                )
            return (CreateSourceFileOperation(
                kind="create_source_file",
                reference=sf.path,
                source_file=sf,
            ),)

        # Intenção simples: "criar arquivo <path>" ou "criar módulo <path>"
        if isinstance(intent, str):
            return self._compile_text_intent(intent)

        raise NotImplementedError(
            f"Intenção não reconhecida: {intent}"
        )

    def _compile_text_intent(self, intent: str) -> tuple[Operation, ...]:
        # Formato: "criar arquivo <path>" ou "criar módulo <path>"
        for prefix in ("criar arquivo ", "criar módulo "):
            if intent.startswith(prefix):
                path = intent.removeprefix(prefix).strip()
                raise ValueError(
                    f"Intenção sem conteúdo: '{intent}'. "
                    f"Um SourceFile precisa ter declarações ou imports."
                )

        raise NotImplementedError(
            f"Intenção não reconhecida: {intent}"
        )
