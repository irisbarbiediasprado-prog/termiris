from pathlib import Path
from models import Artifact, ResourceReference

class ArtifactRepository:
    def fetch(self, ref: ResourceReference) -> Artifact:
        uri = ref.uri
        if uri.startswith("filesystem://"):
            clean_path = Path(uri.replace("filesystem://", ""))
            if clean_path.exists():
                content = clean_path.read_text(encoding="utf-8")
                return Artifact(uri=uri, content=content, metadata={"size": len(content)})
        raise ValueError(f"URI não suportada ou recurso inexistente: {uri}")
