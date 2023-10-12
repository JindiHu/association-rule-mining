import itertools
import random
import pandas as pd


def generate_transactions():
    df = pd.read_csv('datasets/groceries_dataset.csv', sep=',')
    print(df.shape)
    unique_items = df["itemDescription"].unique()
    num_of_unique_items = len(unique_items)
    # Group by Member_number and Date, and aggregate the items as lists
    data = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).reset_index()
    data.columns = ['Member_number', 'Date', 'Items']

    transactions = data["Items"]
    num_of_transactions = len(transactions)
    return transactions, unique_items, num_of_transactions, num_of_unique_items


def generate_datasets_with_different_num_of_unique_items(fixed_num_transactions,
                                                         max_item_width,
                                                         unique_item_counts):
    transactions, unique_items, num_of_transactions, num_of_unique_items = generate_transactions()

    print("Summary of transactions from original dataset")
    print("number of transactions:", num_of_transactions)
    print("number of unique items:", num_of_unique_items)

    # Create subsets with varying numbers of unique items
    for num_items in unique_item_counts:
        transactions_sample = {"Items": []}
        available_items = list(set(itertools.islice(unique_items, num_items)))
        for i in range(fixed_num_transactions):
            transaction = []
            num_of_items = random.randint(1, max_item_width)
            for _ in range(num_of_items):
                transaction.append(random.choice(available_items))
            transactions_sample["Items"].append(transaction)

        df = pd.DataFrame(transactions_sample, columns=['Items'])
        df.to_csv(f'./datasets/fixed_num_transactions/{fixed_num_transactions}_transactions_{num_items}_unique_items.csv', index=False)
    print("datasets with different number of unique items created successfully")
    print("*" * 20, "\n")


def generate_datasets_with_different_num_of_transactions(fixed_unique_item_count,
                                                         max_item_width,
                                                         transactions_counts):
    transactions, unique_items, num_of_transactions, num_of_unique_items = generate_transactions()

    print("Summary of transactions from original dataset")
    print("number of transactions:", num_of_transactions)
    print("number of unique items:", num_of_unique_items)

    # Create subsets with varying numbers of transactions
    for num_transactions in transactions_counts:
        transactions_sample = {"Items": []}
        available_items = list(set(itertools.islice(unique_items, fixed_unique_item_count)))
        for i in range(num_transactions):
            transaction = []
            num_of_items = random.randint(1, max_item_width)
            for _ in range(num_of_items):
                transaction.append(random.choice(available_items))
            transactions_sample["Items"].append(transaction)

        df = pd.DataFrame(transactions_sample, columns=['Items'])
        df.to_csv(f'./datasets/fixed_num_unique_items/{fixed_unique_item_count}_unique_items_{num_transactions}_transactions.csv', index=False)
    print("datasets with different number of unique items created successfully")
    print("*" * 20, "\n")
