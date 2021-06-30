


import pandas as pd

def doc(args):
    doc_list = ["도장", "해체", "설치", "양중", "굴착", "정리", "매설"]
    df = pd.DataFrame()
    
    chli = 0
    ch = [0] * len(args)
    
    for i in doc_list:
        tmp = []
        for j in args:
            # 단어 분해
            tmp_list = j.split(' ')
            a = 0
            ch[chli] = 0
            # 단어 세기
            for inpu in tmp_list:
                if i in inpu:
                    a += 1
                else:
                    ch[chli] += 1
                    
            tmp.append(a)
            
            chli += 1
        # 데이터 프레임 추가
        df[i] = tmp
        
        chli = 0
        
    tmp = []
    
    for i in ch:
        if i != 0:
            tmp.append(i)
        else:
            tmp.append("F")
    
    df["기타"] = tmp
    return df

#아래는 개발 후 수정하면 됨
dataset = pd.read_excel('DTM/data.xlsx')
data = dataset['재해개요']

result = doc(data)

print(result)
result.to_csv('DTM/작업.csv', encoding='utf-8-sig')