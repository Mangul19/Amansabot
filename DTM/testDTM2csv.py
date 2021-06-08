import pandas as pd

bi = ["도장", "해체", "설치", "양중", "굴착", "정리", "매설", "기타"]

def doc(args):
    doc_list = []
    df = pd.DataFrame()
    for i in args:
        # 단어 분해
        tmp_list = i.split(" ")

        for inpu in tmp_list:
            for biin in bi:
                if biin in inpu:
                    # 리스트 결합
                    doc_list.append(biin)
                    doc_list = list(set(doc_list))
                    break

    for i in doc_list:
        tmp = []
        for j in args:
            # 단어 분해
            tmp_list = j.split(' ')
            # 단어 세기
            for inpu in tmp_list:
                for biin in bi:
                    if biin in inpu:
                        tmp.append(biin.count(i))
                        break
        # 데이터 프레임 추가
        df[i] = tmp
    return df

#아래는 개발 후 수정하면 됨
dataset = pd.read_excel('DTM/비계사례DB.xlsx')
data = dataset['재해개요']

result = doc(data)

print(result)
result.to_csv('DTM/작업.csv', encoding='utf-8-sig')