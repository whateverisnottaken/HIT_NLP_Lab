class WordDictBasic:
    word_list = []
    punctuations = []
    __max_word_length = 0

    def __init__(self, filename):
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
        for cur_word in self.word_list:
            if word == cur_word:
                return True

    def find_punctuation(self, punctuation):
        for temp_punctuation in self.punctuations:
            if temp_punctuation == punctuation:
                return True
        return False

    def get_max_word_length(self):
        return self.__max_word_length


def get_ind(ch):
    ch_gbk_bytes = ch.encode('gbk')  # big first in gbk
    return (ch_gbk_bytes[0] - 0x81) * 190 + (ch_gbk_bytes[1] - 0x40) - (ch_gbk_bytes[1] // 128)


class WordDictHash(WordDictBasic):
    class HashNode:
        data = ""
        next_node = None

        def __init__(self, word, next_node=None):
            self.data = word
            self.next_node = next_node

        def append(self, next_node):
            self.next_node = next_node

    hash_nodes = []
    hash_Mod = 0
    __EMPTY_NODE = HashNode("")

    def bkdr_hash(self, word):
        return hash(word) % self.hash_Mod
        # seed = 131
        # hash_val = 0
        # for ch in word:
        #     hash_val = hash_val * seed + get_ind(ch)
        # return int((hash_val & 0x7FFFFFFF) % self.hash_Mod)

    def __init__(self, filename, hash_size):
        super().__init__(filename)
        self.hash_Mod = hash_size
        self.hash_nodes = [self.__EMPTY_NODE for i in range(self.hash_Mod)]
        for cur_word in self.word_list:
            hash_val = self.bkdr_hash(cur_word)
            cur_node = self.HashNode(cur_word)
            if self.hash_nodes[hash_val] == self.__EMPTY_NODE:
                self.hash_nodes[hash_val] = cur_node
            else:
                node_in_list = self.hash_nodes[hash_val]
                while node_in_list.next_node is not None:
                    node_in_list = node_in_list.next_node
                node_in_list.append(cur_node)

    def find_word(self, word):
        hash_val = self.bkdr_hash(word)
        if self.hash_nodes[hash_val] == self.__EMPTY_NODE:
            return False
        else:
            cur_node = self.hash_nodes[hash_val]
            while cur_node.data != word and cur_node.next_node is not None:
                cur_node = cur_node.next_node
            return cur_node.data == word
