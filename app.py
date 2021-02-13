'''
    Главный модуль дашборда
    Также ответственен за обработку функций обратных вызовов
'''
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
from elements import sidebar, header, content, confusion_matrix_plot, create_table_from_DF, result, dataset, comparison_table, donut_chart, subplot_donuts
from dataframes import confusion_matrix
from layouts import compare, overview


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
# prevent_initial_callbacks=True
# Добавить в конец, когда на Heroku станет можно поставить новую версию Dash

server = app.server

table_header = [
    html.Thead(html.Tr([html.Th("Дата"), html.Th("G"), html.Th("lG"), html.Th("O"), html.Th("Матрица ошибок")]))
]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# -----------------------------------------------
# Блок обработки функций обратных вызовов
# -----------------------------------------------

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
    # Возвращение ошибки 404 на не предусмотренные адреса
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
    if date_value == None or date_value == []:
        new_table = dbc.Row(
            [
                dbc.Col(html.Div('Выберите даты')),
            ],
        ),
    else:
        if date_value == 'All':
            df = result.copy(deep=True)
            df = df.reset_index()
            df2 = comparison_table(df)
            df_cm = confusion_matrix.copy(deep=True)
            confusion_matrix_plot(df_cm)
            matrixs = base64.b64encode(open('figura.png', 'rb').read())
        else:
            df = result[result.date.isin(date_value)].copy(deep=True)
            df = df.reset_index()
            df2 = comparison_table(df)
            df_cm = confusion_matrix[confusion_matrix.date.isin(date_value)].copy(deep=True)
            confusion_matrix_plot(df_cm)
            matrixs = base64.b64encode(open('figura.png', 'rb').read())



        new_table = dbc.Row(
            [
                dbc.Col(
                    [
                        create_table_from_DF(df2),
                        dbc.Row(children=[subplot_donuts(i) for i in date_value]),

                    ]
                ),
                dbc.Col(html.Img(src='data:image/png;base64,{}'.format(matrixs.decode()), width='100%', height='auto')),
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

# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)
