import streamlit as st
import pandas as pd
import data_analysis
import model

st.set_page_config(page_title="Lincolnshire (UK) House Prices", layout="wide", initial_sidebar_state="auto")
st.sidebar.header('Фильтры для визуализации датасета')

st.markdown("<h1 style='text-align: center;'>Lincolnshire (UK) House Prices", unsafe_allow_html=True)
info_table, prediction_table = st.tabs(["Датафрейм", "Предсказание"])

dataframe = pd.read_csv('new_houseprices.csv')
months = st.sidebar.select_slider(label="Выберите какие месяца отобразить", options=sorted(dataframe['Month'].unique()), value=(dataframe['Month'].min(), dataframe['Month'].max()))
geo_name = st.sidebar.multiselect(label="Выберите какие регионы отобразить", options=sorted(dataframe['GeoName'].unique()), default=sorted(dataframe['GeoName'].unique()))
price_type = st.sidebar.multiselect(label="Выберите какие средние цены отобразить", options=model.targets, default=model.targets)

model.initModel()

with info_table:
    st.markdown("<h4 style='text-align: center;'>Датасет, содержащий информацию по месяцу, расположению и средним ценам для каждого типа домов", unsafe_allow_html=True)
    updated_dataframe = (dataframe.loc[
        (dataframe['Month'].between(months[0], months[1])) &
        (dataframe['GeoName'].isin(geo_name)),
        ['Month', 'GeoEntityName', 'GeoName'] + price_type
    ])
    st.dataframe(updated_dataframe)

with prediction_table:
    st.markdown("<h4 style='text-align: center;'>Предсказание цен для выбранного месяца, локации и типа жилья", unsafe_allow_html=True)
    prediction_dataframe = (dataframe.loc[
        (dataframe['Month'].between(months[0], months[1])) &
        (dataframe['GeoName'].isin(geo_name)),
        ['Month', 'GeoEntityName', 'GeoName']
    ])

    prepared_data = []
    range_months = range(months[0], months[1]+1)

    for cur_month in range_months:
        for name in geo_name:
            entity_name = data_analysis.geo_entity_map.get(name)
            entity_name_num = data_analysis.geo_entity_number.get(entity_name)
            name_code = data_analysis.name_code_map.get(name)
            prepared_data.append([cur_month, entity_name_num, name_code])

    model.predictPrice(prepared_data)
    for cur_target in price_type:
        prediction_dataframe[cur_target] = model.predictions[cur_target]
    st.dataframe(prediction_dataframe)