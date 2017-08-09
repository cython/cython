# mode: run
# tag: pep489

import os.path

module_spec = __spec__
module_file = __file__


def check_spec(spec=__spec__):
    """
    >>> check_spec()
    """
    assert __spec__ is not None
    assert __spec__ is spec

    assert __name__
    assert __name__ == spec.name

    assert spec.loader is not None
    assert spec.loader is __loader__

    assert not spec.parent
    assert not __package__

    assert spec.origin
    assert spec.origin == module_file
    assert spec.origin == __file__
    assert os.path.basename(spec.origin).startswith(__name__)


# validate that ModuleSpec is already complete at module initialisation time
check_spec()
check_spec(__spec__)
check_spec(module_spec)


def file_in_module():
    """
    >>> print(file_in_module())
    mod__spec__
    """
    return os.path.basename(module_file).split('.', 1)[0]


def file_in_function():
    """
    >>> print(file_in_function())
    mod__spec__
    """
    return os.path.basename(__file__).split('.', 1)[0]
