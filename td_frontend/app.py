import streamlit as st
import pandas as pd

from similar_users import get_similarity_by_category
from discord_sim import get_similar
from search_engine import find_best_result
from workshop_recommend import workshop_recommendations
from visualizations import plot_ages, plot_education, plot_skills, plot_majors

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

st.sidebar.header('Visualization Tool')

visual_btn = st.sidebar.button('By the Numbers')

st.sidebar.header('Search Tool')

query = st.sidebar.text_input('Your query string')

search_btn = st.sidebar.button('Search workshops')

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

recommend_btn = st.sidebar.button('Get recommendations')
discord_btn = st.sidebar.button('Match with Discord users')


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
# Default - about page
#-------------------------------------------------------------------------------

about_widgets = [
    st.title('About'),
    st.header('Created by'),
    st.text('''* Arch Desai
* Dillon Jaghory
* Rui-Liang (Larry) Lyu
* Michelle Xia
''')
]


def _remove_about_widgets():
    for widget in about_widgets:
        widget.empty()

#-------------------------------------------------------------------------------
# TAMU Datathon by the numbers
#-------------------------------------------------------------------------------

if visual_btn:
    _remove_about_widgets()

    st.title('TAMU Datathon by the Numbers')

    st.header('Most applicants are between the ages of 18 and 20')
    st.pyplot(plot_ages())

    st.header('Undergrads made up the overwhelming majority of applicants')
    st.pyplot(plot_education())

    st.header('Python is by far the most widely known skill')
    st.pyplot(plot_skills())

    st.header('The number of math and statistics majors towered over the rest of the majors')
    st.pyplot(plot_majors())


#-------------------------------------------------------------------------------
# Search button
#-------------------------------------------------------------------------------

if search_btn:
    _remove_about_widgets()

    st.title('Search workshops')

    st.write('Three workshops best matching your query string:')

    results = find_best_result(query)
    st.table(results)

    st.info('''This code takes in a user query string, then calculates two similarity indexes
between the query and the workshops:

* **The name similarity index** measures the similarity between the user query string and the workshop title
* **The tag similarity index** picks apart the user query string and checks its similarity to the workshop tags

The two indexes and then combined into an **aggregate similarity index** based predefined weights.
''')


#-------------------------------------------------------------------------------
# Teammate & Workshop recommendations
#-------------------------------------------------------------------------------

if recommend_btn:
    _remove_about_widgets()

    st.title('Get recommendations')

    st.subheader('Top Datathon participants who match your info & preferences:')

    st.write(get_similarity_by_category(user_inputs, user_prefs))

    st.info('''You were matched with other participants based on three categories:

* personal background
* level of experience
* skills & industries

For each category, your preferences were compared with each participant's profile using cosine similarity.

You were able to specify for each category whether you wanted to find teammates who were similar or dissimilar
to you, and how important said category was to you.

Each participant was given a total score (0 - 1) based on how well they fit your preferences. Your top recommended
teammates are:
''')

    st.subheader('Top workshops that match your info')

    st.write(workshop_recommendations(user_inputs))

    st.info('''Workshop recommendation:

- Step 1: get the data of users who have attended the bootcamp, clean workshop data

- Step 2: 2 main Machine learning models

    - features: user info (age_bin, classification, ds experience, technologies, etc.)

    - tragets:
        - (1) Whether a user will attend a bigginer or intermediate or advance workshop? : Target = difficulty

        - (2) Whether a user will attend a DS/ML/DL workshop? : Target = track

    - For target 1 (i.e. difficulty) multiple RF models are built as the target is ordnial classes (difficulty 0 or 1 or 2)

    - For target 2 (i.e. track) one RF model is built (track DS or DL or ML etc.)

- Step 3: Ranking

    - Based on user's predicted difficulty workshops list will be ranked

    - Based on user's predicted track probabilities workshops will be given another rank

- Step 4: Final Ranking

    - Based on both of these ranking, final workshop lists will be recommended. The difficulty of a workshop is given higher weightage.
''')


#-------------------------------------------------------------------------------
# Discord user matching
#-------------------------------------------------------------------------------

if discord_btn:
    _remove_about_widgets()

    st.title('Match with Discord users')

    results = get_similar(user_desc)
    results = pd.DataFrame(results, columns=['name', 'username', 'message', 'similarity_score'])

    # Convert byte literals to strings
    results['message'] = pd.Series([ msg.decode('utf-8') for msg in results.message ], index=results.index)

    close_matches = results[results.similarity_score > 0.9]

    st.write('''There are **{}** people who have a `similarity_score > 0.9` with you!

The person who matches the best with you is **{}** (`@{}`). Here is their introduction:

> {}

Your other close matches are:'''.format(
        len(close_matches),
        close_matches.loc[0]['name'],
        close_matches.loc[0]['username'],
        close_matches.loc[0]['message']
    ))

    st.table(close_matches.iloc[1:])

    st.info('''Your self-description was compared with all messages posted in the official
    TAMU Datathon Discord `#introductions` channel using a netural language processing (NLP) model.''')
