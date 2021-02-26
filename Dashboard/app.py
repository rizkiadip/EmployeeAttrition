# Importing Libraries 
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Import Dataset
df = pd.read_csv('Employee Train Data.csv')

# Initiate Flask
app = Flask(__name__)

# Root
@app.route('/')
def route_root():
    return render_template('home.html')

# Homepage
@app.route('/home')
def route_home():
    return render_template('home.html')

# Dataset
@app.route('/dataset')
def route_dataset():
    return render_template('dataset.html', data=df)
    

# Visualization
@app.route('/visualization')
def route_visualization():
    return render_template('visualization.html')

# Prediction
@app.route('/predict', methods = ['GET'])
def route_predict():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def route_result():
    if request.method == 'POST':
        input = request.form

        df_predict = pd.DataFrame({
            'Age' : [int(input['Age'])],
            'BusinessTravel' : [input['BusinessTravel']],
            'Department' : [input['Department']],
            'DistanceFromHome' : [int(input['DistanceFromHome'])], 
            'Education' : [int(input['Education'])],
            'EducationField' : [input['EducationField']],
            'EnvironmentSatisfaction' : [int(input['EnvironmentSatisfaction'])],
            'Gender' : [input['Gender']],
            'JobInvolvement' : [int(input['JobInvolvement'])],
            'JobLevel' : [int(input['JobLevel'])],
            'JobRole' : [input['JobRole']],
            'JobSatisfaction' : [int(input['JobSatisfaction'])], 
            'MaritalStatus' : [input['MaritalStatus']],
            'MonthlyIncome' : [int(input['MonthlyIncome'])],
            'MonthlyRate' : [int(input['MonthlyRate'])],
            'NumCompaniesWorked' : [int(input['NumCompaniesWorked'])],
            'OverTime' : [input['OverTime']],
            'PercentSalaryHike' : [int(input['PercentSalaryHike'])],
            'PerformanceRating' : [int(input['PerformanceRating'])],
            'RelationshipSatisfaction' : [int(input['RelationshipSatisfaction'])],
            'StockOptionLevel' : [int(input['StockOptionLevel'])],
            'TotalWorkingYears' : [int(input['TotalWorkingYears'])],
            'TrainingTimesLastYear' : [int(input['TrainingTimesLastYear'])],
            'WorkLifeBalance' : [int(input['WorkLifeBalance'])],
            'YearsAtCompany' : [int(input['YearsAtCompany'])],
            'YearsInCurrentRole' : [int(input['YearsInCurrentRole'])],
            'YearsSinceLastPromotion' : [int(input['YearsSinceLastPromotion'])],
            'YearsWithCurrManager' : [int(input['YearsWithCurrManager'])],
        })

        prediksi = model.predict_proba(df_predict)[:,1]

        threshold = 0.42
        if prediksi > threshold :
            result = 'Employee might Leave'
        else:
            result = 'Employee might Stay'
        
        return render_template('predict.html', results = result)

if __name__ == "__main__":
    filename = 'Random_Forest.sav'
    model = pickle.load(open(filename,'rb'))
    
    app.run(debug = True)