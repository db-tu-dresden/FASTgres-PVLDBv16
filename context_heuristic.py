
import utility as u
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram

# for now, most of these functions are unused and for possible future work


def merge_context_queries(context_query_dict: dict):
    new_dict = dict()
    new_context = set()
    merged = set()
    merged_dict = dict()
    for context in context_query_dict:
        new_context = new_context.union(set(context))
        merged.add(frozenset(context))
    new_context = frozenset(new_context)
    for context in context_query_dict:
        try:
            new_dict[new_context] = new_dict[new_context].union(context_query_dict[context])
        except KeyError:
            new_dict[new_context] = context_query_dict[context]
    merged_dict[new_context] = merged
    return new_dict, merged_dict


def get_roll_up_candidates(context_dict: dict, query_threshold: int):
    candidates = list()
    contexts = context_dict.keys()

    for context in contexts:
        context_queries = context_dict[context]
        if len(context_queries) < query_threshold:
            candidates.append(context)
    return candidates


def get_set_distance(set_1: set, set_2: set):
    distance = len((set_1.union(set_2)) - set_1.intersection(set_2))
    return distance


def build_triangular_distance_matrix(candidates):
    dim = len(candidates)
    triangular = np.zeros((dim, dim))

    # set distance commutes
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            triangular[i, j] = get_set_distance(set(candidates[i]), set(candidates[j]))

    return triangular


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
    return


def roll_up_context_dict(context_dict: dict, query_threshold: int, merge_distance: int) -> dict:
    merged_dict = context_dict.copy()
    while True:
        candidates = list(set(get_roll_up_candidates(merged_dict, query_threshold)))
        if not candidates:
            break

        triangular = build_triangular_distance_matrix(candidates)

        cluster = AgglomerativeClustering(metric="precomputed", linkage="single",
                                          distance_threshold=merge_distance, n_clusters=None)
        cluster.fit(triangular)

        c_labels = cluster.labels_
        uniques = np.unique(c_labels)
        for unique in uniques:
            to_merge = u.tree()
            for i in range(len(c_labels)):
                idx = c_labels[i]
                if unique == idx:
                    context = candidates[idx]
                    to_merge[context] = context_dict[context]
                    merged_dict.pop(context)
            merged = merge_context_queries(to_merge)
            merged_dict[merged.keys()] = merged[merged.keys()]

    print(context_dict.keys())
    print(merged_dict.keys())

    return context_dict

