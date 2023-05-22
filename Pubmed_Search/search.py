# 检索
import json
spec_d = {}
spec_papers_d = {}
for i in ["Bactology", "Mycology", "Virology"]:

    with open("specs_list/%s.txt" % (i), "r") as f:
        specs = [i.replace("\"", "").replace("\n", "").lower() for i in f.readlines()]
    
    spec_paper_d = {}
    for spec in specs:
        spec_paper_d[spec] = []
    spec_papers_d[i] = spec_paper_d

iter_list = set(range(100, 1114, 100))
iter_list.add(1114)
for i in iter_list:

    with open("words_dic/words_dic_%s.txt" % i, "r") as f:
        content = f.read()
        words_dic = json.loads(content)
    print("read: words_dic_%s.txt" % i)
    
    for k,v in words_dic.items():
        words_dic[k] = set(v)
        
    for spec_type in spec_papers_d:
                    
        spec_paper_d = spec_papers_d[spec_type]
        
        for spec in spec_paper_d: 

            term = spec.lower().split(" ")
            if spec_type in ["Bactology", "Mycology"]:
                if len(term) > 1:
                    term_set = words_dic.setdefault(term[0][0], {0}) | words_dic.setdefault(term[0], {0})
                else:
                    term_set = words_dic.setdefault(term[0], {0})
            else:
                term_set = words_dic.setdefault(term[0], {0})

            for j in range(1,len(term)):
                term_set = term_set & words_dic.setdefault(term[j],{0})

            spec_paper_d[spec] = spec_paper_d[spec]+ list(term_set)
        
        spec_papers_d[spec_type] = spec_paper_d

    print("search finished: words_dic_%s.txt" % i)

    del(words_dic)
    with open("search_results/search_results.txt", "w") as f:
        a = json.dumps(spec_papers_d)
        f.write(a)
