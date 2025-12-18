import fileinput
import urllib.parse

if __name__ == '__main__':
    import fileinput

    for line in fileinput.input():
        line = line.strip()
        print(urllib.parse.quote(line, safe=''))
