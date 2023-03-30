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
from folium.plugins import MarkerCluster

st.set_page_config(page_title='Visão Cuisines', page_icon='', layout='wide')


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

st.header('Visão Cuisines')

image = Image.open('image_delivery.jpg')
st.sidebar.image(image, width=300, caption='Restaurants Delivery')

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""___""")

country_options = st.sidebar.multiselect('Selecione os Países',
                                         ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland','Philippines', 'Qatar',
                                          'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England',
                                          'United States of America'],
                                         default=['India', 'United States of America', 'England', 'South Africa', 'United Arab Emirates',
                                                  'Brazil'])


cuisines_options = st.sidebar.multiselect('Selecione as Cuisines',
                                          ['North Indian', 'Italian', 'European', 'Continental', 'BBQ', 'French',
                                           'Cafe'], default=['North Indian', 'Italian', 'European', 'Continental', 'BBQ', 'French',
                                           'Cafe'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Ricardo Ninomiya')


# Filtro de Países na Barra Lateral
linhas_selecionadas = df['Country'].isin(country_options)
df = df.loc[linhas_selecionadas, :]

# Filtro de Cuisines na Barra Lateral
linhas_selecionadas = df['Cuisines'].isin(cuisines_options)
df = df.loc[linhas_selecionadas, :]


###############################
# Layout no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

with st.container():
    st.header('Top 10 Restaurantes')
    cols1 = ['Restaurant ID', 'Restaurant Name', 'Country', 'Aggregate rating', 'City', 'Cuisines',
             'Average Cost for two', 'Votes']
    linhas = df['Aggregate rating'] > 4

    top10 = df.loc[linhas, cols1].groupby(cols1).mean('Aggregate rating').sort_values(
        ['Aggregate rating', 'Restaurant ID'], ascending=[False, True]).reset_index()
    top10 = top10.head(10)
    st.dataframe(top10)

with st.container():
    col1, col2 = st.columns(2, gap='large')

    with col1:
        cols10 = ['Cuisines', 'Aggregate rating']
        linhas = df['Aggregate rating'] > 4

        top10_max = df.loc[linhas, cols10].groupby('Cuisines').mean('Aggregate rating').sort_values(
            ['Aggregate rating'], ascending=[False]).reset_index()
        top10_max = top10_max.head(10)
        fig = px.bar(top10_max, x='Cuisines', y='Aggregate rating', text_auto=True,
                     title='Top 10 Melhores Tipos de Culinárias', color='Cuisines')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cols10 = ['Cuisines', 'Aggregate rating']
        linhas = (df['Aggregate rating'] < 4) & (df['Cuisines'] != 'nan')

        top10_min = df.loc[linhas, cols10].groupby('Cuisines').mean('Aggregate rating').sort_values(
            ['Aggregate rating'], ascending=[True]).reset_index()
        top10_min = top10_min.head(10)
        fig = px.bar(top10_min, x='Cuisines', y='Aggregate rating', text_auto=True,
                     title='Top 10 Piores Tipos de Culinárias', color='Cuisines')

        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.header('Visão Geográfica dos melhores Restaurantes estão aqui')
    cols = ['City', 'Restaurant ID', 'Latitude', 'Longitude', 'Rating color']
    df_mapa = df.loc[:, cols].groupby('City').median().reset_index()
    map_ = folium.Map(zoom_start=11)

    cluster = MarkerCluster().add_to(map_)

    for index, location_info in df_mapa.iterrows():
        folium.Marker([location_info['Latitude'],
                       location_info['Longitude']],
                      icon=folium.Icon(color='lightgray', icon='home', prefix='fa'),
                      popup=location_info[['City', 'Restaurant ID']]).add_to(cluster)

    folium_static(map_, width=1024, height=600)
    # folium_static(map_)




