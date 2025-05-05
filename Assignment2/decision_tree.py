# Environment
# OS: MacOS
# Language: Python 3.13

import sys
import math

def get_data(file):
    lines = file.readlines()
    attribute_names = lines[0].strip().split('\t')
    attribute_values = []
    for line in lines[1:]:
        attribute_values.append(line.strip().split('\t'))
    return attribute_names, attribute_values

def calculate_entropy(attribute_values, class_index):
    class_count = {}
    for row in attribute_values:
        class_value = row[class_index]
        if class_value not in class_count:
            class_count[class_value] = 0
        class_count[class_value] += 1
    total = len(attribute_values)
    entropy = 0
    for count in class_count.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def calculate_information_gain(attribute_values, attribute_index, class_index):
    entropy_before = calculate_entropy(attribute_values, class_index)
    value_data = {}
    for row in attribute_values:
        value = row[attribute_index]
        if value not in value_data:
            value_data[value] = []
        value_data[value].append(row)
    total = len(attribute_values)
    entropy_after = 0
    for subset in value_data.values():
        p = len(subset) / total
        entropy_after += p * calculate_entropy(subset, class_index)
    information_gain = entropy_before - entropy_after
    return information_gain

def calculate_split_info(attribute_values, attribute_index):
    value_count = {}
    for row in attribute_values:
        value = row[attribute_index]
        if value not in value_count:
            value_count[value] = 0
        value_count[value] += 1
    total = len(attribute_values)
    split_info = 0
    for count in value_count.values():
        p = count / total
        split_info -= p * math.log2(p)
    return split_info

def calculate_gain_ratio(attribute_values, attribute_index, class_index):
    information_gain = calculate_information_gain(attribute_values, attribute_index, class_index)
    split_info = calculate_split_info(attribute_values, attribute_index)
    if split_info == 0:
        return 0
    else:
        return information_gain / split_info

def feature_selection(attribute_values, attribute_names, used_attributes, class_index):
    best_attribute = -1
    best_gain_ratio = -1
    for i in range(len(attribute_names) - 1):
        if i in used_attributes:
            continue
        else:
            current_gain_ratio = calculate_gain_ratio(attribute_values, i, class_index)
            if current_gain_ratio > best_gain_ratio:
                best_attribute = i
                best_gain_ratio = current_gain_ratio
    return best_attribute, best_gain_ratio

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
