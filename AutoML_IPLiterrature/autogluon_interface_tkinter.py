import os
import pandas as pd
from tkinter import filedialog, Tk, Button, Label, OptionMenu, StringVar, Entry, Checkbutton
from autogluon.tabular import TabularPredictor
from autogluon.multimodal import MultiModalPredictor
from autogluon.timeseries import TimeSeriesPredictor
import threading
import time

# Define variables to store training and test data
train_data = None
test_data = None

# Define the predictor variable
predictor = None

def import_data():
    global train_data
    file_path = filedialog.askopenfilename()  # Open a file dialog for user to select the data file
    if file_path.endswith('.csv'):
        train_data = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        train_data = pd.read_excel(file_path)
    # Further code for handling data or displaying feedback to the user can be added here

def train_model():
    global predictor
    selected_model = model_var.get()
    label = label_var.get()
    model_path = model_path_entry.get()
    time_limit_text = time_limit_entry.get()
    time_limit = convert_to_seconds(time_limit_text) # Convert the time limit text to seconds

    # Train the selected AutoGluon model based on user choice
    if selected_model == 'Tabular':
        predictor = TabularPredictor(label=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
    elif selected_model == 'MultiModal':
        predictor = MultiModalPredictor(label=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
    elif selected_model == 'TimeSeries':
        predictor = TimeSeriesPredictor(target=label, path=model_path).fit(train_data, presets="best_quality", time_limit=time_limit)
    # Further code for handling model training or displaying feedback to the user can be added here

def import_test_data():
    global test_data
    test_file_path = filedialog.askopenfilename()  # Open a file dialog for user to select the test data file
    if test_file_path.endswith('.csv'):
        test_data = pd.read_csv(test_file_path)
    elif test_file_path.endswith(('.xls', '.xlsx')):
        test_data = pd.read_excel(test_file_path)
    # Further code for handling test data or displaying feedback to the user can be added here

def select_model_path():
    folder_selected = filedialog.askdirectory()  # Open a dialog to select a folder
    model_path_entry.delete(0, 'end')  # Clear the entry field
    model_path_entry.insert(0, folder_selected)

def load_model_path():
    model_file_path = filedialog.askopenfilename()  # Open a file dialog for user to select the model file
    if model_file_path:
        model_path_entry.delete(0, 'end')  # Clear the entry field
        model_path_entry.insert(0, model_file_path)

def convert_to_seconds(time_limit_text):
    time_values = {
        'minutes': 60,
        'hour': 3600,
        'hours': 3600
    }

    value, unit = time_limit_text.split()
    value = int(value)

    return value * time_values.get(unit, 1)

def predict():
    def perform_prediction():
        global predictor, test_data
        # Display "Computing" text and spinner
        computing_label.config(text="Computing")
        spinner.pack()

        if use_last_model.get() == "Yes":
            # Use last trained model for prediction
            if predictor is None:
                # Display an error or prompt the user to train a model first
                pass
            else:
                # Predict label column for test data
                pred_data = predictor.predict(test_data)
                confidence = predictor.predict_proba(test_data)

                # Store predicted data in test_data DataFrame
                test_data['predicted_label'] = pred_data

                # Save predicted data as a CSV file in the same directory as the test data
                save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if save_path:
                    # test_data.to_csv(save_path, index=False)
                    # Further code for handling successful saving or display feedback to the user

                    if confidence is not None:
                        max_confidence = confidence.apply(lambda row: row.max(), axis=1)
                        test_data['confidence'] = max_confidence
                        # confidence_save_path = os.path.splitext(save_path)[0] + "_confidence.csv"
                    test_data.to_csv(save_path, index=False)
                        # Further code for handling successful saving of confidence or display feedback to the user

        else:
            # Use a new model selected by the user for prediction
            selected_model_path = model_path_entry.get()
            if selected_model_path == '':
                # Display an error or prompt the user to select a model
                pass
            else:
                selected_model = model_var.get()
                label = label_var.get()
                if selected_model == 'Tabular':
                    predictor = TabularPredictor.load(selected_model_path)
                elif selected_model == 'MultiModal':
                    predictor = MultiModalPredictor.load(selected_model_path)
                elif selected_model == 'TimeSeries':
                    predictor = TimeSeriesPredictor.load(selected_model_path)

                # Predict label column for test data
                pred_data = predictor.predict(test_data)
                confidence = predictor.predict_proba(test_data)

                # Store predicted data in test_data DataFrame
                test_data['predicted_label'] = pred_data

                # Save predicted data as a CSV file in the same directory as the test data
                save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if save_path:
                    # test_data.to_csv(save_path, index=False)
                    # Further code for handling successful saving or display feedback to the user

                    if confidence is not None:
                        max_confidence = confidence.apply(lambda row: row.max(), axis=1)
                        test_data['confidence'] = max_confidence
                        # confidence_save_path = os.path.splitext(save_path)[0] + "_confidence.csv"
                    test_data.to_csv(save_path, index=False)
                        # Further code for handling successful saving of confidence or display feedback to the user

    # Hide the spinner and "Computing" text after computations are done
    spinner.pack_forget()
    computing_label.config(text="")


    # Start a new thread for performing the prediction
    prediction_thread = threading.Thread(target=perform_prediction)
    prediction_thread.start()

# Create the basic UI
root = Tk()
root.title("AutoGluon Model Trainer")

# Label for importing training data
import_data_label = Label(root, text="Import Training Data")
import_data_label.pack()

# Import training data button (assumes import_data() function handles importing)
import_data_button = Button(root, text="Browse", command=import_data)
import_data_button.pack()

# Label for model selection
model_selection_label = Label(root, text="Model Selection")
model_selection_label.pack()

# Model selection dropdown
models = ['Tabular', 'MultiModal', 'TimeSeries']
model_var = StringVar(root)
model_var.set(models[0])  # Default model selection
model_dropdown = OptionMenu(root, model_var, *models)
model_dropdown.pack()

# Label for label selection
label_selection_label = Label(root, text="Label Selection")
label_selection_label.pack()

# Entry for label selection
label_var = StringVar()
label_entry = Entry(root, textvariable=label_var)
label_entry.pack()
label_entry.insert(0, "Enter Label Column Name")

# Label for model file path selection
model_file_label = Label(root, text="Select Model File")
model_file_label.pack()

# Entry for model file path
model_path_entry = Entry(root)
model_path_entry.pack()
# model_path_entry.insert(0, "Select Model Folder")

# Button to browse and select folder to save model
browse_button = Button(root, text="Browse", command=select_model_path)
browse_button.pack()

# Label for time limit entry
time_limit_label = Label(root, text="Time Limit")
time_limit_label.pack()

# Dropdown for time limit
time_limit_entry = StringVar(root)
time_limit_entry.set("5 minutes")  # Default time limit

time_limit_options = ["5 minutes", "10 minutes", "30 minutes", "1 hour", "3 hours"]
time_limit_dropdown = OptionMenu(root, time_limit_entry, *time_limit_options)
time_limit_dropdown.pack()

# Train model button (assumes train_model() function handles model training)
train_model_button = Button(root, text="Train Model", command=train_model)
train_model_button.pack()

# Label for importing test data
import_test_data_label = Label(root, text="Import Test Data")
import_test_data_label.pack()

# Import test data button (assumes import_test_data() function handles importing test data)
import_test_data_button = Button(root, text="Browse", command=import_test_data)
import_test_data_button.pack()

# Checkbox to use the last trained model for testing
use_last_model = StringVar()
use_last_model_checkbox = Checkbutton(root, text="Use Last Trained Model", variable=use_last_model, onvalue="Yes", offvalue="No")
use_last_model_checkbox.pack()

# Button to load a test model path when 'Use Last Trained Model' is unchecked
load_model_button = Button(root, text="Load Model Path", command=select_model_path)

# Predict button
predict_button = Button(root, text="Predict", command=predict)

def check_use_last_model():
    if use_last_model.get() == "Yes":
        load_model_button.pack_forget()  # Hide the button if the checkbox is checked
        predict_button.pack()  # Show the Predict button
    else:
        load_model_button.pack()  # Show the Load Model Path button
        predict_button.pack_forget()  # Hide the Predict button if the checkbox is unchecked

# Keep checking the checkbox status and show/hide the buttons accordingly
root.after(100, check_use_last_model)

# Label and spinner for "Computing"
computing_label = Label(root)
computing_label.pack()

spinner = Label(root, text="Computing...")
# Further configuration for spinner (e.g., using an actual spinner widget) can be added here

# Pack the buttons initially
load_model_button.pack()
predict_button.pack()

root.mainloop()