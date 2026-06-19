# Welcome to Cython's documentation

The current Cython documentation is hosted at [cython.readthedocs.io](https://cython.readthedocs.io/)

The main documentation files are located in the `cython/docs/src` folder
and the code that is used in those documents is located in `cython/docs/examples`

Before building, you need to install the Python dependencies from `doc-requirements.txt`.
On Linux you will also need: `make`, `texlive` (texlive-formats-extra on Debian, only for PDFs),
GCC (cc on Debian), C++ compiler (g++ on Debian).

Debian install command:
```shell
sudo apt update && sudo apt install make texlive-formats-extra cc g++
```

To install from `doc-requirements.txt`, run in the root folder of the repository

```shell
pip install -r doc-requirements.txt
```

To build the documentation, go into the `docs` folder and run

```shell
make html
```

You can then see the documentation by opening `cython/docs/build/html/index.html` in a browser.

Generally follow the structure of the existing documents.

If you are creating a (sub)section add a link for it in the TOC of the page.

<details>
<summary>Notes</summary>

1) Some css work should definitely be done.
2) Use local 'top-of-page' contents rather than the sidebar, imo.
3) Fix cython highlighter for cdef blocks

</details>
