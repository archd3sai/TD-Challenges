import pandas as pd
import spacy


def get_similar(s):
    """input string s: user's writing sample
        output list out: ordered list with name, username, intro text, similarity score"""
    nlp = spacy.load('en_core_web_sm')

    attributes = s

    reviews_df = pd.read_csv("data/discord_applicants.csv", engine='python')

    reviews_df = reviews_df.dropna()

    reviews_df['similarity'] = -1

    for index, row in reviews_df.iterrows():
        reviews_df.loc[index, 'similarity'] = nlp(row["Text"]).similarity(nlp(attributes))

    reviews_df = reviews_df.sort_values(by=['similarity'], ascending=False)

    for i, row in reviews_df.iterrows():
        reviews_df.at[i, 'Text'] = reviews_df.at[i, 'Text'].encode('utf-8')

    # drop introductions they wrote of themselves
    for sim in reviews_df['similarity']:
        if sim > .95:
            reviews_df.drop(reviews_df.loc[reviews_df['similarity']==sim].index, inplace=True)

    return reviews_df.values.tolist()


if __name__ == "__main__":
    results = pd.DataFrame(get_similar("Hello! My name is Annemarie! I’m a freshman general Engineering major (hopefully mechanical) at Texas A&M. My coding experience is limited, but I’m happy for any experience I can get to add to it!"), columns=['name', 'username', 'message', 'similarity_score'])

    print("")
    print(results.head(10))
