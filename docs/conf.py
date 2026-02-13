# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import itertools
from pathlib import Path
import re
import sys
import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

YEAR = datetime.date.today().strftime("%Y")

project = 'Cython'
authors = 'Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al.'
copyright = f'{YEAR}, {authors}'

### Custom Cython Docs changes ###
highlight_language = "cython"
pygments_style = "sphinx"
imgmath_image_format = "svg"
issues_github_path = "cython/cython"
sphinx_tabs_disable_tab_closing = True
root_doc = "index"

# Looking up the release/version
try:
    _match_version = re.compile(r'^\s*_*version\s*_*\s*=\s*["\']([^"\']+)["\'].*').match
    cwd = Path.cwd().absolute()
    shadow = cwd.parent / "Cython" / "Shadow.py"
    if not shadow.exists():
        raise FileNotFoundError(f"Version lookup failed, unable to find {shadow}")
    with shadow.open() as fp:
        for line in itertools.islice(fp, 5):  # assume version comes early enough
            _m = _match_version(line)
            if _m:
                release = _m.group(1)
                break
        else:
            print("FAILED TO PARSE PROJECT VERSION !")
            release = "VERSION PARSE FAILED"
except:
    pass

# The short X.Y version.
version = re.sub("^([0-9]+[.][0-9]+).*", r"\g<1>", release)

# Autodoc: Adding the root of the repo to the Python Path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))


## HTML
html_theme = "nature"
# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/cythonlogo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/tabs.css"]
html_context = {
    # "dev version" warning banner
    "development": "a" in release
    or "b" in release,
}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False

# Output file base name for HTML help builder.
htmlhelp_basename = "Cythondoc"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "setuptools": ("https://setuptools.pypa.io/en/latest/", None),
    "wheel": ("https://wheel.readthedocs.io/en/latest/", None),
}
extensions = [
    "sphinx.ext.imgmath",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx_issues",  # if this is missing, pip install sphinx-issues
    "sphinx_tabs.tabs",  # if this is missing, pip install sphinx-tabs
]
try:
    import rst2pdf
except ImportError:
    pass
else:
    extensions.append("rst2pdf.pdfbuilder")
# todo
todo_include_todos = True
### Custom Cython Docs changes ###


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ["_templates"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
