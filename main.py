import sys
from dataset_generator import generate_datasets_with_different_num_of_unique_items, \
    generate_datasets_with_different_num_of_transactions
from groceries_analysis import run_analysis_with_fix_num_transactions, run_analysis_with_fix_num_unique_items

if __name__ == "__main__":
    if sys.version_info[0:2] != (3, 11):
        raise Exception("Requires python 3.11")

    fixed_transactions_count = 100
    unique_item_counts = [10, 15, 20, 25, 30, 35, 40]
    # generate dataset with fixed number of transactions and varying number of unique items
    # comment out next line to skip the data regeneration
    generate_datasets_with_different_num_of_unique_items(
        fixed_num_transactions=fixed_transactions_count,
        unique_item_counts=unique_item_counts,
        max_item_width=10)

    run_analysis_with_fix_num_transactions(
        fixed_transactions_count=fixed_transactions_count,
        unique_item_counts=unique_item_counts)

    fixed_unique_item_count = 20
    transactions_counts = [50, 60, 70, 80, 90, 100, 110]
    # generate dataset with fixed number of unique items and varying number of transaction
    # comment out next line to skip the data regeneration
    generate_datasets_with_different_num_of_transactions(
        fixed_unique_item_count=fixed_unique_item_count,
        transactions_counts=transactions_counts,
        max_item_width=10)

    run_analysis_with_fix_num_unique_items(
        fixed_unique_item_count=fixed_unique_item_count,
        transactions_counts=transactions_counts)
