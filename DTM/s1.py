import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    dataset = pd.read_csv('DTM.csv')

    column_list = dataset.columns[1:]
    word_length = len(column_list)

    count_dict = {}

    for doc_number in tqdm(range(len(dataset)), desc='단어쌍 만들기 진행중'):
        tmp = dataset.loc[doc_number]
        for i, word1 in enumerate(column_list):
            if tmp[word1]:
                for j in range(i + 1, word_length):
                    if tmp[column_list[j]]:
                        count_dict[column_list[i], column_list[j]] = count_dict.get((column_list[i], column_list[j]), 0) + max(tmp[word1], tmp[column_list[j]])

    count_list = []

    for words in count_dict:
        count_list.append([words[0], words[1], count_dict[words]])

    df = pd.DataFrame(count_list, columns=["word1", "word2", "freq"])
    df = df.sort_values(by=['freq'], ascending=False)
    df = df.reset_index(drop=True)

    df.to_csv('networkx.csv', encoding='utf-8-sig')