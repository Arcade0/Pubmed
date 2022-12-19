__author__ = 'Qiao Jin'
import os
import glob
import json
import xml.etree.ElementTree as ET

files = os.listdir("pubmed_2022")
files.sort()
for xml_path in files:
    
    check = os.path.exists("pubmed_2022d/%s" % xml_path.replace("xml", "json"))
    if not check:
        print('Processing %s' % xml_path)
        output = {}

        tree = ET.parse("pubmed_2022/%s" % xml_path)
        root = tree.getroot()

        for citation in root.iter('MedlineCitation'):
            
            # 获取pmid
            pmid = citation.find('PMID')
            if pmid == None:
                continue
            else:
                pmid = pmid.text
            
            #获取标题
            texts = {}
            title = citation.find('Article/ArticleTitle')
            if title is None:
                texts["Title"] = ""
            else:
                texts["Title"] = " ".join(title.itertext())
            
            # 获取期刊
            journal = citation.find("Article/Journal/Title")
            if journal is None:
                texts["Journal"] = ""
            else:
                texts["Journal"] = " ".join(journal.itertext())
                
            # 获取摘要，摘要存在分段
            info_l = []
            for info in citation.iter('AbstractText'):
                if info is None:
                    abstract = ""
                if info is not None:
                    abstract = " ".join(info.itertext())
                    info_l.append(abstract)
            texts["Ab"] = texts["Title"] + " " + " ".join(info_l)
            
            # 存取mesh词汇
            MHs = []
            mesh = citation.find("MeshHeadingList")
            if  mesh is None:
                MHs = []
            else:
                for MH in mesh:
                    MHs.append([mh.text for mh in MH])

            # 存取日期
            date = citation.find("DateCompleted/Year")
            if  date is None:
                dates = ""
            else:
                dates = date.text
            
            output[pmid] = {'pmid': pmid,
                            'texts': texts,
                            'Meshhead':MHs,
                            "date":dates}
        
        with open('pubmed_2022d/%s.json' % xml_path.split('.')[0], 'w') as f:
            json.dump(output, f, indent=4)
            f.close()