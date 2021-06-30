import pandas as pd
import re

def doc(args):
    doc_list = []
    df = pd.DataFrame()
    for i in args:
        # 단어 분해
        tmp_list = i.lower().replace(',','').split(' ')
        #불용어 처리 들어갈 부분(반점만 없애고 싶은데,,,)
        # 리스트 결합
        doc_list += tmp_list
    doc_list = list(set(doc_list))
    
    for i in doc_list:
        tmp = []
        for j in args:
            # 단어 분해
            tmp_list = j.lower().replace(',','').split(' ')
            # 단어 세기
            tmp.append(tmp_list.count(i))
        # 데이터 프레임 추가
        df[i] = tmp
    return df

#아래는 개발 후 수정하면 됨(전체 파일 읽는법 시도 해봤지만 자꾸 오류뜸 ㅠㅠ)
dataset = pd.read_excel('DTM/30_.xlsx')
data = dataset['재해개요']

result = doc(data)

print(result)
result.to_csv('DTM/DTM2.csv', encoding='utf-8-sig')