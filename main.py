# search target-file from base-folder.

# if target-file include other environment string,
# output filename, that string, and line that string written.

# however if that string defined target environment's exclusion-word,
# exclude that string.

import yaml
import pprint
import os
import re


class SettingCheck:
    def __init__(self):
        self.search_list = {}
        self.file_list = []
        self.target = []

    def read_conf(self, yml_path):
        with open(yml_path) as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader)
            # pprint.pprint(yml)
            self.search_list = {y['name']: y['string'] for y in
                                yml['order']['environments']}
            self.target = yml['target']
        # pprint.pprint(self.search_list)

    def check_string(self, string, target_env=''):
        r = []
        for key in self.search_list.keys():
            if key == target_env: continue
            for value in self.search_list[key]:
                x = string.find(value, 0)
                while x >= 0:
                    r.append([x, value])
                    x = string.find(value, x + len(value))
        r.sort()
        return r

    def match_file_list(self, folder):
        r = []
        stack = [folder]
        while stack:
            now = stack.pop()
            if os.path.isdir(now):
                stack += [join_path(now, df) for df in os.listdir(now)]
            if os.path.isfile(now) and self.is_match_file(now):
                r.append(now)
        return r

    def is_match_file(self, file):
        r = False
        for t in self.target:
            if re.fullmatch(t, file):
                r = True
                break
        return r


def check_string(string, search):
    """
    return 'is string include search ?'
    :param string:
    :param search:
    :return:
    """


def check_string_top(string, search, start=0):
    """
    return 'is string include '
    :param string:
    :param search:
    :param start:
    :return:
    """


def output_string(filepath, line_num, char_num, hit_str, ):
    CHAIN = ' :: '
    l = [filepath, line_num, char_num, hit_str]
    return CHAIN.join([str(x) for x in l])


def join_path(base, path):
    return os.path.join(base, path).replace('\\', '/')


if __name__ == '__main__':
    # 実行時引数を読み込む
    base_folder = 'dummy'
    # 設定ファイルを読み込む
    yml_path = 'conf/setting-check.yml'
    sc = SettingCheck()
    sc.read_conf(yml_path)
    # 検知対象ファイル列挙
    fl = sc.match_file_list(base_folder)
    # 検索開始
    for file in fl:
        print(file)
        i = 0
        with open(file, mode='r') as f:
            l_num = 0
            for l in f:
                for c, s in sc.check_string(l, 'stg'):
                    print(output_string(file, l_num, c, s))
                l_num += 1

