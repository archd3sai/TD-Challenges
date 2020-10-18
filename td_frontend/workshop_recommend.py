import pickle
import pandas as pd
from numpy import dot
from numpy.linalg import norm


with open('data/clf1_0.pkl', 'rb') as f:
    clf1_0 = pickle.load(f)
with open('data/clf1_1.pkl', 'rb') as f:
    clf1_1 = pickle.load(f)
with open('data/clf1_2.pkl', 'rb') as f:
    clf1_2 = pickle.load(f)
with open('data/clf2.pkl', 'rb') as f:
    clf2 = pickle.load(f)
with open('data/workshops.pkl', 'rb') as f:
    workshops = pickle.load(f)
with open('data/technologies.pkl', 'rb') as f:
    technologies = pickle.load(f)

def _format_user_input(user_inputs):

    formatted = {}

    # age_bin
    if user_inputs['age'] <= 18:
        formatted['age_bin'] = 0
    elif user_inputs['age'] <= 20:
        formatted['age_bin'] = 1
    elif user_inputs['age'] <= 22:
        formatted['age_bin'] = 2
    elif user_inputs['age'] <= 25:
        formatted['age_bin'] = 3
    elif user_inputs['age'] <= 30:
        formatted['age_bin'] = 4
    elif user_inputs['age'] <= 50:
        formatted['age_bin'] = 5

    # classification
    _class_to_index = {
        'Undergraduate': 0,
        'Masters': 1,
        'PhD': 2
    }
    formatted['classification'] = _class_to_index[user_inputs['classification']]
    formatted['Masters'] = 1 if user_inputs['classification'] == 'Masters' else 0
    formatted['PhD'] = 1 if user_inputs['classification'] == 'PhD' else 0
    formatted['undergrad'] = 1 if user_inputs['classification'] == 'Undergraduate' else 0

    # first_generation
    formatted['first_generation'] = 1 if user_inputs['first_generation'] == 'Yes' else 0

    # datascience_experience
    formatted['datascience_experience'] = int(user_inputs['datascience_experience'])

    # num_hackathons_attended
    formatted['num_hackathons_attended'] = 4 if user_inputs['num_hackathons_attended'] == '>3' else int (user_inputs['num_hackathons_attended'])

    # technologies
    for tech in technologies:
        formatted[tech] = 1 if tech in user_inputs['technology_experience'] else 0

    return pd.DataFrame([formatted])


def get_workshops_recommendation(diff_0, diff_1, diff_2, DL, DS, Industry, ML, rec_df):

    rec_df['rank1'] = 0
    if diff_0 == 0:
        rec_df['rank1'] = rec_df.difficulty.rank(method = 'dense')
    elif diff_1 == 0:
        rec_df['rank1'] = [1 if i==1 else 4 for i in rec_df.difficulty]
        rec_df.rank1[rec_df.difficulty == 2] = 2
        rec_df.rank1[rec_df.difficulty == 3] = 3
    elif diff_2 == 0:
        rec_df['rank1'] = [1 if i==2 else 4 for i in rec_df.difficulty]
        rec_df.rank1[rec_df.difficulty == 3] = 2
        rec_df.rank1[rec_df.difficulty == 1] = 3
    else:
        rec_df['rank1'] = rec_df.difficulty.rank(method = 'dense', ascending = False)

    rec_df['rank2'] = rec_df.track
    rec_df['rank2'] = rec_df['rank2'].map({'DL':DL, 'DS':DS, 'Industry':Industry, 'ML':ML})
    rec_df['rank2'] = rec_df.rank2.rank(method = 'dense', ascending = False)

    rec_df = rec_df.sort_values(['rank1', 'rank2']).reset_index(drop = True)
    rec_df['overall_rank'] = rec_df.index + 1
    return rec_df


def workshop_recommendations(user_inputs):

    data = _format_user_input(user_inputs)

    data = data[['age_bin', 'classification', 'first_generation',
       'datascience_experience', 'num_hackathons_attended', 'undergrad',
       'Masters', 'PhD', 'Excel', 'Python', 'Tableau', 'Pandas', 'NumPy',
       'MATLAB', 'Pytorch', 'Scikit-learn', 'full_stack', 'TensorFlow', 'R',
       'SQL', 'dev_ops', 'Keras', 'cloud']]

    diff_0, diff_1, diff_2 = clf1_0.predict(data), clf1_1.predict(data), clf1_2.predict(data)

    DL, DS, Industry, ML = clf2.predict_proba(data)[0,0], clf2.predict_proba(data)[0,1], \
        clf2.predict_proba(data)[0,2], clf2.predict_proba(data)[0,3]

    workshops_df = get_workshops_recommendation(diff_0, diff_1, diff_2, DL, DS, Industry, ML, workshops)

    return workshops_df


