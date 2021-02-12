'''
    Модуль ответственный за обработку функций обратных вызовов

'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import layouts
import dash_bootstrap_components as dbc
import pandas as pd

from elements import compare_table,  create_table_from_DF
from layouts import compare
from dataframeCheck import result


