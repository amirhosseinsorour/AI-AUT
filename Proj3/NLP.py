import collections


def get_sentences(filePath):
    # filePath = "train_set\\" + poet + "_train.txt"
    temp_list = list()
    punctuations = ".،:؛!؟*\"\'«»"
    with open(filePath, 'r') as f:
        for line in f.readlines():
            line = line.translate(line.maketrans('', '', punctuations))
            line = "</s> " + line.rstrip("\n") + " <s>"
            temp_list.append(line)
    return temp_list


def get_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = sentence.split()
        for word in sentence:
            temp_list.append(word)
    return temp_list


def get_pair_of_words(sentences_list):
    temp_list = list()
    for sentence in sentences_list:
        sentence = sentence.split()
        for i in range(sentence.__len__() - 1):
            pair = [sentence[i], sentence[i + 1]]
            temp_list.append(pair)
    return temp_list


def build_dictionary(sentences, n):
    frequencies_dict = dict()
    if n == 1:
        words = get_words(sentences)
        for word in words:
            if word in frequencies_dict:
                newFrequency = frequencies_dict[word] + 1
                frequencies_dict.update({word: newFrequency})
            else:
                frequencies_dict.update({word: 1})
        temp_dict = frequencies_dict.copy()
        for word in temp_dict:
            if temp_dict.get(word) <= 5:
                frequencies_dict.pop(word)
        return frequencies_dict
    if n == 2:
        pair_of_words = get_pair_of_words(sentences)
        for pair in pair_of_words:
            if pair in frequencies_dict:
                newFrequency = frequencies_dict[pair] + 1
                frequencies_dict.update({pair: newFrequency})
            else:
                frequencies_dict.update({pair: 1})
        temp_dict = frequencies_dict.copy()
        for pair in temp_dict:
            if temp_dict.get(pair) <= 2:
                frequencies_dict.pop(pair)
        return frequencies_dict


def build_unigram(unigram_dict):
    unigram_model = dict()
    M = sum(unigram_dict.values())
    for word, count in unigram_dict.items():
        unigram_model.update({word: count / M})
    sorted_y = sorted(unigram_model.items(), key=lambda kv: kv[1])
    sorted_unigram_model = collections.OrderedDict(sorted_y)
    return sorted_unigram_model


def build_bigram(unigram_dict, bigram_dict):
    bigram_model = dict()
    for pair, count in bigram_dict.items():
        bigram_model.update({pair: count / unigram_dict[pair[0]]})
    sorted_y = sorted(bigram_model.items(), key=lambda kv: kv[1])
    sorted_bigram_model = collections.OrderedDict(sorted_y)
    return sorted_bigram_model


if __name__ == '__main__':
    ferdowsi_all_sentences = get_sentences("train_set\\ferdowsi_train.txt")
    hafez_all_sentences = get_sentences("train_set\\hafez_train.txt")
    molavi_all_sentences = get_sentences("train_set\\molavi_train.txt")

    ferdowsi_unigram_dict = build_dictionary(ferdowsi_all_sentences, 1)
    hafez_unigram_dict = build_dictionary(hafez_all_sentences, 1)
    molavi_unigram_dict = build_dictionary(molavi_all_sentences, 1)

    test_sentences = get_sentences("test_set\\test_file.txt")
