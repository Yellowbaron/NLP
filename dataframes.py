'''
    Модуль ответственный за обработку данных из SQL

'''

import pandas as pd
import sqlite3
from sqlite3 import Error
import pandas as pd
from datetime import datetime, date, time
from sqlalchemy import create_engine


sqlite3.paramstyle = 'named'  # Возможность использовать переменные в запросе
engine = create_engine("sqlite:///experimental_results.db")  # Подключаемся к локальной БД

# -----------------------------------------------
# Маппинг БД
# -----------------------------------------------

result_dict = {
    'kind_of_set': 'На множестве',
    'precision': 'Точность',
    'recall': 'Полнота'
}
confusion_matrix_dict = {
    'test_pred': "test \ pred",
    'set_o': "O",
    'set_g': "G",
    'set_lg': "lG"
}
dataset_dict = {
    'class_set': 'Класс',
    'amount': 'Кол-во'
}
word2vec_model_dict = {
    'model': 'Модель'
}
architecture_dict = {
    'hyperparameters': "Слои/Гиперпараметры",
    'major_characteristic': "Количество элементов(нейронов/контейнеров)",
    'minor_characteristic': "Хар-ка"
}
epochs_dict = {
    'class_epoch': "Эпоха",
    'numeric_characteristic': "Число",
    'val_acc': "val acc",
    'val_loss': "val loss",
    'acc': "val acc",
    'loss': "loss"
}
accuracy_dict = {
    'name_test': 'Название теста',
    'accuracy': 'Точность'
}

# ----------------------------------------------------------------------
# Обработка данных из SQL в pandas.DataFrame
# Так как данных априори не юудет много, загрузим их все в датафреймы
# ----------------------------------------------------------------------

dates = pd.read_sql_query('SELECT * FROM experiments', con=engine)
result = pd.read_sql_query('SELECT date, kind_of_set, precision, recall FROM result', con=engine)
confusion_matrix = pd.read_sql_query('SELECT date, test_pred, set_o, set_g, set_lg FROM confusion_matrix', con=engine)
dataset = pd.read_sql_query('SELECT date, class_set, amount FROM dataset', con=engine)
word2vec_model = pd.read_sql_query('SELECT date, model FROM word2vec_model', con=engine)
architecture = pd.read_sql_query('SELECT date, hyperparameters, major_characteristic, minor_characteristic FROM architecture', con=engine)
epochs = pd.read_sql_query('SELECT date, class_epoch, numeric_characteristic, val_acc, val_loss, acc, loss FROM epochs', con=engine)
accuracy = pd.read_sql_query('SELECT date, name_test, accuracy FROM accuracy', con=engine)

select_dates = dates.to_dict('records')
for i in select_dates:
    i['label'] = i.pop('date')




