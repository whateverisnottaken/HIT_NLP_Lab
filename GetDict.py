def convert2gbk(cur_word):
    cur_word = cur_word.strip()
    return cur_word.encode("gbk")


def get_len(cur_punctuation):
    return len(cur_punctuation)


if __name__ == '__main__':
    word_dict = {}
    with open('./199801_seg.txt') as f:
        seg_lines = f.readlines()
        for seg_line in seg_lines:
            seg_line = seg_line.strip()
            if seg_line == "":
                continue
            words = seg_line.split(' ')
            for word in words:
                if word == words[0]:
                    continue
                if word == "":
                    continue
                ind = word.find('/')
                if word[0] == '[':
                    word_dict[word[1:ind]] = word[ind:]
                else:
                    word_dict[word[0:ind]] = word[ind:]

    with open('dict.txt', 'w') as f:
        outs = []
        punctuations = []
        for item in word_dict.items():
            out = str(item[0])
            if item[1] == '/w':
                punctuations.append(item[0])
                continue
            outs.append(out)
        outs.sort(key=convert2gbk)
        for out in outs:
            f.write(out)
            f.write('\n')
        f.write("PUNCTUATIONS:\n")
        punctuations.sort(key=get_len)
        for punctuation in punctuations:
            word_part = False
            for out in outs:
                if punctuation in out:
                    word_part = True
            if not word_part:
                f.write(punctuation + '\n')
