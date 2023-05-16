
# README

Este repositorio contiene la implementación de una API que proporciona información sobre la oferta de entretenimiento de una plataforma de streaming y un sistema de recomendación de películas.

La API se ha implementado utilizando Python y FastAPI. El servidor se aloja en render.com y se puede acceder a la API a través del enlace indicado al pie de la página.

El conjunto de datos utilizado en esta API contiene información sobre la oferta de entretenimiento más de 45 mil películas. La información incluye títulos, géneros, calificaciones, presupuestos y más.

Para utilizar la API, debe hacer una solicitud HTTP GET a la URL de la API con el endpoint correspondiente.

El servidor proporciona las siguientes funciones:

- peliculas_mes(mes: str): retorna la cantidad de películas que se estrenaron ese mes (ejemplo ‘december’) históricamente.

- peliculas_dia(dia: str): retorna la cantidad de películas que se estrenaron ese día de la semana (ejemplo ‘monday’) históricamente.

- franquicia(franquicia: str): se ingresa el nombre de la franquicia (ejemplo ‘toy story collection) y retorna la cantidad de películas, ganancia total y promedio.

- peliculas_pais(pais: str): se ingresa el código del país (ejemplo ‘ar’ para Argentina o ‘us’ para Estados Unidos) y retorna la cantidad de películas producidas en el mismo.

- productoras(productora: str): se ingresa el nombre de la productora (ejemplo ‘universal pictures’) y retorna la ganancia total y la cantidad de películas que produjeron.

- retorno(pelicula: str): se ingresa el nombre de la película (ejemplo ‘interstellar’) y retorna la inversion, la ganancia, el retorno y el año en el que se lanzó.

- recomendacion(titulo: str): se ingresa el nombre de una película y recomienda las similares en una lista.

El sistema de recomendación solicita el titulo de una película existente dentro de la base de datos existente y devuelve una serie de cinco títulos de películas similares a la proporcionada. Para su funcionamiento se basa en un modelo de k-vecinos entrenado a través de una matriz de características que selecciona los cinco títulos mas cercanos.

El servidor web utiliza varias librerías de Python como pandas, numpy, requests, io, sklearn, scipy, uvicorn y FastAPI. Los conjuntos de datos utilizados se descargan del archivo .csv alojado en este repositorio.

El desarrollo paso a paso de la aplicación se puede ver en el notebook de desarrollo .ipynb de este repositorio.

Links de interés:

- Aplicación de Render: https://pi-01-kp3m.onrender.com
- Video de YouTube: https://youtu.be/zeOxk6R8x5Y

Consultas de ejemplo (una para cada función):

- https://pi-01-kp3m.onrender.com/get_peliculas_mes/november
- https://pi-01-kp3m.onrender.com/get_peliculas_dia/sunday
- https://pi-01-kp3m.onrender.com/get_franquicia/toy%20story%20collection
- https://pi-01-kp3m.onrender.com/get_peliculas_pais/ar
- https://pi-01-kp3m.onrender.com/get_productoras/universal%20pictures
- https://pi-01-kp3m.onrender.com/get_retorno/interstellar
- https://pi-01-kp3m.onrender.com/get_recomendacion/heavy%20metal

Nota: Las funciones admiten palabras en inglés. Para países, introducir el código del país (ejemplo 'ar' para Argentina, 'dk' para Dinamarca).
