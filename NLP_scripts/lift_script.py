#!/usr/bin/python2.7
import csv
from nltk.corpus import stopwords
import re
import string
import decimal
import sys
from collections import defaultdict
import pandas as pd
import io

itr =0
stop = stopwords.words('english')
df1 = pd.DataFrame(columns=['nb','nb2','value'])
inter1 = []
posts_all = []
posts_clean = []
keys_all = []           # Array to store all keys from the ---- edmunds_pair_keys1.txt ---- file
file_length = 0		# calculate the number of rows in the file
results_dict = {'Pair':'Lift Value'};
writer_output = csv.writer(open('Lift_Values.csv', 'w'),delimiter=str(','), quotechar=str('"'), lineterminator='\n')

dictionary1 = {}
d2_dict = defaultdict(dict)

with open('edmunds_pair_keys.txt') as fileText:
    for row_pairkey in fileText:
        row_pairkey = row_pairkey.replace(",", " ")


#Use this when getting unicode error
with io.open('edmunds_new_output.csv', 'r', encoding='utf-8', errors='ignore') as infile, open('edmunds_new_output_m.csv', 'w') as outfile:
     inputs = csv.reader(infile)
     output = csv.writer(outfile)
     for index, row in enumerate(inputs):
        if index == 0:
            continue
        output.writerow(row)

with open('edmunds_new_output_m.csv') as f:
    rows = csv.reader(f,  delimiter=str(','), quotechar=str('"'))
	#file_length = '[%s]' % len(f.readlines())
	#print "Hello"
    for row in rows:
        inter1.append(row[2])
	file_length = file_length + 1

file_length = file_length + 1
inter1.append(row_pairkey)

for row in inter1:
    #sentences = re.split(r' *[\.\?!][\'"\)\]]* *', row)
    out1 = re.sub('[%s]' % re.escape(string.punctuation), '', row.lower())
    posts_all.append(out1)

for post in posts_all:
    s = []
    for i in post.split():
        if i not in stop:
            s.append(i)
    posts_clean.append(s)

print "WARNING::EVERYTHING NEEDS TO BE IN LOWER CASE edmunds_pair_keys.txt file"
with open('edmunds_pair_keys.txt') as fileText:
    for row in fileText:
        keys_all = row.split(",")
    #print keys_all
    length = len(keys_all)
    for index in range(len(keys_all)):
        #print str(index) + '  ' + keys_all[index]
        subs_counter = index + 1
        while subs_counter < len(keys_all):
            #print keys_all[index] + '    ' + keys_all[subs_counter]
            #with open('edmunds_pair_keys.csv') as f:
                #pair_key_rows = csv.DictReader(f, delimiter = ',')
                #for row in pair_key_rows:
                    #nb = raw_input('Choose a Word 1: ')
                    #nb2 = raw_input('Choose the Word 2: ')

                    #nb = row["car_maker1"]
                    #nb2 = row["car_maker2"]
            nb = keys_all[index]
            nb2 = keys_all[subs_counter]
            print '-------------------' + nb + ' and ' + nb2 + '-------------------'
            subs_counter = subs_counter + 1

            nb_plu = nb + 's'
            nb_app = nb + "'s"

            nb2_plu = nb2 + 's'
            nb2_app = nb2 + "'s"

            for post in posts_clean:
                for n,word in enumerate(post):
                    if(word == nb_plu or word == nb_app):
                        post[n] = nb
                    elif(word == nb2_plu or word == nb2_app):
                        post[n] = nb2

            for post in posts_clean:
                for word in post:
                    dictionary1[word] = 0

            for post in posts_clean:
                x = {}
                for word in post:
                    x[word] = 1
                for word in post:
                    if (x[word] > 0):
                        dictionary1[word] = dictionary1[word] + 1
                    x[word] = -1

            writer = csv.writer(open('word_post.csv', 'wb'))
            for key, value in dictionary1.items():
                writer.writerow([key, value])

            for post in posts_clean:
                for word in post:
                    for word2 in post:
                        if(word != word2):
                            d2_dict[word][word2] = 0

            for post in posts_clean:
                d3_dict = defaultdict(dict)
                for word in post:
                    for word2 in post:
                        if(word != word2):
                            d3_dict[word][word2] = 1

                for word in post:
                    for word2 in post:
                        if(word != word2):
                            if (d3_dict[word][word2] > 0):
                                d2_dict[word][word2] = d2_dict[word][word2] + 1
                            d3_dict[word][word2] = -1


            if(dictionary1.has_key(nb)):
                print nb + " " + str(dictionary1[nb])
            else:
                print "This word is not present"
                exit(0)

            if(dictionary1.has_key(nb2)):
                print nb2 + " " + str(dictionary1[nb2])
            else:
                print "This word is not present"
                exit(0)

            if(d2_dict.has_key(nb)):
                if(d2_dict[nb].has_key(nb2)):
                    print nb +" " +nb2 +" " + str(d2_dict[nb][nb2])
                    #print 'Rows in file: ', file_length
                    #if(d2_dict[nb].has_key(nb2)):
                    #results_dict['Pair'] = nb + "_" +nb2
                    #results_dict['Lift Value'] = decimal.Decimal(decimal.Decimal(file_length*(d2_dict[nb][nb2]))/decimal.Decimal((dictionary1[nb]*dictionary1[nb2])))
                    results_dict.update({nb + "_" +nb2:decimal.Decimal(decimal.Decimal(file_length*(d2_dict[nb][nb2]))/decimal.Decimal((dictionary1[nb]*dictionary1[nb2])))})
                    print 'lift('+ nb + "," +nb2 + ')',decimal.Decimal(decimal.Decimal(file_length*(d2_dict[nb][nb2]))/decimal.Decimal((dictionary1[nb]*dictionary1[nb2])))
                    val = decimal.Decimal(decimal.Decimal(file_length*(d2_dict[nb][nb2]))/decimal.Decimal((dictionary1[nb]*dictionary1[nb2])))
                    df1.loc[itr] = [nb, nb2, val]  # adding a row
                    itr = itr + 1
                    writer_output = csv.writer(open('Lift_Values.csv', 'wb'))
                    for key, value in results_dict.items():
                        writer_output.writerow([nb + "_" +nb2, decimal.Decimal(decimal.Decimal(file_length*(d2_dict[nb][nb2]))/decimal.Decimal(dictionary1[nb]*dictionary1[nb2]))])
                else:
                    print "These words are not present together in a post"
                    exit(0)
            else:
                print "These words are not present together in a post"
                exit(0)
print '--------------------------------------------------------'
df1.to_csv('Lift_Values.csv')

df1 = pd.read_csv("Lift_Values.csv")
df2 = pd.read_csv("Lift_Values.csv")
df2 = df2.rename(columns={'nb': 'k', 'nb2': 'nb'})
df2 = df2.rename(columns={'k': 'nb2'})
frames = [df1, df2]
result = pd.concat(frames)

table = pd.pivot_table(result, values='value', index='nb',columns='nb2', fill_value=0.00)
print table
print ("---------------")

for i in range(table.shape[0]):
    for j in range(table.shape[1]):
        if i>=j:
            table.iloc[i,j] = " "

table.index.names = ['']
print table
table.to_csv('Lift_Matrix.csv')

print 'Consolidated lift values amd matrix  can be found in Lift_Values.csv file and Lift_Matrix.csv'


