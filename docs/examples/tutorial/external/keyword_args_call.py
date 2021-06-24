import cython

def main():
    data: p_char = "hfvcakdfagbcffvschvxcdfgccbcfhvgcsnfxjh"
    pos: p_char = strstr(needle='akd', haystack=data)
    print(pos is not cython.NULL)
