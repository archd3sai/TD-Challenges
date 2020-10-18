# TD For-you Page
We wanted to get to know the diverse range of participants a little better. Since we didn't have time to talk to every person, we were inspired by the task to create a personalized recommendation for every person. Through the data, we learned a bit more about each person's background, their interests, experiences, and their hopes for the future. Along the way, we also deepened our understanding of NLP and search matching along the way.

## How to use

Install dependencies:

```
conda env create -n streamlit -f environment.yml
```

Run Streamlit:

```
conda activate streamlit
cd td_frontend
streamlit run app.py
```

## Project Organization

```
.
├── for you                                         : Contains the python notebooks, scripts and pickle files
│     ├── matplotlib_visualizations.ipynb           : Python Notebook to visualize users profiles
│     ├── search_engine.py                          : Script to search workshops using queries
│     ├── Clean data.ipynb                          : Python Notebook to clean applicants data
│     ├── Similar users.ipynb                       : Python Notebook to find similar or different users based on filters
│     ├── workshop recommendation.ipynb             : Python Notebook to get recommendation of workshops
│     └── discord_rec
│         └── discord_sim.ipynb                     : Python Notebook to match with discord users
├── screenshots                                     : Contains the Streamlit APP figures 
├── td_frontend                                     : Customer Segmentation based on product aisles
│     ├── app.py                                    : Streamlit App
│     ├── environment.yaml                          : Environment requirements file
│     ├── discord_sim.py                            : Script to match with discord users
│     ├── search_engine.py                          : Script to search workshops using queries
│     ├── similar_users.py                          : Script to find similar or different users based on filters
│     ├── visualizations.py                         : Script to visualize users profiles
│     └── workshop_recommend.py                     : Script to get recommendation of workshops
├── gitignore                                       : gitignore file
└── README.md                                       : Project Report 
```
