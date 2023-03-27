import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='')

image = Image.open('image_delivery.JPG')

st.sidebar.image(image, width=150)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Restaurant Delivery')
st.sidebar.markdown("""___""")

st.write('# Fome Zero Dashboard')

st.markdown(
    """
        Fome Zero Dashboard foi construido para acompanhar a Qualidade, Comida e Preços dos Restaurantes ao redor do Mundo.
        ### Como utilizar esses Dashboard?
        - Visão Países:
            - TOP 6 - Quantidade de Restaurantes registrados por País.
            - TOP 6 - Quantidade de Cidades registrados por País.
            - TOP 6 - Média de Avaliações feitas por País.
            - TOP 6 - Média de Preço de um prato para duas pessoas por País
            
        - Visão Cidades:
            - Top 10 Cidades com mais Restaurantes.
            - Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4.
            - Top 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2.5
            - Top 10 Cidades com Restaurante com Tipos de Culinárias distintos.
            
        - Visão Cuisines:
            - Top 10 Restaurantes.
            - Top 10 Melhores Tipos de Culinárias.
            - Top 10 Piores Tipos de Culinárias.
        ### Ask for help
        - Time de Data Science no Discord
            - ricardo_ninomiya#2135

    """

)