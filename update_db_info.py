
import os.path

from tqdm import tqdm

import utility as u
import os
import argparse

from psycopg2._psycopg import AsIs
from query import Query


def get_distinct_entries(db_string: str, table: str, column: str) -> list[str]:
    conn, cursor = u.establish_connection(db_string)
    sql_string = "SELECT DISTINCT({}) FROM {};".format(column, table)
    cursor.execute(sql_string)
    result = cursor.fetchall()
    result = [i[0] for i in result]
    cursor.close()
    conn.close()
    return result


def get_sample_cardinalities(db_string: str, table: str, column: str, samples: str) -> list[int]:
    conn, cursor = u.establish_connection(db_string)
    cursor.execute("SELECT COUNT(%s) FROM %s WHERE %s in %s GROUP BY %s",
                   [AsIs(column), AsIs(table), AsIs(column), tuple(samples), AsIs(column)])
    result = cursor.fetchall()
    result = [i[0] for i in result]
    cursor.close()
    conn.close()
    return result


def get_wildcard_cardinality(db_string: str, table: str, column: str, operator: str, filter_attribute: str):
    conn, cursor = u.establish_connection(db_string)
    cursor.execute("SELECT COUNT(%s) FROM %s where %s %s %s",
                   (AsIs(column), AsIs(table), AsIs(column), AsIs(operator), filter_attribute))
    return cursor.fetchall()[0][0]


def main(minmax_path, db_string, overwrite, label_path, wildcard_path, queries, query_path):

    if not os.path.exists(minmax_path + "mm_dict.pkl") or overwrite:
        min_max_dict = u.build_db_min_max(db_string)
        u.save_pickle(min_max_dict, minmax_path + "mm_dict.pkl")
    else:
        print('Min-Max dictionary path already exists. Consider deleting the dictionary or changing the save path using'
              ' the -mm option.')
    # change exists
    if not os.path.exists(label_path + "label_encoders.pkl") or overwrite:
        label_encoders = u.build_label_encoders(db_string)
        # save every label encoder to counter memory overload
        u.save_pickle(label_encoders, label_path + "label_encoders.pkl")
    else:
        print("Label encoder path already exists. Consider deleting them or changing the save path using the -l option")

    if not os.path.exists(wildcard_path + "wildcard_dict.json") or overwrite:
        wild_card_dict = u.tree()
        db_type_dict = u.build_db_type_dict(db_string)
        for query_name in tqdm(queries):
            query = Query(query_name, query_path)
            for table in query.attributes:
                max_v = 0
                for column in query.attributes[table]:
                    for operator in query.attributes[table][column]:
                        if (operator == "like" or operator == "ilike") \
                                and db_type_dict[table][column] == "character varying" \
                                or db_type_dict[table][column] == "character":

                            filter_attribute = query.attributes[table][column][operator]
                            # check if we would overwrite an entry beforehand
                            if filter_attribute in wild_card_dict[table][column].keys():
                                if wild_card_dict[table][column][filter_attribute] > 0:
                                    continue

                            if max_v == 0:
                                conn, cursor = u.establish_connection(db_string)
                                cursor.execute("SELECT COUNT(*) FROM {}".format(table))
                                max_v = cursor.fetchall()[0][0]
                                wild_card_dict[table]['max'] = max_v

                            cardinality = get_wildcard_cardinality(db_string, table, column, operator, filter_attribute)
                            if cardinality:
                                wild_card_dict[table][column][filter_attribute] = cardinality
        u.save_json(wild_card_dict, wildcard_path + "wildcard_dict.json")
    else:
        print("Wildcard information path already exists. "
              "Consider deleting them or changing the save path using the -w option")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect database information such that featurization can be sped up")
    parser.add_argument("db", help="Database string in the psycopg2-format.")
    parser.add_argument("-mm", "--minmax", default="", help="Save path for min-max dictionary. Defaults to program "
                                                            "execution root.")
    parser.add_argument("-ow", "--overwrite", default=False, help="Option to overwrite existing paths")
    parser.add_argument("-l", "--label", default="", help="path to label encoders")
    parser.add_argument("-w", "--wildcard", default="", help="path to wildcard information")
    parser.add_argument("-q", "--queries", default="", help="training queries to be used for wild card filters")

    args = parser.parse_args()

    args_db_string = args.db
    if args_db_string == 'imdb':
        args_db_string = u.PG_IMDB
    elif args_db_string == 'stack':
        args_db_string = u.PG_STACK_OVERFLOW
    elif args_db_string == "stack-2016":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_16
    elif args_db_string == "stack-2013":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_13
    elif args_db_string == "stack-2010":
        args_db_string = u.PG_STACK_OVERFLOW_REDUCED_10
    elif args_db_string == "tpch":
        args_db_string = u.PG_TPC_H
    args_mm = args.minmax
    args_label = args.label
    args_wildcard = args.wildcard
    args_overwrite = args.overwrite
    args_queries = u.get_queries(args.queries)

    main(args_mm, args_db_string, args_overwrite, args_label, args_wildcard, args_queries, args.queries)
