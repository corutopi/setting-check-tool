# search target-file from base-folder.

# if target-file include other environment string,
# output filename, that string, and line that string written.

# however if that string defined target environment's exclusion-word,
# exclude that string.

import pprint
import os
import re
import argparse

import yaml


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
        inc = []
        exc = []
        for key in self.search_list.keys():
            if key == target_env:
                tmp = exc
            else:
                tmp = inc
            for value in self.search_list[key]:
                x = string.find(value, 0)
                while x >= 0:
                    tmp.append([x, value, 0])
                    x = string.find(value, x + len(value))
        exc.sort()
        inc.sort()
        for e in exc:
            e_start = e[0]
            e_end = e[0] + len(e[1]) - 1
            for i in inc:
                i_start = i[0]
                i_end = i[0] + len(i[1]) - 1
                if e_end < i_start: break
                if e_start <= i_start and i_end <= e_end:
                    i[2] = 1
        return [i[:2] for i in inc if i[2] == 0]

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


def output_string(filepath, line_num, char_num, hit_str, ):
    CHAIN = ' :: '
    l = [filepath, line_num, char_num, hit_str]
    return CHAIN.join([str(x) for x in l])


def join_path(base, path):
    return os.path.join(base, path).replace('\\', '/')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('folderfile', help='folder or file path')
    parser.add_argument('env', help='environment string')
    parser.add_argument('conffile', help='yaml file defined target ' +
                                         'file names and check strings')
    return parser.parse_args()


if __name__ == '__main__':
    import sys

    sys.argv.append('dummy')
    sys.argv.append('stg')
    sys.argv.append('conf\setting-check.yml')

    # 実行時引数を読み込む
    args = get_args()
    base_folder = args.folderfile
    env = args.env
    # 設定ファイルを読み込む
    yml_path = 'conf/setting-check.yml'
    sc = SettingCheck()
    sc.read_conf(yml_path)
    # 検知対象ファイル列挙
    fl = sc.match_file_list(base_folder)
    print('target folder: {}'.format(base_folder))
    # 検索開始
    print('------')
    for file in fl:
        i = 0
        with open(file, mode='r') as f:
            l_num = 0
            for l in f:
                for c, s in sc.check_string(l, env):
                    print(output_string('.' + file[len(base_folder):],
                                        l_num, c, s))
                l_num += 1
