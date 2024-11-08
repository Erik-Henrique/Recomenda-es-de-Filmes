import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(layout='wide',
                   page_title = 'Recomendações de Filmes'
)

st.write('# Olá, seja bem vindo ao nosso sistema de recomendação de filmes')
st.write('### Estamos aqui para ajudar você a escolher um filme com base em outro que tenha visto e gostado.')

filmes = pd.read_csv('https://raw.githubusercontent.com/Erik-Henrique/Recomendacoes_de_Filmes/refs/heads/main/Filmes.csv')

rating = pd.read_csv('https://raw.githubusercontent.com/Erik-Henrique/Recomendacoes_de_Filmes/refs/heads/main/Ratings.csv', sep=';')

df = filmes.merge(rating, on='movieId')
filmes_amostra = df.drop(['movieId','userId','rating'], axis=1).drop_duplicates().reset_index(drop=True)
filmes_amostra.rename(columns={"title": "Título                                                            ", "genres": "Gênero                                                                                                                                        ",
                                "year":"Ano de Lançamento        "}, inplace=True)

col1, col2 = st.columns(2)
with col1:
    st.dataframe(filmes_amostra)
with col2:
    st.write('#### Ao lado, você pode analisar todos os filmes disponíveis para os quais podemos gerar uma recomendação. Escolha um filme, digite o título abaixo, e informaremos outros 5 filmes com seu respectivo nível de similaridade, que varia de 0 a 1 – sendo 0 nada parecido e 1 muito parecido.')

df.title = df.title.str.upper()

df_pivot = df.pivot_table(index='title', columns='userId', values='rating').fillna(0)

cos = cosine_similarity(df_pivot)
df_cos = pd.DataFrame(cos, index=df_pivot.index, columns=df_pivot.index)

filme_select = st.text_input(label='Digite aqui o filme que gostaria de dar como exemplo')
filme_select = filme_select.upper()


recomendacao = df_cos.loc[filme_select].sort_values(ascending=False)[1:6]
recomendacao.index.name = 'Recomendação'
recomendacao.name = 'Nível de similaridade'

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.dataframe(recomendacao)
with col2:
    st.write('##### Estes são os filmes indicados para você assistir. Divirta-se.')
