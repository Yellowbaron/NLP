'''
    Модуль ответственный за макеты страниц

'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import base64
from elements import sidebar, compare_table, header, content, select_dates, create_table_from_DF, result, dataset


# -----------------------------------------------
# Страница сравнения
# -----------------------------------------------

compare = html.Div([
    dbc.Row(dbc.Col(header), no_gutters=True),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar,
                    html.Div("Выберите даты экспериментов", style={'align': 'center', 'padding': '8px', "color": "white", "background-color": "#2060F5", 'margin-top': '256px', 'position':'absolute'}),
                    # Всё держится на одной строчке, нужно пофиксить! no_gutters
                    html.Div("Выберите даты экспериментов", style={'align': 'center', 'padding': '8px', "color": "white", "background-color": "#2060F5", 'margin-top': '256px', 'padding-left': '16px', 'width': '16rem'}),
                    dcc.Dropdown(
                        id="select",
                        options=select_dates,
                        multi=True,
                        style={'height': 'auto', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '14rem',
                               'align': 'center'},
                        # value=1
                    ),
                    html.Div("byGalimyanov", style={"color": "white", 'position': 'fixed', "bottom": '0px', "left": '8px', "width": "16rem",})
                ],
                width='16rem',
                style={'position': 'relative', 'height': '100%'}
            ),
            dbc.Col(compare_table, style={'padding': '16px'}),
        ],
        style={'height': '100%'},
        no_gutters=True,
    ),
], style={'height': '100%', 'width': '100%', 'position': 'relative'})

# -----------------------------------------------
# Страница обзора
# -----------------------------------------------

overview = html.Div([
    dbc.Row(dbc.Col(header), no_gutters=True),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar,
                    html.Div("Выберите даты экспериментов", style={'align': 'center', 'padding': '8px', "color": "#2060F5", "background-color": "#2060F5", 'margin-top': '256px', 'position':'absolute'}),
                    # Всё держится на одной строчке, нужно пофиксить! no_gutters
                    html.Div("Выберите даты экспериментов", style={'align': 'center', 'padding': '8px', "color": "#2060F5", "background-color": "#2060F5", 'margin-top': '256px', 'padding-left': '16px'}),
                    # dcc.Dropdown(
                    #     id="select",
                    #     options=select_dates,
                    #     multi=True,
                    #     style={'height': 'auto', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '14rem',
                    #            'align': 'center'},
                    #     # value=1
                    # ),
                    html.Div("byGalimyanov", style={"color": "white", 'position': 'fixed', "bottom": '0px', "left": '8px', "width": "16rem",})
                ],
                width='16rem',
                style={'position': 'relative', 'height': '100%'}
            ),
            dbc.Col(content, style={'padding': '16px', 'margin-left': '16px'}),
        ],
        style={'height': '100%'},
        no_gutters=True,
    ),
], style={'height': '100%', 'width': '100%', 'position': 'relative'})