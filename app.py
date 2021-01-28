# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def generate_table(dataframe, max_rows=10):          # Функция для создания таблицы в html
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
result = pd.DataFrame({
    "На множестве": ["O", "G", "lG", "На всём"],
    "Точность": ["97.35%", "75.00", "90.00%", "-"],
    "Полнота": ["98.73", "71.74", "50.00", "-"]
})
confusion_matrix = pd.DataFrame({
    "test \ pred": ["O", "G", "lG"],
    "O": [697, 8, 1],
    "G": [13, 33, 0],
    "lG": [6, 3, 9]
})
dataset = pd.DataFrame({
    "Класс": ["Всего предложений", "Элементов G и lG", "G", "lG", "O", "Длинна векторов"],
    "Кол-во": ["268", "64", "46", "18", "706", "43, левый паддинг"]
})
word2vec_model = pd.DataFrame({
    "Шаблон": ["1"]
})
architecture = pd.DataFrame({
    "Слои/Гиперпараметры": ["Эмбединги", "LSTM", "Выходной (Dense)", "Оптимизатор", "f ошибки", "Метрики", "?Оптимизация?"],
    "Количество элементов(нейронов/контейнеров)": [100, 64, 4, "Adam", "Категор. кросс-энтропия", "Accuracy", "64"],
    "Хар-ка": ["non-trainable", "Двунаправленная", "f актив - softmax", "-", "-", "-", "Пакетная"]
})
epochs = pd.DataFrame({
    "Эпоха": ["Максимум", "Лучшая", "Конец", "patience", "Переобучение"],
    "Число": [300, 86, 136, 50, "~70"],
    "val acc": ["-", "99.57", "99.22", "-", "-"],
    "val loss ": ["-", "2.57", "2.93", "-", "-"],
    "acc": ["-", "99.74", "99.99", "-", "-"],
    "loss": ["-", "1.25", "0.30", "-", "-"]
})

accuracy = pd.DataFrame({
    "Название теста": ["Chunk 01_02"],
    "Точность": ["98.2%"]
})


app.layout = html.Div(children=[
    html.H1(children='Дашборд для событийного детектора'),
    html.H4(children='byGalimyanov'),
    html.Div(children='''
        На 26/01/2021
    '''),
    generate_table(result),
    html.Div(children='Матрица ошибок'),
    generate_table(confusion_matrix),
    html.Div(children='Обучающее множество'),
    generate_table(dataset),
    html.Div(children='Векторная модель'),
    generate_table(word2vec_model),
    html.Div(children='Архитектура'),
    generate_table(architecture),
    html.Div(children='Количество эпох обучения'),
    generate_table(epochs),
    html.Div(children='Accuracy по итогам обучения'),
    generate_table(accuracy)

])

if __name__ == '__main__':
    app.run_server(debug=True)
