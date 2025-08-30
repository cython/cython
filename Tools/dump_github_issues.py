"""
Dump the GitHub issues of the current project to a file (.json.gz).

Usage:  python3 Tools/dump_github_issues.py
"""

import configparser
import gzip
import json
import os.path

from datetime import datetime
from urllib.request import urlopen

GIT_CONFIG_FILE = ".git/config"


class RateLimitReached(Exception):
    pass


def gen_urls(repo):
    i = 0
    while True:
        yield f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={i}"
        i += 1


def read_rate_limit():
    with urlopen("https://api.github.com/rate_limit") as p:
        return json.load(p)


def parse_rate_limit(limits):
    limits = limits['resources']['core']
    return limits['limit'], limits['remaining'], datetime.fromtimestamp(limits['reset'])


def load_url(url):
    with urlopen(url) as p:
        data = json.load(p)
    if isinstance(data, dict) and 'rate limit' in data.get('message', ''):
        raise RateLimitReached()

    assert isinstance(data, list), type(data)
    return data or None  # None indicates empty last page


def join_list_data(lists):
    result = []
    for data in lists:
        if not data:
            break
        result.extend(data)
    return result


def output_filename(repo):
    timestamp = datetime.now()
    return f"github_issues_{repo.replace('/', '_')}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json.gz"


def write_gzjson(file_name, data, indent=2):
    with gzip.open(file_name, "wt", encoding='utf-8') as gz:
        json.dump(data, gz, indent=indent)


def find_origin_url(git_config=GIT_CONFIG_FILE):
    assert os.path.exists(git_config)
    parser = configparser.ConfigParser()
    parser.read(git_config)
    return parser.get('remote "origin"', 'url')


def parse_repo_name(git_url):
    if git_url.endswith('.git'):
        git_url = git_url[:-4]
    return '/'.join(git_url.split('/')[-2:])


def dump_issues(repo):
    """Main entry point."""
    print(f"Reading issues from repo '{repo}'")
    urls = gen_urls(repo)
    try:
        paged_data = map(load_url, urls)
        issues = join_list_data(paged_data)
    except RateLimitReached:
        limit, remaining, reset_time = parse_rate_limit(read_rate_limit())
        print(f"FAILURE: Rate limits ({limit}) reached, remaining: {remaining}, reset at {reset_time}")
        return

    filename = output_filename(repo)
    print(f"Writing {len(issues)} to {filename}")
    write_gzjson(filename, issues)


### TESTS

def test_join_list_data():
    assert join_list_data([]) == []
    assert join_list_data([[1,2]]) == [1,2]
    assert join_list_data([[1,2], [3]]) == [1,2,3]
    assert join_list_data([[0], [1,2], [3]]) == [0,1,2,3]
    assert join_list_data([[0], [1,2], [[[]],[]]]) == [0,1,2,[[]],[]]


def test_output_filename():
    filename = output_filename("re/po")
    import re
    assert re.match(r"github_issues_re_po_[0-9]{8}_[0-9]{6}\.json", filename)


def test_find_origin_url():
    assert find_origin_url()


def test_parse_repo_name():
    assert parse_repo_name("https://github.com/cython/cython") == "cython/cython"
    assert parse_repo_name("git+ssh://git@github.com/cython/cython.git") == "cython/cython"
    assert parse_repo_name("git+ssh://git@github.com/fork/cython.git") == "fork/cython"


def test_write_gzjson():
    import tempfile
    with tempfile.NamedTemporaryFile() as tmp:
        write_gzjson(tmp.name, [{}])

        # test JSON format
        with gzip.open(tmp.name) as f:
            assert json.load(f) == [{}]

        # test indentation
        with gzip.open(tmp.name) as f:
            assert f.read() == b'[\n  {}\n]'


### MAIN

if __name__ == '__main__':
    repo_name = parse_repo_name(find_origin_url())
    dump_issues(repo_name)
