from pathlib import Path

from .schemas import RepositoryRequest, RepositoryResponse


LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".md": "Markdown",
    ".json": "JSON",
    ".html": "HTML",
    ".css": "CSS",
    ".yml": "YAML",
    ".yaml": "YAML",
}

IMPORTANT_FILES = {
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "Dockerfile",
    ".env.example",
    "docker-compose.yml",
}


def inspect_repository(request: RepositoryRequest) -> RepositoryResponse:

    repo_path = Path(request.path)

    # Validation
    if not repo_path.exists():
        raise FileNotFoundError(f"{repo_path} does not exist.")

    if not repo_path.is_dir():
        raise ValueError("Path must be a directory.")

    files = []
    languages = set()
    important_files = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        relative = file.relative_to(repo_path)

        files.append(str(relative))

        if file.name in IMPORTANT_FILES:
            important_files.append(str(relative))

        extension = file.suffix.lower()

        if extension in LANGUAGE_MAP:
            languages.add(LANGUAGE_MAP[extension])

    return RepositoryResponse(
        total_files=len(files),
        languages=sorted(list(languages)),
        important_files=important_files,
        files=sorted(files),
    )