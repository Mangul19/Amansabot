from gensim.models import Word2Vec, Doc2Vec
import pickle

def test_word2vec(model, inputword, search_keyword=None):
    if search_keyword is not None:
        if len(inputword) == 1:
            print("========================================================")
            print("단어 '%s'와(과) 가장 연관성이 높은 %s 그룹 단어는:" % (inputword[0],
            search_keyword))
            results = model.most_similar(positive=inputword, topn=len(model.wv.vocab))
            
            for word, score in results:
                if search_keyword in word:
                    print("word: %s, score: %.3f" % (word, score))
                    print("========================================================\n")
        else:
            vectors = [model.wv[w] for w in inputword]
            result = model.similar_by_vector(sum(vectors), topn=100)

            print("========================================================")
            print("%s들의 덧셈 연산 결과와 가장 연관성이 높은 %s 그룹 단어는:" %
            (str(inputword), search_keyword))
            results = list(filter(lambda r: r[0] not in inputword, result))
            for word, score in results:
                if search_keyword in word:
                    print("word: %s, score: %.3f" % (word, score))
                    print("========================================================\n")
    else:
        if len(inputword) == 1:
            print("========================================================")
            print("단어 '%s'와(과) 가장 연관성이 높은 단어는:" % (inputword[0]))
            results = model.most_similar(positive=inputword, topn=100)
            for word, score in results:
                print("word:%s, score:%.3f" % (word, score))
                print("=====================================================\n")
        else:
            vectors = [model.wv[w] for w in inputword]
            result = model.similar_by_vector(sum(vectors), topn=10)

            print("=====================================================")
            print("%s들의 덧셈 연산 결과와 가장 연관성이 높은 단어는:" % str(inputword))
            print(list(filter(lambda r: r[0] not in inputword, result)))
            print("=====================================================\n")
        
def test_doc2vec(model, input):
    if input.isdigit():
        print("=====================================================")
        print("%s번 문서와 가장 연관성이 높은 문서는:" % input)
        result = model.docvecs.most_similar(str(int(input)-1))
        for idx in range(len(result)):
            doc_idx, sim = result[idx]
            print("문서번호 %d 유사도:%.3f" % (int(doc_idx)+1, sim))
        print("=====================================================\n")
    else:
        with open('datalist.pkl', 'rb') as listfile:
        datalist = pickle.load(listfile)

        print("=====================================================")
        print("단어 '%s'을(를) 포함한 문서 번호는:" % input)
        for idx, doc in enumerate(datalist):
            if input in doc:
                print("Document ID:", idx+1)
        print("=====================================================\n")

if __name__ == "__main__":
    # 인자들은 각자 맞게 수정하면 됨
    word2vec_model = Word2Vec.load("weights/word2vec/model.model")
    doc2vec_model = Doc2Vec.load("weights/doc2vec/model.model")

    # 시나리오 1. word2vec 단일 단어 검색
    test_word2vec(word2vec_model, inputword=['사다리/N/cause'], search_keyword="prevent")
    test_word2vec(word2vec_model, inputword=["추락/N"])

    # 시나리오 2. word2vec 여러 단어 검색 --> 각 단어 벡터의 합 연산
    #test_word2vec(word2vec_model, ["맨홀/N", "청소/N"], search_keyword="summary")
    test_word2vec(word2vec_model, ["사다리/N/summary", "추락/N/summary"])

    # 시나리오 3. doc2vec 문서 id 검색 --> 가장 연관성이 높은 문서의 id 반환
    test_doc2vec(doc2vec_model, '228')

    #시나리오 4. 특정 단어 검색 시 해당 단어가 token으로 포함된 문서 번호 출력
    test_doc2vec(doc2vec_model, '작업대/N/summary')