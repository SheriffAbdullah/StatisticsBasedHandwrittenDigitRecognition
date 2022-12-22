import numpy as np
from main import *

#question part

question='question'

file = '/Users/sheriffabdullah/Projects/StatisticsBasedHandwrittenDigitRecognition/%s.png' % question

dataCropped, top, bottom, left, right = crop(convertImg(file))
compressed = segment(dataCropped, top, bottom, left, right)
divs = noOfDivs

distance = {}
for i in range(10):
    for x in range(1, 9):
        temp = 0
        for j in range(divs):
            for k in range(divs):
                temp+=(compressed[j][k]-trained_data[str(i)+'_'+str(x)][j][k])**2
        temp=np.sqrt(temp)
        # Neurons
        distance[str(i)+'_'+str(x)] = temp 
        print('distance from ',i,':\n',distance[str(i)+'_'+str(x)])
        
least = distance[str(0)+'_'+str(1)]
for i in distance:
    if distance[i] < least:
        least = distance[i]
        
secLeast = distance[str(0)+'_'+str(1)]
for i in distance:
    if distance[i] == least:
        pass
    elif distance[i] < secLeast:
        secLeast = distance[i]
        
for t in distance.items():
    if (t[1] == least):
        print("You wrote:", t[0][0])
        break
    
for t in distance.items():
    if (t[1] == secLeast):
        print("Or maybe:", t[0][0])
        break

'''
correct = input('Correct or not? [1-Correct] & [0-Not]: ')
if correct == 1:
    for i in range(100):
        try: 
            file = '/Users/sheriffabdullah/Projects/StatisticsBasedHandwrittenDigitRecognition/Number Samples/%d/%d_%d.png' % (t[0][0], t[0][0],j)
            convertImg(file)
        except:
            
            
    i = t[0][0]
    j = '/Users/sheriffabdullah/Projects/StatisticsBasedHandwrittenDigitRecognition/Number Samples/%d/%d_%d.png' % (i,i,j)

'''