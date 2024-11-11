# Movie Recommender Web App

## Demo Video
#### User Input: Discover movies based on your preferences – explore by genre, cast, keyword, or description.

<img src="https://github.com/kumarUjjawal3621/movie_recommendation/assets/136676393/498a33af-71f1-441d-9558-1e1874a277b4" width="550" height="550" alt="Demo Gif">

## Workflow

### Data Collection
- Web Scraping: Gathered data from the IMDB advanced search page.
- Kaggle Dataset: Utilized the TMDB movie metadata dataset from Kaggle ([TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)).
- Movie Images: Fetched movie images from the TMDB website's API.

### Data Wrangling and Feature Engineering
- Extracted meaningful features from JSON-like columns.
- Final data for NLP includes three features: movie ID, movie Title, sentiment.
  - Sentiment comprises keywords, genres, top 3 cast names, director name, and a short description of the movie.

### Model Building
- Utilized Bag of Words and TF-IDF for document embedding.
- For any query, the system returns the top 20 movies with the highest cosine similarity.

### Deployment

 #### Database
 - Stored the data in a MySQL server.
 - Built a cursor in `app.py` to fetch the data according to the query.

 #### UI
 - Built the user interface using Streamlit.
 - Deployed the webpage locally.
