
import math
import re
import time
import numpy as np
import json
import os
import pickle
import pandas as pd
import psycopg2 as pg

from tqdm import tqdm
from hint_sets import HintSet, set_hints
from typing import Optional as Opt
from mo_sql_parsing import parse
from configparser import ConfigParser
from collections import defaultdict

cfg = ConfigParser()
cfg.read("config.ini")

dbs = cfg["DBConnections"]
PG_IMDB = dbs["imdb"]
PG_STACK_OVERFLOW = dbs["stack_overflow"]
PG_STACK_OVERFLOW_REDUCED_16 = dbs["stack_overflow_reduced_16"]
PG_STACK_OVERFLOW_REDUCED_13 = dbs["stack_overflow_reduced_13"]
PG_STACK_OVERFLOW_REDUCED_10 = dbs["stack_overflow_reduced_10"]
PG_TPC_H = dbs["tpc_h"]

operator_dictionary = {
    "eq": [0, 0, 1],
    "gt": [0, 1, 0],
    "lt": [1, 0, 0],
    "lte": [1, 0, 1],
    "gte": [0, 1, 1],
    "neq": [1, 1, 0],
    "IS": [0, 0, 1],
    "in": [0, 0, 1],
    "like": [1, 1, 1]
}


def min_max_encode(min_value, max_value, value_to_encode, offset):
    value_to_encode = min(value_to_encode, max_value)
    value_to_encode = max(value_to_encode, min_value)
    adjusted_min = min_value - offset
    encoding = round((value_to_encode - adjusted_min) / (max_value - adjusted_min), 8)
    return encoding


def get_sorted_dict(values, sort_by):
    mixed = list(zip(values, sort_by))
    mixed.sort(key=lambda x: x[1])
    mixed_dict = {mixed[i][0]: i for i in range(len(values))}
    return mixed_dict


class MyLabelEncoder:
    def __init__(self):
        self.classes_ = None
        self.encoder = dict()

    def fit(self, y: list, sorty_by: list) -> None:
        self.classes_ = pd.Series(y).unique()
        self.encoder = get_sorted_dict(y, sorty_by)
        return

    def transform(self, values: list) -> list:
        return_list = list()
        for item in values:
            return_list.append(self.encoder[item])
        return return_list


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def tree() -> defaultdict:
    return defaultdict(tree)


def get_queries(path: str) -> list[str]:
    queries = list()
    for file in os.scandir(path):
        if os.path.isfile(os.path.join(path, file.name)):
            if file.name.endswith('sql'):
                queries.append(file.name)
    return queries


def get_parsed_queries(queries: list[str], parsed_path: str):
    parsed = dict()
    for query in queries:
        parsed_name = query[:-4] + '.json'
        parsed[query] = load_json(parsed_path + parsed_name)
    return parsed


def binary_to_int(bin_list: list[int]) -> int:
    return int("".join(str(x) for x in bin_list), 2)


def int_to_binary(integer: int) -> list[int]:
    return [int(i) for i in bin(integer)[2:].zfill(len(HintSet.operators))]


def one_hot_to_binary(one_hot_vector: list[int]) -> list[int]:
    ind = int(np.argmax(one_hot_vector))
    return int_to_binary(ind)


def load_json(path: str):
    with open(path, 'r') as file:
        loaded = json.load(file)
    return loaded


def load_pickle(path: str):
    with open(path, 'rb') as file:
        loaded = pickle.load(file)
    return loaded


def save_json(to_save, path: str) -> None:
    json_dict = json.dumps(to_save)
    with open(path, 'w') as f:
        f.write(json_dict)
    return


def save_pickle(to_save, path: str) -> None:
    with open(path, 'wb') as f:
        pickle.dump(to_save, f)
    return


def replace_expression_in_query(query_path: str, query: str, expression: str, replacement: str,
                                write_to_new: bool = False) -> None:
    with open(query_path + query, 'r', encoding='utf-8') as file:
        data = file.read()
    data = data.replace(expression, replacement)
    save_path = query_path + query
    if write_to_new:
        save_path += '_replaced'
    with open(query_path + query, 'w', encoding='utf-8') as file:
        file.write(data)
    return


