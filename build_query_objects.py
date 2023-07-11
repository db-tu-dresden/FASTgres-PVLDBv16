
import utility as u
from query import Query
from tqdm import tqdm, trange
from time import time


def main():
    print("Building Query Objects v.02 - xy Edition")
    path = "path/to/queries/"
    stack_queries = u.get_queries(path)

    save_path = "path/to/save.pkl"
    save_path_time = "path/to/save_timings.json"

    query_objects = dict()
    encoding_time = dict()
    for query_name in tqdm(stack_queries):
        t0 = time()
        query_objects[query_name] = Query(query_name, path)
        encoding_time[query_name] = time() - t0

    u.save_pickle(query_objects, save_path)
    u.save_json(encoding_time, save_path_time)
    print("Done")

    return


if __name__ == "__main__":
    main()
