upload_wheels() {
    echo ${PWD}
    if [[ -z ${TOKEN} ]]; then
        echo no token set, not uploading
    else
        if compgen -G "./dist/*.whl"; then
            echo "Found wheel"
            anaconda -q -t ${TOKEN} upload --force -u scientific-python-nightly-wheels ./dist/*.whl
            echo "PyPI-style index: https://pypi.anaconda.org/scientific-python-nightly-wheels/simple"
        else
            echo "Files do not exist"
            return 1
        fi
    fi
}
