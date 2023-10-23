fn i32 f() except -1:
    let dict d
    let object x, z
    let i32 i
    z = dict
    d = dict(x)
    d = dict(*x)
    d.clear()
    z = d.copy()
    z = d.items()
    z = d.keys()
    z = d.values()
    d.merge(x, i)
    d.update(x)
    d.merge_pairs(x, i)
