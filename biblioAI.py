import csv
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from flask import Flask, url_for, request, render_template, jsonify
from tabulate import tabulate
from scipy.sparse import csr_matrix
from pandas.api.types import is_numeric_dtype
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings("ignore")

def convert_emoji_to_base64(emoji):
    emoji_bytes = emoji.encode('utf-8')
    base64_data = base64.b64encode(emoji_bytes).decode('utf-8')
    return f'data:image/png;base64,{base64_data}'

emoji = '📚'  # Replace with your desired emoji

base64_url = convert_emoji_to_base64(emoji)
print(base64_url)

books = pd.read_csv("/Users/wannurfarahinwanrusmadi/Downloads/df_book.csv")

books.drop_duplicates(subset=['title_book'], inplace=True)

books1 = pd.read_csv("/Users/wannurfarahinwanrusmadi/Downloads/YA dataset/YA_dataset.csv")

df = pd.concat([books, books1])

df.drop_duplicates(subset='title_book', inplace=True)

df.to_csv('/Users/wannurfarahinwanrusmadi/Downloads/cleaned_data.csv', index=False)

data=df.pivot_table(index="title_book",columns="avg_rating",values="index_no").fillna(0)

model = NearestNeighbors(metric='cosine')
model.fit(data.values) 

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def search_data():
    if request.method == 'POST':
        search_query = request.form.get('search-query')

        recommendations = get_recommends(search_query)
        # Return the filtered data to the HTML templater
        return render_template('data.html', search_query=search_query, recommendations=recommendations)
    else:
        return render_template('index.html')

# function to return recommended books - this will be tested
def get_recommends(search_query = ""):
  try:
    search_query = search_query.title()
    book = data.loc[search_query]
  except KeyError as e:
    print('The given book', e, 'does not exist')
    return

  distance, indice = model.kneighbors([book.values], n_neighbors=6)

  recommended_books = pd.DataFrame({
      'title'   : data.iloc[indice[0]].index.values,
      'distance': distance[0]
    }) \
    .sort_values(by='distance', ascending=False) \
    .head(5)

  return [search_query, recommended_books.to_string(index=False)]

@app.route('/')
def display_table():
    # Read the CSV file using pandas
    df = pd.read_csv('/Users/wannurfarahinwanrusmadi/Downloads/cleaned_data-2.csv')
    
    # Convert the DataFrame to HTML table
    table_html = df.to_html(classes='table table-striped table-bordered')

    # Render the template and pass the HTML table data
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
     app.debug = True
     app.run()