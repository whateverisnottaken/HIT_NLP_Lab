import re


def convert2gbk(cur_word):
    cur_word = cur_word.strip()
    return cur_word.encode("gbk")


def get_len(punctation):
    return len(punctation)


if __name__ == '__main__':
    word_partofspeech = {}
    with open('./199801_seg.txt') as f:
        seg_lines = f.readlines()
        for seg_line in seg_lines:
            words = seg_line.split(' ')
            for word in words:
                ind = word.find('/')
                word_partofspeech[word[:ind]] = word[ind:]

    with open('dict.txt', 'w') as f:
        outs = []
        punctuations = []
        for item in word_partofspeech.items():
            out = str(item[0])
            if item[1] == '/w':
                if item[0][0]=='[':
                    punctuations.append(item[0][1:])
                else:
                    punctuations.append(item[0])
                # if len(out) == 1:
                #     print('\''+out+'\'', end=',')
                # else:
                #     print('\'\''+out+'\'\'', end=',')
            pat = r'[|0-9|０-９]*[\u4e00-\u9fa5]+'
            results = re.findall(pat, out)
            if len(results) > 2:
                outs.append(out + '\n')
                continue
            if results:
                outs.append(results[0] + '\n')
        outs.sort(key=convert2gbk)
        out_map = {}
        count = {}
        for out in outs:
            if out not in out_map:
                out_len = len(convert2gbk(out)) / 2
                if out_len in count:
                    count[out_len] += 1
                else:
                    count[out_len] = 1
                out_map[out] = 1
                f.write(out)
        f.write("PUNCTUATIONS:\n")
        punctuations.sort(key=get_len)
        for punctuation in punctuations:
            f.write(punctuation + '\n')
        print(count)
