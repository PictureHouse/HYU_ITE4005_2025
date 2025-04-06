import sys
from collections import Counter

def get_transactions(input):
    transactions = []
    for line in input:
        transaction = [int(num) for num in line.split()]
        if transaction:
            transactions.append(transaction)
    return transactions

def pruning(itemset, transaction_count, min_support):
    frequent_itemset = set()
    pruned = set()
    itemset_counter = Counter(itemset)
    for item in itemset_counter.keys():
        if (itemset_counter[item] / transaction_count * 100) >= min_support:
            frequent_itemset.add(item)
        else:
            pruned.add(item)
    return frequent_itemset, pruned

def get_L1(transactions, min_support):
    itemset = list()
    for transaction in transactions:
        for item in transaction:
            itemset.append(frozenset([item]))
    frequent_1_itemset = set()
    frequent_1_itemset, _ = pruning(itemset, len(transactions), min_support)
    return frequent_1_itemset

def generate_Ck(k, frequent_itemset, pruned_set):
    candidate = set()
    for i in frequent_itemset:
        for j in frequent_itemset:
            tmp = j.union(i)
            if tmp not in pruned_set and len(tmp) == k:
                candidate.add(tmp)
    return candidate

def test_Ck(ck, transactions, min_support):
    itemset = list()
    for c in ck:
        for transaction in transactions:
            if c.issubset(transaction):
                itemset.append(c)
    frequent_k_itemset = set()
    pruned = set()
    frequent_k_itemset, pruned = pruning(itemset, len(transactions), min_support)
    return frequent_k_itemset, pruned

def apriori(transactions, min_support):
    k = 1
    frequent_itemsets = get_L1(transactions, min_support)
    pruned_set = set()
    while True:
        k += 1
        ck = []
        ck = generate_Ck(k, frequent_itemsets, pruned_set)
        lk, pruned = test_Ck(list(ck), transactions, min_support)
        if len(lk) == 0:
            break
        else:
            frequent_itemsets.update(lk)
        pruned_set.update(pruned)
    result = list()
    for itemset in frequent_itemsets:
        result.append(set(itemset))
    return result

def get_association_rules(frequent_itemsets, min_support):
    return 0

def write_output(output):
    return 0

def main():
    args = sys.argv[1:]
    min_support = float(args[0])
    with open(args[1], 'r') as input:
        transactions = get_transactions(input)

    frequent_itemsets = list()
    frequent_itemsets = apriori(transactions, min_support)
    print(frequent_itemsets)

    with open(args[2], 'w') as output:
        write_output(output)

if __name__ == '__main__':
    main()
