import pandas as pd
import collections
import numpy as np
import matplotlib.pyplot as plt


applicants = pd.read_csv("data/applicants_cleans.csv")
del applicants['userid']

plt.style.use('fivethirtyeight')


Medicine_Public_Health = ['Public Health','Molecular & Cellular Medicine']

Social_Sciences_Liberal_Arts = ['Sociology', 'English','International Studies', 'Political Science',
                              'International Affairs', 'Economics']

Business = ['Marketing','Accounting', 'Agricultural Economics','Business', 'Finance']

Science = ['Genetics', 'Oceanography','Entomology', 'Soil and Crop Sciences',
          'Geoscience', 'Geography', 'Neuroscience', 'Biochemistry and Biophysics',
           'Geology', 'Ecosystem Science and Management', 'Atmospheric Sciences',
           'Physics', 'Astronomy', 'Biology', 'Chemistry', 'Biomedical Sciences', 'Material Science',
           'Plant Pathology and Microbiology']

Engineering = ['Biological and Agricultural Engineering', 'Engineering Technology & Industrial Distribution',
              'Architecture', 'Construction Science', 'Civil Engineering', 'Electronic Systems Engineering',
               'Petroleum Engineering', 'Chemical Engineering', 'Ocean Engineering','Nuclear Engineering',
               'Aerospace Engineering', 'Mechanical Engineering','Computer Science & Engineering',
               'Biomedical Engineering','Industrial and/or Systems Engineering', 'Electrical Engineering']

Education = ['Educational Administration & Human Resource Development']

Psychology = ['Educational Psychology', 'Psychology']

Math = ['Mathematics','Applied Mathematics','Statistics']

Data_Science = ['Information Science','Information and Operations Management','Analytics',
                'Data Science & Analytics','Management Information Systems']

Other = ['Other', 'Agronomy', 'Landscape Architecture & Urban Planning','Visualization']


major_categories = [Medicine_Public_Health, Social_Sciences_Liberal_Arts, Business,
                   Science, Engineering, Education, Psychology, Math, Data_Science, Other]


#-------------------------------------------------------------------------------
# Ages
#-------------------------------------------------------------------------------

def plot_ages(user_age=1):  #this represents input on the user's data
    age_counts = applicants['age_bin'].value_counts().to_dict()

    #re-ordering dictionary by keys, so that youngest age group goes on bottom, oldest on top
    age_counts = collections.OrderedDict(sorted(age_counts.items()))

    keys = list(age_counts.keys())
    values = list(age_counts.values())


    for n, i in enumerate(keys):
        if i == 0:
            keys[n] = "15-18"

    for n, i in enumerate(keys):
        if i == 1:
            keys[n] = "18-20"

    for n, i in enumerate(keys):
        if i == 2:
            keys[n] = "20-22"

    for n, i in enumerate(keys):
        if i == 3:
            keys[n] = "22-25"

    for n, i in enumerate(keys):
        if i == 4:
            keys[n] = "25-30"

    for n, i in enumerate(keys):
        if i == 5:
            keys[n] = "30-50"

    fig, ax = plt.subplots()

    bars = plt.barh(keys, values, align='center', color = '#4455C2')

    bars[user_age].set_color('#00FF8C')

    bars = plt.title('Number of Applicants by Age Group', color = 'black')

    return fig


#-------------------------------------------------------------------------------
# Education
#-------------------------------------------------------------------------------

def plot_education(user_edu=0):  # 0 = undergrad, 1 = masters, 2 = phd
    edu_df = applicants[['undergrad','Masters','PhD']]

    edu_categories = ['Undergrad', 'Masters', 'PhD']
    edu_sums = []

    columns = list(edu_df)

    for column in columns:
        total = edu_df[column].sum()
        edu_sums.append(total)

    fig, ax = plt.subplots()

    bars = plt.barh(edu_categories, edu_sums, align='center', color = '#4455C2')

    bars[user_edu].set_color('#00FF8C')

    bars = plt.title('Number of Applicants by Education', color = 'black')

    return fig


#-------------------------------------------------------------------------------
# Skills
#-------------------------------------------------------------------------------

def plot_skills(user_skills=1):
    skills_df = applicants[['Excel','Python','Tableau','Pandas',
                            'NumPy','MATLAB','Pytorch',
                            'Scikit-learn','full_stack','TensorFlow',
                            'R','SQL','dev_ops','Keras','cloud']]

    columns = list(skills_df)
    skills_sums = []

    for column in columns:
        total = skills_df[column].sum()
        skills_sums.append(total)

    fig, ax = plt.subplots()

    bars = plt.barh(columns, skills_sums, align='center', color='#4455C2')

    if isinstance(user_skills, list):
        for skill in user_skills:
            bars[skill].set_color('#00FF8C')
    else:
        bars[user_skills].set_color('#00FF8C')

    bars = plt.title('Data Science Skills', color = 'black')

    return fig


#-------------------------------------------------------------------------------
# Majors
#-------------------------------------------------------------------------------

def plot_majors(user_majors=7):
    subset_totals = []
    for category in major_categories:
        subset_total = 0
        subset = applicants[category]
        subset_columns = list(subset)
        for column in subset_columns:
            column_total = subset[column].sum()
            subset_total += column_total
        subset_totals.append(subset_total)

    total_applicants = sum(subset_totals)

    labels = ['Medicine', 'Social Science/Lib. Arts', 'Business', 'Science',
            'Engineering', 'Education', 'Psychology', 'Math', 'Data Science', 'Other']

    #this represents input on the user's data
    user_maj = 2

    fig, ax = plt.subplots()

    bars = plt.barh(labels, subset_totals, align='center', color='#4455C2', alpha=0.8)

    if isinstance(user_majors, list):
        for major in user_majors:
            bars[major].set_color('#00FF8C')
    else:
        bars[user_majors].set_color('#00FF8C')

    bar = plt.title('Applicants by Major', color='black')

    return fig
