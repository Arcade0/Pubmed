import requests
import time
import hashlib
import uuid

def mk_dir(file_path):

    folder = os.path.exists(file_path)
    if not folder:
        os.makedirs(file_path)
        
def youdao_trans(translate_text):

    youdao_url = 'https://openapi.youdao.com/api'  # 有道api地址

    # 翻译文本生成sign前进行的处理
    input_text = ""

    # 当文本长度小于等于20时，取文本
    if (len(translate_text) <= 20):
        input_text = translate_text

    # 当文本长度大于20时，进行特殊处理
    elif (len(translate_text) > 20):
        input_text = translate_text[:10] + str(
            len(translate_text)) + translate_text[-10:]

    # 编辑sign
    time_curtime = int(time.time())  # 秒级时间戳获取
    app_id = "24726bcc0cd1827f"  # 应用id
    uu_id = uuid.uuid4()  # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = "rXB3wNMTCz70xQi0OTUDTKs9ZEExwkkb"  # 应用密钥

    sign = hashlib.sha256(
        (app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()  # sign生成

    # 编辑输入
    data = {
        'q': translate_text,  # 翻译文本
        'from': "en",  # 源语言
        'to': "zh-CHS",  # 翻译语言
        'appKey': app_id,  # 应用id
        'salt': uu_id,  # 随机生产的uuid码
        'sign': sign,  # 签名
        'signType': "v3",  # 签名类型，固定值
        'curtime': time_curtime,  # 秒级时间戳
    }

    # 获得输出
    r = requests.get(youdao_url, params=data).json()  # 获取返回的json()内容
    print(r)
    results = r["translation"][0]  # 获取翻译内容
    return results

def trans(paper, input_path, output_path):
    
    # 添加翻译

    with open(input_path + "/%s" % paper, "r") as f:
        full = f.read()
        f.close()
    
    import re
    text_l = re.findall(r'.{5000}', full)
    
    full_cn = full + "\n"
    for i in text_l:
        full_cn = full_cn + youdao_trans(i)
    
    with open(output_path + "/%s" % paper, "w") as f:
        f.write(full_cn)
        f.close()