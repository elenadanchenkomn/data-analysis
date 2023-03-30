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
print(df.dtypes)
