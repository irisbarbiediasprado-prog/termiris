from pathlib import Path
from protocol.ast import ProtocolNode, BootstrapNode, RetrieveNode, ResourceType, InvalidNode
from protocol.parser import ProtocolParser
from models import Artifact, ArtifactMetadata, ResourceReference, DomainOperation, OperationType, RuntimeResult
from runtime.engine import RuntimeEngine
from interfaces import ArtifactRepositoryInterface
from providers.filesystem import TemporaryArtifactProvider
from providers.query import SystemQueryProvider

class ProtocolDispatcher:
    def __init__(
        self,
        engine: RuntimeEngine,
        bootstrap_repo: ArtifactRepositoryInterface,
        temp_artifacts: TemporaryArtifactProvider,
        queries: SystemQueryProvider
    ):
        self.engine = engine
        self.bootstrap_repo = bootstrap_repo
        self.temp_artifacts = temp_artifacts
        self.queries = queries

    def dispatch(self, raw_input: str) -> RuntimeResult:
        node: ProtocolNode = ProtocolParser.parse(raw_input)

        match node:
            case BootstrapNode():
                artifacts = self.bootstrap_repo.list_artifacts()
                # Pega apenas o Card 000 (primeiro artefato do repositório)
                first_artifact = artifacts[0] if artifacts else None
                            
                if first_artifact:
                    op = DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=first_artifact)

                    return self.engine.apply(op)
                return runtimeresult(success=true, snapshot=none, artifacts_processed=0)
            case RetrieveNode(resource_type=ResourceType.FILE, target=path_str):
                target_path = Path(path_str)
                
                # Se não existir no caminho relativo/absoluto informado, busca na pasta do protocolo
                if not target_path.exists():
                    file_name = path_str if path_str.endswith(".md") else f"{path_str}.md"
                    protocol_path = Path.home() / ".termiris" / "protocol" / file_name
                    if protocol_path.exists():
                        target_path = protocol_path

                if not target_path.exists():
                    err_artifact = self.temp_artifacts.create_text_artifact(
                        name="protocol_error",
                        content="BEGIN RETRIEVE\nSTATUS: ERROR\nERROR: FILE_NOT_FOUND\nEND RETRIEVE\n",
                        artifact_type="diagnostics",
                        priority=100
                    )
                    return self.engine.apply(DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=err_artifact))

                artifact = Artifact(
                    metadata=ArtifactMetadata(id=f"file_{target_path.name}", artifact_type="source_code", priority=90),
                    resource=ResourceReference(uri=f"filesystem://{target_path.resolve()}")
                )
                return self.engine.apply(
                    DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=artifact)
                )
             
            case RetrieveNode(resource_type=ResourceType.TREE, target=dir_str):
                tree_output = self.queries.tree(dir_str)
                artifact = self.temp_artifacts.create_text_artifact(
                    name="retrieve_tree", content=tree_output, artifact_type="diagnostics", priority=80
                )
                return self.engine.apply(DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=artifact))

            case RetrieveNode(resource_type=ResourceType.SEARCH, target=query_str):
                search_output = self.queries.search(query_str)
                artifact = self.temp_artifacts.create_text_artifact(
                    name="retrieve_search", content=search_output, artifact_type="diagnostics", priority=80
                )
                return self.engine.apply(DomainOperation(type=OperationType.INGEST_ARTIFACT, artifact=artifact))

            case InvalidNode():
                return RuntimeResult(success=False, snapshot=None, artifacts_processed=0, warnings=["Invalid Protocol Command"])

