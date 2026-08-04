# Architecture - TP v0.2

Este documento registra COMO o v0.2 implementa a SPEC.

## Backend

- BackendRegistry.resolve() levanta BackendNotFoundError (implementação concreta do erro tipado exigido pela SPEC)
- ISABackend: traduz LIST_DIRECTORY, INJECT_RESOURCE, BOOTSTRAP_GENESIS para PrimitiveISA
- FilesystemBackend: legado, tornado puro em v0.2, retorna Operation(LIST) sem os.listdir

## Decisões v0.2

1. BackendNotFoundError criado - ValueError genérico removido
2. validate() / compile() separados - compile puro, sem IO
3. MigrationPlan.emit() removido após rg confirmar 0 consumidores (124 tests passaram)
4. FilesystemBackend purificado - IO movido para RuntimeEngine.apply()

## Verificação

rg "plan\.emit" --type py => 0 resultados
rg "\.emit\(" --type py => apenas emitter.emit em runtime/executors.py
pytest -q => 124 passed
