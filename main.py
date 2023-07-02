from flask import Flask, render_template, request
import requests
import time
import pandas as pd

df = pd.read_pickle('files/df2.pkl')
df_original = pd.read_pickle('files/df_original.pkl')
cosine_sim2 = pd.read_pickle('files/similarity.pkl')
df_tv = pd.read_pickle('files/tv_df.pkl')
df_movie = pd.read_pickle('files/movie_df.pkl')
app = Flask(__name__)


def fetch_poster(x):
    responsed = requests.get('https://api.jikan.moe/v4/anime/{}/pictures'.format(x))
    data = responsed.json()
    cnt = 0
    if (data):
        for item in data['data']:
            jpg_url = item['jpg']['large_image_url']
            return jpg_url


img_path = []
img_path_movie = []
img_path_tv = []

Anime_id = list(df['Anime_id'].values)
Anime_id_tv = list(df_tv['Anime_id'].values)
Anime_id_movie = list(df_movie['Anime_id'].values)
for i in range(0, 16):
    img_path.append(fetch_poster(Anime_id[i]))
    time.sleep(.34)

for i in range(0, 16):
    img_path_tv.append(fetch_poster(Anime_id_tv[i]))
    time.sleep(.34)

for i in range(0, 16):
    img_path_movie.append(fetch_poster(Anime_id_movie[i]))
    time.sleep(.34)


@app.route("/")
def index():
    return render_template('home.html', Anime_Name=list(df['Title'].values),
                           description=list(df['Synopsis'].values),
                           Anime_Type=list(df['Type'].values),
                           Anime_epi=list(df['Episodes'].values),
                           imgs=img_path)



@app.route("/", methods=['post'])
def recommender():
    user_input = request.form.get('Anime_input')
    movie_index = df[df['Title'] == str(user_input)].index[0]
    distances = sorted(list(enumerate(cosine_sim2[movie_index])), reverse=True, key=(lambda x: x[1]))[1:9]
    y = []
    for i in range(0, 8):
        y2 = []
        y2.append(fetch_poster(df['Anime_id'][distances[i][0]]))
        y2.append(df['Title'][distances[i][0]])
        y2.append(df['Type'][distances[i][0]])
        y2.append(df['Synopsis'][distances[i][0]])
        y2.append(df['Episodes'][distances[i][0]])
        y.append(y2)
        time.sleep(.8)
    return render_template('recommender.html', data=y, Anime_Name=list(df['Title'].values))




@app.route("/popular")
def popular():
    return render_template('popular.html', Anime_Name=list(df['Title'].values),
                           description=list(df['Synopsis'].values),
                           Anime_Type=list(df['Type'].values),
                           Anime_epi=list(df['Episodes'].values),
                          imgs=img_path)


@app.route("/Tv")
def Tv():
    return render_template('TV.html', Anime_Name=list(df_tv['Title'].values),
                           description=list(df_tv['Synopsis'].values),
                           Anime_Type=list(df_tv['Type'].values),
                           Anime_epi=list(df_tv['Episodes'].values),
                           imgs=img_path_tv)


@app.route("/Movie")
def Movie():
    return render_template('Movie.html', Anime_Name=list(df_movie['Title'].values),
                           description=list(df_movie['Synopsis'].values),
                           Anime_Type=list(df_movie['Type'].values),
                           Anime_epi=list(df_movie['Episodes'].values),
                           imgs=img_path_movie)


if __name__ == '__main__':
    app.run(debug=True,port=500)
