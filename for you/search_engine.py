import pandas as pd
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords
import distance

nlp = spacy.load('en')

#EXPLANATION: 
#This code takes in a user query string with the find_best_result function.
#It then calculates two similarity indexes between the query and the workshops
#The name similarity index measures the similarity between the user query string and the workshop title
#The tag similarity index picks apart the user query string and checks its similarity to the workshop tags
#The arrange_results function takes the two indexes and combines them into an aggregate similarity index
#This aggregate similarity index weights tag_similarity less than name_similarity... This can be tweaked and played around with if needed
#The arrange_results function then looks at the three workshops with the highest similarity index and that is the final output

#This script must be modified so that it can be integrated with the rest of the app

#I did not make a similarity index for the description column... that is worth exploring if we have the time


workshop_data = pd.read_csv("workshops.csv")
query_data = pd.read_csv("queries.csv")

#overall similarity with all factors considered
similarity = []

#adding column of processed workshop names
workshop_data["processed_names"] = workshop_data["workshop"].str.lower()


#################################################################################
def name_similarity_index(query):
        name_similarity = []
        #similarity with workshop name only
        for value in workshop_data["workshop"]:
                doc1 = query
                doc1 = nlp(remove_stopwords(doc1))
                doc2 = nlp(value)
                sim_value = doc1.similarity(doc2)
                if sim_value > 0.85:
                        sim_value = sim_value * 5
                name_similarity.append(sim_value)
        return name_similarity

###################################################################################
def tag_similarity(query):
        tag_similarity = []
        #similarity with tags
        words_list = []
        query_words = query.split(" ")
        for value in workshop_data["tags"]:
                words = value.split(", ")
                words_list.append(words)

        #iterating through each list of tags, finding similarity for each tag
        #each workshop now has a list with the similarities between each tag and the query word
        word_similarities = []
        for list in words_list:
                list_sim = []
                for word in list:
                        doc1_dist = remove_stopwords(query)
                        doc1_sim = nlp(doc1_dist)
                        doc2_dist = word
                        doc2_sim = nlp(word)
                        word_sim = doc1_sim.similarity(doc2_sim)
                        if word_sim >= 0.70:
                                word_sim = word_sim * 2
                        if word_sim == 1.00:
                                word_sim = word_sim * 10
                        for part in query_words:
                                word_dist = distance.levenshtein(part, str(doc2_dist))
                                if word_dist < 3:
                                        word_sim = word_sim * 3
                                """       print(word_dist)
                                        print(part)
                                        print(doc2_dist)"""
                        list_sim.append(word_sim)
                tag_similarity.append(sum(list_sim) / len(list_sim))
        return tag_similarity

#############################################################################
# description similarity index






############################################################################

def arrange_results(tag_similarity, name_similarity):
        workshop_data["tag_similarity"] = tag_similarity
        workshop_data["name_similarity"] = name_similarity
        workshop_data["similarity"] = 0.33 * workshop_data["tag_similarity"] + workshop_data["name_similarity"]
        results_df = workshop_data[["workshop","similarity"]]
        results_df = results_df.sort_values(by='similarity', ascending=False)
     #   print(results_df.head())
     #   print("             ")
        best_result = results_df.nlargest(3, "similarity")
        best_result = best_result["workshop"]
        print(best_result)
        return best_result

def find_best_result(query):
        name_similarity_index(query)
        tag_similarity(query)
        arrange_results(tag_similarity(query), name_similarity_index(query))

find_best_result("for while logic")

'''
for value in query_data["query"]:
        find_best_result(value)
        print("------------------------------------------")


test_results_df = query_data
test_results_df["test_results"] = final_results

test_results_df.to_csv("test_results.csv", index = False)

'''
