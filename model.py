from decimal import *
from catboost import CatBoostRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import data_analysis

features = ['Month', 'GeoEntityName', 'GeoCode']
targets = [
    'AveragePrice',
    'AveragePriceDetached',
    'AveragePriceSemiDetached',
    'AveragePriceTerraced',
    'AveragePriceFlatOrMaisonette'
]

X = data_analysis.edit_dataframe[features].values
Y = data_analysis.edit_dataframe[targets].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.3, random_state=42)

models = {}
predictions = {}

def initModel():
    for i, target in enumerate(targets):
       model = CatBoostRegressor(iterations=700, learning_rate=0.2, depth=1, verbose=False)
       model.fit(X_train, Y_train[:, i])
       models[target] = model

def predictPrice(selected_data):
    selected_data_scaled = scaler.fit_transform(selected_data)
    for target in targets:
       pred = models[target].predict(selected_data_scaled)
       predictions[target] = [Decimal(num).quantize(Decimal("1")) for num in pred]