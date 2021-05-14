from konlpy.tag import Kkma

kkma = Kkma()

def morph(text):
    sentences = kkma.sentences(text)
    # 텍스트를 문장으로 분리
    for sentence in sentences:
        print('=' * 50)
        print(sentence)
        print('morphs : ', kkma.morphs(sentence))
    
    # 형태소 분석
    print('pos : ', kkma.pos(sentence))
    # 태깅
    print('nouns : ', kkma.nouns(sentence))
    # 명사 추출
    
    while True:
        text = input('문장을 입력하세요 : ')
        if text == 'exit':
            break
        else:
            morph(text)