#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind

pd.set_option('display.max_rows', 50) # показывать больше строк
pd.set_option('display.max_columns', 50) # показывать больше колонок

stud = pd.read_csv('C:\\Users\\79082\\Desktop\\датасеты\stud_math.csv')
stud.columns = ['school_abbreviation', 'sex', 'age', 'addres_type', 'family_size', 'parents_status', 'mother_education', 'father_education', 'mother_job', 'father_job','reason_choice_school','guardian'
,'time_to_get_to_school','studytime','failures','schoolsup','famsup','paid_math','extracurricular_activities','nursery ','study_time_granular','higher_education','internet_availability','romantic',
'family_relationship','free_time','time_with_friends','health','absence_from_class','math_exam_scores'] # для удобства, дадим нашим колоннам более понятные имена
stud.head(10) 

#Преобразуем данные по условию задачи

stud.astype({'mother_education': str})
was = [1,2,3,4,0]
to_be = ['4 class', '5-9 class', 'averege-special education or 11 class', 'high education', 'Do not have education']
d = dict(zip(was, to_be))
stud.mother_education = stud.mother_education.replace(d)
stud.head()

stud.astype({'father_education': str})
was = [1,2,3,4,0] 
to_be = ['4 class', '5-9 class', 'averege-special education or 11 class', 'high education', 'Do not have education']
d = dict(zip(was, to_be))
stud.father_education = stud.father_education.replace(d)

stud.astype({'time_to_get_to_school': str})
was = [1,2,3,4] 
to_be = ['<15 мин.', '15-30 мин.', '30-60 мин.', '>60 мин.']
d = dict(zip(was, to_be))
stud.time_to_get_to_school = stud.time_to_get_to_school.replace(d)

stud.astype({'studytime': str})
was = [1,2,3,4] 
to_be = ['<2 часов', '2-5 часов', '5-10 часов', '>10 часов']
d = dict(zip(was, to_be))
stud.studytime = stud.studytime.replace(d)

stud.astype({'family_relationship': str})
was = [1,2,3,4,5] 
to_be = ['very bad', 'bad', 'normal', 'good','very good']
d = dict(zip(was, to_be))
stud.family_relationship = stud.family_relationship.replace(d)

stud.astype({'free_time': str})
was = [1,2,3,4,5] 
to_be = ['very little time', 'little time', 'enough time', 'a lot of time','a lot of time 2 ']
d = dict(zip(was, to_be))
stud.free_time = stud.free_time.replace(d)

stud.astype({'time_with_friends': str})
was = [1,2,3,4,5] 
to_be = ['very little time', 'little time', 'enough time', 'a lot of time','a lot of time 2 ']
d = dict(zip(was, to_be))
stud.time_with_friends = stud.time_with_friends.replace(d)

stud.astype({'health': str})
was = [1,2,3,4,5] 
to_be = ['very bad', 'bad', 'normal', 'good','very good']
d = dict(zip(was, to_be))
stud.health = stud.health.replace(d)


# In[38]:


num_columns = ['absence from class','study_time_granular','failures']#Заполним пропуски в числовых переменных медианной 
#данных переменный , а пропуски в номинативных переменных заменим самым часто встречающимися значениями
math_exam_score=['math_exam_scores']

for column in stud.columns:
    if column in num_columns:
        median_ = stud[column].median()
        stud[column].fillna(value=median_, inplace=True, axis=0)
    elif column in math_exam_score:
        None
    else:
        mode_ = stud[column].mode()[0]
        stud[column].fillna(value=mode_, inplace=True, axis=0)
        


# In[39]:


for column in stud.columns: #Заменяем выбросы на пороговое значение
    if column in num_columns:
        q1 = stud[column].quantile(q = 0.25)
        q3 = stud[column].quantile(q = 0.75)
        for value in stud[column]:
            if value - 2*(stud[column].std()) >= q3:
                value = q3
            elif value + 2*(stud[column].std()) <= q1:
                value = q1


# In[40]:


stud.select_dtypes(include='object').nunique() #Оценим количество уникальных значений для номинативных переменных


# In[41]:


stud.shape
df2 = stud.drop_duplicates()
df2.shape # Проверим наш датафрейм на дубликаты.Дубликаты не обнаружены


# In[42]:


stud.age.hist() # Как мы видим, здесь присутствуют выбросы, но мы не должны их устранять, так как они в условии задачи (15-22)
stud.age.describe()


# In[43]:


stud.failures.hist() #Видим , что подавляющее большинство учащихся не испытывает неудач
stud.failures.describe()


# In[44]:


stud.study_time_granular.hist() 
stud.study_time_granular.describe()


# In[45]:


stud.absence_from_class.hist() 
stud.absence_from_class.describe()


# In[47]:


stud.math_exam_scores.hist() 
stud.math_exam_scores.describe()


# In[34]:


stud.corr() #Проведем корреляционный анализ числовых столбоцов
#Можно сделать следующие выводы
#1.В дата сете присутствуют сильная отрицательная корреляция между переменными :failures и math scores
#2Присутствуют слабокоррелирующие переменные : math scores и absence from class,s
#3. study_time_granular не сильно коррелирует с math_exam_scores


# In[16]:


def get_stat_dif(column):
    cols = stud.loc[:, column].value_counts()
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        if ttest_ind(stud.loc[stud.loc[:, column] == comb[0], 'math_exam_scores'], 
                        stud.loc[stud.loc[:, column] == comb[1], 'math_exam_scores']).pvalue \
            <= 0.05/len(combinations_all): # Учли поправку Бонферони
            print('Найдены статистически значимые различия для колонки', column)
            break
            #С этим пунктом возникли проблемы, не понимаю, почему так много предупреждений.Подскажите пожалуйста)

            


# In[8]:


for col in ['school_abbreviation', 'sex', 'age', 'addres_type', 'family_size', 'parents_status', 'mother_education', 'father_education', 'mother_job', 'father_job','reason_choice_school','guardian'
,'time_to_get_to_school','studytime','schoolsup','famsup','paid_math','extracurricular_activities','nursery ','study_time_granular','higher_education','internet_availability','romantic',
'family_relationship','free_time','time_with_friends']:
    get_stat_dif(col) #Найдены статистически значимые различия для колонки mother_job


# In[ ]:




