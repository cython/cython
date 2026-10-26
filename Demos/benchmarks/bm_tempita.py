import cython

import Cython.Tempita._tempita as Tempita

import time


def generate_template():
    template = """
    {{for i in range(100)}}
        {{for row in rows}}
            Row {{i}}::{{row}}
            {{for cell in columns}}Field-{{cell}} {{endfor}}
            End-Row
        {{endfor}}
    {{endfor}}
    """
    return template


def bm_parse_template(scale: cython.long, timer=time.perf_counter):
    parse = Tempita.parse
    content = generate_template() * 100 * scale

    t = timer()
    parse(content, "Tables")
    t = timer() - t
    return t


def bm_run_template(scale: cython.long, timer=time.perf_counter):
    content = generate_template() * scale
    rows = columns = [f"r{i}" for i in range(10)]
    substitute = Tempita.Template(content, "Tables").substitute

    t = timer()
    substitute(rows=rows, columns=columns)
    t = timer() - t
    return t


def run_benchmark(repeat: bool, scale=10):
    from util import repeat_to_accuracy

    for name, func in [
            ('tempita_parse_template', bm_parse_template),
            ('tempita_run_template', bm_run_template),
            ]:
        timings = repeat_to_accuracy(func, scale=scale, repeat=repeat)[0]
        print(f"{name}: {timings}")
