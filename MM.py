# -*- coding:utf-8 -*-
from WordDict import WordDictBasic
from WordDict import WordDictHash
from WordDict import WordDictDATrie
import datetime


def get_words_fmm(fmm_seg, sentence, word_dict):
    while len(sentence) > 0:
        length = min(len(sentence), word_dict.get_max_word_length())
        temp_word = sentence[0:length]
        while not word_dict.find_word(temp_word):
            if len(temp_word) == 1:
                break
            temp_word = temp_word[0:len(temp_word) - 1]
        fmm_seg.append(temp_word)
        sentence = sentence[len(temp_word):]


def get_words_bmm(bmm_seg, sentence, word_dict):
    temp_seg = []
    while len(sentence) > 0:
        length = min(len(sentence), word_dict.get_max_word_length())
        temp_word = sentence[len(sentence) - length:]
        while not word_dict.find_word(temp_word):
            if len(temp_word) == 1:
                break
            temp_word = temp_word[1:]
        temp_seg.append(temp_word)
        sentence = sentence[:len(sentence) - len(temp_word)]
    temp_seg_ind = len(temp_seg) - 1
    while temp_seg_ind >= 0:
        bmm_seg.append(temp_seg[temp_seg_ind])
        temp_seg_ind = temp_seg_ind - 1


def update_seg(line, begin_ind, end_ind, bmm_seg, fmm_seg, word_dict, punctuation_len=0):
    sentence = line[begin_ind:end_ind]
    get_words_fmm(fmm_seg, sentence, word_dict)
    get_words_bmm(bmm_seg, sentence, word_dict)
    if punctuation_len == 0:
        return end_ind, end_ind
    punctuation_end_ind = end_ind + punctuation_len
    cur_punctuation = f'{line[end_ind:punctuation_end_ind]}'
    fmm_seg.append(cur_punctuation)
    bmm_seg.append(cur_punctuation)

    return punctuation_end_ind, punctuation_end_ind


def word_seg(sent_filename, word_dict):
    with open(sent_filename, 'r') as file_sent:
        lines = file_sent.readlines()
        fmm_seg_out = []
        bmm_seg_out = []
        seg_count = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            seg_count = seg_count + 1
            # print(seg_count)
            # print(line)
            fmm_seg = []
            bmm_seg = []
            last_ind = 0
            line_len = len(line)
            ind = 0
            while ind < line_len:
                if ind + 1 < line_len:
                    if line[ind] == '—':
                        if line[ind + 1] == '—':
                            if ind + 2 < line_len:
                                if line[ind + 2] == '－' or line[ind + 2] == '—':
                                    punctuation_len = 3
                                    last_ind, ind = update_seg(line, last_ind, ind, bmm_seg, fmm_seg,
                                                               word_dict, punctuation_len)
                                    continue
                                punctuation_len = 2
                                last_ind, ind = update_seg(line, last_ind, ind, bmm_seg, fmm_seg,
                                                           word_dict, punctuation_len)
                                continue
                if ind + 1 < line_len:
                    if line[ind] == '±':
                        if line[ind + 1] == '%':
                            punctuation_len = 2
                            last_ind, ind = update_seg(line, last_ind, ind, bmm_seg, fmm_seg,
                                                       word_dict, punctuation_len)
                            continue
                if ind + 1 < line_len:
                    if line[ind] == "…" and line[ind + 1] == "…":
                        punctuation_len = 2
                        last_ind, ind = update_seg(line, last_ind, ind, bmm_seg, fmm_seg,
                                                   word_dict, punctuation_len)
                        continue
                if word_dict.find_punctuation(line[ind]):
                    punctuation_len = 1
                    last_ind, ind = update_seg(line, last_ind, ind, bmm_seg, fmm_seg,
                                               word_dict, punctuation_len)
                    continue
                ind = ind + 1
            if last_ind == 0:
                update_seg(line, last_ind, line_len, bmm_seg, fmm_seg, word_dict)
            fmm_seg_out.append(fmm_seg)
            bmm_seg_out.append(bmm_seg)
            # break
    print(datetime.datetime.now())
    with open('seg_FMM.txt', 'w') as FMM_file:
        for fmm_seg in fmm_seg_out:
            for seg in fmm_seg:
                FMM_file.write(seg + "  ")
    with open('seg_BMM.txt', 'w') as BMM_file:
        for bmm_seg in bmm_seg_out:
            for seg in bmm_seg:
                BMM_file.write(seg + "  ")
    print("Word Seg OK!")


if __name__ == "__main__":
    # word_dict_basic = WordDictBasic(filename="dict.txt")
    # word_seg("199801_sent.txt", word_dict_basic)
    hash_size = 10001659
    word_dict_hash = WordDictHash(hash_size=hash_size, filename_or_word_list="dict.txt")
    print("Hash Build")
    print(datetime.datetime.now())
    word_seg("199801_sent.txt", word_dict_hash)
    print(datetime.datetime.now())
    word_dict_DATrie = WordDictDATrie(filename="dict.txt")
    print("DATrie build")
    print(datetime.datetime.now())
    word_seg("199801_sent.txt", word_dict_DATrie)
    print(datetime.datetime.now())
