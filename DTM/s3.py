import pandas as pd
from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Okt
from konlpy.utils import pprint
from sklearn.feature_extraction.text import CountVectorizer


if __name__ == '__main__':
    t_file_name = open('List.txt', 'r', encoding='utf-8')

    title_list = []
    for line in t_file_name.readlines():
        title_list.append(line[:-1])

    t_file_name.close()

    dataset = pd.read_excel('data.xlsx')

    tagger = Okt()

    for title in title_list:        # title_list에 대해 반복문을 실행
        cv = CountVectorizer()
        
        # 각 문서들의 말뭉치(corpus)를 저장할 리스트 선언
        corpus = []

        # 각 타이틀에 대한 문서들의 말 뭉치를 저장한다. (데이터가 많으면 이 부분에서 장시간이 소요될 수 있다.)
        for doc_num in range(6770):
            # 각 말뭉치에서 명사 리스트를 만든다.
            noun_list = tagger.nouns(dataset[title].loc[doc_num])
            
            # 이를 문자열로 저장해야하기 때문에 join함수로 공백으로 구분해 corpus에 append한다.
            corpus.append(' '.join(noun_list))

        # CountVectorizer의 fit_transform 함수를 통해 DTM을 한번에 생성할 수 있다.
        DTM_Array = cv.fit_transform(corpus).toarray()

        # feature_names 함수를 사용하면 DTM의 각 열(column)이 어떤 단어에 해당하는지 알 수 있다.
        feature_names = cv.get_feature_names()

        # 추출해낸 데이터를 DataFrame 형식으로 변환한다.
        DTM_DataFrmae = pd.DataFrame(DTM_Array, columns=feature_names)

        # 최종적으로 DTM을 csv 파일로 저장한다.
        DTM_DataFrmae.to_csv('DTM.csv', encoding='utf-8-sig')