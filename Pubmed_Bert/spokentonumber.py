import re
import os
import string
from word2number import w2n

_known = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    "thousand": 1000,
    "million": 1000000,
    }

def mk_dir(file_path):
    folder = os.path.exists(file_path)
    if not folder:
        os.makedirs(file_path)

def cut_digit(sen):

    p = re.compile("\d+ \d+?")
    for com in p.finditer(sen):
        mm = com.group()
        sen = sen.replace(mm, mm.replace(" ", ""))
        
    p = re.compile("\d+,\d+?")
    for com in p.finditer(sen):
        mm = com.group()
        sen = sen.replace(mm, mm.replace(",", ""))
    return sen

def del_non_digit(text):
    
    text = text.strip().lower()
    text = cut_digit(text)
    text = text.translate(str.maketrans(string.punctuation, " "*32,)).replace("  ", " ")
    
    dig_list = list(_known.keys())
    dig_list.extend(['and'])
    text = text.split(" ")
    digit_words = ""
    for word in text:
        if word.isdigit():
            digit_words = digit_words + "_" + word + "_"
        elif word in dig_list:
            digit_words = digit_words + " " + word
        else:
            digit_words = digit_words + "_"
    digit_word_list = [i for i in digit_words.split("_") if len(i) > 0]
    
    digit_list = []
    for word in digit_word_list:
        # print(word)
        if word.isdigit():
            digit_list.append(word)
        else:
            if word != " and":
                digit_list.append(w2n.word_to_num(word))
    return digit_list