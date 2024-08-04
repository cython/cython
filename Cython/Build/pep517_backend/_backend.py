from setuptools.build_meta import (
    get_requires_for_build_wheel,
    prepare_metadata_for_build_wheel,
    build_sdist as build_sdist,
)

try:
    from setuptools.build_meta import (
        get_requires_for_build_editable,
        prepare_metadata_for_build_editable,
        build_editable
    )
except ImportError:
    pass

def build_sdist():
    pass