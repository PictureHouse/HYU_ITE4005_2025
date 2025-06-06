# Environment
# OS: MacOS
# Language: Python 3.13

import sys

def get_data(file):
    data = []
    for line in file:
        tmp = line.strip().split('\t')
        data.append((int(tmp[0]), float(tmp[1]), float(tmp[2])))
    return data

def main():
    args = sys.argv[1:]
    input_data = []
    with open(args[0], 'r') as input:
        input_data = get_data(input)
        input.close()
    n = int(args[1])
    eps = int(args[2])
    min_pts = int(args[3])

if __name__ == '__main__':
    main()