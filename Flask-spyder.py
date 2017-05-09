from flask import Flask
from flask import request
from flask import render_template
from bs4 import BeautifulSoup
import requests
import pandas as pd
import keras
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from PIL import Image
import numpy as np
from keras.models import model_from_json

app = Flask(__name__)

## function that preprocesses the unseen data the similar way it was done on our training data
def data_prep(dat):
	tokenizer = Tokenizer(lower=True)
	tokenizer.fit_on_texts(dat)
	sequences = tokenizer.texts_to_sequences(dat)
	word_index = tokenizer.word_index
	MAX_SEQUENCE_LENGTH = 5
	data1 = pad_sequences(sequences,maxlen = MAX_SEQUENCE_LENGTH)
	return data1
## make the front end page where the url is to be entered
@app.route('/')
def my_form():
    return render_template("my-form.html")

## a post method that takes the url , to scrape the data from the website
@app.route('/', methods=['POST'])
def my_form_post():

    url = request.form['text']
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser') ## use beautiful soup to scrape the webpage and get the textual information
    recipe = soup.find_all("p",itemprop="reviewBody")
    reviews = []
    for i in recipe:
    	reviews.append(i.string)
    basic_nutrients = soup.find_all("li",class_="nutrientLine__item")
    nutrients = []
    for i in basic_nutrients:
    	nutrients.append(i.string)
    amount = soup.find_all("li",class_="nutrientLine__item--amount")
    values = []
    for i in amount:
    	for j in i.find_all("span"):
    		text = "".join([j.text,j.next_sibling])
    		values.append(text)
    nutrient_values = []
    for i,j in zip(nutrients,values):
    	nutrient_values.append("".join([i,j]))
    instructions = soup.find_all("span", class_="recipe-directions__list--item")
    instructions = instructions[:-1]
    preparation = []
    for i in instructions:
    	preparation.append(i.string)
    	ingred = soup.find_all("span",itemprop="ingredients")
    ingredients = []
    for i in ingred:
    	ingredients.append(i.string)
    photo_title = soup.find(class_= "rec-photo")
    image_url = photo_title['src']
    title = photo_title['title']
    data = []
    data.extend(preparation)
    data.extend(ingredients)
    data.extend(nutrient_values)
    data.extend(reviews)
    data.append(title)
    data_preprocessed = data_prep(data) ## add all the data into one list 
    model_loaded = load_model('glove-keras.h5') ## load the model we already established
    predictions = model_loaded.predict(data_preprocessed) ## make predictions on unseen data
    predicted_class = []
    for i in predictions:
    	predicted_class.append(np.where(np.max(i) == i)[0][0])
    prep = []
    ingred = []
    nutr = []
    revi = []
    heading = []
    for i,j in zip(data,predicted_class):
    	if j == 0:
    		prep.append(i)   ## adding in preparation
    	elif j ==1:
    		ingred.append(i) ## adding in ingredients
    	elif j == 2:
    		nutr.append(i) ## adding in nutrients
    	elif j == 3:
    		revi.append(i) ## adding in reviews
    	elif j == 4:
    		heading.append(i) ## adding in the title

    df = pd.DataFrame() ## create dataframe for the predictions
    df['preparation'] = prep
    df1= pd.DataFrame({'ingredients':ingred})
    df2= pd.DataFrame({'nutrients':nutr})
    df3 = pd.DataFrame({'reviews':revi})
    df4 = pd.DataFrame({'title':heading})
    predicted_table = pd.concat([df,df1,df2,df3,df4], axis=1) ## the model predictions to be output
    html_1 = '<!DOCTYPE html><HTML><HEAD><TITLE>Results\
                 </TITLE></HEAD><BODY>{}</BODY></HTML>'.format(
                 predicted_table.to_html())
    with open("templates/results.html", "w") as outf:
    	outf.write("<H1>"+title+"</H1>")               ## adding in the title
    	outf.write('<img src='+"'"+image_url+"'"'/>')  ## adding the image
    	outf.write(html_1)                             ## adding our predicted results
    return render_template("results.html")

if __name__ == '__main__':
    app.run(host= '10.3.32.242', port=9001, debug=True) ## host the flask app on the host address publicly
    #app.run(debug=True)                                ## host the flask app locally