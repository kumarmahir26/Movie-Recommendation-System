import mysql.connector
import streamlit as st
import requests
import gensim
from gensim import corpora, models, similarities

import pickle  
with open('models/dictionary.pkl', 'rb') as f:
    dictionary = pickle.load(f)
with open('models/tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)

###
import zipfile
zip_file_path = 'models/index.zip'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract('index.pkl', 'temp_directory')
with open('temp_directory/index.pkl', 'rb') as f:
    index = pickle.load(f)
import shutil
shutil.rmtree('temp_directory')
###

# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="movies"
)

mycursor=mydb.cursor()
print("Connection Established")

# This function brings image for a movie poster using tmdb api
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Returns a list of movies most similar to the query
def recommend(movie_query):
    global tfidf, index,dictionary
    
    query=''
    try:
        sql_query = f"SELECT sentiment FROM movie_data4 WHERE title = '{movie_query}'"
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        query=result[0]
        
    except:
        query=movie_query
        
    query=gensim.utils.simple_preprocess(query)
    query_bow = dictionary.doc2bow(query)
    query_tfidf = tfidf[query_bow]

    # Get the similarity scores between the query and the documents in the corpus
    sims = index[query_tfidf]

    # Sort the similarities in descending order
    sims = sorted(enumerate(sims), key=lambda x: -x[1])
    rid=[]
    for i in sims[:20]:
        sql_query = f"SELECT id FROM movie_data4 WHERE RowNumber = {i[0]}"
        mycursor.execute(sql_query)
        # Fetch the result
        result = mycursor.fetchone()
        movie_id = result[0]
        rid.append(movie_id)
    
    return rid  # id of the movies to be recommended


st.header('Movie recommendation system')

# Create Streamlit App
def main():
    
    movie_query=st.text_input("Enter any keyword like movie name, genres, actor names")
    rid=recommend(movie_query)
    
    num_rows = 10
    num_columns = 2

    for row in range(num_rows):
        st.text('   ')
        st.text('   ')
        row_container = st.columns(num_columns)

        for col in range(num_columns):
            index = row * num_columns + col
            movie_id = rid[index]

            with row_container[col]:
                sql_query = f"SELECT title FROM movie_data1 WHERE id = {movie_id}"
                mycursor.execute(sql_query)

                # Fetch the result
                result = mycursor.fetchone()

                if result:
                    movie = result[0]
                    st.text(movie)
                    st.image(fetch_poster(movie_id),width=300)

    
 
if __name__ == "__main__":
    main()
