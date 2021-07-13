import pandas as pd
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template
import os
from flask import send_from_directory
app = Flask(__name__)
   
df_30 = pd.read_csv('AI/features_30_sec.csv', index_col='filename')
labels = df_30[['label']]
df_30 = df_30.drop(columns=['length', 'label'])
df_30_scaled = sklearn.preprocessing.scale(df_30)
df_30 = pd.DataFrame(df_30_scaled, columns=df_30.columns)
similarity = cosine_similarity(df_30)
sim_df = pd.DataFrame(similarity, index=labels.index, columns=labels.index)

@app.route('/<song>')
def songCH(song):
   try:
      song += ".wav"
      def inputing (songname):
         print("---------------------------------------------")
         print(songname + "분석 요청")
         print("---------------------------------------------")
         mera = ""
         
         series = sim_df[songname].sort_values(ascending=False)
         series = series.drop(songname)
         insong = series.head(10).to_frame()
         mera += "추천곡_리스트_및_분석_파일" + str(insong)
         
         testv = str(insong).split("\n")
         testv = testv[2:]

         song = [[0, 0, 0, "hiphop"],
            [0, 0, 0, "reggae"],
            [0, 0, 0, "disco"],
            [0, 0, 0, "pop"],
            [0, 0, 0, "metal"],
            [0, 0, 0, "jazz"],
            [0, 0, 0, "blues"],
            [0, 0, 0, "classical"],
            [0, 0, 0, "country"],
            [0, 0, 0, "rock"],]
         
         for i in testv:
            listin = list(filter(None,i.split(" ")))
            
            for inpu in song:
               if listin[0].split(".")[0] == inpu[3]:
                  inpu[0] += 1
                  inpu[1] += float(listin[1])
                  if inpu[2] < float(listin[1]):
                     inpu[2] = float(listin[1])
               
         plus = 0
         for inpu in song:
            plus += inpu[1]
                  
         mera += "^" + songname + '과 비슷한 추천 음악^'
         panel = ""
         high = [0, ""]
         for inpu in song:
            if inpu[0] != 0:
               main = inpu[1] / plus * 100
               iniam = inpu[1] / inpu[0] * 100
               line = iniam * (inpu[2] * 100) * inpu[0] / chzero((100 - (inpu[2] * 100))) / 2.5
               
               mera += inpu[3] + " 장르 확률 정보 |||| 일반 확률 : " + str(inpu[0] * 10) + " % |||| 정규 백분율 : " + str(round(main, 5)) + " % |||| 개인 백분율 : " + str(round(iniam,5)) + " %^최대 백분율 : " + str(round(inpu[2]*100,5)) +  " % |||| 가중 백분율 " + str(round(line,5)) + " %^"
               
               if line >= 100:
                  panel += inpu[3] + ", "
                  if line > high[0]:
                     high = [line, inpu[3]]
                     
         mera += "^해당 음악은 " + panel + "장르와 흡사합니다^또한 해당  음악은 " + high[1] + "장르와 가장 흡사합니다"
         return(mera)

      def chzero (num):
         if num <= 0:
            return 1
         else:
            return num

      x = inputing(song)
      print(x)
      return render_template('/hello.html', song = x)
   except KeyError:
      print("해킹시도 OR 오입력 오류 페이지 출력")
      return render_template('/error.html')

@app.route('/')
def main():
   return render_template('/main.html')

@app.errorhandler(404)
def not_found_error(error):
   print("해킹시도 가능성 높음 OR 오입력 오류 페이지 출력")
   return render_template('error.html')

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run(debug = True, host='192.103.0.2', threaded=True, port=80)