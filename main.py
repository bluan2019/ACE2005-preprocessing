import os
from parser import Parser
import json
import argparse


def get_data_paths(ace2005_path):
    test_files, dev_files, train_files = [], [], []

    with open('./data_list.csv', mode='r') as csv_file:
        rows = csv_file.readlines()
        for row in rows[1:]:
            items = row.replace('\n', '').split(',')
            data_type = items[0]
            name = items[1]

            path = os.path.join(ace2005_path, name + '.apf.xml')
            if data_type == 'test':
                test_files.append(path)
            elif data_type == 'dev':
                dev_files.append(path)
            elif data_type == 'train':
                train_files.append(path)
    return test_files, dev_files, train_files


def preprocessing(data_type, files):
    data = []
    for file in files:
        data.extend(Parser(xml_path=file).get_data())
    with open('output/{}.json'.format(data_type), 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="Path of ACE2005 English data", default='./data/ace_2005_td_v7/data/English')
    args = parser.parse_args()
    test_files, dev_files, train_files = get_data_paths(args.data)
    preprocessing('test', test_files)
    preprocessing('train', train_files)
    preprocessing('dev', dev_files)
