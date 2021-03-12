from flask import Flask, render_template, request, send_from_directory, current_app
import pickle
import numpy as np
import pandas as pd
import sqlalchemy as db
import plotly
import plotly.graph_objs as go
import json


# Import dataset from csv
# df = pd.read_csv('Employee Attrition EDA.csv')

# Initiate Flask
app = Flask(__name__, static_url_path='', 
            static_folder='static'
)

# Import dataset from database
def sql() :
    engine = db.create_engine(f'mysql+pymysql://root:{12345}@localhost:3306/hr_analysis')
    con = engine.connect()
    meta = db.MetaData()
    df_sql = pd.read_sql('SELECT * FROM attrition', con)
    return df_sql

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
    df = sql()
    return render_template('dataset.html', table=df)

# Visualization
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'Department', cat_y = 'MonthlyIncome',
    estimator = 'count', hue = 'Attrition') :

    attrition = sql()

    if cat_plot == 'histplot' :
        data = []

        for val in attrition[hue].unique() :
            hist = go.Histogram(
                x = attrition[attrition[hue]==val][cat_x],
                y = attrition[attrition[hue]==val][cat_y],
                histfunc = estimator,
                name = val
            )
            data.append(hist)

        title = 'Histogram'
    
    elif cat_plot == 'boxplot' :
        data = []

        for val in attrition[hue].unique() :
            box = go.Box(
                x = attrition[attrition[hue]==val][cat_x],
                y = attrition[attrition[hue]==val][cat_y],
                name = val
            )
            data.append(box)

        title = 'Box'
    
    if cat_plot == 'histplot' and estimator == 'count' :
        layout = go.Layout(
            title = title,
            xaxis = dict(title = cat_x),
            yaxis = dict(title = 'employees'),
            boxmode = 'group'
        )
    else : 
        layout = go.Layout(
            title = title,
            xaxis = dict(title = cat_x),
            yaxis = dict(title = cat_y),
            boxmode='group'
        )
    
    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/visualization')
def visualization():
    plot = category_plot()

    # list dropdown
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Boxplot')]
    list_x = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]
    list_y = [('Age', 'Age'), ('DistanceFromHome', 'Distance From Home'), ('MonthlyIncome', 'Monthly Income'), ('MonthlyRate', 'Monthly Rate'), ('NumCompaniesWorked', 'Number Companies Worked'), ('PercentSalaryHike', 'Percent Salary Hike'), ('TotalWorkingYears', 'Total Working Years'), 
            ('TrainingTimesLastYear', 'Training Times Last Year'), ('YearsAtCompany', 'Years At Company'), ('YearsInCurrentRole', 'Years In Current Role'), ('YearsSinceLastPromotion', 'Years Since Last Promotion'), ('YearsWithCurrManager', 'Years With Curr Manager')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]

    return render_template(
        'category.html',
        plot=plot,
        focus_plot='histplot',
        focus_x = 'Department',
        focus_estimator='count',
        focus_hue='Attrition',
        drop_plot=list_plot,
        drop_x=list_x,
        drop_y=list_y,
        drop_estimator=list_est,
        drop_hue=list_hue
        )

@app.route('/cat_fn')
def cat_fn():

    cat_plot = request.args.get('cat_plot')
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    estimator = request.args.get('estimator')
    hue = request.args.get('hue')

    if cat_plot == None and cat_x == None and cat_y == None and estimator == None and hue == None :
        cat_plot = 'histplot'
        cat_x = 'Department' 
        cat_y = 'MonthlyIncome'
        estimator = 'count' 
        hue = 'Attrition'

    if estimator == None:
        estimator = 'count'

    if cat_y == None:
        cat_y = 'MonthlyIncome'

    # dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Boxplot')]
    list_x = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]
    list_y = [('Age', 'Age'), ('DistanceFromHome', 'Distance From Home'), ('MonthlyIncome', 'Monthly Income'), ('MonthlyRate', 'Monthly Rate'), ('NumCompaniesWorked', 'Number Companies Worked'), ('PercentSalaryHike', 'Percent Salary Hike'), ('TotalWorkingYears', 'Total Working Years'), 
            ('TrainingTimesLastYear', 'Training Times Last Year'), ('YearsAtCompany', 'Years At Company'), ('YearsInCurrentRole', 'Years In Current Role'), ('YearsSinceLastPromotion', 'Years Since Last Promotion'), ('YearsWithCurrManager', 'Years With Curr Manager')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        'category.html',
        plot=plot,
        focus_plot=cat_plot,
        focus_x = cat_x,
        focu_y = cat_y,
        focus_estimator=estimator,
        focus_hue=hue,
        drop_plot=list_plot,
        drop_x=list_x,
        drop_y=list_y,
        drop_estimator=list_est,
        drop_hue=list_hue
        )
            
