from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import sys
import os

# Ensure src is in path


from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Prediction route
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method == "GET":
            return render_template('home.html')

        # Collect form data safely
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score', 0)),
            writing_score=float(request.form.get('writing_score', 0))
        )

        pred_df = data.get_data_as_data_frame()
        print("Input Data:\n", pred_df)

        # Prediction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results=round(results[0], 2))

    except Exception as e:
        print("Error:", e)
        return render_template('home.html', results="Error occurred. Check input!")


if __name__ == "__main__":
    application.run(debug=True, host="127.0.0.1", port=5000, use_reloader=True)