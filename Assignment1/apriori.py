import sys

args = sys.argv[1:]
minSupport = args[0]
input = open(args[1], 'r')
output = open(args[2], 'w')

while True:
    line = input.readline()
    if not line: break
    print(line)

input.close()
output.close()