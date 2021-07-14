from cython.cimports.strstr import strstr

def main():
    data: cython.p_char = "hfvcakdfagbcffvschvxcdfgccbcfhvgcsnfxjh"

    pos = strstr(needle='akd', haystack=data)
    print(pos is not cython.NULL)
