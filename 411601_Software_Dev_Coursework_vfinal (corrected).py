
'''

Task Management System

This is a task management system enabling users to create and manage tasks effectively.
To use it, please follow the prompts and create an account if you do not already have one.
Additionally you can generate Gantt charts and Calendar views of your tasks after creation 
even load file of a similar format to visualise your tasks and modify them as needed.
'''


# Installations

# pip install timedelta
# pip install calendar-view
# pip install altair

# Imports
import datetime as dt
from datetime import datetime
import re
import pandas as pd
import altair as alt
import time
from dateutil.relativedelta import relativedelta

from calendar_view.calendar import Calendar
from calendar_view.core.event import EventStyles
from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event
import timedelta
import csv

user_journal={}

# A decorator to time a function

def time_this(func):
    def wrapper():
        start_datetime = dt.datetime.now().strftime('%X')
        start_time= time.time()
        print(f'Starting time: {start_datetime}')
        func()
        end_time= time.time()
        print(f'Task time: {end_time - start_time} seconds')
    return wrapper



# Recursion for error handling aim to be a decorator 
# To recall the function until a valid input is provided
# Decorator function

def is_input_valid(func):
  def check_test(*args):
    try:
      d=func(*args)
      return d
    except (ValueError, KeyError):
      print('Please try again with a valid input.')
      return check_test(*args)
  return check_test

# To check whether the input is an integer or not 

@is_input_valid
def is_integer(text):
    number=int(input(text))
    return number

# Error Handling for identifier

@is_input_valid
def check_identifier(a):
    user_input=input(a)
    if user_input.isidentifier():
        return user_input
    else:
        print('This is no a valid identifier\n')
        raise ValueError


# To check for valid date format

@is_input_valid
def check_date_format(txt):
  '''
  This function aims to ensure that the details entered are of a vaild date format.
  If an invalid format is entered the program will notify and raise a ValueError that will recall the function.
  The function is recalled via a decorator that will continue to request until a valid input is entered.
  '''
  pattern_1= re.compile(r'\d{2}-\d{2}-\d{4}')
  pat_1= '%d-%m-%Y'
  pattern_2= re.compile(r'\d{2}/\d{2}/\d{4}')
  pat_2= '%d/%m/%Y'
  user_input= input(txt)
  if pattern_1.search(user_input):
    user_input=datetime.strptime(user_input, pat_1)
    return user_input.strftime(pat_1)
  elif pattern_2.search(user_input):
    user_input=datetime.strptime(user_input, pat_2)
    return user_input.strftime(pat_2)
  else:
    print('\nThis is not an expected format.\n')
    user_input=pd.to_datetime(user_input, dayfirst = True)
    user_input= user_input.strftime(pat_1)
    print(f'However, it has been reported as {user_input}')
    date_check= input('Is this the correct date ? Please answer with Yes or No')
    if date_check == 'Yes':
      return user_input
    else:
      raise ValueError

# To check for valid datetime format 

@is_input_valid #Modified
def check_endtime(y):
  '''
  This function aims to ensure that the details entered are of the right datetime or time format and prevents the operation to failed due to invalid input.
  As long as the input differs from the recorded pattern the program will request for a valid input.
  '''

  pattern_1= re.compile(r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}')
  pattern_2= re.compile(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}')
  pattern_3= re.compile(r'\d{2}:\d{2}')
  pattern_4= re.compile(r'\d{2}:\d{2} (A|P)M')
  user_input=input(y)
  
  if pattern_1.search(user_input) or pattern_2.search(user_input):
    user_input=pd.to_datetime(user_input, dayfirst = True)
    return user_input.strftime('%d-%m-%Y %I:%M %p')
  
  elif pattern_3.search(user_input) or pattern_4.search(user_input):
    user_input=pd.to_datetime(user_input, dayfirst = True)
    return user_input.strftime('%I:%M %p')
  
  elif 'h' in user_input and len(user_input) <=5:
      r=user_input.find('h')+1
      if r == len(user_input):
        user_input=user_input+'00'
        return user_input
      return user_input
  else:
       print('This is not the right format. Please enter a valid input')
       raise ValueError

# Account creation

