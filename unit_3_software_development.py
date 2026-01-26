
'''
Unit 3 Software Development
Area of a Figure
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

''' Calculating the area of a figure with a user input function '''

def area_fig():
  number_fig= int(input('Please provide the number of figures you would like to calculate the area :\n'))
  for i in range(number_fig):
    fig=input('\nPlease name the figure you would like to calculate the area:')
    if fig =='rectangle':
      print('\nPlease input the width and length, respectively:')
      w,l=input(),input()
      w,l=float(w),float(l)
      area = w*l
    elif fig=='triangle':
      print('\nPlease input the base and height of the triangle, respectively:')
      h,b=input(), input()
      h,b=float(h),float(b)
      area= (h*b)/2
    print(f'The area of the {fig} is {area}')
  return area

area_fig()