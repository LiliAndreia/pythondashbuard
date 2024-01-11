import streamlit as st
import pandas as pd
from api.Service import get_data
import folium
from  streamlit_folium import st_folium


st.image('img/IF.png', width=150)
st.title('Cruviana Dashboard')
st.subheader('Estação Meteorológica: UAPP IFPI Oeiras')
dicionario_dados = """
- Datetime: Tempo preciso em que a leitura ocorreu em formato americano.
- id: Identificador único da leitura.
- Data_add: Data em que a leitura ocorreu em formato americano.
- BarTrend: Tendência da pressão para 3h.
- Barometer: Pressão barométrica.
- TempOut: Temperatura do ar em grau em (⁰C).
- WindSpeed: Velocidade do vento em (km/h).
- WindSpeed10Min: Média de velocidade do vento nos últimos 10 minutos em (km/h).
- WindDir: Direção do vento em (⁰).
- HumOut: Umidade relativa do ar em (%).
- RainRate: Volume de chuva por hora (mm).
- SolarRad: Radiação solar em (W/m²).
- RainDay: Volume de chuva acumulado no dia em (mm).
- RainMonth: Volume de chuva acumulado no Mês em (mm).
- RainYear: Volume de chuva acumulado no ano em (mm).
- ETDay: Volume de evapotranspiração acumulado no dia em (mm).
- ETMonth: Volume de evapotranspiração acumulado no mês em (mm).
- ETYear: Volume de evapotranspiração acumulado no ano em (mm).
- RainStorm: Volume de chuva considerada tempestade (mm).
- HeatIndex: Índice de calor em (⁰C).
- WindChill: Sensação térmica considerando vento (⁰C).
- THSWIndex: Sensação térmica considerando umidade, radiação solar, vento e temperatura.
- Station: Identificador da estação meteorológica.
"""
st.subheader('Dicionário de Dados')
st.text(dicionario_dados)

st.write('---')
st.header("Leituras")
data = st.date_input('Data')

def load_data():
    df = pd.DataFrame(get_data(data))

    df = df.drop(columns=['Data_add', 'Data',
                          'WindSpeed', 'WindSpeed10Min',
                          'RainRate', 'ETMonth',
                          'RainStorm', 'Station'])


    df = df.set_index('id')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Datetime'] = df['Datetime'].dt.strftime('%d/%m/%Y %H:%M')

    return df

leituras = load_data()
st.write(leituras)
st.write('---')
st.subheader('Temperatura')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#F00')
st.write(f'Temperatura minima:{leituras.TempOut.min()}ºC')
st.write(f'Temperatura maxima:{leituras.TempOut.max()}ºC')
st.subheader('Umidade')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#003333')
st.write(f'Umidade minima:{leituras.HumOut.min()}º%')
st.write(f'Umidade maxima:{leituras.HumOut.max()}º%')
st.subheader('Radiação_solar')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#00CCCC')
st.write(f'Radiação_solar minima:{leituras.SolarRad.min()}ºW/m²')
st.write(f'Radiação_solar maxima:{leituras.SolarRad.max()}ºW/m²')
st.write('---')
st.subheader('Precipitações')
st.line_chart(data=leituras, x='Datetime', y='RainDay')
st.write(f'Volume total acumulado:{leituras.RainDay.max()} mm')
st.write('---')
st.subheader('Localização')

m = folium.Map (location=[-7.000126399270931, -42.10095318786533],
                zoom_start=20)
folium.Marker(
    [-7.000126399270931, -42.10095318786533],
    popup='Estação meteorologica UAPP - IFPI',
    tooltip='Estação meteorologica UAPP - IFPI',
).add_to(m)

mapa = st_folium(m, width=700)
