# -*- coding: utf-8 -*-
'''

Unit 6 Soft Dev 

To-do list (CRUD)

'''

import pandas as pd
import datetime as dt
import re

task_diary={}

dates={}

"""# Check input function"""

def check_number(a):
  while True:
    user_input=input(a)
    if user_input.isdigit():
      #print('This is a number')
      break
    else:
      print('This was not a number. Please provide a number')
      user_input=input()
      if user_input.isdigit():
        print('This is a number')
        break
  return user_input

def task_create():
  global task_diary
  global dates
  global df
  task_num=int(check_number('Please provide the number of task you would like to add'))
  for i in range(task_num):
    task_title =input('Please enter the title of the task:\n')
    task_description = input('Please enter the description of the task:\n')
    task_date=input('Please enter the date of the task:\n')
    task_time=input('Please provide the time slot of the event:\n')
    task_duration=input('Please provide the duration of the task:\n')
    task_date=task_date+' '+task_time
    task_date=pd.to_datetime(task_date, format='%d-%m-%Y %H:%M')
    task_date_s=task_date.strftime('%d-%b-%y')
    task_status=input('Please enter the status of the event:\n')
    task_id= task_date_s+task_date.strftime('%H%M')
    task_diary.update({task_id:{'Task_Title':task_title.title(),'Description':task_description.title(),'Date':task_date, 'Time Slot':task_time, 'Duration':task_duration,'Flag':task_status.title()}})
    dates.update({task_date_s:task_date})
  df=pd.DataFrame.from_dict(task_diary)
  df=df.T
  return task_diary, dates, df

def task_del():
  global df
  a=input('Please enter the date of the task you would like to delete:\n')
  b=input('Please enter the time of the task you would like to delete:\n')
  c=a+' '+b
  c=pd.to_datetime(c, format='%d-%m-%Y %H:%M')
  s_c=c.strftime('%d-%b-%y%H%M')
  for i in range(len(df.index)):
    if s_c in df.index[i]:
      df=df.drop(df.index[i])
      del task_diary[s_c] # To test
      print('Task deleted')
      break
  return df, task_diary


def task_modify():
  global df
  task_num=input('Please insert the number of the event you would like to modify:') # Number for loop
  task_num=int(task_num)
  for i in range(task_num):
    task_name=input(f'Please insert the name of the event {i+1}:\n')
    task_date=input(f'Please insert the date of the event {i+1}:\n')
    task_time= input(f'Please input the time of the event {i+1}:\n')
    task_date= task_date+ ' '+task_time
    task_date=pd.to_datetime(task_date, format='%d-%m-%Y %H:%M')
    hl=[*task_diary[task_date.strftime('%d%b%y%j%H%M')].keys()]
    task_id=task_date.strftime('%d%b%y%j%H%M')
    aim_task= input(f'Please input the event detail you would like to change among those below:\n{hl}\n')
    if aim_task == 'Start Time' or aim_task == 'Start_Datetime' :
      aim_value= input(f'Please enter the new value for {aim_task} of {task_name} the {task_date} starting at {task_time} as (HH:MM):\n')
      task_diary[task_date.strftime('%d%b%y%j%H%M')].update({'Start Time':aim_value,'Start_Datetime':task_date.strftime('%d-%m-%Y')+''+aim_value})
    elif aim_task == 'End Time' or aim_task == 'End_Datetime' :
      aim_value= input(f'Please enter the new value for {aim_task} of {task_name} the {task_date} starting at {task_time} as (HH:MM):\n')
      task_diary[task_id].update({'End Time':aim_value})
      task_diary[task_id].update({'End_Datetime':task_id+''+aim_value})
    elif task_diary[task_id]['Start_Datetime']>=task_diary[task_id]['End_Datetime']:
      print('Please modify the end time, otherwise it would be incorrect')
      task_diary[task_id].update({aim_task:aim_value})
      print(task_diary[task_id])
      return task_modify()
    elif aim_task=='Date':
      task_diary[task_id].update({aim_task:aim_value})
      task_diary[task_id].update({'Weekday':aim_value.strftime('%A')})
      task_diary[task_id].update({'Start_Datetime':aim_value.strftime('%d-%m-%Y')+''+task_date.strftime('%H:%M')})
    else:
      aim_value= input(f'Please enter the new value for {aim_task} of {task_name} the {task_date} starting at {task_time}:\n')
      task_diary[task_id].update({aim_task:aim_value})
  task_diary[task_id].update({'Expected Duration':task_diary[task_id]['End_Datetime']-task_diary[task_date.strftime('%d%b%y%j%H%M')]['Start_Datetime']})
  print(task_diary[task_id])
  return None

def mark_task():

  global df
  global marked

  a= check_number('How many task would you like to mark as completed ?\n')
  for i in range(int(a)):
    x=input(f'Please provide the date of the event {a} you would like to mark as completed:\n')
    y=input(f'Please provide the time of the event {a} you would like to mark as completed:\n')
    task_id=pd.to_datetime(x+' '+y, format= '%d-%m-%Y %H:%M')
    task_id=task_id.strftime('%d-%b-%y')
    task_diary[task_id].update({'Status':'Completed'})
  marked= {i:h for i,h in zip(task_diary.keys(),task_diary.values()) if h['Status'] == 'Completed'} # Dict comprehension
  marked= pd.DataFrame.from_dict(marked, orient='index')
  print(marked.to_string())
  return marked



task_create()

print(task_diary)

task_del()

print(task_diary)

task_modify()

print(task_diary)