def create_account():

  global user_journal
  global user_df

  name=input('Please provide your full name:\n')
  user=check_identifier('Please provide your username:\n')
  password=check_identifier('Please provide your password:\n')
  user_journal.update({name:{'Username':user, 'Password':password}})
  user_df= pd.DataFrame.from_dict(user_journal, orient='index')
  user_list= 'user_list.csv'
  with open(user_list, 'w') as f_:
    f_.write(user_df.to_csv(index=True))
    
  return authentication()


# To check whether the event is a time slot or deadline

@is_input_valid
def event_nature(text):
    
    user_input=input(text)

    if user_input == 'TS' or user_input == 'Time Slot' or user_input == 'Ts':
      user_input = 'TS'
      return user_input
    
    elif user_input == 'D' or user_input == 'Deadline' or user_input == 'd':
      user_input = 'D'
      return user_input
    
    else:
      print('This was not a valid input. Please try again.')
      raise ValueError


# Authentication process

def authentication():

  i=0

  global user_df
  global full_name

  try:

    user_df = pd.read_csv('user_list.csv', index_col=0)

    while True:

      user = check_identifier('Please provide your username:\n')
      password = check_identifier('Please provide your password:\n')

      if (user, password) in zip(user_df['Username'],user_df['Password']):
        full_name = user_df.loc[user_df['Username']==user].index.astype(str).tolist()
        full_name = full_name[0]
        print(f'Welcome back {full_name} !')
        return full_name, main() 
      elif i == 2:
        print('You have reached the maximum number of attempts. Please try again later:\n')
        break
      else:
        print('Invalid credentials')
        i += 1
  except (NameError, FileNotFoundError):
      print('\nNo account with the given credentials have been found. Please create an account first\n')
      return create_account()



def deco_manual(func):
  def deco_man():
          '''
  Hello World

  This is a function for a task management system that aims to facilitate the creation of tasks through user inputs

  Here you may find some useful information regarding the use of the function and it capabilities

  Please note that some of the inputs have to be in a specific format such as dates, times or frequency

  Dates should be in the format DD-MM-YYYY

  Times must be in the format HH:MM

  Frequency must be in a format N number of frequency and frequency type D or W

  For instance 2D for every 2 days and 3W for every three weeks

  Please mind the format of all inputs as it could significantly change results

  '''
          func()
          return None
  return deco_man


#A decorator to save and update both dataframe and csv files

def save_dataframe():
  global df
  global journal_task
  global f
  global journal_title
  global full_name
  global file_name
  df = pd.DataFrame.from_dict(journal_task, orient='index')
  df = df.sort_values(by='Start_Datetime', ascending=True)
  df = df.rename(columns={'Name' : 'Task'})
  file_name = f'{full_name}_{journal_title}.csv'
  with open(file_name, 'w') as f:
    f.write(df.to_csv(index = True))
  return df, main()
    



# Task creation as a function without classes
# A bit long but works fine for organisation and readability I have used classes

