import pandas as pd
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

df_30 = pd.read_csv('AI/features_30_sec.csv', index_col='filename')
labels = df_30[['label']]
df_30 = df_30.drop(columns=['length', 'label'])
df_30_scaled = sklearn.preprocessing.scale(df_30)
df_30 = pd.DataFrame(df_30_scaled, columns=df_30.columns)
similarity = cosine_similarity(df_30)
sim_df = pd.DataFrame(similarity, index=labels.index, columns=labels.index)

def find_similar_songs(name, n=10):
    series = sim_df[name].sort_values(ascending=False)
    series = series.drop(name)
    print (series.head(n).to_frame())
    print("\n")
    return series.head(n).to_frame()

def printoutput (jang, plus):
    if jang[0] != 0:
        print(jang[2] + " 장르일 확률 : " + str(jang[0] * 10)
              + " % - 정규 백분율 : " + str(round(jang[1] / plus * 100, 5))
              + " % - 개인 백분율 : " + str(round(jang[1] / jang[0] * 100, 5)) 
              + "% - 가중 백분율 : " + str(round(jang[1] / jang[0] * 100 * (jang[0] / 2), 5)) + "%")

def chek (jang, listin):
    if listin[0].split(".")[0] == jang[2]:
            jang[0] += 1
            jang[1] += float(listin[1])

def inputing (song):
    insong = find_similar_songs(song)
    
    testv = str(insong).split("\n")
    testv = testv[2:]

    hiphop = [0, 0, "hiphop"]
    reggae = [0, 0, "reggae"]
    disco = [0, 0, "disco"]
    pop = [0, 0, "pop"]
    metal = [0, 0, "metal"]
    jazz = [0, 0, "jazz"]
    blues = [0, 0, "blues"]
    classical = [0, 0, "classical"]
    country = [0, 0, "country"]
    rock = [0, 0, "rock"]

    for i in testv:
        listin = list(filter(None,i.split(" ")))
        
        chek(hiphop, listin)
        chek(reggae, listin)
        chek(disco, listin)
        chek(pop, listin)
        chek(metal, listin)
        chek(jazz, listin)
        chek(blues, listin)
        chek(classical, listin)
        chek(country, listin)
        chek(rock, listin)
            
    plus = hiphop[1] + reggae[1] + disco[1] + pop[1] + jazz[1] + metal[1] + blues[1] + classical[1] + country[1] + rock[1]
            
    print(song + " 분석 결과")
    
    printoutput(hiphop, plus)
    printoutput(reggae, plus)
    printoutput(disco, plus)
    printoutput(pop, plus)
    printoutput(jazz, plus)
    printoutput(metal, plus)
    printoutput(blues, plus)
    printoutput(classical, plus)
    printoutput(country, plus)
    printoutput(rock, plus)
    
inputing('blues.00012.wav')
inputing('classical.00065.wav')
inputing('country.00056.wav')
inputing('disco.00034.wav')
inputing('hiphop.00009.wav')
inputing('jazz.00028.wav')
inputing('metal.00094.wav')
inputing('pop.00054.wav')
inputing('reggae.00041.wav')
inputing('rock.00077.wav')