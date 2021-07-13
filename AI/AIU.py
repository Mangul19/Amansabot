import pandas as pd
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

df_30 = pd.read_csv('AI/features_30_sec.csv', index_col='filename')

labels = df_30[['label']]
df_30 = df_30.drop(columns=['length', 'label'])

df_30_scaled = sklearn.preprocessing.scale(df_30)

df_30 = pd.DataFrame(df_30_scaled, columns=df_30.columns)

print(df_30.head())

similarity = cosine_similarity(df_30)

sim_df = pd.DataFrame(similarity, index=labels.index, columns=labels.index)

print(sim_df.head())

def find_similar_songs(name, n=5):
  series = sim_df[name].sort_values(ascending=False)

  series = series.drop(name)

  return series.head(n).to_frame()

print(find_similar_songs('hiphop.00018.wav'))