def task_create():

  global journal_task
  global journal_title
  global dates
  global df
  global f

  print('Task creation')
  journal_task, dates={},{}

  journal_title=input('Please provide the title of the journal:\n')
  task_num=is_integer('Please insert the number of events you would like to create:\n')
  i=1
  for i in range(task_num):
    task_name=input(f'Please insert the name of the event {i+1}:\n')
    task_nature= event_nature(f'Please clarify whether the event {i+1} is a time slot (with TS)  or a deadline (with D) :\n')
    if task_nature =='TS':
      task_start_date=check_date_format(f'Please insert the date of the event {i+1}:\n')
      task_time= check_endtime(f'Please enter the start time of the event {i+1}:\n')
    else:
      task_start_date=dt.datetime.now().strftime('%d-%m-%Y')
      task_time=dt.datetime.now().strftime('%I:%M %p')
    task_duration= check_endtime(f'Please enter the expected duration of the event {i+1} or the end date and time in format (DD-MM-YYYY HH:MM):\n')
    task_location=input(f'Please provide the location of the event {i+1}:\n')
    task_urgency=input(f'Please enter the urgency of the event {i+1}:\n')
    task_category=input(f'Please enter the category of the event {i+1}:\n')
    task_frequency= input(f'Please enter the frequency of {task_name} as \'(number)D\' for every number of days or \'(number)W\' for week frequency (like every n week) :\n')
    task_start_date= task_start_date+' '+task_time
    task_start_date=pd.to_datetime(task_start_date, format='%d-%m-%Y %I:%M %p', dayfirst = True)
    if len(task_duration)>5:
      task_duration=pd.to_datetime(task_duration, format='%d-%m-%Y %I:%M %p', dayfirst = True)
      task_end_time= task_duration
      task_end_date= task_duration
      task_duration= task_end_time-task_start_date
      task_duration= f'{task_duration.days} days'
    else:
      task_dur_time= task_duration.split('h')  # Splitting hours and minutes to determine end time
      task_dur_time= dt.timedelta(hours=int(task_dur_time[0]), minutes=int(task_dur_time[1]))
      task_end_time= task_start_date + task_dur_time
      task_end_date= task_end_time
      task_end_time= task_end_time.strftime('%I:%M %p')
    s_task_date= task_start_date.strftime('%d-%m-%Y')
    dates.update({s_task_date:task_start_date}) # Probably not needed
    task_id= task_start_date.strftime('%d %B %Y %I:%M %p')
    journal_task.update({task_id:{'Date':s_task_date,'Weekday':task_start_date.strftime('%A'),'Task':task_name,
                                  'Start Time':task_time,'End Time':task_end_time,'Expected Duration':task_duration,
                                  'Location':task_location, 'Urgency':task_urgency, 'Category':task_category, 'Start_Datetime': task_start_date, 'End_Datetime':task_end_date,'Nature':task_nature, 'Status':'Due'}})
    time_limit=dt.datetime.now()+relativedelta(months=12) # add a request for time limit or reduce the limit
    time_limit=pd.to_datetime(time_limit, format='%d-%m-%Y', dayfirst = True)
    if task_frequency!='0':
      if 'W' in task_frequency:
        event_frq=pd.date_range(start=task_start_date, end=time_limit, freq=task_frequency+'-'+task_start_date.strftime('%a'))
      elif 'D' in task_frequency:
        event_frq=pd.date_range(start=task_start_date, end=time_limit, freq=task_frequency)
      for d in event_frq:
        dates.update({d.strftime('%d-%m-%Y'):d})
        task_end_date= d+task_dur_time
        task_id= d.strftime('%d %B %Y %I:%M %p')
        journal_task.update({task_id:{'Date':d.strftime('%d-%m-%Y'),'Weekday':d.strftime('%A'),'Task':task_name,
                                    'Start Time':task_time,'End Time':task_end_time,'Expected Duration':task_duration,
                                    'Location':task_location, 'Urgency':task_urgency, 'Category':task_category,
                                      'Start_Datetime':d,'End_Datetime':task_end_date, 'Nature':task_nature,'Status':'Due'}})
  return journal_task, journal_title, save_dataframe()


# Classes for Task creation of time slot task

class TaskManager_TSi:
    def __init__(self):
        self.name = input('Please insert the name of the event :\n')
        self.start_date = check_date_format('Please insert the date of the event:\n')
        self.start_time = check_endtime('Please enter the start time of the event:\n')
        self.duration = check_endtime('Please enter the expected duration of the event '
                                      'as HHhMM like 1h30 :\n')
        self.location = input('Please provide the location of the event:\n')
        self.description = input('Please enter the urgency of the event:\n')
        self.category = input('Please enter the category of the event:\n')
        self.recurrence = input(f'Please enter the frequency of {self.name} as \'(number)D\' '
                                'for every number of days or \'(number)W\' for week frequency (like every n week) :\n')
        self.nature = 'TS'
        self.status = 'Due'

    def calculate_end_time(self):
        '''
        Docstring for calculate_end_time
        
        :param self: Start_Datetime and Duration
        '''
        self.start_datetime = pd.to_datetime((' ').join([self.start_date, self.start_time])
                             , format = '%d-%m-%Y %I:%M %p', dayfirst = True)
        self.dur_time = self.duration.split('h')  # Splitting hours and minutes to determine end time
        self.dur_time = dt.timedelta(hours = int(self.dur_time[0]), minutes = int(self.dur_time[1]))
        self.end_time = self.start_datetime + self.dur_time
        self.end_date = self.end_time
        self.end_datetime = self.end_time.strftime('%d-%m-%Y %H:%M')
        self.end_time = self.end_time.strftime('%I:%M %p')
        self.end_date = self.end_date.strftime('%d-%m-%Y %I:%M %p')
        del self.dur_time


# Classes for Task creation of a task with a deadline

