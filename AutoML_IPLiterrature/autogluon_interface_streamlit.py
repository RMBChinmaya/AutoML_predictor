import os
import pandas as pd
import streamlit as st
from autogluon.tabular import TabularPredictor
from autogluon.multimodal import MultiModalPredictor
from autogluon.timeseries import TimeSeriesPredictor

# Define variables to store training and test data
train_data = None
test_data = None
predictor = None

# Function to import training data
def import_data():
    global train_data
    file_path = st.file_uploader("Import Training Data", type=['csv', 'xls', 'xlsx'])
    if file_path is not None:
        train_data = pd.read_csv(file_path) if file_path.name.endswith('.csv') else pd.read_excel(file_path)

# Function to train model
def train_model():
    global predictor, train_data
    selected_model = st.selectbox("Model Selection", ('Tabular', 'MultiModal', 'TimeSeries'))
    label = st.text_input("Label Selection:", "Enter Label Column Name")
    model_path = st.text_input("Paste Folder path to save Model:")
    time_limit_text = st.selectbox("Time Limit", ["5 minutes", "10 minutes", "30 minutes", "1 hour", "3 hours"])
    time_limit = convert_to_seconds(time_limit_text)
    if not model_path:
        st.error("Error: Please provide a valid folder path.")
        return

    # Ensure the directory exists or create it
    if not os.path.exists(model_path):
        try:
            os.makedirs(model_path)
        except OSError as e:
            st.error(f"Error: {e}")
            return

    # Train the selected AutoGluon model based on user choice
    if selected_model == 'Tabular':
        predictor = TabularPredictor(label=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
    elif selected_model == 'MultiModal':
        predictor = MultiModalPredictor(label=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
    elif selected_model == 'TimeSeries':
        predictor = TimeSeriesPredictor(target=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)

# Function to import test data
def import_test_data():
    global test_data, file_path_test
    file_path_test = st.file_uploader("Import Test Data", type=['csv', 'xls', 'xlsx'])
    if file_path_test is not None:
        test_data = pd.read_csv(file_path_test) if file_path_test.name.endswith('.csv') else pd.read_excel(file_path_test)

def convert_to_seconds(time_limit_text):
    time_values = {
        'minutes': 60,
        'hour': 3600,
        'hours': 3600
    }

# Function to perform prediction
def predict():
    global predictor, test_data
    use_last_model = st.checkbox("Use Last Trained Model")
    if use_last_model:
        if predictor is None:
            st.error("Error: No model available. Please train a model first.")
        else:
            pred_data = predictor.predict(test_data)
            confidence = predictor.predict_proba(test_data)

            # Further code for handling prediction results or displaying feedback to the user

    else:
        selected_model_path = st.text_input("Paste Folder path for model to be used:")
        if not selected_model_path:
            st.error("Error: Please select a model.")
        else:
            selected_model = st.selectbox("Type of Model:", ('Tabular_M', 'MultiModal_M', 'TimeSeries_M'))
            #label = st.text_input("Label Selection", "Enter Label Column Name")

            # Load model based on user choice
            if selected_model == 'Tabular_M':
                predictor = TabularPredictor.load(selected_model_path)
            elif selected_model == 'MultiModal_M':
                predictor = MultiModalPredictor.load(selected_model_path)
            elif selected_model == 'TimeSeries_M':
                predictor = TimeSeriesPredictor.load(selected_model_path)

            pred_data = predictor.predict(test_data)
            test_data['predicted_label'] = pred_data
            confidence = predictor.predict_proba(test_data)
            if confidence is not None:
                max_confidence = confidence.apply(lambda row: row.max(), axis=1)
                test_data['confidence'] = max_confidence

            # Further code for handling prediction results or displaying feedback to the user
    output_file_name = st.text_input("Enter Output filename:")
    if st.button("Save Predictions"):
        if output_file_name.endswith('.csv'):
            test_data.to_csv(os.path.join(os.path.dirname(file_path_test.name), output_file_name), index=False)
            st.success(f"Predictions saved to {output_file_name}.")
        else:
            st.error("Error: Please provide a valid CSV file name.")

# Streamlit UI components
st.title("AutoGluon Model Trainer")

# Import training data
import_data()

# Train model
train_model()

# Import test data
import_test_data()

# Perform prediction
predict()