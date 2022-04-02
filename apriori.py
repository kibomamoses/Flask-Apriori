
from itertools import chain, combinations
from collections import defaultdict


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def min_support_items(item_set, transaction_list, min_support, freq_set):
    """calculates the support for items in the item_set and returns a subset
    of the item_set each of whose elements satisfies the minimum support"""
    _item_set = set()
    local_set = defaultdict(int)

    for item in item_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    for item, count in local_set.items():
        if count >= min_support:
            _item_set.add(item)
    return _item_set


def combine_set(item_set, length):
    """Join a set with itself and returns the n-element item_sets"""
    return set(
        [i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length]
    )


def find_frequency_1_dataset(iterator):
    transaction_list = list()
    item_set = set()
    for record in iterator:
        transaction = frozenset(record)
        transaction_list.append(transaction)
        for item in transaction:
            item_set.add(frozenset([item]))  # Generate 1-item_sets
    return item_set, transaction_list


def run_apriori(data_iter, min_support):
    item_set, transaction_list = find_frequency_1_dataset(data_iter)
    freq_set = defaultdict(int)
    large_set = dict()
    # Global dictionary which stores (key=n-item_sets,value=support)
    # which satisfy min_support

    onec_set = min_support_items(item_set, transaction_list, min_support, freq_set)
    # print(onec_set)
    currentl_set = onec_set
    k = 2
    while currentl_set != set([]):
        large_set[k - 1] = currentl_set
        currentl_set = combine_set(currentl_set, k)
        current_set = min_support_items(
            currentl_set, transaction_list, min_support, freq_set
        )
        currentl_set = current_set
        k = k + 1

    #Pruning
    frequent_items = []
    if not large_set:
        return []
    length = 1
    while length<len(large_set):
        for item in large_set.get(length):
            is_superset_frequent = False
            for superset in large_set.get(length+1):
                if frozenset.issubset(item, superset):
                    is_superset_frequent = True
            if not is_superset_frequent:
                frequent_items.append((tuple(item), freq_set[item]))
        length = length+1
    for item in large_set.get(length):
        frequent_items.append((tuple(item), freq_set[item]))
    return frequent_items

def format_results(items):
    """prints the generated item_sets sorted by support"""
    i = []
    for item, count in sorted(items, key=lambda x: x[1]):
        x = "item: %s ,suport: %s" % (str(item), str(count))
        i.append(x)
    return i


def get_data(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, newline="") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(list(map(str.strip, line.split(",")[1:])))
            #print(record)
            yield record



