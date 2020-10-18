import streamlit as st
import pandas as pd

from similar_users import get_similarity_by_category


applicants = pd.read_csv('data/applicants.csv')

_school = sorted(list(set(applicants['school'])))

_other_school = list(set(applicants['other_school']))
_other_school = _other_school[1:]  # The first element is `nan`, remove it
_other_school = ['None'] + sorted(_other_school)

_education_levels = ['Undergraduate', 'Masters', 'PhD']

_majors = sorted([
    'Landscape Architecture & Urban Planning',
    'Plant Pathology and Microbiology',
    'Electrical Engineering',
    'Material Science',
    'Mechanical Engineering',
    'Computer Science & Engineering',
    'Biomedical Engineering',
    'Industrial and/or Systems Engineering',
    'Economics',
    'Finance',
    'Applied Mathematics',
    'Statistics',
    'Management Information Systems',
    'Aerospace Engineering',
    'Nuclear Engineering',
    'Psychology',
    'Other',
    'Biomedical Sciences',
    'Chemistry',
    'Ocean Engineering',
    'Data Science & Analytics',
    'Biology',
    'Chemical Engineering',
    'Mathematics',
    'Petroleum Engineering',
    'Astronomy,Physics',
    'Electronic Systems Engineering',
    'Agronomy',
    'Atmospheric Sciences',
    'Civil Engineering',
    'Ecosystem Science and Management',
    'Geology',
    'Business',
    'Biochemistry and Biophysics',
    'Analytics',
    'Construction Science',
    'Neuroscience',
    'Architecture',
    'Agricultural Economics',
    'Geography',
    'International Affairs',
    'Political Science',
    'Engineering Technology & Industrial Distribution',
    'Geoscience',
    'Accounting',
    'Information and Operations Management',
    'Information Science',
    'Molecular & Cellular Medicine',
    'International Studies',
    'English',
    'Educational Administration & Human Resource Development',
    'Soil and Crop Sciences',
    'Visualization',
    'Biological and Agricultural Engineering',
    'Entomology',
    'Oceanography',
    'Genetics',
    'Sociology',
    'Public Health',
    'Marketing',
    'Educational Psychology'
])

_minors = sorted([
    'Hispanic Studies',
    'History',
    'Philosophy',
    'Communications',
    'Teaching',
    'Learning & Culture',
    'Environmental Law',
    'Anthropology',
    'Public Service and Administration'
])

_technological_skills = sorted([
    'Excel', 'Python', 'Tableau', 'Pandas', 'NumPy',
    'MATLAB', 'Pytorch', 'Scikit-learn', 'full_stack',
    'TensorFlow', 'R', 'SQL', 'dev_ops', 'Keras', 'cloud'
])

_relevant_industries = sorted([
    'consulting', 'public_policy', 'other', 'technology', 'education',
    'healthcare', 'insurance', 'finance', 'aerospace', 'transportation',
    'sports', 'retail', 'energy',
])


#-------------------------------------------------------------------------------
# Generate input widgets
#-------------------------------------------------------------------------------

st.sidebar.header('Your Personal Info')

backgrounds = {
    'school':           st.sidebar.selectbox('School', _school),
    'classification':   st.sidebar.selectbox('Education level', _education_levels),
    'majors':           st.sidebar.multiselect('Majors', _majors),
    'minors':           st.sidebar.multiselect('Minors', _minors),
    'first_generation': st.sidebar.radio('Are you a first generation college student?', ['Yes', 'No']),
    'age':              st.sidebar.slider('Age', min_value=15, max_value=50, step=1)
}

experience = {
    'datascience_experience':  st.sidebar.select_slider('Experience in data science (0 = none, 3 = very rich)', ['0', '1', '2', '3']),
    'num_hackathons_attended': st.sidebar.select_slider('Number of hackathons attended', ['0', '1', '2', '3', '>3'])
}

skills = {
    'technology_experience': st.sidebar.multiselect('Your technological skills', _technological_skills),
    'relavent_industries':   st.sidebar.multiselect('Your relevant industries', _relevant_industries)
}

self_description = st.sidebar.text_area('Self-description')

st.sidebar.header('Your Matching Preferences')
st.sidebar.subheader('Personal background')

backgrounds_pref = {
    'similarity': st.sidebar.radio(
        label='I\'m looking for people...',
        options=['similar with me', 'different from me'],
        key="backgrounds.similarity"
    ),
    'importance': st.sidebar.select_slider(
        label='Importance to me (1 = least, 5 = most)',
        options=['1', '2', '3', '4', '5'],
        key="backgrounds.importance"
    )
}

st.sidebar.subheader('Level of experience')

experience_pref = {
    'similarity': st.sidebar.radio(
        label='I\'m looking for people...',
        options=['similar with me', 'different from me'],
        key="experience.similarity"
    ),
    'importance': st.sidebar.select_slider(
        label='Importance to me (1 = least, 5 = most)',
        options=['1', '2', '3', '4', '5'],
        key="experience.importance"
    )
}

st.sidebar.subheader('Skills & industries')

skills_pref = {
    'similarity': st.sidebar.radio(
        label='I\'m looking for people...',
        options=['similar with me', 'different from me'],
        key="skills.similarity"
    ),
    'importance': st.sidebar.select_slider(
        label='Importance to me (1 = least, 5 = most)',
        options=['1', '2', '3', '4', '5'],
        key="skills.importance"
    )
}

search_btn = st.sidebar.button('Search users')
recommend_btn = st.sidebar.button('Get recommendations')
discord_btn = st.sidebar.button('Match with Discord users')
visual_btn = st.sidebar.button('Visualize where you fit in')


#-------------------------------------------------------------------------------
# Parse data into a dictionary with the same format as applicants.csv
#-------------------------------------------------------------------------------

# To be fed into Arch's recommendation engine
user_inputs = { **backgrounds, **experience, **skills }

# To be used with Michelle's NLP model
user_desc = self_description

# To be used to weigh similarities/disimlarities returned by Arch's algo
user_prefs = {
    'backgrounds': backgrounds_pref,
    'experience': experience_pref,
    'skills': skills_pref
}

#-------------------------------------------------------------------------------
# Button actions
#-------------------------------------------------------------------------------

if search_btn:
    st.title('Search users')

if recommend_btn:
    st.title('Get recommendations')

    st.write('''Each participant of the hackthon is matched to the user in three categories:

* personal backgrounds
* level of experience
* skills & industries

For each category, each participant is compared to the user based on their cosine similarity.

The user can specify for each category if he wants to find teammate who are similar or disimilar
to him, and how this category is important to him.

Each participant is given a total score (0 - 1) based on the user's preference. The top recommended
teammates are:
''')
    st.write(get_similarity_by_category(user_inputs, user_prefs))

if discord_btn:
    st.title('Match with Discord users')

if visual_btn:
    st.title('Visualize where you fit')
