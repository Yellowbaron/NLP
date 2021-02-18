<h1 align="center">Event detector and dashboard</h1>
<h2 align="center"><a  href="https://dashboard1evdet.herokuapp.com/">Dashboard for compare results of experiments</a></h2>
<h2 align="center"><a  href="https://colab.research.google.com/drive/1J7w75A8V1vIXliTsA72HbEbPeWNHJfUw">Notebook on google colab with deep neural networks (LSTM)</a></h2>
<h2 align="center"><a  href="https://colab.research.google.com/drive/1V2vfY_koRPNsWx9E0IodDAXhIj7Dp6qo">Notebook on google colab with demonstration work on a bite of the dataset from Lenta.ru</a></h2>

## Event detector description

This detector only for russian languages.
The event detector learned from a simple set of events in conll-u format. 
There is no unambiguous definition of an event in annotation markup. 
We looked for it in English, French, and Chinese research. 
We decided to use the law of dialectics about the transition of quantitative changes to qualitative ones.
In our training set, we have removed all kinds of sentences with an ambiguous interpretation and any hint of procedurality.

### Tags of dataset

<p>G - event trigger - the word used to refer to the event in the text.</p>
<p>lG - auxiliary trigger - for cases when the reference is verbose (for example, "a meeting took place").</p>
<p>O - other words in the text.</p>
<p>Corpus_Event.txt - dataset</p>

### Technologies

<p>Programming language - Python 3</p>
<p>Class of artificial neural networks - bidirectional recurrent neural networks (LSTM)</p>
<p>Software library for machine learning - Tensorflow (Keras interface)</p>

### Current state

Increasing the teaching set.
<p>Significant precision - 79.4%</p>
<p>Significant recall - 81.3%</p>

## Dashboard description

The dashboard is designed to track the results of experiments with a neural network. 
After the experiment, all data about it are recorded in the database (automatically after pressing a button in the notebook)
The dashboard takes data from this database. (You need to manually push the updated database to the github.)
<p> <img src="https://media.giphy.com/media/PrnYOwAgmOEJXGbD6f/giphy.gif"> </p>

### Technologies

<p>Backend and frontend on plotly dash open-source framework of python</p>
<p>Relational database management system - SQLite and SQLAlchemy</p>


