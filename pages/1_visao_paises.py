# Bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import re
import haversine
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Países', page_icon='', layout='wide')


# Importacao do DataFrame
df = pd.read_csv('zomato.csv')


# Limpeza e Cópia dos Dados
# Função Preenchimento do nome dos países

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

df['Country'] = df['Country Code'].apply(country_name)


# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

df['Price_Type'] = df['Price range'].apply(create_price_tye)

# Criação do nome das Cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

df['Colors'] = df['Rating color'].apply(color_name)


# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Apenas o registro do indice 0
df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])

# Reordenando as colunas
df = df.reindex(columns=['Restaurant ID', 'Restaurant Name', 'Country Code', 'Country', 'City', 'Address',
       'Locality', 'Locality Verbose', 'Longitude', 'Latitude', 'Cuisines',
       'Average Cost for two', 'Currency', 'Has Table booking',
       'Has Online delivery', 'Is delivering now', 'Switch to order menu',
       'Price range', 'Price_Type', 'Aggregate rating', 'Rating color', 'Colors', 'Rating text',
       'Votes'])

###############################
# Barra Lateral no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

st.header('Visão Países')

image = Image.open('image_delivery.JPG')
st.sidebar.image(image, width=300, caption='Restaurants Delivery')

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""___""")

country_options = st.sidebar.multiselect('Selecione os Países',
                                         ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland','Philippines', 'Qatar',
                                          'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England',
                                          'United States of America'],
                                         default=['India', 'United States of America', 'England', 'South Africa', 'United Arab Emirates',
                                                  'Brazil'])


st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Ricardo Ninomiya')

# Filtro de Países na Barra Lateral
linhas_selecionadas = df['Country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]


###############################
# Layout no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

with st.container():
    cols1 = ['Country', 'Restaurant ID']
    qtd_restaurantes = df.loc[:, cols1].groupby('Country').count().sort_values('Restaurant ID',
                                                                               ascending=False).reset_index()

    qtd_restaurantes = qtd_restaurantes.head(6)

    fig = px.bar(qtd_restaurantes, x='Country', y='Restaurant ID', text_auto=True,
                 title='TOP 6 - Quantidade de Restaurantes registrados por País', color='Country')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    cols2 = ['Country', 'City']
    qtd_city = df.loc[:, cols2].groupby('Country').count().sort_values('City', ascending=False).reset_index()

    qtd_city = qtd_city.head(6)

    fig = px.bar(qtd_city, x='Country', y='City', text_auto=True,
                 title='TOP 6 - Quantidade de Cidades registrados por País', color='Country')

    st.plotly_chart(fig, use_container_width=True)


with st.container():
    cols3 = ['Country', 'Votes']

    mean_votes = df.loc[:, cols3].groupby('Country').mean().sort_values('Votes', ascending=False).reset_index()
    mean_votes = mean_votes.head(6)

    fig = px.bar(mean_votes, x='Country', y='Votes', text_auto=True,
                 title='TOP 6 - Média de Avaliações feitas por País', color='Country'
                 )

    st.plotly_chart(fig, use_container_width=True)


with st.container():
    cols4 = ['Country', 'Average Cost for two']

    mean_average = df.loc[:, cols4].groupby('Country').mean().sort_values('Average Cost for two',
                                                                          ascending=False).reset_index()
    mean_average = mean_average.head(6)

    fig = px.bar(mean_average, x='Country', y='Average Cost for two', text_auto=True,
                 title='TOP 6 - Média de Preço de um prato para duas pessoas por País', color='Country'
                 )
    st.plotly_chart(fig, use_container_width=True)