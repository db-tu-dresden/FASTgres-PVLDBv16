# FASTgres

This repository contains FASTgres, the learned model to enhance hint set prediction using context based gradient boosting. Currently, FASTgres is designed to evaluate a given workload. 

Note that this implementation is still in development and may be subject to change.

## Introduction

We shortly introduce FASTgres' architecture to reinforce the necessary steps when evaluating a workload.

![FASTgres Architecture](docs/figures/fg_workflow.svg)

FASTgres has an input workload that on which it is trained. Since FASTgres uses **supervised learning**, such a workload needs to be **labeled**. For evaluation purposes it is adviced to also label any traing set or simply the whole data set in advance.

To be able to encode each query (i.e., **featurization**), additional **database and workload statistics** have to be obtained.

Lastly, FASTgres can be run to obtain workload predictions that can then be evaluated.


Note that FASTgres does not support all commonly available workload at this moment, as it is still in a very early stage of development.
Currently supported workloads include Stack-Overflow [^1] and Join-Order-Benchmark [^2]. TPC-H [^3] has been evaluated but its support is currently disabled due to refactoring.

**TLDR:** FASTgres:
- Needs labeled data, and database and workload information
- Supports Stack, JOB, and TPCH (currently disabled)

## Project Structure

| Name | Description |
|------|-------------|
| db_info | Folder that contains information for each workload. Some pregenerated auxiliary information is already present. This is the folder in which the generated database information should reside |
| queries | Contains workload queries that are delivered with each workload. Stack queries have been split into contexts for further investigation if desired. TPC-H queries have been generated using scale factor 10. |
| bao_server_eval.py | Script to evaluate BAO on our architecture. **Optional**.|
| build_query_objects.py | Script used to build query objects to speed up query featurization during runtime. Needs database info to be build first. **Optional but recommended**. |
| config.ini | Configuration template that is accessed during most steps. Needs to be adapted to fit the current databases. Psycopg2-format. **Required**. |
| context_heuristic.py | Auxiliary file.|
| evaluate_queries.py | Main script. Used to evaluate workloads. Make sure your database info is present in `config.ini`, `update_db_info.py` and possibly `build_query_objects.py` have been run, and `generate_labels.py` has been run to create an archive.|
| featurize.py | Auxiliary file.|
| fill_eval_dict.py | Script to update unseen predictions within the query archive that is used for training. It is recommended to update the archive after each hint set prediction such that further analysis is improved and redundant query execution can be avoided. **Optional but recommended**.|
| generate_labels.py | Script to build an initial archive with labeled queries. Building large workload archives like for Stack (6191 queries) may take up days to be created, depending on your hardware, Postgres version, and database settings.  **Required**.|
| hint_sets.py | Auxiliary file. |
| query.py | Auxiliary file.|
| update_db_info.py | Script to build database information. Usually, `-mm`, `-l`, `-w` should be the `db_info/<-workload->` directory. **Required**.|
| utility.py | Auxiliary file.|

Examplary call using stack, precomputed query_objects, and no critical query detection:
```python3 evaluate_queries.py -db stack -a <path/to/archive.json> -dbip <path/to/db_info/> -qo <path/to/query_objects.pkl> -cqd False```

After `evaluate_queries.py` has been run, predictions can be added to the archive using `fill_eval_dict.py`. 

**Note**: Keep in mind that when using the retraining option, FASTgres will naturally execute some query-hint-set combinations. This increases the runtime performance depending on hardware, configuration, ... . 

Using no retraining will result in FASTgres only using its initial predictions, which is way faster.

## Evaluation Environment

FASTgres was evaluated on PostgreSQL v12.4 for comparability to BAO [^1] and v14.6 as this version was the most up-to-date at the time of development.

We tested FASTgres on two hardware environments:


| OS | CPU | CPU Cores | Architecture | RAM | Storage |
|:--:|:---:|:---------:|:------------:|:---:|:-------:|
| CentOS 64-bit | Intel Xeon Gold 6216 | 12 | Skylake | 92 GiB | 1.8TB HDD |
| Windows 10 64-bit | Intel Xeon E-2186M | 6 | Coffee Lake| 64 GiB | 1.8 TiB NVMe SSD |

## License

This software is available under the Apache License Version 2.0.

## References

[^1]: Marcus, Ryan, et al. "Bao: Making learned query optimization practical." Proceedings of the 2021 International Conference on Management of Data. 2021.
[^2]: Leis, Viktor, et al. "How good are query optimizers, really?." Proceedings of the VLDB Endowment 9.3 (2015): 204-215.
[^3]: [TPC-H](https://www.tpc.org/tpch/)
