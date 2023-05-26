import csv
import pandas as pd
import matplotlib.pyplot as plt

'''
% Model,SPM_1kW_4poles.mph
% Version,COMSOL 6.0.0.318
"% Date,""Aug 5 2022, 17:42"""
% Table,Data NO - Export Data NO
'''

#1-2 пункт
#считвыаем файл и представляем его в виде словаря 
f = open("1kW_4poles_NO.csv")#открыли соединение с файлом
reader = csv.DictReader(f, delimiter=',')
#for row in reader:
#    print(row)

#3 пункт
#df = pd.read_csv("1kW_4poles_NO.csv", error_bad_lines=False) #считываем как обычный DataFrame
df = pd.DataFrame.from_dict(reader) #считываем DataFrame из словаря
#print(df)

#4пункт
CA = pd.pivot_table(df, index='% f (Hz)', columns='Time (s)', values=['Coil current A (A)', 'Coil current C (A)', 'Coil current B (A)'])
#print(CA)

VA = pd.pivot_table(df, index='% f (Hz)', columns='Time (s)', values=['Coil voltage A (V)','Coil voltage C (V)', 'Coil voltage B (V)'])
#print(VA)

AT = pd.pivot_table(df, index='% f (Hz)', columns='Time (s)', values=['Axial torque (N*m)'])
#print(AT)

RL = pd.pivot_table(df, index='% f (Hz)', columns='Time (s)', values=['Rotor Losses (W)', 'Stator Losses (W)', 'Coil Losses (W)'])
#print(RL)

#5пункт
class DataFrameHandler():
    def __init__(self, filename:str, **kwargs) -> None:
        self.df = pd.read_csv("1kW_4poles_NO.csv", **kwargs) #сохранение датафрейма
        self.headers = list(self.df.columns.values) #получаем список названий столбцов
        self.table_time_name = 'Time (s)' #свойство для хранения названия времени
        self.multi = self.df.set_index(self.headers) #создаем мультиндекс
    
    #построение графика по двум столбцам c указанием частоты (пункт 5)
    def draw(self, table_name_x:str, table_name_y:str, hz=None, kind='line') -> None:
        if hz == None:
            self.df.plot(x=table_name_x, y = table_name_y,  kind = kind)
            plt.show()
        else:
            self.df[self.df['% f (Hz)'] == hz].plot(x=table_name_x, y = table_name_y, kind = kind)
            plt.show()

    #среднее значение от времени (пункт 6 a)
    def mean(self, time_start:float, time_stop:float,  table_name:str) -> list:
        results = []
        res1 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 50 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 50) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res2 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 100 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 100) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res3 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 200 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 200) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res4 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 250 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 250) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res5 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 300 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 300) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res6 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 350 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 350) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        res7 = f"Среднее значение по столбцу '{table_name}' за период [{time_start}с - {time_stop}c] c частотой 400 ->" + " " + str(self.df[(self.df['% f (Hz)'] == 400) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].mean())
        results.append(res1)
        results.append(res2)
        results.append(res3)
        results.append(res4)
        results.append(res5)
        results.append(res6)
        results.append(res7)
        print('\n')
        print('-'*40, 'Среднее значение', '-' * 40)
        for element in results:
            print(element)
        print('-'*101)
        print('\n')
        return results

    #интегральная сумма (пункт 6 b) 
    def integral(self, hz:int, time_start:float, time_stop:float,  table_name:str):
        res = self.df[(self.df['% f (Hz)'] == hz) & (self.df[self.table_time_name] >= time_start) & (self.df[self.table_time_name] <= time_stop)][table_name].sum()
        print(f'Интегральная сумма по столбцу {table_name} с частотой {hz} во временном диапазоне [{time_start}c - {time_stop}] ->', res)
        return res
        

data = DataFrameHandler("1kW_4poles_NO.csv")
data.draw(data.table_time_name, 'Coil current A (A)')
data.draw(table_name_x=data.table_time_name, table_name_y='Coil current A (A)', hz=50)

time_start = float(input("Введите время начала: "))
time_stop = float(input("Введите время окончания: "))
table_name = input("Введите имя столбца: ")

res = data.mean(time_start, time_stop, table_name) #вычисляем среднее значение по столбцу


hz = float(input("Введите величину HZ: "))
time_start = float(input("Введите время начала: "))
time_stop = float(input("Введите время окончания: "))
table_name = input("Введите имя столбца: ")

inte = data.integral(hz, time_start, time_stop, table_name) #вычисляем интегральную сумму

f.close() #закрыли соединение с файлом