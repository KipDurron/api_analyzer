def get_words_dict(words):
    temp_dict = {}
    for word in words:
        if word in temp_dict:
            temp_dict[word] = temp_dict[word] + 1
        else:
            temp_dict[word] = 1
    return temp_dict