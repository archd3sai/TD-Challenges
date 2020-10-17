#!/usr/bin/python2.7
# change file name in line 17, text must be in column 3.
# output file is called limit_post.csv. Change this name before you run the script each time.
import csv
from nltk.corpus import stopwords
import re
import string
import io

stop = stopwords.words('english')

inter1 = []
posts_clean = []
posts = []
posts_found_with_brand = []
limited_post = []
limited_post2 = []
with io.open('edmunds_new_output.csv', 'r', encoding='utf-8', errors='ignore') as infile, open('final1.csv', 'w') as outfile:
     inputs = csv.reader(infile)
     output = csv.writer(outfile)

     for index, row in enumerate(inputs):
         # Create file with no header
         if index == 0:
             continue
         output.writerow(row)

with open('final1.csv') as f:
    rows = csv.reader(f,  delimiter=str(','), quotechar=str('"'))
    for row in rows:
        inter1.append(row[2])
        #print row[2]
        #print "--------------------"

for row in inter1:
    sentences_all = []
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', row)
    for s in sentences:
        in1 = ''.join(s)
        out = re.sub('[%s]' % re.escape(string.punctuation), '', in1.lower())
        sentences_all.append(out)
    posts.append(sentences_all)

for post in posts:
    sentences_clean = []
    for sentence in post:
        s = []
        for i in sentence.split():
            if i not in stop:
                s.append(i)
        sentences_clean.append(s)
    posts_clean.append(sentences_clean)

nb = raw_input('Choose a Brand: ')
nb2 = raw_input('Choose an Attribute: ')
nb3 = raw_input('Limit of the words in the sentence: ');

for post in posts_clean:
    for sentence in post:
        x = 0
        for i in sentence:
            if(i == nb):
                x = 1
                posts_found_with_brand.append(post)
                break

        if(x == 1):
            break

print(posts_found_with_brand)
limit = int(nb3) + 1

for post in posts_found_with_brand:
    sentence_with_attribute = []
    position_in_sentences = []
    for sentence in post:
        position  = 0
        for i in sentence:
            if(i == nb2):
                position_in_sentences.append(position)
                sentence_with_attribute.append(sentence)
            position = position + 1

    j = 0
    for sentence in sentence_with_attribute:
        limited_sentence = []
        for i in range(len(sentence)):
            if(abs(i - position_in_sentences[j]) < limit):
                limited_sentence.append(sentence[i])
        j = j + 1
        limited_post.append(limited_sentence)




for sent in limited_post:
    limited_post2.append(' '.join(sent))

# for sent in limited_post2:
#   print sent

f = open('limit_post.csv', 'wb')
out = csv.writer(f,  delimiter=str(','), quotechar=str('"'))
#out = csv.writer(f, delimiter=",")
for sent in limited_post2:
    out.writerow([sent])

f.close()

print "written limit_post.csv"

