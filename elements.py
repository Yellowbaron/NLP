'''
    Модуль ответственный за компоненты дашборда

'''

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import pandas as pd
import matplotlib.pyplot as plt
from dataframeCheck import dates, result, confusion_matrix, dataset, word2vec_model, architecture, epochs, accuracy
from icons import material_icons
import seaborn as sns
from io import BytesIO
from math import ceil
import plotly.express as px



# -----------------------------------------------
# Блок оформления
# -----------------------------------------------
SIDEBAR_STYLE = {
    'position': 'fixed',
    "top": '100px',
    # "left": 0,
    "bottom": 0,
    "width": "16rem",
    # "padding": "100rem 1rem",
    'height': '100%',
    # 'padding-bottom': '100%',
    "background-color": "#2060F5",
    'margin-right': '0rem',
    'padding-left': '16px'
}

COLAB_LOGO = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/googlecolab.svg'
GITHUB_LOGO = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/github.svg'
LOGO = base64.b64encode(open('logo.png', 'rb').read())

# -----------------------------------------------
# Блок функций
# -----------------------------------------------

# Рендер таблицы
def create_table_from_DF(df):
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table

# -----------------------------------------------
# Блок элементов страницы
# -----------------------------------------------

# -----------------------------------------------
# Всплывающая легенда классов в датасете
# -----------------------------------------------

toast = html.Div(
    [
        dbc.Button(
            "Открыть легенду классов", id="positioned-toast-toggle", color="info"
        ),
        dbc.Toast(
            '''
                \nG - Событийная метка лексемы. \nОбозначает, что слово несёт \nсобытийную информацию в тексте.
                \nlG - Вспомогательная метка лексемы. \nОбозначает вспомогательную информацию, \nслужит для однозначности основной метки.
                \nO - Метка, которая показывает, \nчто лексема не несёт событийной информации.
            ''',
            id="positioned-toast",
            header="Легенда меток классов",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={'white-space':'pre', "position": "fixed", "top": 66, "right": 10, "width": 350, 'z-index': '1', 'background-color': 'white'},
        ),
    ]
)

# -----------------------------------------------
# Боковая панель
# -----------------------------------------------

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("ОБЗОР", href="/", active="exact", style={'color':'white'}),
                dbc.NavLink("СРАВНЕНИЕ", href="/page-1", active="exact", style={'color':'white'}),
                dbc.NavLink("ДЕМОНСТРАЦИЯ", href="/page-2", active="exact", style={'color':'white'}),
            ],
            style={'padding-top': '32px'},
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# -----------------------------------------------
# Хэдер
# -----------------------------------------------

header = dbc.Navbar(
    [
        html.A(

            dbc.Row(
                [
                    html.Img(src='data:image/png;base64,{}'.format(LOGO.decode()), height="80px", style={'position':'absolute', 'top':'0px', 'left':'32px'}),
                    dbc.Col(dbc.NavbarBrand("Дашборд для событийного детектора", className="ml-2", style={'font-size':'20pt'}), style={'margin-left':'16rem', 'margin-top': '15px', 'margin-bottom': '15px'}, align='center'),
                    dbc.Col(dbc.NavLink(html.Img(src=COLAB_LOGO, height="80px"), href="https://colab.research.google.com/drive/1J7w75A8V1vIXliTsA72HbEbPeWNHJfUw"), align='center'),
                    dbc.Col(dbc.NavLink(html.Img(src=GITHUB_LOGO, height="60px"), href="https://github.com/Yellowbaron/NLP"), align='center', style={'right': '0px'}),
                    dbc.Col(toast),
                ],
                align="start",
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="#2060F5",
    dark=True,
)

# -----------------------------------------------
# Контент обзорной страницы
# -----------------------------------------------

# Donut chart по количеству классов в датасете
pie = pd.DataFrame(columns=['Класс', 'Кол-во'])
for index, row in dataset[dataset['date'] == dataset['date'].max()].iterrows():
    if row['class_set'] != 'G' and row['class_set'] != 'lG' and row['class_set'] != 'O': continue
    pie.loc[index] = [
                           row['class_set'],
                           row['amount'],
                     ]

donut_dataset = px.pie(pie, values='Кол-во', names='Класс', hole=.7)

# Точность на тесте
accuracy_last_info = accuracy[accuracy['date'] == accuracy['date'].max()]
accuracy_progress = dbc.Card(
    [
        dbc.CardHeader("Точность на тесте " + str(accuracy_last_info['name_test'].values[0])),
        dbc.CardBody(
            [
                dbc.Progress(str(accuracy_last_info['accuracy'].values[0]) + '%', value=accuracy_last_info['accuracy'].values[0])
            ]
        ),
    ],)
# Точность и полнота по классам
accuracy_by_classes = result[result['date'] == result['date'].max()].copy()
accuracy_by_classes.set_index('kind_of_set', inplace=True)
accuracy_by_classes_progress = dbc.Row(
    [
        # Класс O
        dbc.Col([
            dbc.Card(
                [
                dbc.CardHeader("Точность на классе \"O\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['precision']['O']), value=float(accuracy_by_classes['precision']['O'].rstrip('%')))
                    ]
                ),
                ], ),
            dbc.Card(
                [
                dbc.CardHeader("Полнота на классе \"O\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['recall']['O']), value=float(accuracy_by_classes['recall']['O'].rstrip('%')))
                    ]
                ),
                ], ),
        ]),
        # Класс G
        dbc.Col([
            dbc.Card(
                [
                dbc.CardHeader("Точность на классе \"G\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['precision']['G']), value=float(accuracy_by_classes['precision']['G'].rstrip('%')))
                    ]
                ),
                ], ),
            dbc.Card(
                [
                dbc.CardHeader("Полнота на классе \"G\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['recall']['G']), value=float(accuracy_by_classes['recall']['G'].rstrip('%')))
                    ]
                ),
                ], ),
        ]),
        # Класс lG
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader("Точность на классе \"lG\""),  # Подход «один против всех»
                    dbc.CardBody(
                        [
                            dbc.Progress(str(accuracy_by_classes['precision']['lG']),
                                         value=float(accuracy_by_classes['precision']['lG'].rstrip('%')))
                        ]
                    ),
                ], ),
            dbc.Card(
                [
                    dbc.CardHeader("Полнота на классе \"lG\""),  # Подход «один против всех»
                    dbc.CardBody(
                        [
                            dbc.Progress(str(accuracy_by_classes['recall']['lG']),
                                         value=float(accuracy_by_classes['recall']['lG'].rstrip('%')))
                        ]
                    ),
                ], ),
        ]),
    ])
