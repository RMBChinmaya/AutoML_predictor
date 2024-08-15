from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from autogluon.tabular import TabularPredictor
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER

# Function to create folders if they don't exist
def create_folders():
    for folder in [UPLOAD_FOLDER, MODEL_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    try:
        create_folders()

        # Get uploaded file
        file = request.files['file']
        if file:
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Load data using pandas
            if file.filename.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file.filename.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file_path)
            else:
                return jsonify({'success': False, 'message': 'Unsupported file format!'})

            target_column = request.form['target']
            supported_columns = request.form.getlist('supported_columns')

            # Additional processing and AutoGluon training can go here
            # ...

            # Example: Train AutoGluon
            predictor = TabularPredictor(label=target_column, path=app.config['MODEL_FOLDER']).fit(data)

            return jsonify({'success': True, 'message': 'Upload and training successful!'})
        else:
            return jsonify({'success': False, 'message': 'No file uploaded!'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
