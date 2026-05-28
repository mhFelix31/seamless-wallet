import importlib
from pathlib import Path

from fastapi import APIRouter

IGNORED_FILES = {
    "__init__.py",
    "dependencies.py",
    "schemas.py",
    "models.py",
    "utils.py",
}

IGNORED_DIRS = {
    "__pycache__",
    "tests",
}


def create_api_router() -> APIRouter:
    main_router = APIRouter()
    base_dir = Path(__file__).parent  # src/api/rest

    for file in sorted(_iter_python_files(base_dir)):
        module_path = _to_module_path(base_dir, file)

        module = importlib.import_module(module_path)

        router = getattr(module, "router", None)

        # Keep your original behavior, but safer
        if not isinstance(router, APIRouter):
            continue

        prefix = _build_prefix(base_dir, file)

        # TODO CORRECT TO PROPER LOGGING
        print(f"[Router] {module_path} -> {prefix}")

        main_router.include_router(router, prefix=prefix)

    return main_router


def _iter_python_files(base_dir: Path):
    for path in base_dir.rglob("*.py"):
        if path.name in IGNORED_FILES:
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        if path.name.startswith("_"):
            continue

        yield path


def _to_module_path(base_dir: Path, file: Path) -> str:
    relative = file.relative_to(base_dir).with_suffix("")
    parts = relative.parts
    return "src.api." + ".".join(parts)


def _build_prefix(base_dir: Path, file: Path) -> str:
    relative = file.relative_to(base_dir).with_suffix("")
    parts = relative.parts

    # Example:
    # v1/status.py -> ["v1", "status"]
    # v1/users/create.py -> ["v1", "users", "create"]

    return "/" + "/".join(parts)
