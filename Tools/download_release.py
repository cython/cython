#!/usr/bin/python3

import json
import logging
import shutil
import datetime

from concurrent.futures import ProcessPoolExecutor as Pool, as_completed
from pathlib import Path
from urllib.request import urlopen, Request

logger = logging.getLogger()

PARALLEL_DOWNLOADS = 6
GITHUB_API_URL = "https://api.github.com/repos/cython/cython"


def find_github_files(version, api_url=GITHUB_API_URL):
    url = f"{api_url}/releases/tags/{version}"
    release, _ = read_url(url, accept="application/vnd.github+json", as_json=True)

    for asset in release.get('assets', ()):
        yield asset['browser_download_url']


def read_url(url, decode=True, accept=None, as_json=False):
    if accept:
        request = Request(url, headers={'Accept': accept})
    else:
        request = Request(url)

    with urlopen(request) as res:
        charset = _find_content_encoding(res)
        content_type = res.headers.get('Content-Type')
        data = res.read()

    if decode:
        data = data.decode(charset)
    if as_json:
        data = json.loads(data)
    return data, content_type


def _find_content_encoding(response, default='iso8859-1'):
    from email.message import Message
    content_type = response.headers.get('Content-Type')
    if content_type:
        msg = Message()
        msg.add_header('Content-Type', content_type)
        charset = msg.get_content_charset(default)
    else:
        charset = default
    return charset


def download1(wheel_url, dest_dir):
    wheel_name = wheel_url.rsplit("/", 1)[1]
    logger.info(f"Downloading {wheel_url} ...")
    with urlopen(wheel_url) as w:
        file_path = dest_dir / wheel_name
        if (file_path.exists()
                and "Content-Length" in w.headers
                and file_path.stat().st_size == int(w.headers["Content-Length"])):
            logger.info(f"Already have {wheel_name}")
        else:
            temp_file_path = file_path.with_suffix(".tmp")
            try:
                with open(temp_file_path, "wb") as f:
                    shutil.copyfileobj(w, f)
            except:
                if temp_file_path.exists():
                    temp_file_path.unlink()
                raise
            else:
                temp_file_path.replace(file_path)
                logger.info(f"Finished downloading {wheel_name}")
    return wheel_name


def download(urls, dest_dir, jobs=PARALLEL_DOWNLOADS):
    with Pool(max_workers=jobs) as pool:
        futures = [pool.submit(download1, url, dest_dir) for url in urls]
        try:
            for future in as_completed(futures):
                wheel_name = future.result()
                yield wheel_name
        except KeyboardInterrupt:
            for future in futures:
                future.cancel()
            raise


def dedup(it):
    seen = set()
    for value in it:
        if value not in seen:
            seen.add(value)
            yield value


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    from itertools import cycle, islice
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


def main(*args):
    if not args:
        print("Please pass the version to download")
        return

    version = args[0]
    dest_dir = Path("dist") / version
    if not dest_dir.is_dir():
        dest_dir.mkdir()

    start_time = datetime.datetime.now().replace(microsecond=0)
    urls = roundrobin(*map(dedup, [
        find_github_files(version),
    ]))
    count = sum(1 for _ in download(urls, dest_dir))
    duration = datetime.datetime.now().replace(microsecond=0) - start_time
    logger.info(f"Downloaded {count} files in {duration}.")


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)-15s  %(message)s",
    )
    main(*sys.argv[1:])
