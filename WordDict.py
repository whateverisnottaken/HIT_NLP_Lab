class WordDict:
    word_list = []
    punctuations = []
    __max_word_length = 0
    dict_type = 'BASIC'

    def __init__(self, filename, dict_type='BASIC'):
        with open(filename, 'r') as file_dict:
            punctuation_flag = 0
            file_lines = file_dict.readlines()
            for file_line in file_lines:
                file_line = file_line.strip()
                if file_line == "PUNCTUATIONS:":
                    punctuation_flag = 1
                    continue
                if punctuation_flag == 0:
                    self.__max_word_length = max(self.__max_word_length, len(file_line))
                    self.word_list.append(file_line)
                else:
                    self.punctuations.append(file_line)

    def find_word(self, word):
        for temp_word in self.word_list:
            if word == temp_word:
                return True

    def find_punctuation(self, punctuation):
        for temp_punc in self.punctuations:
            if temp_punc == punctuation:
                return True
        return False

    def get_max_word_length(self):
        return self.__max_word_length

class WordDict:
    word_list = []
    punctuations = []
    __max_word_length = 0

    def __init__(self, filename, dict_type='BASIC'):
        with open(filename, 'r') as file_dict:
            punctuation_flag = 0
            file_lines = file_dict.readlines()
            for file_line in file_lines:
                file_line = file_line.strip()
                if file_line == "PUNCTUATIONS:":
                    punctuation_flag = 1
                    continue
                if punctuation_flag == 0:
                    self.__max_word_length = max(self.__max_word_length, len(file_line))
                    self.word_list.append(file_line)
                else:
                    self.punctuations.append(file_line)

    def find_word(self, word):
        for temp_word in self.word_list:
            if word == temp_word:
                return True
        return False

    def find_punctuation(self, punctuation):
        for temp_punc in self.punctuations:
            if temp_punc == punctuation:
                return True
        return False

    def get_max_word_length(self):
        return self.__max_word_length