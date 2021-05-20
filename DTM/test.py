import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
#from gensim.models import Word2Vec
#from konlpy.tag import Okt

#데이터 위치를 불러옴
pos_data=pd.read_excel('DTM/30_.xlsx', sheet_name='비계사고',header = None, names = ['재해개요'])

# 문장을 각각 읽어옴
lines_pos=[]
for i in pos_data:
    try:
        f = open(i, 'r')
        temp = f.readlines()[0]
        lines_pos.append(temp)
        f.close()
    except Exception as e:
        continue

pos_data['재해개요'] = pos_data['재해개요'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
print(pos_data)

'''
#불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
#okt = Okt()
tokenized_data = []
for sentence in pos_data['재해개요']:
    #temp_X = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    tokenized_data.append(temp_X)

#word2vec 
#model = Word2Vec(tokenized_data, sg=1, window=2, min_count=3)
'''