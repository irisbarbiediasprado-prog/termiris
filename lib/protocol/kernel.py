import importlib
import pkgutil
import re
from typing import Dict, List, Optional

from protocol.base import ProtocolPlugin
from protocol.compiler import ProtocolCompiler
from protocol.isa import Operation


class Tokenizer:
    TOKEN_PATTERN = re.compile(r"<<\s*(.*?)\s*>>")

    @classmethod
    def tokenize(cls, raw_text: str) -> List[str]:
        match = cls.TOKEN_PATTERN.search(raw_text.strip())

        if not match:
            return []

        return match.group(1).split()


class CommandRouter:
    def __init__(self):
        self._routes: Dict[str, ProtocolPlugin] = {}

    def register(self, plugin: ProtocolPlugin):
        self._routes[plugin.command.upper()] = plugin

    def route(
        self,
        command: str,
    ) -> Optional[ProtocolPlugin]:
        return self._routes.get(command.upper())

    def auto_discover(self):
        import protocol.plugins as plugins_pkg

        for _, name, ispkg in pkgutil.iter_modules(
            plugins_pkg.__path__
        ):
            if not ispkg:
                continue

            module = importlib.import_module(
                f"protocol.plugins.{name}"
            )

            for obj in vars(module).values():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, ProtocolPlugin)
                    and obj is not ProtocolPlugin
                ):
                    self.register(obj())


class ProtocolKernel:

    def __init__(
        self,
        router: CommandRouter,
        compiler: ProtocolCompiler | None = None,
    ):
        self.router = router
        self.compiler = compiler or ProtocolCompiler()

    def compile(
        self,
        raw_input: str,
    ) -> List[Operation]:

        tokens = Tokenizer.tokenize(raw_input)

        if not tokens:
            return []

        command = tokens[0]
        args = tokens[1:]

        plugin = self.router.route(command)

        if plugin is None:
            raise ValueError(
                f"Comando do protocolo não reconhecido: {command}"
            )

        ast = plugin.parse_ast(args)

        intent = plugin.lower_to_intent(ast)

        return self.compiler.compile(intent)
