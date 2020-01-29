from importlib import import_module, invalidate_caches as importlib_invalidate_caches
from pkgutil import walk_packages
from sys import path as sys_path


def import_submodules(package_name: str) -> None:
    """
    Import all submodules under a given package.
    Adapted from \
        https://github.com/allenai/allennlp/blob/master/allennlp/common/util.py.
    Originally Licensed under Apache 2.
    :param package_name: Package to import.
    """
    importlib_invalidate_caches()

    sys_path.append(".")

    module = import_module(package_name)
    path = getattr(module, "__path__", [])
    path_string = "" if not path else path[0]

    for module_finder, name, _ in walk_packages(path):
        if path_string and module_finder.path != path_string:
            continue
        subpackage = f"{package_name}.{name}"
        import_submodules(subpackage)