class TaskManager_DLi():
    def __init__(self):
        self.name = input(f'Please insert the name of the event :\n')
        self.start_date= datetime.now().strftime('%d-%m-%Y %I:%M %p')
        self.start_time= datetime.now().strftime('%I:%M %p')
        self.duration = check_endtime(f'Please enter the expected duration of the event'
                                      ' or the end date and time in format (DD-MM-YYYY HH:MM):\n')
        self.location = input(f'Please provide the location of the event:\n')
        self.description = input(f'Please enter the urgency of the event:\n')
        self.category = input(f'Please enter the category of the event:\n')
        self.recurrence = '0'
        self.nature = 'D'
        self.status='Due'

    def calculate_duration(self):
        '''
        Docstring for calculate_duration
        
        :param self: Duration
        '''
        self.duration=pd.to_datetime(self.duration, format='%d-%m-%Y %I:%M %p', dayfirst = True)
        self.start_datetime= datetime.now()
        self.end_time= self.duration
        self.end_date= self.duration.strftime('%d-%m-%Y')
        self.end_datetime= self.end_time.strftime('%d-%m-%Y %H:%M')
        self.duration= self.end_time-self.start_datetime
        self.end_time= self.end_time.strftime('%I:%M %p')
        self.duration= f'{self.duration.days} days'


@deco_manual
def task_creation():
  '''
  This function creates a journal of task events based on user input in regards to the nature of the event being a time slot or deadline.
  Additionally, it allow for frequent events to be created based on user defined recurrence and time limit.
  Results are provided in a dictionary and dataframe format for further processing with a decorator.
  '''

  global journal_task
  global journal_title
  global df
  global file_name
  global f

  journal_title=input('Please provide the title of the journal:\n')
  task_num=is_integer('Please insert the number of events you would like to create:\n')
  journal_task= {}

  for i in range(task_num):

      task_nature= event_nature(f'Please clarify whether the event {i+1} is a time slot (with TS)  or a deadline (with D) :\n')
      
      if task_nature == 'TS':
          task= TaskManager_TSi()
          tsk_dict = task.calculate_end_time()
      else:
          task= TaskManager_DLi()
          tsk_dict = task.calculate_duration()

      tsk_dict = task.__dict__
      tsk_id= task.start_datetime.strftime('%d%b%y%I%M%p')
      tsk_start_datetime = task.start_datetime.strftime('%d-%m-%Y %H:%M')
      journal_task.update({tsk_id:{k.title():v.title() for k,v in tsk_dict.items() if isinstance(v,str)}})
      journal_task[tsk_id].update({'Start_Datetime':tsk_start_datetime})
      

      if task.recurrence != '0':
          n_limit = int(input(f'Please insert the upper range of the event {task.name}'))
          time_limit = datetime.now()+relativedelta(months=n_limit) # add a request for time limit or reduce the limit
          time_limit = pd.to_datetime(time_limit, format='%d-%m-%Y', dayfirst = True)
          if 'W' in task.recurrence:
              event_frq = pd.date_range(start=task.start_datetime, end=time_limit, freq=task.recurrence+'-'+task.start_datetime.strftime('%a'))
          elif 'D' in task.recurrence:
              event_frq = pd.date_range(start=task.start_datetime, end=time_limit, freq=task.recurrence)
          for d in event_frq:
              tsk_id = d.strftime('%d%b%y%I%M%p')
              task.start_date= d.strftime('%d-%m-%Y')
              tsk_dict = task.calculate_end_time()
              tsk_dict = task.__dict__
              tsk_start_datetime = task.start_datetime.strftime('%d-%m-%Y %H:%M')
              journal_task.update({tsk_id:{k.title():v.title() for k,v in tsk_dict.items() if isinstance(v,str)}})
              journal_task[tsk_id].update({'Start_Datetime':tsk_start_datetime})
  return journal_task, journal_title, save_dataframe()




