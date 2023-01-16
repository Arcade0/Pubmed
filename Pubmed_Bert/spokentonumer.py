import re
import os
import string
_known = {
    'zero': 0,
    'one': 1,
    'a':1,
    'an':1,
    'case':1,
    'two': 2,
    'both':2,
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
    "thousand": 1000
    }
def mk_dir(file_path):
    folder = os.path.exists(file_path)
    if not folder:
        os.makedirs(file_path)

def spoken_word_to_number(n):
    
    """Assume n is a positive integer".
    assert _positive_integer_number('nine hundred') == 900
    assert spoken_word_to_number('one hundred') == 100
    assert spoken_word_to_number('iven') == 11
    assert spoken_word_to_number('twenty two') == 22
    assert spoken_word_to_number('thirty-two') == 32
    assert spoken_word_to_number('forty two') == 42
    assert spoken_word_to_number('two hundred thirty two') == 232
    assert spoken_word_to_number('two thirty two') == 232
    assert spoken_word_to_number('nineteen hundred eighty nine') == 1989
    assert spoken_word_to_number('nineteen eighty nine') == 1989
    assert spoken_word_to_number('one thousand nine hundred and eighty nine') == 1989
    assert spoken_word_to_number('nine eighty') == 980
    assert spoken_word_to_number('nine two') == 92 # wont be able to convert this one
    assert spoken_word_to_number('nine thousand nine hundred') == 9900
    assert spoken_word_to_number('one thousand nine hundred one') == 1901
    """
    
    n = n.lower().strip()
    
    if n in _known:
        return _known[n]
    else:
        inputWordArr = re.split('[ -]', n)
    print(inputWordArr)
    
    assert len(inputWordArr) > 1 #all single words are known
    #Check the pathological case where hundred is at the end or thousand is at end
    if inputWordArr[-1] == 'hundred':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[-1] == 'thousand':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[0] == 'hundred':
        inputWordArr.insert(0, 'one')
    if inputWordArr[0] == 'thousand':
        inputWordArr.insert(0, 'one')
    inputWordArr = [word for word in inputWordArr if word not in ['and', 'minus', 'negative']]
    currentPosition = 'unit'
    prevPosition = None
    output = 0
    for word in reversed(inputWordArr):
        if currentPosition == 'unit':
            number = _known[word]
            output += number
            if number > 9:
                currentPosition = 'hundred'
            else:
                currentPosition = 'ten'
        elif currentPosition == 'ten':
            if word != 'hundred':
                number = _known[word]
                if number < 10:
                    output += number*10
                else:
                    output += number
            #else: nothing special
            currentPosition = 'hundred'
        elif currentPosition == 'hundred':
            if word not in [ 'hundred', 'thousand']:
                number = _known[word]
                output += number*100
                currentPosition = 'thousand'
            elif word == 'thousand':
                currentPosition = 'thousand'
            else:
                currentPosition = 'hundred'
        elif currentPosition == 'thousand':
            assert word != 'hundred'
            if word != 'thousand':
                number = _known[word]
                output += number*1000
        else:
            assert "Can't be here" == None
    return(output)

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

dig_list = ['zero', 'one', 'a', 'an', 'case', 'two', 'both', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
            'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 
            'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand','million', "and"]

def del_non_digit(text):
    
    text = text.strip().lower()
    text = cut_digit(text)
    text = text.translate(str.maketrans(string.punctuation, " "*32,)).replace("  ", " ")
    text = text.split(" ")
    digit_list = []
    digit_words = ""
    for word in text:
        if word.isdigit():
            digit_words = digit_words + "_" + word + "_"
        elif word in dig_list:
            digit_words = digit_words + " " + word
        else:
            digit_words = digit_words + "_"
    digit_word_list = [i for i in digit_words.split("_") if len(i) > 0]
    
    for word in digit_word_list:
        if word.isdigit():
            digit_list.append(word)
        else:
            if word != " and":
                digit_list.append(spoken_word_to_number(word))        
    return digit_list