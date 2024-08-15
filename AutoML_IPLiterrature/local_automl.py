# import necessary packages
import pandas as pd 
from autogluon.tabular import TabularDataset, TabularPredictor
from autogluon.multimodal import MultiModalPredictor
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor

#import data file

if file.filename.endswith('.csv'):
    train_data = pd.read_csv(file_path)
elif file.filename.endswith(('.xls', '.xlsx')):
    train_data = pd.read_excel(file_path)

label = train_data['col_name']   #user selected col_name
model_path = path ## user input file_path
time_limit = time_limit ## user input file_path

# select autogluon model based on user choice
if user.input == 'Tabular':
    predictor = TabularPredictor(label=label, path=model_path ).fit(train_data, presets="best_quality", time_limit=time_limit)
elif user.input == 'MultiModal':
    predictor = MultiModalPredictor(label=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
elif user.input == 'TimeSeries':
    predictor = TimeSeriesPredictor(target=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)

#if model already trained load the presaved model
saved_model_path = path

#predictor = # load model ckpt

#import data for which model should be used for prediction
if file.filename.endswith('.csv'):
    test_data = pd.read_csv(file_path)
elif file.filename.endswith(('.xls', '.xlsx')):
    test_data = pd.read_excel(file_path)


#predict the value of label
pred_data = predictor.predict(test_data)
confidence = predictor.proba(test_data)




#Imprve the code, also add a react node.js UI code where a user can import data, add model file path and select model for training.