def add_or_create_dict_entry(dictionary: dict, key, values) -> dict:
    if key in dictionary.keys():
        if isinstance(values, list):
            union = dictionary[key].union(values)
        else:
            union = dictionary[key].union([values])
    else:
        if isinstance(values, list):
            union = set(values)
        else:
            union = {values}
    dictionary[key] = union
    return dictionary


def merge_disjunct_dicts(dict1: dict, dict2: dict) -> dict:
    for key in dict1:
        if key in dict2:
            raise KeyError("Trying to merge non-disjunct dictionaries")
    return {**dict1, **dict2}


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except:
        return False


def parse_query(query_path: str, query: str):
    with open(query_path + query, encoding='utf-8') as file:
        q = file.read()
    try:
        parsed_query = parse(q)
    except:
        print(query)
        raise ValueError('Could not parse query')
    return parsed_query


def is_query(parsed_statement):
    try:
        t = parsed_statement['select']
        return True
    except:
        return False


def build_db_min_max(db_string: str) -> dict:
    unhandled = set()
    conn, cursor = establish_connection(db_string)
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    mm_dict = dict()
    for table in cursor.fetchall():
        t = table[0]
        cursor.execute(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}';".format(t))
        col_dict = dict()
        for column, d_type in cursor.fetchall():
            if d_type in ['integer', 'timestamp without time zone', 'date', 'numeric']:
                cursor.execute("SELECT min({}), max({}) FROM {};".format(column, column, t))
                mm_val = list(cursor.fetchall()[0])
                col_dict[column] = mm_val
            else:
                unhandled.add(d_type)
        mm_dict[t] = col_dict
    cursor.close()
    conn.close()
    print('Unhandled d_types: ', unhandled)
    return mm_dict


def build_label_encoders(db_string: str) -> tree:
    unhandled = set()
    label_encoders = tree()
    conn, cursor = establish_connection(db_string)
    cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        t = table[0]
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns  WHERE table_name = '{}';"
                       .format(t))
        for column, d_type in tqdm(cursor.fetchall()):
            if d_type == 'character varying' or d_type == 'character':
                skip = False
                if "stack_overflow" in db_string:
                    skipped_string_columns = {
                        "account": ["display_name"],
                        "answer": ["title", "body"],
                        "question": ["title", "tagstring", "body"],
                        "site": ["site_name"],
                        "tag": ["name"],
                        "badge": ["name"],
                        "comment": ["body"]
                    }
                    # skipping all unneeded columns
                    for skipped_table in skipped_string_columns:
                        if t == skipped_table and column in skipped_string_columns[skipped_table]:
                            skip = True
                            break
                if skip:
                    continue

                cursor.execute("SELECT {}, COUNT({}) FROM {} GROUP BY {}".format(column, column, t, column))
                filter_list = list()
                for filter_value, cardinality in cursor.fetchall():
                    filter_list.append((filter_value, cardinality))
                print("Fitting label encoder to table: {}, column: {}".format(t, column))
                label_encoder = MyLabelEncoder()
                label_encoder.fit(*list(zip(*filter_list)))
                label_encoders[t][column] = label_encoder
            else:
                unhandled.add(d_type)
    cursor.close()
    conn.close()
    print("Unhandled types for label encoding: {}".format(unhandled))

    return label_encoders


def get_context(query_name, path) -> frozenset:
    parsed = parse_query(path, query_name)
    table_dict = dict()
    for entry in parsed['from']:
        try:
            # alias - name
            table_dict[entry['name']] = entry['value']
        except (KeyError, TypeError):
            # no alias
            table_dict[entry] = entry
    return frozenset(sorted(table_dict.values()))


