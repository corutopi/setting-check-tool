from chardet.universaldetector import UniversalDetector


def file_encoding(file):
    ud = UniversalDetector()
    with open(file, mode='rb') as f:
        for binary in f:
            ud.feed(binary)
            if ud.done:
                break
    ud.close()
    re = ud.result['encoding']
    re = 'cp932' if re == 'Windows-1252' else re     # sjis判定できない問題の暫定回避
    return re


if __name__ == '__main__':
    t = '../dummy/aaa_sjis.txt'
    with open(t, mode='r', encoding=file_encoding(t)) as f:
        print(f.read())
    t = '../dummy/aaa_utf8.txt'
    with open(t, mode='r', encoding=file_encoding(t)) as f:
        print(f.read())
