import ast
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
from brute_forace import BruteForceAssociationRuleMiner


def get_brute_force_execution_time(transactions):
    start = time.time()

    bf = BruteForceAssociationRuleMiner(
        data=transactions,
        min_support=0.002,
        min_confidence=0.05,
    )
    bf.mine_association_rules()
    end = time.time()

    execution_time = end - start
    return execution_time


def get_estimated_brute_force_execution_time(
        execution_time_on_small_dataset,
        num_of_transactions_on_small_dataset,
        num_of_unique_items_on_small_dataset,
        actual_num_of_transactions,
        actual_num_of_unique_items):
    # knowing that the time complexity of brute force is O((2^N)*T)
    # where T is the number of transactions, N is the number of unique items
    # calculate the constant factor
    c = execution_time_on_small_dataset / ((2 ** num_of_unique_items_on_small_dataset) *
                                           num_of_transactions_on_small_dataset)

    # based on the constant to estimate the execution time on large dataset
    estimated_execution_time = c * (
            2 ** actual_num_of_unique_items) * actual_num_of_transactions

    return estimated_execution_time


def get_fp_growth_execution_time(transactions):
    start = time.time()

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=0.002, use_colnames=True)
    association_rules(frequent_itemsets, metric="confidence", min_threshold=0.05)

    end = time.time()
    execution_time = end - start
    return execution_time


def get_apriori_execution_time(transactions):
    start = time.time()

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.002, use_colnames=True)
    association_rules(frequent_itemsets, metric="confidence", min_threshold=0.05)

    end = time.time()
    execution_time = end - start
    return execution_time


def run_analysis_with_fix_num_transactions(fixed_transactions_count, unique_item_counts):
    execution_times = {"brute_force": [], "fp_growth": [], "apriori": []}
    execution_times_mean = {"brute_force": [], "fp_growth": [], "apriori": []}
    num_of_iterations = 10

    for index, item_counts in enumerate(unique_item_counts):
        df = pd.read_csv(
            "./datasets/" + str(fixed_transactions_count) + "_transactions_" + str(item_counts) + "_unique_items.csv")
        # convert the string literal in Item column to a list
        df['Items'] = df['Items'].apply(ast.literal_eval)
        transactions = df["Items"]

        brute_force_execution_times = []
        fp_growth_execution_times = []
        apriori_execution_times = []
        for i in range(num_of_iterations):
            if index == 0:
                brute_force_execution_times.append(get_brute_force_execution_time(transactions))
            else:
                estimated_brute_force_execution_time = get_estimated_brute_force_execution_time(
                    execution_time_on_small_dataset=execution_times["brute_force"][0][i],
                    num_of_transactions_on_small_dataset=fixed_transactions_count,
                    num_of_unique_items_on_small_dataset=unique_item_counts[0],
                    actual_num_of_transactions=fixed_transactions_count,
                    actual_num_of_unique_items=item_counts)
                brute_force_execution_times.append(estimated_brute_force_execution_time)

            fp_growth_execution_times.append(get_fp_growth_execution_time(transactions))
            apriori_execution_times.append(get_apriori_execution_time(transactions))

        execution_times["brute_force"].append(brute_force_execution_times)
        avg = mean(brute_force_execution_times)
        print("average execution time for Brute-force:",
              avg, "sec (T=", fixed_transactions_count, " N=", item_counts, ")")
        execution_times_mean["brute_force"].append(mean(brute_force_execution_times))

        execution_times["fp_growth"].append(fp_growth_execution_times)
        avg = mean(fp_growth_execution_times)
        print("average execution time for FP-Growth:",
              avg, "sec (T=", fixed_transactions_count, " N=", item_counts, ")")
        execution_times_mean["fp_growth"].append(mean(fp_growth_execution_times))

        execution_times["apriori"].append(apriori_execution_times)
        avg = mean(apriori_execution_times)
        print("average execution time for Apriori:",
              avg, "sec (T=", fixed_transactions_count, " N=", item_counts, ")")
        execution_times_mean["apriori"].append(mean(apriori_execution_times))
        print("*" * 20, "\n")

    fig, axs = plt.subplots(3)
    fig.suptitle("Fixed number of " + str(fixed_transactions_count) + " transactions")

    axs[0].set_title("Brute Force")
    axs[0].plot(np.arange(len(execution_times_mean["brute_force"])) + 1, execution_times_mean["brute_force"],
                color='r', label="")
    axs[0].boxplot(execution_times["brute_force"], labels=unique_item_counts, patch_artist=True)

    axs[1].set_title("FP-Growth")
    axs[1].plot(np.arange(len(execution_times_mean["fp_growth"])) + 1, execution_times_mean["fp_growth"],
                color='g')
    axs[1].boxplot(execution_times["fp_growth"], labels=unique_item_counts, patch_artist=True)

    axs[2].set_title("Apriori")
    axs[2].plot(np.arange(len(execution_times_mean["apriori"])) + 1, execution_times_mean["apriori"],
                color='b')
    axs[2].boxplot(execution_times["apriori"], labels=unique_item_counts, patch_artist=True)

    for ax in axs.flat:
        ax.set(xlabel='Number of unique items', ylabel='Time (sec)')

    plt.tight_layout()
    plt.savefig('./figures/fixed_num_transactions.png')
    plt.show()