# Контент для обзора
content = html.Div(
    [
        dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("Количество классов в датасете"),
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(figure=donut_dataset),
                                        ]
                                    ),
                                ],
                                # style={'height': 'auto', 'width': '600px'}
                            )
                        ],
                    ),
                    dbc.Col([
                        accuracy_progress,
                        accuracy_by_classes_progress,
                    ],)
                ],
            ),
        ],
    id='content'
    )
# -----------------------------------------------
# Таблицы сравнений экспериментов
# -----------------------------------------------
compare_table = html.Div(
    [
        ],
    id='compare_table',
    )
parametrs = dbc.Row(
    [

    ]
)

# -----------------------------------------------
# Блок составных элементов
# -----------------------------------------------

# Выпадающий список дат экспериментов
select_dates = dates.to_dict('records')
for i in select_dates:
    i['label'] = i.pop('date')
    i['value'] = i.pop('id')
# print(select_dates)
select_dates.append({'label': '(Выбрать все)', 'value': 'All'})
# select = dcc.Dropdown(
#     id="select",
#     options=select_dates,
#     multi=True,
#     style={'height': 'auto', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '14rem', 'align': 'center'},
#     #style={"background-color": "#2060F5"},
# )



compare_table = html.Div([], id='compare_table')

def C_T(dataf):

    df1 = pd.DataFrame(
        columns=['Дата', 'Точность G', 'Полноста G', 'Точность lG', 'Полноста lG', 'Точность O', 'Полноста O'])
    for i in range(int(dataf.size/4/3)):
        df1.loc[i] = [
                           dataf['date'][3*i],
                           dataf['precision'][3*i+1], dataf['recall'][3*i+1],
                           dataf['precision'][3*i+2], dataf['recall'][3*i+2],
                           dataf['precision'][3*i], dataf['recall'][3*i]
                     ]

        print(df1)

    return df1

# -----------------------------------------------
# Блок работы с матрицами ошибок
# -----------------------------------------------

def confusion_matrix_plot(df_to_plotly):
    df_to_plotly = df_to_plotly.rename(columns={'test_pred': 'Тестовое', 'set_o': 'O', 'set_g': 'G', 'set_lg': 'lG'})
    df_to_plotly.set_index('Тестовое', inplace=True)

    # Максимум выброса в матрице определяем как 120% от класса 'G'. Такова специфика данных
    max_for_outlier_in_statistics = ceil( df_to_plotly['G']['G'].max() * 1.2)
    confuz = []  # Це румынский. Массив выводимых матриц ошибок

    for matrix in df_to_plotly['date'].unique():
        confuz.append(df_to_plotly.loc[df_to_plotly['date'] == matrix])  #

    if len(confuz) % 3 == 0: quantity_x = 3
    elif len(confuz) % 2 == 0: quantity_x = 2
    else: quantity_x = 1
    quantity_y = int(len(confuz) // quantity_x)
    if quantity_y == quantity_x == 1: quantity_x = 2
    fig, ax = plt.subplots(quantity_y, quantity_x, figsize=(8, 3), dpi=240)
    k = 0

    for i in confuz:
        date_temp = str(dates[dates['id'] == i['date']['G']]['date'].values[0])
        print(date_temp)
        i = i.drop(['date'], axis=1)
        sns.heatmap(i, annot=True, cmap='Blues', fmt='g', robust=True, vmax=max_for_outlier_in_statistics, ax=ax[k])
        ax[k].set_title('Спрогнозированные метки на ' + date_temp)
        k += 1

    plt.tight_layout()
    plt.savefig('figura.png', format='png')


