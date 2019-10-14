def remove_blank(lines):
    for line_ind in range(len(lines)):
        lines[line_ind] = lines[line_ind].strip()
    while "" in lines:
        lines.remove("")
    return lines


def get_line_words_for_std(line):
    words = line.split(' ')
    ret_words = []
    for word in words:
        if word == "":
            continue
        word_ind = word.find('/')
        if word[0] == '[':
            ret_words.append(word[1:word_ind])
        else:
            ret_words.append(word[:word_ind])
    return ret_words[1:]


def compare(test_lines, result_lines):
    assert len(test_lines) == len(result_lines)
    lines_len = len(test_lines)

    precision = 0
    recall = 0
    for i in range(lines_len):
        test_words = get_line_words_for_std(test_lines[i])
        result_words = result_lines[i].split(' ')
        right_word = 0
        for result_word in result_words:
            for test_word in test_words:
                if result_word == test_word:
                    right_word += 1
                    break
        precision += right_word / len(test_words)
        recall += right_word / len(result_words)
    precision = precision / lines_len * 100
    recall = recall / lines_len * 100
    print("Precision: %f Recall: %f" % (precision, recall))
    f1_score = 2 * precision * recall / (precision + recall)
    print("F1 : %f" % f1_score)


if __name__ == '__main__':
    test_filename = "199801_seg.txt"
    file_std = open(test_filename, 'r')
    source_filename = "199801_sent.txt"
    file_sent = open(source_filename, 'r')

    std_lines = file_std.readlines()
    sent_lines = file_sent.readlines()
    remove_blank(std_lines)
    remove_blank(sent_lines)
    file_bmm = open("seg_BMM.txt", 'r')
    file_fmm = open("seg_FMM.txt", 'r')

    fmm_lines = file_fmm.readlines()
    remove_blank(fmm_lines)
    bmm_lines = file_bmm.readlines()
    remove_blank(bmm_lines)
    print("BMM:")
    compare(test_lines=std_lines, result_lines=fmm_lines)
    compare(test_lines=std_lines, result_lines=bmm_lines)
