from pathlib import Path
from models import Artifact, ArtifactMetadata, ResourceReference

class TemporaryArtifactProvider:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def create_text_artifact(self, name: str, content: str, artifact_type: str, priority: int) -> Artifact:
        file_path = self.cache_dir / f"{name}.txt"
        file_path.write_text(content, encoding="utf-8")
        
        return Artifact(
            metadata=ArtifactMetadata(id=name, artifact_type=artifact_type, priority=priority),
            resource=ResourceReference(uri=f"filesystem://{file_path.resolve()}")
        )