def task_add():

  '''
  This function adds tasks to an existing journal of task if existing
  '''

  global journal_task
  global full_name
  global file_name
  global journal_title
  global df 
  global f

  try: # Checking first if the variable exist
    journal_task
    journal_title
    df
    full_name
    print('Here we can see the current journal output: \n')
    print(df.to_string(index=True)+ '\n')
  except NameError: # Otherwise
     return task_creation()


  task_num = is_integer('Please insert the number of events you would like to create:\n')

  for i in range(task_num):

      task_nature= event_nature(f'Please clarify whether the event {i+1} is a time slot (with TS)  or a deadline (with D) :\n')
      
      if task_nature == 'TS':
          task = TaskManager_TSi()
          tsk_dict = task.calculate_end_time()
      else:
          task = TaskManager_DLi()
          tsk_dict = task.calculate_duration()

      tsk_dict = task.__dict__
      tsk_id = task.start_datetime.strftime('%d%b%y%I%M%p')
      tsk_start_datetime = task.start_datetime.strftime('%d-%m-%Y %H:%M')
      journal_task.update({tsk_id:{k.title():v.title() for k,v in tsk_dict.items() if isinstance(v,str)}})
      journal_task[tsk_id].update({'Start_Datetime':tsk_start_datetime})
      
      if task.recurrence !='0':
          n_limit = int(input(f'Please insert the upper range of the event {task.name}'))
          time_limit = datetime.now() + relativedelta(months = n_limit) # add a request for time limit or reduce the limit
          time_limit = pd.to_datetime(time_limit, format='%d-%m-%Y', dayfirst = True)
          if 'W' in task.recurrence:
              event_frq = pd.date_range(start=task.start_datetime, end=time_limit, freq=task.recurrence+'-'+task.start_datetime.strftime('%a'))
          elif 'D' in task.recurrence:
              event_frq = pd.date_range(start=task.start_datetime, end=time_limit, freq=task.recurrence)
          for d in event_frq:
              tsk_id = d.strftime('%d%b%y%I%M%p')
              task.start_date= d.strftime('%d-%m-%Y')
              tsk_dict = task.calculate_end_time()
              tsk_dict = task.__dict__
              tsk_start_datetime = task.start_datetime.strftime('%d-%m-%Y %H:%M')
              journal_task.update({tsk_id:{k.title():v.title() for k,v in tsk_dict.items() if isinstance(v,str)}})
              journal_task[tsk_id].update({'Start_Datetime':tsk_start_datetime})
  return journal_task, journal_title, save_dataframe()
  


def gantt():

  global df
  global journal_task
  global full_name
  global journal_title

  df1 = df[df['Nature']=='D'].copy()
  df1['Start_Datetime'] = pd.to_datetime(df1['Start_Datetime'], format='%d-%m-%Y %H:%M', dayfirst=True)
  df1['End_Datetime'] = pd.to_datetime(df1['End_Datetime'], format='%d-%m-%Y %H:%M', dayfirst=True)
  df1 = df1[['Start_Datetime','Task','End_Datetime', 'Nature']].copy()

  # Gantt Chart

  gantt_chart = alt.Chart(df1).mark_bar().encode(
      x = alt.X('Start_Datetime', title='Date'),
      x2 = 'End_Datetime',
      y = alt.Y('Task', title='Project Task'),
      color = alt.Color('Task'),
      tooltip = ['Task', 'Start_Datetime','End_Datetime']
  ).properties(
      title = 'Project Gantt Chart',
      width = 700,
      height = 400
  )

  gantt_chart.save(f'{journal_title}_gantt_chart.png')

  return gantt_chart, main()



def detailed_events():

  '''
  This function rearrange events details to be compatible with calendar view package
  '''

  global df
  global ly
  global ddates
  global dd


  print('Detailed events')

  ly = []                                 # List of events made in a compatible format for calendar view
  dd = []                                 # Compatible date range format for calendar view no more than 2 weeks
  ts_df = df[df['Nature'] == 'Ts'].copy()
  datetime_format = '%d-%m-%Y %H:%M'
  ts_df['Start_Datetime'] = pd.to_datetime(ts_df['Start_Datetime'], format = datetime_format, dayfirst = True)
  start_date = ts_df['Start_Datetime'].iloc[0]

  tf = df[['Start_Time','End_Time']].copy()
  tf['Start_Time'] = pd.to_datetime(tf['Start_Time'], format='%I:%M %p')
  tf['End_Time'] = pd.to_datetime(tf['End_Time'], format='%I:%M %p')

  print('Almost there...')

  tf['Start_Time'] = tf['Start_Time'].dt.strftime('%H:%M')
  tf['End_Time'] = tf['End_Time'].dt.strftime('%H:%M')
  ts_df['Start_Time'] = tf['Start_Time'].copy()
  ts_df['End_Time'] = tf['End_Time'].copy()
  
  dd.append(start_date.strftime('%d-%m-%Y'))
  added_time = dt.timedelta(days=14)
  end_date = start_date + added_time
  dd.append(end_date.strftime('%d-%m-%Y'))
  ts_df = ts_df[ts_df['Start_Datetime'] <= end_date].copy()
  ddates = ' - '.join(dd)

  print('About to finish...')
  
  for i in range(len(ts_df)):
    title, day, start, end= (ts_df['Task'].iloc[i], ts_df['Start_Datetime'].iloc[i].date(), ts_df['Start_Time'].iloc[i], ts_df['End_Time'].iloc[i])
    ly.append(Event(title, day=day, start=start, end=end))
  
  print('Done correcting event window')

  return ly, config_calendar()