def run_analysis_with_fix_num_unique_items(fixed_unique_item_count, transactions_counts):
    execution_times = {"brute_force": [], "fp_growth": [], "apriori": []}
    execution_times_mean = {"brute_force": [], "fp_growth": [], "apriori": []}
    num_of_iterations = 10

    for index, transactions_count in enumerate(transactions_counts):
        df = pd.read_csv(
            "./datasets/" + str(fixed_unique_item_count) + "_unique_items_" + str(transactions_count)
            + "_transactions.csv")
        # convert the string literal in Item column to a list
        df['Items'] = df['Items'].apply(ast.literal_eval)
        transactions = df["Items"]

        brute_force_execution_times = []
        fp_growth_execution_times = []
        apriori_execution_times = []
        for i in range(num_of_iterations):
            if index == 0:
                brute_force_execution_times.append(get_brute_force_execution_time(transactions))
            else:
                estimated_brute_force_execution_time = get_estimated_brute_force_execution_time(
                    execution_time_on_small_dataset=execution_times["brute_force"][0][i],
                    num_of_transactions_on_small_dataset=transactions_counts[0],
                    num_of_unique_items_on_small_dataset=fixed_unique_item_count,
                    actual_num_of_transactions=transactions_count,
                    actual_num_of_unique_items=fixed_unique_item_count)
                brute_force_execution_times.append(estimated_brute_force_execution_time)

            fp_growth_execution_times.append(get_fp_growth_execution_time(transactions))
            apriori_execution_times.append(get_apriori_execution_time(transactions))

        execution_times["brute_force"].append(brute_force_execution_times)
        avg = mean(brute_force_execution_times)
        print("average execution time for Brute-force:",
              avg, "sec (T=", transactions_count, " N=", fixed_unique_item_count, ")")
        execution_times_mean["brute_force"].append(mean(brute_force_execution_times))

        execution_times["fp_growth"].append(fp_growth_execution_times)
        avg = mean(fp_growth_execution_times)
        print("average execution time for FP-Growth:",
              avg, "sec (T=", transactions_count, " N=", fixed_unique_item_count, ")")
        execution_times_mean["fp_growth"].append(mean(fp_growth_execution_times))

        execution_times["apriori"].append(apriori_execution_times)
        avg = mean(apriori_execution_times)
        print("average execution time for Apriori:",
              avg, "sec (T=", transactions_count, " N=", fixed_unique_item_count, ")")
        execution_times_mean["apriori"].append(mean(apriori_execution_times))
        print("*" * 20, "\n")

    fig, axs = plt.subplots(3)
    fig.suptitle("Fixed number of " + str(fixed_unique_item_count) + " unique items")

    axs[2].set_title("Brute Force")
    axs[0].plot(np.arange(len(execution_times_mean["brute_force"])) + 1, execution_times_mean["brute_force"],
                color='r')
    axs[0].boxplot(execution_times["brute_force"], labels=transactions_counts, patch_artist=True)

    axs[2].set_title("FP-Growth")
    axs[1].plot(np.arange(len(execution_times_mean["fp_growth"])) + 1, execution_times_mean["fp_growth"],
                color='g')
    axs[1].boxplot(execution_times["fp_growth"], labels=transactions_counts, patch_artist=True)

    axs[2].set_title("Apriori")
    axs[2].plot(np.arange(len(execution_times_mean["apriori"])) + 1, execution_times_mean["apriori"],
                color='b')
    axs[2].boxplot(execution_times["apriori"], labels=transactions_counts, patch_artist=True)

    for ax in axs.flat:
        ax.set(xlabel='Number of transactions', ylabel='Time (sec)')

    plt.tight_layout()
    plt.savefig('./figures/fixed_num_unique_items.png')
    plt.show()
