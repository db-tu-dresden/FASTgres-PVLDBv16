
import utility as u
import argparse

from hint_sets import HintSet
from tqdm import tqdm


def get_queries_to_fill(prediction_dict):
    return list(prediction_dict.keys())


class FillingElements:
    # possible BAO 'Arms' we take care of 63 is pg default and already done
    # 111 111 -> 63
    # 110 111 -> 63 - 8 = 55
    # 101 111 -> 63 - 16 = 47
    # 101 011 -> 47 - 4 = 43
    # 100 011 -> 43 - 8 = 35
    bao_hints = [55, 47, 43, 35]

    def __init__(self, eval_dict, use_bao, additions, query_path, db_info, prediction_path, prediction_format):
        self.eval_dict = eval_dict
        self.use_bao = use_bao
        self.additions = additions
        self.query_path = query_path
        self.db_info = db_info
        self.prediction_path = prediction_path
        self.format = prediction_format
        self.predictions = self.get_predictions()

    def get_predictions(self):
        if self.format == "classic":
            predictions = [u.load_json(self.prediction_path)]
        else:
            predictions = list()
            multi_predictions = u.load_pickle(self.prediction_path)
            for context in multi_predictions:
                for split in multi_predictions[context]:
                    predictions.append(multi_predictions[context][split])
        return predictions


def update_optimal_solution(eval_dict):
    for query_name in eval_dict:
        opt_set = eval_dict[query_name]["opt"]
        opt_time = eval_dict[query_name][str(opt_set)]
        for hint_set in eval_dict[query_name]:
            if hint_set == "opt":
                continue
            if eval_dict[query_name][str(hint_set)] < opt_time:
                print(f"Fixing optimal set {query_name}: {opt_set} -> {hint_set}")
                eval_dict[query_name]["opt"] = hint_set
    return eval_dict


def fill_dict(fill_elements: FillingElements, save_path):
    print(f"Detected {len(fill_elements.predictions)} dictionaries to fill")
    for prediction_dict in tqdm(fill_elements.predictions):
        fill_elements.eval_dict = fill_single_dict(fill_elements, prediction_dict)
        # fill_elements.eval_dict = update_optimal_solution(fill_elements.eval_dict)
        u.save_json(fill_elements.eval_dict, save_path)
        print("Done Saving.")
    return


def fill_single_dict(fill_elements: FillingElements, prediction_dict):
    bao_hints = fill_elements.bao_hints
    eval_dict = fill_elements.eval_dict
    eval_bao = fill_elements.use_bao
    queries = get_queries_to_fill(prediction_dict)
    additions = fill_elements.additions
    q_path = fill_elements.query_path

    for query in tqdm(queries):
        try:
            pg_default_time = min(150, eval_dict[query]['63'])
        except:
            pg_default_time = 150
        # double default time with 1 second offset suffices to show bad queries, even for smaller loads
        timeout = int(2 * pg_default_time + 1)

        prediction = prediction_dict[query]

        hints_to_evaluate = set(additions)
        try:
            _ = eval_dict[query][str(prediction)]
        except KeyError:
            hints_to_evaluate.add(int(prediction))

        if eval_bao:
            for bao_hint in bao_hints:
                try:
                    _ = eval_dict[query][str(bao_hint)]
                except KeyError:
                    hints_to_evaluate.add(int(bao_hint))

        for hint_set_int in hints_to_evaluate:

            try:
                # catch additions
                _ = eval_dict[query][str(hint_set_int)]
                continue
            except KeyError:
                pass

            eval_hint_set = HintSet(hint_set_int)
            pred_eval = u.evaluate_hinted_query(q_path, query, eval_hint_set, fill_elements.db_info, timeout)

            if pred_eval is None:
                # unneeded cast to be safe
                pred_eval = int(timeout)
            eval_dict[query][str(hint_set_int)] = pred_eval

    return eval_dict


def run():
    print('Using Dictionary Filling v.0.1.0 - Revised')
    parser = argparse.ArgumentParser(description="Evaluate Fastgres on given strategy")
    parser.add_argument("eval", default=None, help="Evaluation dictionary path")
    parser.add_argument("-p", "--prediction", default=None,
                        help="Path to the prediction dict to consider")
    parser.add_argument("-b", "--bao", default=False,
                        help="Additionally evaluates five Hint Sets from BAO if not done already. "
                             "Can be set to True or False")
    parser.add_argument("-a", "--addition", default=None, help="Path to additional hints to consider (JSON-list)")
    parser.add_argument("-qp", "--querypath", default="stack", help="Queries to use. stack or job.")
    parser.add_argument("-db", "--dbinfo", default="stack", help="Database to use. Currently supports stack and imdb")
    parser.add_argument("-f", "--format", default="classic", help="Which format the predictions are. "
                                                                  "classic: Query -> Hint Set json or "
                                                                  "multi: Context -> Split -> Query -> Prediction pkl")
    args = parser.parse_args()

    args_eval = args.eval
    args_prediction_path = args.prediction
    args_bao = True if args.bao == "True" else False
    if args.addition is None:
        args_addition = list()
    else:
        args_addition = list(u.load_json(args.addition))

    args_eval_dict = u.load_json(args_eval)

    args_dbi = args.dbinfo
    if args_dbi == "stack":
        args_dbinfo = u.PG_STACK_OVERFLOW
    elif args_dbi == "imdb":
        args_dbinfo = u.PG_IMDB
    elif args_dbi == "stack-2016":
        args_dbinfo = u.PG_STACK_OVERFLOW_REDUCED_16
    elif args_dbi == "stack-2013":
        args_dbinfo = u.PG_STACK_OVERFLOW_REDUCED_13
    elif args_dbi == "stack-2010":
        args_dbinfo = u.PG_STACK_OVERFLOW_REDUCED_10
    elif args_dbi == "tpch":
        args_dbinfo = u.PG_TPC_H
    else:
        raise ValueError("Unrecognized database info")

    args_query_path = args.querypath
    if args_query_path == "stack":
        args_q_path = "queries/stack/all/"
    elif args_query_path == "job":
        args_q_path = "queries/job/"
    elif args_query_path == "tpch":
        args_q_path = "queries/tpch/"
    else:
        raise ValueError("Query path input -qp -> {} not recognized".format(args_query_path))

    args_format = args.format
    if args_format != "classic" and args_format != "multi":
        raise ValueError("Unrecognized prediction format")

    print("Filling Predictions")
    filling_elements = FillingElements(args_eval_dict, args_bao, args_addition, args_q_path,
                                       args_dbinfo, args_prediction_path, args_format)

    fill_dict(filling_elements, args_eval)


if __name__ == "__main__":
    run()
