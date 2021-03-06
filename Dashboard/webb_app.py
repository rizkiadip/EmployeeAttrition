from flask import Flask, render_template, request, send_from_directory, current_app
import pickle
import numpy as np
import pandas as pd


# Import Dataset
df = pd.read_csv('Employee Attrition EDA.csv')

# Initiate Flask
app = Flask(__name__, static_url_path='', 
            static_folder='static'
)

# Home
@app.route('/')
def home():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Dataset
@app.route('/dataset')
def dataset():
    return render_template('dataset.html', table=df)

# Visualization
@app.route('/visualization', methods=['POST', 'GET'])
def visualization():
    return render_template('visualization.html')

# EDA
@app.route('/eda')
def eda():
    return render_template('eda.html')

# Predict
@app.route('/predict', methods=['POST', 'GET'])
def prediction():
    return render_template('predict.html')

# Result
@app.route('/result', methods=['GET','POST'])
def result():
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

        
        df_html = df_predict.copy()
        for i in df_html :
            if i == 'BusinessTravel' :
                df_html[i] = df_html[i].replace({'Non-Travel' : 'Non-Travel', 'Travel_Rarely' : 'Travel Rarely', 'Travel_Frequently' : 'Travel Frequently'})
            elif i == 'Education' :
                df_html[i] = df_html[i].replace({1 : 'Below College', 2 : 'College', 3 : 'Bachelor', 4 : 'Master', 5 : 'Doctor'})
            elif i == 'EnvironmentSatisfaction' :
                df_html[i] = df_html[i].replace({1 : 'Low', 2 : 'Medium', 3 : 'High', 4 : 'Very High'})
            elif i == 'JobInvolvement' :
                df_html[i] = df_html[i].replace({1 : 'Low', 2 : 'Medium', 3 : 'High', 4 : 'Very High'})
            elif i == 'JobLevel' :
                df_html[i] = df_html[i].replace({1 : 'Staff', 2 : 'Officer', 3 : 'Assistant Manager', 4 : 'Manager', 5 : 'Senior Manager'})
            elif i == 'JobSatisfaction' :
                df_html[i] = df_html[i].replace({1 : 'Low', 2 : 'Medium', 3 : 'High', 4 : 'Very High'})
            elif i == 'PerformanceRating' :
                df_html[i] = df_html[i].replace({1 : 'Low', 2 : 'Good', 3 : 'Excellent', 4 : 'Outstanding'})
            elif i == 'RelationshipSatisfaction' :
                df_html[i] = df_html[i].replace({1 : 'Low', 2 : 'Medium', 3 : 'High', 4 : 'Very High'})
            elif i == 'WorkLifeBalance' :
                df_html[i] = df_html[i].replace({1 : 'Bad', 2 : 'Good', 3 : 'Better', 4 : 'Best'})
            else :
                df_html[i] = df_html[i]
        
        return render_template('result.html', data=df_html, pred=result)

# Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    filename = 'Random_Forest.sav'
    model = pickle.load(open(filename,'rb'))

    app.run(port=7777, debug=True)