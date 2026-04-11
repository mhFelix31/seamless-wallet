def import_all_models():
    import importlib
    import pkgutil
    import src.infrastructure.db.models as models_pkg

    for _, module_name, _ in pkgutil.iter_modules(models_pkg.__path__):
        importlib.import_module(f"{models_pkg.__name__}.{module_name}")