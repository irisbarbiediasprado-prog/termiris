from .plan import Plan, PlanStep, IntentOrigin

class Planner:
    """Planner mínimo. Apenas encapsula intenções em PlanSteps.
    
    Toda inteligência de interpretação pertence ao Compiler.
    """
    
    def plan(self, intent: str, source: str = "user") -> Plan:
        """Cria um plano contendo uma única intenção bruta.
        
        Args:
            intent: Descrição textual da intenção.
            source: Origem da intenção (ex.: 'user', 'agent').
        
        Returns:
            Plan com um único PlanStep.
        """
        step = PlanStep(
            goal=intent,  # string bruta; o Compiler dará significado
            origin=IntentOrigin(source=source, raw_intent=intent),
        )
        return Plan(steps=(step,))
