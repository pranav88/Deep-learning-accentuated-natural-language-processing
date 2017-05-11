# Deep-learning-accentuated-natural-language-processing

This project is foccussed on exploring different methods to classify our text information.

## Motivation

Vast amount of textual information available on the web, we try to classify the the sentences specific to food from a raw html as belonging to one of the five different classes Preparation, Ingredients, Nutrition, Recipe, Title

## Approach

- Set up different architectures and then monitor their metrics to identify the best ones
- Build an end to end system on google cloud 
- Use GPUs to run models over several epochs
- Build a front end flask-app and run the model on unseen data
- Print results on webage, host the app on the host IP Address

## Deep-Glove-embeddings-conv-autoencoders.ipynb

- This notebook contains the model with the best results
- Shows implementing glove on using deep learning
- Also tries an unsupervised approach using Autoencoders
- Refer notebook for code and explanations

## Glove-cnn-lstm-gpu.ipynb

- The best model run on GPUs , the notebook is modified run locally over 1 epoch
- On the cloud the model was run over 60 epochs , screenshots of which are attached as png files
- Color coded confusion matrix and also a function to identify the misclassified sentences
- Model checkpointing to identify the weights of the model with highest accuracy
- keras callbacks to get plots of accuracy and histograms , screenshots are attached
- Refer notebook for code and explanation

## Padded-CNN-LSTM.ipynb

- Running CNN - LSTM network on the padded sentences/sequences
- Runnnig LSTM on the padded sentences/sequences
- Using the keras default embedding layer
- Refer notebook for code and explanation

## Word2vec-Doc2vec-FFN-Tensorboard.ipynb

- Word2vec , doc2vec models using gensim , fed into tensors for a tensorboard visualisation
- The doc2vec vectors are fed into a deep feed forward neural network
- Keras preprocessing is carried out as always
- Refer notebook for code and explanation

## Flask-spyder.py

- The front end for our model
- Generic to allrecipes.com , any recipe url from the website can be passed
- the page is then scrapped using beautiful soup to obtain the textual information
- The sentences are then passed into our established model
- Predictions are made for these sentences(unseen data)
- The final webpage displays the title , image and the predictions for that particular url recipe page
- Refer python script for code and explanation

<a href ="https://gyazo.com/5be2ec48bbcb206f62c3057a1843c63e"> <img src="https://gyazo.com/5be2ec48bbcb206f62c3057a1843c63e"></a>
