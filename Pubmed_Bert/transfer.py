import os
import numpy as np
import pandas as pd
import json
from copy import deepcopy
import re
import shutil
import random
import string
from random import choice
random.seed(10)
# -*- coding:utf-8 -*
import eval
from mkdir import mk_dir
import spokentonumber

def trans_num(df, col):
    
    for i in df.index:
    
        if len({"a", "an", "case"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "1-9"
        elif len({"hundred","thousand"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "100以上"
        else:
            digit_list = spokentonumber.del_non_digit(df.loc[i, col])
            if (len(digit_list) > 0) & ("to" not in df.loc[i, col].lower()):
                clasn = digit_list[0]
                if int(clasn) in range(1,10):
                    clas = "1-9"
                elif int(clasn) in range(10,100):
                    clas = "10-99"
                elif int(clasn) >= 100:
                    clas = "100以上"
                else:
                    clas = "none"
            else:
                clas = "none"
                
        df.loc[i, col] = clas
    
    return df

def trans_age(df, col):
    
    for i in df.index:

        if len({"elder", "elderly", "older", "aging"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "65岁以上"
        elif len({"adult", "adults", "middle","mature"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "18-64岁"
        elif len({"young", "younger", "child", "children",
                  "adolescent", "adolescents", 
                  "pediatric"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "1-17岁"
        elif len({"infant", "infants", 
                  "neonates", "neonate","neonatal",
                  "day", "days", "month", 
                  "months", "premature"} & set(df.loc[i, col].lower().split(" "))) > 0:
            clas = "1岁以下"

        else:
            digit_list = spokentonumber.del_non_digit(df.loc[i, col])
            if (len(digit_list) > 0) & ("to" not in df.loc[i, col].lower()):
                clasn = digit_list[0]
                if int(clasn) in range(1,18):
                    clas = "1-17岁"
                elif int(clasn) in range(18,65):
                    clas = "18-64岁"
                elif int(clasn) in range(65,120):
                    clas = "65岁以上"
                else:
                    clas = "none"
            else:
                clas = "none"
        df.loc[i, col] = clas
    
    return df

def trans_gender(df, col):
    
    for i in df.index:
        
        if (len({"man", "men", "boy", "boys","male", "males", "he", 
                "gentleman", "gentlemen", "his", "him"} & set(df.loc[i, col].lower().split(" "))) > 0) and (len({"woman", "women", "girl","girls", "female", 
                    "females", "fm", "she", "lady", "ladies", "her"} & set(df.loc[i, col].lower().split(" ")))==0):
                clas = "男"
                
        elif (len({"man", "men", "boy", "boys","male", "males", "he", 
                "gentleman", "gentlemen", "his", "him"} & set(df.loc[i, col].lower().split(" "))) == 0) and (len({"woman", "women", "girl","girls", "female", "females", "fm", "she", "lady", "ladies", "her"} & set(df.loc[i, col].lower().split(" ")))>0):
            clas = "女"
        else:
            clas = "none"
    
        df.loc[i, col] = clas
    
    return df

def trans_immu(df, col):
    
    import re
    for i in df.index:
        
        dig_list = re.split(r' |-|/|\.|,', df.loc[i, col].lower())
        print(dig_list)
        if (len({
            "immunodeficiency", "immune deficiency",
            "immunocompromised", "immunocompromise", 
            "immunosuppressive","immunosuppression",
            "immunosuppressed","immunocompromized",
            "immunodepression","immunosuppressant",
            "obstructive","copd","bronchiectasis","fibrosis",
            # "compromised", "suppressed", "supperssive", "suppression",
            "hiv","aids",
            "transplantation", "transplanted","transplant","recipient","recipients",
            "chemotherapy","corticosteroid",
            "malignancy", "malignancies","cancer", "carcinoma", "sarcoma","adenocarcinoma",
            "anemia", "leukemia","leukaemia", "leukemic","lymphoma", "melanoma", "myeloma",
            "impaired immune", "diabetes","diabetic","mellitus","dialysis",
            "failure", "premature","preterm","low birth weight","splenectomized"} & set(dig_list))>0) and (len({"immunocompetent","negative","uninfected"} & set(dig_list))==0):
            clas = "抑制"
        elif "emia" in df.loc[i, col].lower():
            clas = "抑制"
        else:
            clas = "none"
    
        df.loc[i, col] = clas
    
    return df

def transfer_evi(df, col):
    
    for i in df.index:
    
        dig_list = df.loc[i, col].lower().split(" ")

        for dig in dig_list:
            
            if len({"autopsy", "biopsy", "biopsies", 
                "tissue", "postmortem",
                "histopathology", "histology", "histological", "histopathological","histopathologic"} & set(df.loc[i, col].lower().split(" "))) > 0:
                clas = "1：同时具备肺组织病理+病原学证据"
            elif len({"blood","abscess",
                "pleural", "purulent","fluid","pus",
                "csf","cerebrospinal"} & set(df.loc[i, col].lower().split(" "))) > 0:
                clas = "3：血及无菌体液（如脓胸液）"
            elif len({"bronchoscopy","bronchoscopies","bronchoscopic", "thoracoscopic","bronchoscope","transbronchoscopy",
                "tracheal", "bronchial", "throat","tbna",
                "bal", "balf", "bronchoalveolar","lavage"} & set(df.loc[i, col].lower().split(" "))) > 0:
                clas ="4：气管镜活检组织培养出病原体，或者支气管肺泡灌洗液（BALF）定量培养>10**4"
            elif len({"aspirate", "aspiration", "aspirates",
                "secretion", "sputum", "sputa","immunohistochemistry","staining"} & set(df.loc[i, col].lower().split(" "))) > 0:
                clas ="5：气管吸出物或痰/BALF纯培养或优势培养出病原体"
            else:
                clas = "none"
                # print(dig, clas)
        df.loc[i, col] = clas
    
    return df