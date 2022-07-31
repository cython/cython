import sys


if sys.version_info < (3, 5):
    import imp
    load_dynamic = imp.load_dynamic

else:
    import importlib.util
    from importlib.machinery import ExtensionFileLoader

    def load_dynamic(name, path):
        spec = importlib.util.spec_from_file_location(name, loader=ExtensionFileLoader(name, path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
