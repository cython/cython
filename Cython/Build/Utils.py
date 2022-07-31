import sys
import importlib.util
from importlib.machinery import ExtensionFileLoader

def load_dynamic(name, path):
    spec = importlib.util.spec_from_file_location(name, loader=ExtensionFileLoader(name, path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
