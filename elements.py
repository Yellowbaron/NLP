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
from dataframes import dates, result, confusion_matrix, dataset, word2vec_model, architecture, epochs, accuracy
import seaborn as sns
from math import ceil
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import HBox



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
    "background-color": "#2962ff",
    'margin-right': '0rem',
    'padding-left': '16px'
}
PROGRESS_BAR_STYLE = {
    'height': '24px',
    'font-size': '13pt'
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
            "Открыть легенду классов", id="positioned-toast-toggle", color='light', size="sm", style={'width': '128px'}
        ),
        dbc.Toast(
            '''\nG — событийный триггер — слово, \nиспользованное для упоминания события в тексте.
                \nlG — вспомогательный триггер — для случаев, \nкогда упоминание многословное \n(например, «состоялась встреча»).
                \nO — прочие слова в тексте.
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
                    dbc.Col(dbc.NavbarBrand("Обнаружение событий в тексте", className="ml-2", style={'font-size':'20pt'}), style={'margin-left':'16rem', 'margin-top': '15px', 'margin-bottom': '15px'}, align='center'),
                    dbc.Col(dbc.NavLink(html.Img(src=COLAB_LOGO, height="80px"), href="https://colab.research.google.com/drive/1J7w75A8V1vIXliTsA72HbEbPeWNHJfUw"), align='center'),
                    dbc.Col(dbc.NavLink(html.Img(src=GITHUB_LOGO, height="60px"), href="https://github.com/Yellowbaron/NLP"), align='center', style={'right': '0px'}),
                    dbc.Col(toast, align='center', style={'margin-left':'16px'}),
                ],
                align="start",
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="#2962ff",
    dark=True,
)

# -----------------------------------------------
# Контент обзорной страницы
# -----------------------------------------------

# Donut chart по количеству классов в датасете
def donut_chart(date_for_chart):
    pie = pd.DataFrame(columns=['Класс', 'Кол-во'])
    for index, row in dataset[dataset['date'] == date_for_chart].iterrows():
        if row['class_set'] == 'Всего предложений': count_sentences = row['amount']
        if row['class_set'] != 'G' and row['class_set'] != 'lG' and row['class_set'] != 'O': continue
        pie.loc[index] = [
                               row['class_set'],
                               row['amount'],
                         ]

    donut_dataset = px.pie(pie, values='Кол-во', names='Класс', hole=.7, color='Класс',
                           color_discrete_map={'G': '#37FF0D',
                                               'lG': '#FFAB19',
                                               'O': '#007bff'})
    donut_dataset.update_traces(textinfo='value')
    donut_dataset.update_layout(
                                annotations=[dict(text='Предложений', x=0.5, y=0.55, font_size=16, showarrow=False),
                                             dict(text=count_sentences, x=0.5, y=0.45, font_size=16, showarrow=False)],
                                legend=dict(y=0.5)
                                )
    return donut_dataset

# Точность на тесте
accuracy_last_info = accuracy[accuracy['date'] == accuracy['date'].max()]
accuracy_progress = dbc.Card(
    [
        dbc.CardHeader("Точность на тестсете " + str(accuracy_last_info['name_test'].values[0])),
        dbc.CardBody(
            [
                dbc.Progress(str(accuracy_last_info['accuracy'].values[0]) + '%', value=accuracy_last_info['accuracy'].values[0],
                             style=PROGRESS_BAR_STYLE)
            ]
        ),
    ],
    style={'margin-bottom': '16px'})
# Точность и полнота по классам
accuracy_by_classes = result[result['date'] == result['date'].max()].copy()
accuracy_by_classes.set_index('kind_of_set', inplace=True)
accuracy_by_classes_progress = dbc.Row(
    [
        # Класс G
        dbc.Col([
            dbc.Card(
                [
                dbc.CardHeader("Точность на классе \"G\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['precision']['G']), value=float(accuracy_by_classes['precision']['G'].rstrip('%')),
                                     style=PROGRESS_BAR_STYLE)
                    ]
                ),
                ],
                style={'margin-bottom': '16px'}),
            dbc.Card(
                [
                dbc.CardHeader("Полнота на классе \"G\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['recall']['G']), value=float(accuracy_by_classes['recall']['G'].rstrip('%')),
                                     style=PROGRESS_BAR_STYLE)
                    ]
                ),
                ],
                style={'margin-bottom': '16px'}),
        ]),

        # Класс lG
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader("Точность на классе \"lG\""),  # Подход «один против всех»
                    dbc.CardBody(
                        [
                            dbc.Progress(str(accuracy_by_classes['precision']['lG']),
                                         value=float(accuracy_by_classes['precision']['lG'].rstrip('%')),
                                         style=PROGRESS_BAR_STYLE)
                        ]
                    ),
                ],
                style={'margin-bottom': '16px'}),
            dbc.Card(
                [
                    dbc.CardHeader("Полнота на классе \"lG\""),  # Подход «один против всех»
                    dbc.CardBody(
                        [
                            dbc.Progress(str(accuracy_by_classes['recall']['lG']),
                                         value=float(accuracy_by_classes['recall']['lG'].rstrip('%')),
                                         style=PROGRESS_BAR_STYLE)
                        ]
                    ),
                ],
                style={'margin-bottom': '16px'}),
        ]),

        # Класс O
        dbc.Col([
            dbc.Card(
                [
                dbc.CardHeader("Точность на классе \"O\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['precision']['O']), value=float(accuracy_by_classes['precision']['O'].rstrip('%')),
                                     style=PROGRESS_BAR_STYLE)
                    ]
                ),
                ],
                style={'margin-bottom': '16px'}),
            dbc.Card(
                [
                dbc.CardHeader("Полнота на классе \"O\""),  # Подход «один против всех»
                dbc.CardBody(
                    [
                        dbc.Progress(str(accuracy_by_classes['recall']['O']), value=float(accuracy_by_classes['recall']['O'].rstrip('%')),
                                     style=PROGRESS_BAR_STYLE)
                    ]
                ),
                ],
                style={'margin-bottom': '16px'}),
        ]),

    ],
)

# Контент для обзора
content = html.Div(
    [
        dbc.Row(
                [
                    dbc.Col([
                        accuracy_progress,
                        accuracy_by_classes_progress,
                    ],),

                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("Количество классов в датасете"),
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(figure=donut_chart(dataset['date'].max())),
                                        ]
                                    ),
                                ],
                                # style={'height': 'auto', 'width': '600px'}
                            )
                        ],
                        style={'margin-right': '16px'}
                    ),
                ],
                style={'margin-top': '16px'}
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

# -----------------------------------------------
# Блок составных элементов
# -----------------------------------------------

# Выпадающий список дат экспериментов
select_dates = dates.to_dict('records')
for i in select_dates:
    i['label'] = i.pop('date')
    i['value'] = i.pop('id')

select_dates.append({'label': '(Выбрать все)', 'value': 'All'})

compare_table = html.Div([], id='compare_table')

def comparison_table(dataf):

    df1 = pd.DataFrame(
        columns=['Дата', 'Точность G', 'Полноста G', 'Точность lG', 'Полноста lG', 'Точность O', 'Полноста O'])
    for i in range(int(dataf['date'].size/3)):
        df1.loc[i] = [
                           dates[dataf['date'][3*i] == dates['id']]['date'].values[0][5:],
                           dataf['precision'][3*i+1], dataf['recall'][3*i+1],
                           dataf['precision'][3*i+2], dataf['recall'][3*i+2],
                           dataf['precision'][3*i], dataf['recall'][3*i]
                     ]

    return df1


# -----------------------------------------------
# Блок работы с матрицами ошибок
# -----------------------------------------------

def confusion_matrix_plot(df_to_plotly):
    df_to_plotly = df_to_plotly.rename(columns={'test_pred': 'Истинное', 'set_o': 'O', 'set_g': 'G', 'set_lg': 'lG'})
    df_to_plotly.set_index('Истинное', inplace=True)
    df_to_plotly = df_to_plotly.rename_axis('Предсказанное', axis="columns")

    # Максимум выброса в матрице определяем как 120% от класса 'G'. Такова специфика данных
    max_for_outlier_in_statistics = ceil(df_to_plotly['G']['G'].max() * 1.2)
    confuz = []  # Це румынский. Массив выводимых матриц ошибок

    for matrix in df_to_plotly['date'].unique():
        confuz.append(df_to_plotly.loc[df_to_plotly['date'] == matrix])  #
    size_x, size_y = 8, 3  # Пропорции фигуры из матриц

    if len(confuz) % 3 == 0:
        quantity_x = 3
    elif len(confuz) % 2 == 0:
        quantity_x = 2
    else:
        quantity_x = 1

    quantity_y = int(len(confuz) // quantity_x)
    if quantity_y == quantity_x == 1: quantity_x = 2
    if quantity_y > 1: size_y = size_y * quantity_y
    fig = plt.figure(figsize=(size_x, size_y))
    ax = []
    k = 0
    
    for i in confuz:
        date_temp = str(dates[dates['id'] == i['date']['G']]['date'].values[0])
        i = i.drop(['date'], axis=1)
        ax.append(fig.add_subplot(quantity_y, quantity_x, k+1))
        sns.heatmap(i, annot=True, cmap='Blues', fmt='g', robust=True, vmax=max_for_outlier_in_statistics, ax=ax[k])
        ax[k].set_title(date_temp)
        k += 1

    plt.tight_layout()
    plt.savefig('figura.png', format='png')

# -----------------------------------------------
# Блок работы с матрицами ошибок
# -----------------------------------------------
def subplot_donuts(arrDates):
    print("Я внутри")

    return dcc.Graph(figure=donut_chart(arrDates).update_layout(
        title='Датасет на ' + dates[arrDates == dates['id']]['date'].values[0][5:],
        margin=dict(l=20, r=20, t=5, b=5)),
        style={'width': '33%', 'height': '50%'})