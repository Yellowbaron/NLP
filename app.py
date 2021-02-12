# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import base64
from elements import sidebar, header, content, confusion_matrix_plot, create_table_from_DF, result, dataset, C_T
from dataframeCheck import confusion_matrix
from layouts import compare, overview
from io import BytesIO
import matplotlib.pyplot as plt
import callbacks


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server




#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div([
#     dbc.Row(dbc.Col(header), no_gutters=True),
#     dcc.Location(id="url"),
#     dbc.Row(
#         [
#             dbc.Col(
#                 [
#                     sidebar,
#
#                 ],
#                 width='100%',
#             ),
#             #dbc.Col(content, style={'padding':'16px'}),
#         ],
#         no_gutters=True,
#     ),
###################################################################################
    # html.Header(header),
    # header,
    # sidebar,
    # header,
    # row = html.Div(
    #     dbc.Row(
    #         create_table_from_DF(result),
    #         create_table_from_DF(dataset),
    #     ),
    # ),
    # html.Div([
    #     sidebar,
    #     content,
    # ]),
    # create_table_from_DF(dataset),
    # generate_table(result),
    # html.Div(children='Матрица ошибок'),
    # generate_table(confusion_matrix),
    # html.Div(children='Обучающее множество'),
    # generate_table(dataset),
    # html.Div(children='Векторная модель'),
    # generate_table(word2vec_model),
    # html.Div(children='Архитектура'),
    # generate_table(architecture),
    # html.Div(children='Количество эпох обучения'),
    # generate_table(epochs),
    # html.Div(children='Accuracy по итогам обучения'),
    # generate_table(accuracy),

# ])
table_header = [
    html.Thead(html.Tr([html.Th("Дата"), html.Th("G"), html.Th("lG"), html.Th("O"), html.Th("Матрица ошибок")]))
]
# df1 = pd.DataFrame(columns = ['Дата', 'Точность G', 'Полноста G', 'Точность lG', 'Полноста lG', 'Точность O', 'Полноста O'])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return overview
    elif pathname == "/page-1":
        return compare
    elif pathname == "/page-2":
        return html.Div(
            [
                dbc.Row(dbc.Col(header), no_gutters=True),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                sidebar,
                                dbc.Alert(
                                    [
                                        "Скоро этот раздел заработает, а сейчас можете воспользоваться ноутбуком в ",
                                        html.A("Google Colab", href='https://colab.research.google.com/drive/1V2vfY_koRPNsWx9E0IodDAXhIj7Dp6qo'),
                                        ],
                                    color="primary",
                                    style={'margin':'16px', 'margin-left': '17rem', 'margin-right':'16px', 'padding': '10px'},
                                    )
                            ],
                            style={'position': 'relative', 'height': '100%'}
                        )
                    ],
                    no_gutters=True,
                ),

            ],)
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    dash.dependencies.Output('compare_table', 'children'),
    [dash.dependencies.Input('select', 'value')])
def update_table(date_value):
    if date_value == None:
        new_table = dbc.Row(
            [
                dbc.Col(html.Div('Выберите даты')),
            ],
        ),
    else:
        if date_value == 'All':
            df = result.copy(deep=True)
            df = df.reset_index()
        else:
            df = result[result.date.isin(date_value)].copy(deep=True)
            df = df.reset_index()
            df2 = C_T(df)
            df_cm = confusion_matrix[confusion_matrix.date.isin(date_value)].copy(deep=True)
            confusion_matrix_plot(df_cm)
            matrixs = base64.b64encode(open('figura.png', 'rb').read())


        new_table = dbc.Row(
            [
                dbc.Col(create_table_from_DF(df2)),
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(matrixs.decode()), height='320px')),
            ],
        ),


    return new_table

@app.callback(
    Output("positioned-toast", "is_open"),
    [Input("positioned-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n:
        return True
    return False

if __name__ == '__main__':
    app.run_server(debug=True)
