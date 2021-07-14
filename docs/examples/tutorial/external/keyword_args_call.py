import cython
from cython.cimports.strstr import strstr

def main():
    data: p_char = "hfvcakdfagbcffvschvxcdfgccbcfhvgcsnfxjh"

    pos: p_char = strstr(needle='akd', haystack=data)
    print(pos is not cython.NULL)
