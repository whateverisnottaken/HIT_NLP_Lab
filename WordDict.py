from math import log

from FlexibleList import FlexibleList


class WordDictBasic:
    word_list = []
    punctuations = []
    __max_word_length = 0

    def __init__(self, filename):
        with open(filename, 'r') as file_dict:
            punctuation_flag = 0
            dict_lines = file_dict.readlines()
            for dict_line in dict_lines:
                dict_line = dict_line.strip()
                if dict_line == "PUNCTUATIONS:":
                    punctuation_flag = 1
                    continue
                if punctuation_flag == 0:
                    self.add_word(dict_line)
                else:
                    self.punctuations.append(dict_line)

    def add_word(self, word):
        self.word_list.append(word)
        self.__max_word_length = max(self.__max_word_length, len(word))

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


def ch_gbk_encode(ch):
    # return hash(ch) % 1089
    ch_gbk_bytes = ch.encode('gbk')  # big first in gbk
    return (ch_gbk_bytes[0] - 0x81) * 190 + (ch_gbk_bytes[1] - 0x40) - (ch_gbk_bytes[1] // 128)


class WordDictHash(WordDictBasic):
    class HashNode:
        data = None
        next_node = None

        def __init__(self, data, next_node=None):
            self.data = data
            self.next_node = next_node

        def add_next_node(self, next_node):
            self.next_node = next_node

    hash_nodes = []
    hash_Mod = 0
    __EMPTY_NODE = HashNode("")
    ch_encoder = ch_gbk_encode

    def hash_function(self, word):
        # return hash(word) % self.hash_Mod
        seed = 131
        hash_val = 0
        for ch in word:
            hash_val = hash_val * seed + ch_gbk_encode(ch)
        return int((hash_val & 0x7FFFFFFF) % self.hash_Mod)

    def __init__(self, hash_size, filename_or_word_list):
        self.hash_Mod = hash_size
        self.hash_nodes = [self.__EMPTY_NODE for i in range(self.hash_Mod)]
        self.ch_encoder = ch_gbk_encode
        # notice: super() will use override method in super class.
        if type(filename_or_word_list) == str:
            super().__init__(filename_or_word_list)
        else:
            self.word_list = filename_or_word_list

    def add_word(self, word):
        super().add_word(word)
        hash_val = self.hash_function(word)
        cur_node = self.HashNode(word)
        if self.hash_nodes[hash_val] == self.__EMPTY_NODE:
            self.hash_nodes[hash_val] = cur_node
        else:
            node_in_list = self.hash_nodes[hash_val]
            while node_in_list.next_node is not None:
                if node_in_list.data == word:
                    return False
                node_in_list = node_in_list.next_node
            node_in_list.add_next_node(cur_node)
            return True

    def find_word(self, word):
        hash_val = self.hash_function(word)
        if self.hash_nodes[hash_val] == self.__EMPTY_NODE:
            return False
        else:
            cur_node = self.hash_nodes[hash_val]
            while cur_node.data != word and cur_node.next_node is not None:
                cur_node = cur_node.next_node
            return cur_node.data == word


class Trie:
    class TrieNode:
        val = 0
        word_end = True
        check_dict = WordDictHash(1087, [])  # magic prime number size
        children = []

        def __init__(self, val, end):
            self.val = val
            self.word_end = end
            self.check_dict = WordDictHash(1087, [])
            self.children = []

    def __init__(self, words):
        self.root = self.TrieNode("ROOT", False)
        self.node_size = 0
        for word in words:
            self.add(word)
        print("Trie build OK")

    def add(self, word):
        cur_node = self.root
        for ch_ind in range(len(word)):
            ch = word[ch_ind]
            if not cur_node.check_dict.find_word(ch):
                new_node = self.TrieNode(val=ch, end=True if ch_ind == len(word) - 1 else False)
                cur_node.children.append(new_node)
                cur_node.check_dict.add_word(word=ch)
                self.node_size += 1
            for child in cur_node.children:
                if child.val == ch:
                    cur_node = child
                    break


class WordDictDATrie(WordDictBasic):
    __MAX_BASE_SIZE = 300000
    base = [0] * __MAX_BASE_SIZE
    check = [0] * __MAX_BASE_SIZE
    ch_encoder = ch_gbk_encode

    def __init__(self, filename, ch_encoder=ch_gbk_encode):
        super().__init__(filename)
        self.root = 0
        self.base = [0] * self.__MAX_BASE_SIZE
        self.check = [0] * self.__MAX_BASE_SIZE
        self.ch_encoder = ch_encoder
        trie = Trie(self.word_list)
        self.construct_from_trie(trie)
        del trie
        # print(len(self.base))
        # print(len(self.check))

    def construct_from_trie(self, trie):
        nodes = [(trie.root, 0)]
        find_from = 1
        while nodes:
            trie_node, now_state = nodes.pop(0)
            now_base_val = self.find_base(now_state, trie_node.children, find_from)
            find_from = now_base_val
            self.base[now_state] = -now_base_val if trie_node.word_end else now_base_val
            for child in trie_node.children:
                child_encode = self.ch_encoder(child.val)
                next_state = abs(self.base[now_state]) + child_encode
                self.check[next_state] = now_state
                nodes.append((child, next_state))

    def find_base(self, parent, children, base_val=1):
        if parent == 0 or not children:
            return parent
        base_val = max(base_val, 1)
        loop_times = 0
        while True:
            base_ok_flag = True
            for child in children:
                child_state = base_val + self.ch_encoder(child.val)
                if self.base[child_state] != 0 or self.check[child_state] != 0 or child_state == parent:
                    loop_times += 1
                    base_val += int(log(loop_times, 2)) + 1
                    base_ok_flag = False
                    break
            if base_ok_flag:
                break

        return base_val

    def walk(self, parent, ch):
        ch_encode = self.ch_encoder(ch)
        target_ind = abs(self.base[parent]) + ch_encode
        if self.check[target_ind] == parent:
            return target_ind
        else:
            return 0

    def find_word(self, word):
        cur_node = self.root
        word_len = len(word)
        ind = 0
        while ind < word_len:
            ch = word[ind]
            parent = cur_node
            cur_node = abs(self.base[cur_node]) + self.ch_encoder(ch)
            if self.check[cur_node] != parent:
                break
            ind += 1
        if ind == word_len - 1 and self.base[cur_node] < 0:
            return True
        return False
