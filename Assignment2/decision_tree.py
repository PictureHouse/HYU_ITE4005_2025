# Environment
# OS: MacOS
# Language: Python 3.13

import sys

def get_data(file):
    lines = file.readlines()
    attribute_names = lines[0].strip().split('\t')
    attribute_values = []
    for line in lines[1:]:
        attribute_values.append(line.strip().split('\t'))
    return attribute_names, attribute_values

def write_result(file, attributes, data):
    file.write('\t'.join(attributes) + '\n')
    for line in data:
        file.write('\t'.join(line) + '\n')

def main():
    args = sys.argv[1:]
    with open(args[0], 'r') as train:
        train_attribute_names, train_data = get_data(train)
        train.close()
    # 훈련 수행 코드 구현
    with open(args[1], 'r') as test:
        test_attribute_names, test_data = get_data(test)
        test.close()
    # 테스트 수행 코드 구현
    with open(args[2], 'w') as result:
        write_result(result, train_attribute_names, train_data)
        result.close()

if __name__ == '__main__':
    main()
