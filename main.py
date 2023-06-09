from fastapi import FastAPI
import pandas as pd
import requests
import io
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
import uvicorn

# Load file into a dataframe
url = 'https://raw.githubusercontent.com/ejerico/pi_01/main/my_data.csv'
response = requests.get(url).content
df = pd.read_csv(io.StringIO(response.decode('utf-8')))

app = FastAPI()

# FUNCTION 1
@app.get('/get_peliculas_mes/{mes}')
def peliculas_mes(mes: str): 
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente''' 

    respuesta = int(df['month'].str.contains(mes).sum())
    return {'mes':mes, 'cantidad':respuesta}

# FUNCTION 2
@app.get('/get_peliculas_dia/{dia}')
def peliculas_dia(dia: str): 
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente''' 
    
    respuesta = int(df['day'].str.contains(dia).sum())
    return {'dia':dia, 'cantidad':respuesta}

# FUNCTION 3
@app.get('/get_franquicia/{franquicia}')
def franquicia(franquicia: str): 
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio''' 

    quantity_films = df['collection_name'].str.contains(franquicia).sum()
    subset = df[df['collection_name'] == franquicia]
    total_revenue = subset['revenue'].sum()
    average_revenue = total_revenue / quantity_films

    return {'franquicia':franquicia, 'cantidad':quantity_films, 'ganancia_total':total_revenue, 'ganancia_promedio':average_revenue}

# FUNCTION 4
@app.get('/get_peliculas_pais/{pais}')
def peliculas_pais(pais: str): 
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo''' 

    quantity_films = df['production_countries'].str.contains(pais).sum()

    return {'pais':pais, 'cantidad':quantity_films}

# FUNCTION 5
@app.get('/get_productoras/{productora}')
def productoras(productora: str):
    '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron''' 

    quantity_films = df['production_companies'].str.contains(productora).sum()
    df_clean = df.fillna('unknown')
    subset = df_clean[df_clean['production_companies'].str.contains(productora)]
    subset['revenue'] = pd.to_numeric(subset['revenue'], errors='coerce')
    total_revenue = subset['revenue'].sum()

    return {'productora':productora, 'ganancia_total':total_revenue, 'cantidad':quantity_films}

# FUNCTION 6
@app.get('/get_retorno/{pelicula}')
def retorno(pelicula: str): 
    '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''' 

    year =      int(df[df['title'] == pelicula]['release_year'].iloc[0])
    budget =    int(df[df['title'] == pelicula]['budget'].iloc[0])
    revenue =   int(df[df['title'] == pelicula]['revenue'].iloc[0])
    return_ =   int(df[df['title'] == pelicula]['return'].iloc[0])

    return {'pelicula':pelicula, 'inversion':budget, 'ganancia':revenue,'retorno':return_, 'anio':year}

# FUNCTION 7 - MACHINE LEARNING
@app.get('/get_recomendacion/{titulo}')
def recomendacion(titulo: str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''

    df.fillna('', inplace=True)
    df['vote_average'] = df['vote_average'].astype(str)

    # Create a feature matrix using a sparse matrix
    text = df['title'] + ' ' + df['vote_average'] + ' ' + df['genres']
    vectorizer = CountVectorizer(min_df=2)
    X = vectorizer.fit_transform(text)
    sparse_X = csr_matrix(X)

    # Fit a nearest neighbor model on the feature matrix
    nn = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='cosine')
    nn.fit(sparse_X)

    # Define a function to recommend similar movies
    def recommend(movie, nn_model, df, k=5):
        idx = df[df['title'] == movie].index[0]
        distances, indices = nn_model.kneighbors(X[idx], n_neighbors=k+1)
        titles = df.iloc[indices[0], :]['title']
        return list(titles.iloc[1:])

    answer = recommend(titulo, nn, df)

    return {'lista recomendada': answer}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)