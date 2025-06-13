import pandas as pd

dataframe = pd.read_csv('houseprices.csv')
colums_order = [
    'Month',
    'GeoEntityName',
    'GeoCode',
    'GeoName',
    'AveragePrice',
    'AveragePriceDetached',
    'AveragePriceSemiDetached',
    'AveragePriceTerraced',
    'AveragePriceFlatOrMaisonette'
]

edit_dataframe = dataframe[colums_order].copy()
edit_dataframe['Month'] = edit_dataframe['Month'].str[5:7]
edit_dataframe['Month'] = edit_dataframe['Month'].astype(int)
edit_dataframe['GeoCode'] = edit_dataframe['GeoCode'].str.replace('[^0-9]', '', regex=True)
edit_dataframe['GeoCode'] = edit_dataframe['GeoCode'].astype(int)
name_code_map = edit_dataframe.set_index('GeoName')['GeoCode'].to_dict()
geo_entity_map = edit_dataframe.set_index('GeoName')['GeoEntityName'].to_dict()
geo_entity_number = { 'County': 0, 'District Council': 1}
edit_dataframe.sort_values(by=['Month', 'GeoEntityName'], inplace=True)
edit_dataframe.to_csv('new_houseprices.csv', index=False)
edit_dataframe['GeoEntityName'] = edit_dataframe['GeoEntityName'].apply(lambda x: 0 if x == 'County' else 1)
edit_dataframe.drop(['GeoName'], axis=1, inplace=True)