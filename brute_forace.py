import itertools


class BruteForceAssociationRuleMiner:
    def __init__(self, data, min_support=0.1, min_confidence=0.5):
        self.data = data
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.itemset_counts = {}
        self.frequent_itemsets = []
        self.association_rules = []

    def calculate_support(self, itemset):
        return sum(1 for transaction in self.data if itemset.issubset(transaction)) / len(self.data)

    def find_frequent_itemsets(self):
        self.itemset_counts = {}
        self.frequent_itemsets = []

        for transaction in self.data:
            for item in transaction:
                if item in self.itemset_counts:
                    self.itemset_counts[item] += 1
                else:
                    self.itemset_counts[item] = 1

        for itemset_size in range(2, len(self.itemset_counts) + 1):
            for itemset in itertools.combinations(self.itemset_counts.keys(), itemset_size):
                itemset = set(itemset)
                support = self.calculate_support(itemset)
                if support >= self.min_support:
                    self.frequent_itemsets.append((itemset, support))

    def generate_association_rules(self):
        self.association_rules = []

        for itemset, support in self.frequent_itemsets:
            for item in itemset:
                antecedent = itemset - {item}
                confidence = support / self.itemset_counts[item]
                if confidence >= self.min_confidence:
                    self.association_rules.append((antecedent, {item}, support, confidence))

    def mine_association_rules(self):
        self.find_frequent_itemsets()
        self.generate_association_rules()

    def display_association_rules(self):
        for rule in self.association_rules:
            antecedent, consequent, support, confidence = rule
            print(f"Rule: {antecedent} => {consequent}")
            print(f"Support: {support}")
            print(f"Confidence: {confidence}")
            print()
