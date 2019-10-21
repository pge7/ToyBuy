from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
from flaskexample.a_Model import ModelIt
import os
from flaskexample.settings import APP_STATIC
import html


'''
set the path for image folder

'''
IMG_FOLDER = os.path.join('static', 'img')
app.config['IMG_FOLDER'] = IMG_FOLDER

'''
connect to Postgres
'''

user = 'postgres'    
dbname = 'postgres'
username = 'postgres'
password = ""#replace with pathword
con = None
con = create_engine('postgres+psycopg2://%s:%s@localhost/%s'%(username, password, dbname))

if not database_exists(con.url):
    create_database(con.url)

def escape(texts): 
   return html.unescape(str(texts))
 
@app.route('/')
@app.route('/index')
def index():
   return render_template("index.html",
      title = 'Home', logo_image = os.path.join(app.config['IMG_FOLDER'], 'logo.jpg')
      )


@app.route('/toys_output', methods=['POST'])
def toys_output():
    user_input = None
    baby_category = request.form.getlist("baby")
    toddler_category = request.form.getlist("toddler")
    category = ''
    if len(baby_category) != 0:
        category = 'baby'
        baby = [x for x in baby_category[0].split()]
        user_input = baby
		
    elif len(toddler_category) != 0:
        toddler = [x for x in toddler_category[0].split()]
        user_input = toddler
        category = 'toddler'
    text = ""
    
  
    tic_tag, tic_tl, tic_ds, tic_text = ModelIt(user_input, text)
	
    num = len(user_input)

    
    test_query = "SELECT distinct title, description, listing_id, '$' || ' ' || price AS price, img1, url, tpc_tl, tpc_tag, tpc_ds, views FROM totaltoys_v5 where dmt_tag = {} and dmt_ds = {} and dmt_tl = {} and img1 is not NULL order by views DESC, tpc_ds DESC, price DESC ".format(tic_tag, tic_ds, tic_tl)
    print(query)
    query_results=pd.read_sql_query(test_query,con)
    print(query_results)
    toys = []
    for i in range(0,query_results.shape[0]):
	    te = escape(query_results.iloc[i]['title'])
	    ds = escape(query_results.iloc[i]['description'])
	    toys.append(dict(ls = query_results.iloc[i]['listing_id'], img = query_results.iloc[i]['img1'], title = te, description = ds, price = query_results.iloc[i]['price'], url = query_results.iloc[i]['url'], view = query_results.iloc[i]['views']))
	
    return render_template("toys_output.html", toys = toys)