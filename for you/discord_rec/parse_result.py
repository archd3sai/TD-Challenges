import pandas as pd

df = pd.read_csv('Similarity_output.csv')
df.rename(columns=lambda x: x.strip(), inplace=True)
df = df.sort_values(by=['similarity'], ascending=False)
for i in range(len(df)):
    if df['similarity'][i] > .95:
        df = df.drop([i])

df.to_csv('read_to_display.csv')