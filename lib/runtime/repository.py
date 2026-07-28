from pathlib import Path
from typing import List
from models import Artifact, ArtifactMetadata, ResourceReference
from interfaces import ArtifactRepositoryInterface

class FilesystemBootstrapRepository(ArtifactRepositoryInterface):
    def __init__(self, bootstrap_dir: Path = Path.home() / ".termiris" / "tp" / "000-runtime"):
        self.bootstrap_dir = bootstrap_dir

    def list_artifacts(self) -> List[Artifact]:
        artifacts = []
        if self.bootstrap_dir.exists():
            for tp_file in sorted(self.bootstrap_dir.glob("*.md")):
                meta = ArtifactMetadata(
                    id=f"tp_{tp_file.stem}",
                    artifact_type="protocol",
                    priority=100
                )
                res = ResourceReference(uri=f"filesystem://{tp_file.resolve()}")
                artifacts.append(Artifact(metadata=meta, resource=res))
        return artifacts