def scatter_plot(cat_x, cat_y, hue):

    attrition = sql()
    data = []

    for val in attrition[hue].unique():
        scatt = go.Scatter(
            x = attrition[attrition[hue] == val][cat_x],
            y = attrition[attrition[hue] == val][cat_y],
            mode = 'markers',
            name = val
        )
        data.append(scatt)

    layout = go.Layout(
        title = 'Scatter',
        title_x = 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():

    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    if cat_x == None and cat_y == None and hue == None:
        cat_x = 'Age'
        cat_y = 'MonthlyIncome'
        hue = 'Attrition'

    list_x = [('Age', 'Age'), ('DistanceFromHome', 'Distance From Home'), ('MonthlyIncome', 'Monthly Income'), ('MonthlyRate', 'Monthly Rate'), ('NumCompaniesWorked', 'Number Companies Worked'), ('PercentSalaryHike', 'Percent Salary Hike'), ('TotalWorkingYears', 'Total Working Years'), 
            ('TrainingTimesLastYear', 'Training Times Last Year'), ('YearsAtCompany', 'Years At Company'), ('YearsInCurrentRole', 'Years In Current Role'), ('YearsSinceLastPromotion', 'Years Since Last Promotion'), ('YearsWithCurrManager', 'Years With Curr Manager')]
    list_y = [('Age', 'Age'), ('DistanceFromHome', 'Distance From Home'), ('MonthlyIncome', 'Monthly Income'), ('MonthlyRate', 'Monthly Rate'), ('NumCompaniesWorked', 'Number Companies Worked'), ('PercentSalaryHike', 'Percent Salary Hike'), ('TotalWorkingYears', 'Total Working Years'), 
            ('TrainingTimesLastYear', 'Training Times Last Year'), ('YearsAtCompany', 'Years At Company'), ('YearsInCurrentRole', 'Years In Current Role'), ('YearsSinceLastPromotion', 'Years Since Last Promotion'), ('YearsWithCurrManager', 'Years With Curr Manager')]
    list_hue = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot = plot,
        focus_x = cat_x,
        focus_y = cat_y,
        focus_hue = hue,
        drop_x = list_x,
        drop_y = list_y,
        drop_hue = list_hue
    )

def pie_plot(hue = 'Attrition'):

    attrition = sql()
    vcounts = attrition[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])

    data = [
        go.Pie(labels = labels, values = values)
    ]

    layout = go.Layout(title='Pie', title_x=0.5)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'Attrition'

    list_hue = [('Attrition', 'Attrition'), ('BusinessTravel', 'Business Travel'), ('Department', 'Department'), ('Education', 'Education'), ('EducationField', 'Education Field'), ('EnvironmentSatisfaction', 'Environment Satisfaction'),
            ('Gender', 'Gender'), ('JobInvolvement', 'Job Involvement'), ('JobLevel', 'Job Level'), ('JobRole', 'Job Role'), ('JobSatisfaction', 'Job Satisfaction'), ('MaritalStatus', 'Marital Status'), ('OverTime', 'Over Time'),
            ('PerformanceRating', 'Performance Rating'), ('RelationshipSatisfaction', 'Relationship Satisfaction'), ('StockOptionLevel', 'Stock Option Level'), ('WorkLifeBalance', 'Work Life Balance')]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue=list_hue)

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