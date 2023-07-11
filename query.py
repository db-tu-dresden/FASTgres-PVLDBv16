
from utility import tree
import utility as u


class Query:

    def __init__(self, query, path):
        self.name = query
        self.parsed = u.parse_query(path, query)
        try:
            self.select_part = self.parsed['select']
        except:
            try:
                self.select_part = self.parsed['select_distinct']
            except:
                raise ValueError()
        self.from_part = self.parsed['from']
        self.where_part = self.parsed['where']

        self.unhandled = set()

        self.tables = self.get_table_entries()
        self.context = frozenset(sorted(self.tables.values()))
        self.attributes = self.get_attributes()

    def print_info(self):
        print(self.name)
        print('Context: ', self.context)
        print('Unhandled Operators: ', self.unhandled)
        print('\n')
        return

    def get_table_entries(self) -> dict:
        table_dict = dict()
        for entry in self.from_part:
            try:
                # alias - name
                table_dict[entry['name']] = entry['value']
            except (KeyError, TypeError):
                table_dict[entry] = entry
        return table_dict

    def get_attributes(self) -> tree:
        # table -> column -> key -> value to encode
        attribute_dict = tree()

        combination_types = self.where_part.keys()
        if len(combination_types) > 1 and 'and' not in combination_types:
            raise ValueError('Encountered unhandled combinator unequal to - and -')

        # sometimes there might not be more than one where argument
        try:
            and_part = self.where_part['and']
        except KeyError:
            and_part = [self.where_part]
        print(and_part)
        for entry in and_part:
            alias, column, key, value = [None] * 4
            entry_keys = entry.keys()
            # handle equal keys
            if 'eq' in entry_keys:
                key = 'eq'
                equal_statement = entry[key]
                try:
                    alias, column = equal_statement[0].split('.')
                    value = equal_statement[1]['literal']
                except (TypeError, ValueError):
                    # print(entry)
                    alias, column, key, value = [None] * 4
            # handle like keys
            elif 'like' in entry_keys:
                key = 'like'
                like_statement = entry[key]
                try:
                    alias, column = like_statement[0].split('.')
                    value = like_statement[1]['literal']
                except:
                    try:
                        alias, column = like_statement[0]['lower'].split('.')
                        value = like_statement[1]['lower']['literal']
                    except:
                        print(entry)
                        alias, column, key, value = [None] * 4
            # handle gt/lt keys
            elif 'gt' in entry_keys or 'lt' in entry_keys:
                key = 'gt' if 'gt' in entry_keys else 'lt'
                glt_statement = entry[key]
                try:
                    alias, column = glt_statement[0].split('.')
                    value = glt_statement[1]
                    # string gt filters
                    if isinstance(value, dict):
                        try:
                            value = value['literal']
                        except:
                            try:
                                # catching dates
                                value = value['cast'][0]['literal']
                            except:
                                # gt join date + interval
                                print(entry)
                                alias, column, key, value = [None] * 4
                except:
                    print("Encoding issue in: {}".format(key))
                    alias, column, key, value = [None] * 4
            # handle not equal keys
            elif 'neq' in entry_keys:
                key = 'neq'
                neq_statement = entry[key]
                try:
                    alias, column = neq_statement[0].split('.')
                    value = neq_statement[1]['literal']
                except (TypeError, ValueError):
                    print("Encoding issue in: {}".format(key))
                    alias, column, key, value = [None] * 4
            # handle not like keys
            elif 'not_like' in entry_keys:
                key = 'not_like'
                not_like_statement = entry[key]
                try:
                    alias, column = not_like_statement[0].split('.')
                    value = not_like_statement[1]['literal']
                except (TypeError, ValueError):
                    print("Encoding issue in: {}".format(key))
                    alias, column, key, value = [None] * 4
            # handle exists keys
            elif 'exists' in entry_keys:
                key = 'exists'
                exists_statement = entry[key]
                # needs proper representation
                pass
            # handle between keys
            elif 'between' in entry_keys:
                key = 'between'
                between_statement = entry[key]
                # needs proper representation
            # handle in keys
            elif 'in' in entry_keys:
                key = 'in'
                in_statement = entry[key]
                try:
                    alias, column = in_statement[0].split('.')
                    value = in_statement[1]['literal']
                except (TypeError, ValueError):
                    alias, column, key, value = [None] * 4
            # handle 'missing' keys
            elif 'missing' in entry_keys:
                key = 'missing'
                missing_statement = entry[key]
            # handle disjunctive keys inside conjunctive ones
            elif 'or' in entry_keys:
                key = 'or'
                or_statement = entry[key]
                # disjunctive queries are not yet supported
                pass
            elif 'gte' in entry_keys or 'lte' in entry_keys:
                key = 'gte' if 'gte' in entry_keys else 'lte'
                glte_statement = entry[key]
                try:
                    alias, column = glte_statement[0].split('.')
                except ValueError:
                    # no alias was used, currently unhandled
                    # alias = None
                    # column = glte_statement[0]
                    pass
                value = glte_statement[1]
            # handle as needed
            else:
                [self.unhandled.add(i) for i in entry_keys]
                pass
            if column is None:
                pass
            else:
                table = self.tables[alias]
                attribute_dict[table][column][key] = value
        return attribute_dict

