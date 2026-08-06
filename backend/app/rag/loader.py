from pathlib import Path
from hashlib import sha256
from typing import Dict, List

import json
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".json",
    ".py",
    ".js",
    ".ts",
}


LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".md": "markdown",
    ".txt": "text",
    ".json": "json",
    ".pdf": "pdf",
}


class DocumentLoader:

    def __init__(self):

        self.supported_extensions = SUPPORTED_EXTENSIONS

    def load(self, filepath: str) -> List[Dict]:

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(filepath)

        if path.suffix.lower() not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        if path.suffix.lower() == ".pdf":
            return self._load_pdf(path)

        return [self._load_text_file(path)]

    def _hash(self, text: str):

        return sha256(text.encode()).hexdigest()

    def _load_text_file(self, path: Path):

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        metadata = {
            "filename": path.name,
            "filepath": str(path),
            "language": LANGUAGE_MAP.get(path.suffix.lower(), "text"),
            "page": None,
            "hash": self._hash(text)
        }

        if path.suffix.lower() == ".json":

            try:
                parsed = json.loads(text)
                text = json.dumps(parsed, indent=2)

            except Exception:
                pass

        return {
            "content": text,
            "metadata": metadata
        }

    def _load_pdf(self, path: Path):

        reader = PdfReader(path)

        documents = []

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text() or ""

            documents.append(
                {
                    "content": text,
                    "metadata": {
                        "filename": path.name,
                        "filepath": str(path),
                        "language": "pdf",
                        "page": page_number + 1,
                        "hash": self._hash(text)
                    }
                }
            )

        return documents