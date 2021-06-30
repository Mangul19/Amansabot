import pandas as pd

bi = ["도장", "해체", "설치", "양중", "굴착", "정리", "매설", "기타"]

def doc(args):
    doc_list = []
    df = pd.DataFrame()
        
    for i in args:
        # 단어 분해
        tmp_list = i.split(" ")

        
        #분해한 단어 하나씩 넣기
        for inpu in tmp_list:
            ch = True
            #추출하고자 하는 단어 하나씩 넣기
            for biin in bi:
                #단어와 비교단어 하나씩 비교 후 만약 존재한다면
                if biin in inpu:
                    # 리스트 결합
                    doc_list.append(biin)
                    doc_list = list(set(doc_list)) 
                    
                    #체크 기능 비활성
                    ch = False
                    
                    break
                
            #만약 하나도 찾지 못했다면 기타 단어로 처리
            if ch:
                doc_list.append("기타단어")
                doc_list = list(set(doc_list)) 
                
    bi.append("기타단어")
    
    for i in doc_list:
        tmp = []
        
        for j in args:
            # 단어 분해
            tmp_list = j.split(' ')
            
            # 분해한 단어 한개씩 넣기
            for inpu in tmp_list:
                # 비교하고자 하는 단어 하나씩 넣어 비교
                for biin in bi:
                    tmp.append(biin.count(i))
                    
        # 데이터 프레임 추가
        df[i] = tmp
    return df

#아래는 개발 후 수정하면 됨
dataset = pd.read_excel('DTM/비계사례DB.xlsx')
data = dataset['재해개요']

result = doc(data)

print(result)
result.to_csv('DTM/작업.csv', encoding='utf-8-sig')