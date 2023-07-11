
import utility as u
import argparse
import random
import os
import time
from tqdm import tqdm

hints = ['enable_hashjoin', 'enable_mergejoin', 'enable_nestloop',
         'enable_indexscan', 'enable_seqscan', 'enable_indexonlyscan']


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def run_train_query(q, dbi):
    conn, cur = u.establish_connection(dbi)
    cur.execute("SET enable_bao TO ON")  # enable bao in general
    cur.execute("SET enable_bao_selection TO OFF")  # enable bao to use predicted plans
    cur.execute("SET enable_bao_rewards TO ON")  # enable bao to collect training data
    cur.execute("SET bao_num_arms TO 5")
    cur.execute("SET statement_timeout TO 2400000")
    try:
        cur.execute(q)
        cur.fetchall()
    except:
        # If we really exceed the timeout, we return and work with the timeout time
        print('Exceeding timeout, using timeout as measure')
        cur.close()
        conn.close()
        return
    cur.close()
    conn.close()
    return


def run_test_query(q, dbi):
    conn, cur = u.establish_connection(dbi)

    t0 = time.time()
    cur.execute("SET enable_bao TO ON")
    cur.execute("SET enable_bao_selection TO OFF")
    cur.execute("SET enable_bao_rewards TO OFF")
    cur.execute("SET bao_num_arms TO 5")
    cur.execute("SET statement_timeout TO 2400000")
    t1 = time.time() - t0
    try:
        t0 = time.time()
        cur.execute('EXPLAIN ' + q)
        res = cur.fetchall()
        t2 = time.time() - t0
    except:
        # If we really exceed the timeout, we return default postgres - this should be really rare
        print('Exceeding timeout, using PG default')
        pred = [1]*6
        cur.close()
        conn.close()
        return pred, t1
    cur.close()
    conn.close()
    # get prediction through regex
    res_line = None
    for line_tuple in res:
        line = line_tuple[0]
        print(line)
        if 'Bao recommended hint' in line:
            res_line = line
            break
    print('\n')
    if res_line is None:
        raise ValueError('Something went wrong, no bao hint was found')
    if 'ON' in res_line:
        raise ValueError('Bao hint was switched on, this is unexpected behavior and must be caught: ', res_line)

    # every hint that has been shown to be switched off, is set to 0
    pred = [1]*6
    for k in range(len(hints)):
        hint = hints[k]
        if hint in res_line:
            pred[k] = 0

    return pred, t1 + t2


def get_query_content(queries, qp):
    read_queries = dict()
    for query in queries:
        with open(qp + query) as f:
            q = f.read()
        read_queries[query] = q
    return read_queries


def evaluate_bao(query_dict, read_queries, excluded_train_queries: list, dbi):
    seed = 29
    training_time = 0
    prediction_dict, setup_time_dict = dict(), dict()
    train_queries, test_queries = query_dict['train'], query_dict['test']

    difference = set(train_queries).difference(set(excluded_train_queries))
    if len(train_queries) - len(difference) != len(excluded_train_queries):
        raise ValueError("Train Query Splits do not ascend distinctively!")
    train_queries = list(sorted(difference))

    # shuffle with the same seed used throughout the whole evaluation
    random.Random(seed).shuffle(train_queries)

    train_query_range = range(len(train_queries))
    retrain_chunks = [max(i) for i in chunks([i for i in train_query_range], 25)]
    # test_query_range = range(len(test_queries))
    # test_chunks = [max(i) for i in chunks([i for i in test_query_range], 25)]

    # Training phase, like BAO, all 25 queries the model is retrained
    print('Train Phase')
    for j in tqdm(train_query_range):
        train_query = train_queries[j]
        run_train_query(read_queries[train_query], dbi)
        if j in retrain_chunks:
            # we also collect training times for soft comparison of model times
            print('Retraining Model...')
            t0 = time.time()
            os.system("cd ../BaoForPostgreSQL/bao_server && python baoctl.py --retrain")
            os.system("sync")
            training_time += (time.time() - t0)
            print('... done')

    # test queries have not been altered and are shuffled already
    print('Prediction Phase')
    for j in tqdm(range(len(test_queries))):
        test_query = test_queries[j]
        # BAO predicts hints to be switched off only, thus we return a binary list that needs to be cast to an int
        # We also save prediction time as setup time that is needed to obtain a prediction
        prediction, setup_time = run_test_query(read_queries[test_query], dbi)
        prediction = u.binary_to_int(prediction)

        prediction_dict[test_query] = prediction
        setup_time_dict[test_query] = setup_time

        # if we wish to save and retrain while testing
        # run_train_query(read_queries[test_query])
        # if j in test_chunks:
        #     print('Retraining Model...')
        #     t0 = time.time()
        #     os.system("cd ../BaoForPostgreSQL/bao_server && python baoctl.py --retrain")
        #     os.system("sync")
        #     training_time += (time.time() - t0)
        #     print('... done')

    return prediction_dict, training_time, setup_time_dict


def run():
    # python bao_server_eval.py path/to/query/dict.json -o path/to/output.json -pt path/to/pt.json
    print('BAO Evaluation v0.06')
    print('Be sure the BAO Server is up and running!')
    print('After each evaluation it is highly recommended to delete the BAO database as well as its trained model')
    parser = argparse.ArgumentParser(description="Evaluate BAO on given strategy")
    parser.add_argument("queries", default=None, help="Query path to train and test in json format.")
    parser.add_argument("-o", "--output", default=None, help="Output evaluation directory")
    parser.add_argument("-pt", "--process", default=None, help="path to processing time output.")
    parser.add_argument("-eq", "--excluded", default=None, help="List of queries to exclude as JSON.")
    parser.add_argument("-qp", "--querypath", default=None, help="Path to all queries.")
    parser.add_argument("-dbi", "--databaseinfo", default=None, help="Psycopg2 Database Info.")

    args = parser.parse_args()
    q_path = args.queries
    output_path = args.output
    pt_path = args.process
    excluded_train_queries_path = args.excluded
    args_qp = args.querypath

    args_db_string = args.databaseinfo
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

    if output_path is None:
        raise ValueError('No output directory path provided')
    read_queries = get_query_content(u.get_queries(args_qp), args_qp)

    excluded_train_queries = []
    if excluded_train_queries_path is not None:
        try:
            excluded_train_queries = list(u.load_json(excluded_train_queries_path))
        except:
            print("No excluded Queries found, continuing")

    query_dict = u.load_json(q_path)
    prediction_dict, training_time, setup_time_dict = evaluate_bao(query_dict, read_queries, excluded_train_queries,
                                                                   args_db_string)

    # saving routine
    u.save_json(prediction_dict, output_path)
    processing_time_dict = {"setup": setup_time_dict, "train-time": training_time}
    u.save_json(processing_time_dict, pt_path)
    return


if __name__ == "__main__":
    run()
