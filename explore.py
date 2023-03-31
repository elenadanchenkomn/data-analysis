import pandas as pd
df = pd.read_csv('data.csv',encoding='1251')
df.tail(3)
pd.describe_option()
pd.set_option('display.max_info_columns' , 40)
pd.set_option('display.float_format','{:.2f}'.format)
columns = ['DR_Dat','DR_Tim', 'DR_NChk', 'DR_NDoc', 'DR_Apt','DR_CDrugs','DR_Kol','DR_CZak', 'DR_CRoz','DR_SDisc', 'DR_TPay','DR_CDrugs', 'DR_Suppl','DR_CDisc','DR_BCDisc',
         'DR_TabEmpl','DR_VZak', 'DR_Pos']
df = df[columns]
df.columns=['dt','c_time', 'nchk', 'ndoc', 'apt','drug','kol','zak', 'roz','disc', 'pay_type','drug_id', 'suppl','disc_id','disc_barcode',
         'empl','vzak', 'pos']
#меняем тип данных столбца
df['disc_barcode'] = df['disc_barcode'].astype('str').replace('\.0', '' , regex=True)
#выводим типы данных df.dtypes
df['disc_id'] = df['disc_id'].astype('str').replace('\.0', '' , regex=True)
#приведение к формату date //df['dt'] = pd.to_datetime(df['dt']).dt.day_of_year(сколько дней )
df['dt'] = pd.to_datetime(df['dt']).dt.strftime('%d.%m.%Y')
#возвращает уникальные значения //df['vzak'].unique()
df['vzak'] = df['vzak'].astype('str').replace('1' , 'обычный ').replace('2' , 'интернет')
#оценивает количество пропусков // df.isna().any()//fillna(0)Заменит пустые значения 0 ?//dropna()удалит пустые строки
#dropna(axis=1) удалит столбцы в которых содержаться пустые ячейки
#df.info() покажет весь датафрейм (сколько строк, есть ли пропуски,типы данных)

# ОПИСАТЕЛЬНЫЕ СТАТИСТИКА
#df.describe() покажет количество строк,процентиль,отклонение,макс,мин,медиану(50% процентиль) по всем столбцам
print(df.describe())
#категориальные переменные
print(df['pay_type'].value_counts())
#выводим номер аптеки и количество платежей
print(df.apt.value_counts())
#тоже самое но в процентах
print(df.apt.value_counts(normalize=True))

#распределение количества позиций в чеке
#уникальное количество позиций в чеке
print(df.pos.unique())
print(df.pos.value_counts())
#строим гистограмму
df.pos.hist(bins=24)

#корреляция между переменными
import seaborn as sns
#выводит тепловую карту
sns.heatmap(df.corr())
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 6))
sns.heatmap(df.corr(), vmax=1, vmin=-1, annot=True)
plt.rcParams['figure.figsize'] = (16, 6)
#создаем новый столбец который  будет содержать только часы
df['hour'] = pd.to_datetime(df.c_time).dt.hour
#сколько позиций было продано в течении одного часа
gr = df.groupby(['hour'])['kol'].agg(sum)
sns.boxplot(gr)

#посчитать агригатные характеристики с разбивкой по чекам
a = df.groupby(['dt', 'nchk'])['kol', 'roz', 'zak'].agg({
    'kol': sum, 
    'roz': ['sum', 'max'],
    'zak': sum
})
a.reset_index()

#считаем прибыль за каждую дату по сотрудникам
b = df.groupby(['dt', 'empl'])['zak', 'roz'].agg(sum)
# создаем сстолбец с прибылью
b['revenue'] = b['roz'] - b['zak']
df.groupby(['dt', 'empl'])['zak', 'roz', 'kol'].apply(lambda x: sum(x['kol']*(x['roz'] - x['zak'])))

#оцениваем связь между обьемом продаж и рознечной ценой с разбивкой по датам
import numpy as np
df.groupby(['dt', 'drug'])['roz', 'kol'].agg({
    'roz': np.mean, 
    'kol': sum
})
#округляем рознечную сумму
df['rroz'] = df.roz.apply(lambda x: round(x, -2))
с = df.groupby(['dt', 'rroz'])['kol'].agg(sum).reset_index()
с = с[с.loc[:, 'rroz'] < 2000]

sns.scatterplot(x=a['rroz'], y=a['kol'], hue=a.dt)
sns.jointplot(x=a['rroz'], y=a['kol'], hue=a.dt)
# оцениваем переменные с помощью сводных таблиц
#количество продаж в каждый день в каждой аптеке и по каждому сотруднику с разбивкой по видам платежа
b = df.groupby(['dt', 'apt', 'empl', 'pay_type'])['kol'].agg(sum).reset_index()
#создаем сводную таблицу
b.pivot_table(values='kol', index=['dt', 'apt', 'empl'], columns=['pay_type'])
c = df.pivot_table(values='roz', index=['dt', 'apt', 'empl'], columns=['pay_type'], aggfunc=sum)
c = c.reset_index()
pd.melt(c, id_vars=['dt', 'apt', 'empl'], value_vars=[15, 18], var_name='p_type')
df[(df['kol'] > 5) & (df['roz'] > 50)]
df[~df.loc[:, 'pay_type'].isin([15, 20])]
d ={
    'Обычный': 'Simple',
    'Интернет': 'Web'
}

df['vzak'].map(d)
