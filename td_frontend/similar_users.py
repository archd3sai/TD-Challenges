import pickle
import pandas as pd
from numpy import dot
from numpy.linalg import norm


with open('data/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
with open('data/industries.pkl', 'rb') as f:
    industries = pickle.load(f)
with open('data/technologies.pkl', 'rb') as f:
    technologies = pickle.load(f)
with open('data/majors.pkl', 'rb') as f:
    majors = pickle.load(f)

industries.remove('')
technologies.remove('')

users = pd.read_csv('data/applicants_cleans.csv')
users = users.drop('workshop_suggestions', axis=1)
users = users.set_index('userid')

categories = {
    'backgrounds': [
        'age_bin', 'classification', 'first_generation',
        'school_0', 'school_1', 'school_2', 'school_3',
        'school_4', 'school_5', 'school_6', 'school_7',
        *majors
    ],
    'experience': [
        'datascience_experience', 'num_hackathons_attended'
    ],
    'skills': [ *technologies, *industries ]
}


def _cos_sim(a, b):
    if norm(a) * norm(b) == 0:
        return 0
    return (dot(a, b) / (norm(a) * norm(b)))[0]


def get_similarity(user, other_users, similar=1):
    other_users['similarity'] = [ _cos_sim(user, x) for x in other_users.values ]
    other_users = other_users[other_users['similarity'] != 'Null']
    return list(other_users['similarity'])


def _format_user_input(user_inputs):
    formatted = {}

    # school
    school_binary = encoder.transform(pd.DataFrame([user_inputs['school']], columns=['school']))
    for i in range(8):
        formatted['school_{}'.format(i)] = school_binary.loc[0]['school_{}'.format(i)]

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

    # first_generation
    formatted['first_generation'] = 1 if user_inputs['first_generation'] == 'Yes' else 0

    # datascience_experience
    formatted['datascience_experience'] = int(user_inputs['datascience_experience'])

    # num_hackathons_attended
    formatted['num_hackathons_attended'] = 4 if user_inputs['num_hackathons_attended'] == '>3' else int (user_inputs['num_hackathons_attended'])

    # majors & minors
    for major in majors:
        formatted[major] = 1 if major in (user_inputs['majors'] + user_inputs['minors']) else 0
    formatted['Has_minor'] = 1 if len(user_inputs['minors']) > 0 else 0

    # technologies
    for tech in technologies:
        formatted[tech] = 1 if tech in user_inputs['technology_experience'] else 0

    # industries
    for ind in industries:
        formatted[ind] = 1 if ind in user_inputs['relavent_industries'] else 0

    return pd.DataFrame([formatted])


def get_similarity_by_category(user_inputs, prefs, other_users=users):
    formatted = _format_user_input(user_inputs)

    backgrounds_similarity = get_similarity(formatted[categories['backgrounds']], users[categories['backgrounds']])
    experience_similarity = get_similarity(formatted[categories['experience']], users[categories['experience']])
    skills_similarity = get_similarity(formatted[categories['skills']], users[categories['skills']])

    if prefs['backgrounds']['similarity'] == 'different from me':
        backgrounds_similarity = [ 1 - x for x in backgrounds_similarity ]
    if prefs['experience']['similarity'] == 'different from me':
        experience_similarity = [ 1 - x for x in experience_similarity ]
    if prefs['skills']['similarity'] == 'different from me':
        skills_similarity = [ 1 - x for x in skills_similarity ]

    b_imp = int(prefs['backgrounds']['importance'])
    e_imp = int(prefs['experience']['importance'])
    s_imp = int(prefs['skills']['importance'])
    total_imp = b_imp + e_imp + s_imp

    total_score = [
        (b * b_imp + e * e_imp + s * s_imp) / total_imp
        for b, e, s in zip(backgrounds_similarity, experience_similarity, skills_similarity)
    ]

    similarities = {
        'backgrounds': backgrounds_similarity,
        'experience': experience_similarity,
        'skills': skills_similarity,
        'total_score': total_score
    }

    similarities = pd.DataFrame(similarities, index=users.index)

    return similarities.sort_values('total_score', ascending=False)