def get_context_dict() -> dict:
    context_dict = {0: {"site", "so_user", "tag", "tag_question", "question", "badge", "account"},
                    1: {"site", "so_user", "tag", "tag_question", "question", "answer"},
                    2: {"site", "tag", "tag_question", "question"},
                    3: {"site", "so_user", "tag", "tag_question", "question", "badge", "account", "answer"},
                    4: {"site", "post_link", "question"},
                    5: {"site", "so_user", "tag", "tag_question", "question", "account"},
                    6: {"site", "so_user", "tag", "tag_question", "question", "account", "answer"},
                    7: {"site", "so_user", "tag", "tag_question", "question", "comment", "account"},
                    8: {"site", "post_link", "tag", "tag_question", "question", "comment"},
                    9: {"site", "so_user", "tag", "tag_question", "question", "post_link", "account"},
                    10: {"so_user", "badge", "account"}}
    return context_dict


def establish_connection(connection_string: str):
    try:
        connection = pg.connect(connection_string)
        # https://www.psycopg.org/docs/usage.html#transactions-control
        connection.autocommit = True
    except ConnectionError:
        raise ConnectionError('Could not connect to database server')
    cursor = connection.cursor()
    return connection, cursor


def evaluate_hinted_query(path: str, query: str, hint_set: HintSet, connection_string: str, timeout: Opt[float]) \
        -> Opt[float]:
    with open(path + query, encoding='utf-8') as file:
        q = file.read()

    conn, cur = establish_connection(connection_string)
    if timeout is not None:
        # catch faulty timeout measures due to floating point inaccuracies
        if timeout <= 0.0:
            print('Adjusting timeout from {}'.format(timeout))
            timeout = 0.1
        # set and execute timeout to avoid unnecessary computation
        # timeout is in milliseconds: round up and cast to int
        time_out = "SET statement_timeout = '{}ms'".format(int(math.ceil(timeout * 1000)))
        cur.execute(time_out)

    set_hints(hint_set, cur)
    try:
        start = time.time()
        cur.execute(q)
        stop = time.time()
    except:
        return None

    cur.close()
    conn.close()
    return stop - start


def evaluate_k_times(q_path: str, query: str, hint_set: HintSet, connection_string: str, timeout: int, k=5) \
        -> Opt[float]:
    evaluations = list()
    for i in range(k + 1):
        hint_eval = evaluate_hinted_query(q_path, query, hint_set, connection_string, timeout)
        if hint_eval is None:
            # forward timeout
            return None
        evaluations.append(hint_eval)
    # even out measurement fluctuations
    max_v = max(evaluations)
    average = (sum(evaluations) - max_v) / k
    return average


def build_db_type_dict(db_string: str) -> tree:
    conn, cursor = establish_connection(db_string)
    cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
    d_type_dict = tree()
    for table in cursor.fetchall():
        t = table[0]
        cursor.execute(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}';".format(t))
        for column, d_type in cursor.fetchall():
            d_type_dict[t][column] = d_type
    return d_type_dict


def get_explain_cost(query, cursor, hint_set: HintSet):
    # returns lower and upper bounds of root note of an explain tree
    set_hints(hint_set, cursor)
    sql_string = "EXPLAIN {}".format(query)
    cursor.execute(sql_string)
    result = cursor.fetchall()
    pattern = '\d+\.\d+'
    lower, upper = re.findall(pattern, result[0][0])
    return lower, upper


def read_query(query_name, path):
    with open(path + query_name, encoding='utf-8') as file:
        query = file.read()
    return query


def ping_bao_server(query: str, db_string: str) -> bool:
    conn, cur = establish_connection(db_string)

    timeout = 2400000
    cur.execute("SET enable_bao TO ON")
    cur.execute("SET enable_bao_selection TO OFF")
    cur.execute("SET enable_bao_rewards TO OFF")
    cur.execute("SET bao_num_arms TO 5")
    cur.execute("SET statement_timeout TO {}".format(timeout))
    try:
        cur.execute('EXPLAIN ' + query)
        result_string = cur.fetchall()
    except:
        raise ConnectionError("Explain timed out")
    cur.close()
    conn.close()

    for line_tuple in result_string:
        line = line_tuple[0]
        if 'Bao prediction' in line:
            # Bao server is alive
            return True
    return False
