import json
from mkdir import mk_dir
def bset(qa, output_path, filename):
    
    sets = {
        "data": [{
            'paragraphs': [],
            'title': "LungB"
        }],
        "version": "LungB"
    }
    
    sets['data'][0]["paragraphs"] = qa
    
    mk_dir(output_path)
    with open(output_path+filename, "w") as f:
        texts = json.dumps(sets)
        f.write(texts)
    
def train_yn(id, que, ans, context):

    im = {"yes": False, "no": True}
    
    qa = {
        'qas': [{
            'id': id,
            'question': que,
            'is_impossible': im[ans],
            'answers': ans
        }],
        'context': context
        }
    
    return qa

def test_yn(id, que, ans, context):
    
    qa = {
        'qas': [{
            'id': id,
            'question': que,
        }],
        'context': context
        }
    
    return qa

def train_qa(id, que, ans, ansp, context):
    
    qa = {
        "qas": [
            {
            "id": id,
            "question": que,
            "answers": [
                {
                    "text": ans,
                    "answer_start": ansp,
                }
            ]
            }
        ],
        "context": context}
    
    return qa

def test_qa(id, que, context):
    
    qa = {
        "qas": [
            {
            "id": id,
            "question": que,
            "answers": []
            }
        ],
        "context": context}
    
    return qa