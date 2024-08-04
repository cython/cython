from setuptools.build_meta import *  # Re-exporting PEP 517 hooks

# Re-exporting PEP 517 hooks
from ._backend import (
    build_sdist,
    build_wheel,
    get_requires_for_build_wheel,
    prepare_metadata_for_build_wheel,
)

try:
    # Re-exporting PEP 660 hooks
    from ._backend import (  # type: ignore[assignment]  # noqa: WPS436
        build_editable,
        get_requires_for_build_editable,
        prepare_metadata_for_build_editable,
    )
except ImportError:
    # Only succeeds w/ setuptools implementing PEP 660
    pass

def build_wheel(
        wheel_directory,
        config_settings,
        metadata_directory
)