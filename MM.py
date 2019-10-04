# -*- coding:utf-8 -*-
from WordDict import WordDict


def get_words_fmm(sentence, word_dict):
    ret_seg = []
    while len(sentence) > 0:
        length = min(len(sentence), word_dict.get_max_word_length())
        temp_word = sentence[0:length]
        while not word_dict.find_word(temp_word):
            if len(temp_word) == 1:
                break
            temp_word = temp_word[0:len(temp_word) - 1]
        ret_seg.append(temp_word)
        sentence = sentence[len(temp_word):]
    return ret_seg


def get_words_bmm(sentence, word_dict):
    ret_seg = []
    while len(sentence) > 0:
        length = min(len(sentence), word_dict.get_max_word_length())
        temp_word = sentence[len(sentence) - length:]
        while not word_dict.find_word(temp_word):
            if len(temp_word) == 1:
                break
            temp_word = temp_word[1:]
        ret_seg.append(temp_word)
        sentence = sentence[len(temp_word):]
    new_ret_seg = []
    len_ret_seg = len(ret_seg)
    ind = 0
    while ind < len_ret_seg:
        new_ret_seg.append(ret_seg[len_ret_seg - ind - 1])
        ind = ind + 1
    return new_ret_seg


def word_seg(sent_filename, word_dict):
    with open(sent_filename, 'r') as file_sent:
        lines = file_sent.readlines()
        fmm_seg_out = []
        bmm_seg_out = []
        for line in lines:
            line = line.strip()
            if line == " ":
                continue
            fmm_seg = []
            bmm_seg = []
            begin_ind = 0
            line_len = len(line)
            ind = 0
            while ind < line_len:
                if line[ind] == '—':
                    if line[ind + 1] == '—':
                        if line[ind + 2] == '－' or line[ind + 2] == '—':
                            sentence = line[begin_ind:ind]
                            fmm_seg.extend(get_words_fmm(sentence, word_dict))
                            fmm_seg.append(f'{line[ind]}{line[ind + 1]}{line[ind + 2]}')
                            bmm_seg.extend(get_words_fmm(sentence, word_dict))
                            bmm_seg.append(f'{line[ind]}{line[ind + 1]}{line[ind + 2]}')
                            begin_ind = ind + 3
                            ind = begin_ind
                            continue
                        else:
                            sentence = line[begin_ind:ind]
                            fmm_seg.extend(get_words_fmm(sentence, word_dict))
                            fmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                            bmm_seg.extend(get_words_fmm(sentence, word_dict))
                            bmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                            begin_ind = ind + 2
                            ind = begin_ind
                            continue
                if line[ind] == '±' and line[ind + 1] == '%':
                    sentence = line[begin_ind:ind]
                    fmm_seg.extend(get_words_fmm(sentence, word_dict))
                    fmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                    bmm_seg.extend(get_words_fmm(sentence, word_dict))
                    bmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                    begin_ind = ind + 2
                    ind = begin_ind
                    continue
                if line[ind] == "…" and line[ind + 1] == "…":
                    sentence = line[begin_ind:ind]
                    fmm_seg.extend(get_words_fmm(sentence, word_dict))
                    fmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                    bmm_seg.extend(get_words_fmm(sentence, word_dict))
                    bmm_seg.append(f'{line[ind]}{line[ind + 1]}')
                    begin_ind = ind + 2
                    ind = begin_ind
                    continue
                if word_dict.find_punctuation(line[ind]):
                    sentence = line[begin_ind:ind]
                    fmm_seg.extend(get_words_fmm(sentence, word_dict))
                    fmm_seg.append(f'{line[ind]}')
                    bmm_seg.extend(get_words_fmm(sentence, word_dict))
                    bmm_seg.append(f'{line[ind]}')
                    begin_ind = ind + 1
                    ind = begin_ind
                    continue
                ind = ind + 1
            fmm_seg_out.append(fmm_seg)
            bmm_seg_out.append(bmm_seg)
    with open('seg_FMM.txt', 'w') as FMM_file:
        for fmm_seg in fmm_seg_out:
            for seg in fmm_seg:
                FMM_file.write(seg)
    with open('seg_BMM.txt', 'w') as BMM_file:
        for bmm_seg in bmm_seg_out:
            for seg in bmm_seg:
                BMM_file.write(seg)
    print("Word Seg OK!")


if __name__ == "__main__":
    word_dict_basic = WordDict(filename="dict.txt")
    word_seg("199801_sent.txt", word_dict_basic)
