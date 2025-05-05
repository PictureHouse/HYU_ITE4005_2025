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
    best_attribute_index = -1
    best_gain_ratio = -1
    for i in range(len(attribute_names) - 1):
        if i in used_attributes:
            continue
        else:
            current_gain_ratio = calculate_gain_ratio(attribute_values, i, class_index)
            if current_gain_ratio > best_gain_ratio:
                best_attribute_index = i
                best_gain_ratio = current_gain_ratio
    return best_attribute_index, best_gain_ratio

class Node:
    def __init__(self, attribute_name = None, value = None, children = None, class_label = None):
        self.attribute_name = attribute_name
        self.value = value
        self.children = children or {}
        self.class_label = class_label

    def is_leaf(self):
        return self.class_label is not None

def construct_decision_tree(attribute_values, attribute_names, used_attributes, class_index):
    class_values = []
    for row in attribute_values:
        class_values.append(row[class_index])
    all_same = True
    first_class = class_values[0] if class_values else None
    for value in class_values:
        if value != first_class:
            all_same = False
            break
    if all_same and class_values:
        return Node(class_label = class_values[0])

    if len(used_attributes) == len(attribute_names) - 1:
        class_count = {}
        for value in class_values:
            if value not in class_count:
                class_count[value] = 0
            class_count[value] += 1
        most_common_class = None
        max_count = -1
        for class_name, count in class_count.items():
            if count > max_count:
                most_common_class = class_name
                max_count = count
        return Node(class_label = most_common_class)

    best_attribute_index, best_gain_ratio = feature_selection(attribute_values, attribute_names, used_attributes, class_index)
    if best_gain_ratio <= 0:
        class_count = {}
        for value in class_values:
            if value not in class_count:
                class_count[value] = 0
            class_count[value] += 1
        most_common_class = None
        max_count = -1
        for class_name, count in class_count.items():
            if count > max_count:
                most_common_class = class_name
                max_count = count
        return Node(class_label=most_common_class)

    decision_tree = Node(attribute_name = best_attribute_index)
    used_attributes.add(best_attribute_index)
    value_datasets = {}
    for row in attribute_values:
        value = row[best_attribute_index]
        if value not in value_datasets:
            value_datasets[value] = []
        value_datasets[value].append(row)
    for value in value_datasets:
        subset = value_datasets[value]
        child = construct_decision_tree(subset, attribute_names, used_attributes, class_index)
        child.value = value
        decision_tree.children[value] = child
    return decision_tree

def make_prediction(node, sample):
    if node.is_leaf():
        return node.class_label
    else:
        value = sample[node.attribute_name]
        if value in node.children:
            return make_prediction(node.children[value], sample)
        else:
            class_counts = {}
            for child in node.children.values():
                if child.is_leaf():
                    if child.label not in class_counts:
                        class_counts[child.label] = 0
                    class_counts[child.label] += 1
            if class_counts:
                return max(class_counts, key=class_counts.get)

def write_result(file, attributes, data):
    file.write('\t'.join(attributes) + '\n')
    for line in data:
        file.write('\t'.join(line) + '\n')

def main():
    args = sys.argv[1:]
    with open(args[0], 'r') as train:
        attribute_names, train_data = get_data(train)
        train.close()
    used_attributes = set()
    class_index = len(attribute_names) - 1
    decision_tree = construct_decision_tree(train_data, attribute_names, used_attributes, class_index)
    with open(args[1], 'r') as test:
        test_attribute_names, test_data = get_data(test)
        test.close()
    predictions = []
    for sample in test_data:
        prediction = sample + [make_prediction(decision_tree, sample)]
        predictions.append(prediction)
    with open(args[2], 'w') as result:
        write_result(result, attribute_names, predictions)
        result.close()

if __name__ == '__main__':
    main()