def config_calendar():

  '''
  This function configures the calendar view based on user task journal details
  '''

  global df
  global ly
  global ddates
  global dd

  print('Config calendar')


  config=data.CalendarConfig(
  lang='en',
  title=journal_title,
  dates= ddates,
  show_year=True,
  mode= 'day_hours',
  legend=False
  )
  data.validate_config(config)
  data.validate_events(ly, config)
  calendar=Calendar.build(config)
  calendar.add_events(ly)
  calendar.save(f'{full_name}\'s_calendar.png') # Save Calendar view as png file
  print('\n\nThe calendar view of the first two weeks of tasks has been successfully saved as a png file.\n')
  return main()



def task_del():

  ''' Delete task function '''

  global df
  global journal_task
  global full_name
  global journal_title

  try:
    df
    print(df)
  except:
    raise NameError
  
  del_date = check_date_format('\nPlease enter the date of the task you would like to delete:\n') # Delete event not day yet
  del_time = check_endtime('\nPlease enter the time of the task you would like to delete:\n')
  del_datetime = del_date+' '+del_time
  del_datetime = pd.to_datetime(del_datetime, dayfirst = True)
  del_id = del_datetime.strftime('%d%b%y%I%M%p')

  print(del_id)

  df = df.drop(index = del_id)
  del journal_task[del_id]
  print('\n\nTask deleted')
  print(df)
  print(journal_task)
  
  with open('full_task_list.csv', 'w') as full_:
     full_.write(full_df.to_csv(index=True))

  return journal_task, df, save_dataframe()



def mark_task():

  ''' This function marks task as completed '''

  global journal_task
  global journal_title
  global df
  global file_name
  global marked
  global f
  global full_df

  num = is_integer('\nHow many task would you like to mark as completed ?\n')

  for i in range(num):
    x = check_date_format(f'Please provide the date of the event {i+1} you would like to mark as completed:\n')
    y = check_endtime(f'Please provide the time of the event {i+1} you would like to mark as completed:\n')
    g = x + ' ' + y
    task_id = pd.to_datetime(g, dayfirst = True)
    task_id = task_id.strftime('%d%b%y%I%M%p')
    journal_task[task_id]['Status']='Completed'

  marked = {i:h for i,h in journal_task.items() if h['Status'] == 'Completed'} # Dict comprehension for storing marked tasks
  marked = pd.DataFrame.from_dict(marked, orient = 'index')

  print('\n\nPlease see the task marked as completed below:\n')
  print(marked.to_string())
  print(f'\n{file_name} has been updated at {dt.datetime.now().strftime('%X')}\n')

  with open(f'{full_name}_marked_tasks.csv', 'w') as m_:
     m_.write(marked.to_csv(index=True))

  full_df = pd.DataFrame.from_dict(journal_task, orient = 'index')
  print(full_df.to_string())

  with open('full_task_list.csv', 'w') as full_:
     full_.write(full_df.to_csv(index=True))

  return journal_task, marked, full_df, save_dataframe()



def task_modify():

  ''' This function modifies existing task details'''

  global df
  global journal_task
  global full_df

  task_num=input('Please insert the number of the event you would like to modify:') 
  task_num=int(task_num)

  for i in range(task_num):

    task_name = input(f'Please insert the name of the event {i+1}:\n')
    task_date = check_date_format(f'Please insert the date of the event {i+1}:\n')
    task_time = check_endtime(f'Please input the time of the event {i+1}:\n')
    task_date = task_date + ' ' + task_time
    task_date = pd.to_datetime(task_date, dayfirst = True)
    hl = [*journal_task[task_date.strftime('%d%b%y%I%M%p')].keys()]
    task_id = task_date.strftime('%d%b%y%I%M%p')
    aim_task= input(f'Please input the event detail you would like to change among those below:\n{hl}\n')
    aim_value = input(f'Please enter the new value for {aim_task} of {task_name} the {task_date} starting at {task_time}:\n')
    journal_task[task_id].update({aim_task:aim_value})
  full_df = pd.DataFrame.from_dict(journal_task, orient = 'index')
  with open('full_task_list.csv', 'w') as full_:
     full_.write(full_df.to_csv(index=True))
  print(full_df.to_string())

  return journal_task, df, full_df, save_dataframe()



def deco_deco(func):
    def dec_dec():
        print('''
        Welcome to the task management system!\n
        Here are your options:\n
        1. Create
        2. Add
        3. Modify
        4. Delete
        5. View
        6. Mark as Completed
        7. Download Gantt Chart for Deadlines
        8. Download Calendar View for Time Slot Activities
        9. Load file
        10. Exit
              ''')
        func()
    return dec_dec


def main_return(func):
  def back2_main():
    try:
      d=func()
      return d, main()
    except (FileNotFoundError, OSError):
      print('\nNo file found. Please create a task first or upload a file.\n')
    except NameError:
      print('\nNo task found. Please create a task first.\n. ')
      return main()
  return back2_main



@main_return
def view():
   global df

   print('\nPlease see the last events recorded:\n')
   print(df.to_string())
   return None

# Allow for exit

def exit_prg(func):
  def exit_opt(*args):
    c = func(*args)
    if c == 'exit':
      d=input('Are you sure about exiting the program? Please answer with Yes or No.\n')
      if d == 'Yes':
        exit()
      else:
         return c
  return exit_opt



def load_file():
   
   ''' Loading file function '''
   
   global df
   global journal_title
   global journal_task
   global full_name
   global file_name
   global f

   try:
      name_df = input('Please insert the name of the file you would like to upload (without .csv extension)\n')
      df = pd.read_csv(name_df+'.csv', index_col=0, parse_dates=['Start_Datetime', 'End_Datetime'], dayfirst=True)
      
      journal_title = 'loaded'
      journal_task = df.to_dict(orient='index')
      
      print('File loaded successfully.\n')

      print(df.to_string())
      
      return journal_task, journal_title, save_dataframe()
   except FileNotFoundError:
      print('File not found. Please try again.\n')
      raise FileNotFoundError
   except OSError:                                                               # Deals with other file I/O related errors
      print('An error occured please check the format of the file and content before trying again.\n')
      raise OSError
      


@is_input_valid
@deco_deco
@exit_prg
def main():
  menu_opt= input('What would you like to do ? E.g. You can \'create\', \'add\', \'modify\', \'view\' or \'delete\' from a task management system.\n>_')
  match menu_opt:
    case 'Create' | 'create' | '1':
      task_creation()
    case 'Add' | 'add' | '2':
      task_add()
    case 'Modify' | 'modify' | '3':
      task_modify()
    case 'Delete' | 'delete' | '4':
      task_del()
    case 'View' | 'view' | '5':
      view()
    case 'Mark' | 'mark' | '6':
      mark_task()
    case 'Gantt Chart' | 'gantt chart' | '7':
        gantt()
    case 'Calendar View' | 'calendar view'| '8':
        detailed_events()
    case 'Load file'| 'load file' | '9':
      load_file()
    case 'Exit' | 'exit'| '10':
      menu_opt='exit'
      return menu_opt
    case _:                                    # Catch-all other cases
      print('This is not a valid option')
      raise ValueError


@is_input_valid
@exit_prg
def task_management():
  print(''' 
        Please create an account if you do not already have one to access the task management system.\n
        Here are your options:
         1. Create Account
         2. Log In
         3. Exit
         ''')
  
  initial= input(f'Please choose among the options available in the menu above:\n')
  
  if initial == '1' or initial=='create':
     return create_account()
  
  elif initial == '2' or initial=='log in':
     return authentication()
  
  elif initial == '3' or initial=='exit' or initial=='Exit' :
     if initial == '3':
        initial = 'exit'
     return initial
  
  else:
    print('This is not a valid option. Please try again.\n')
    raise ValueError


#import this

task_management()
