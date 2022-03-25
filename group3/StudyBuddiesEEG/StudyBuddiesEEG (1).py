"""

Created on Tue Sep 07 16:35:57 2021

@author: sburrovskij Leonardo Bonetti, Francesco Carlomagno

leonardo.bonetti@clin.au.dk

"""

#################### YOUR DIRECTORY TO BE UPDATED BEFORE RUNNING THE SCRIPT ####################
#logdir = ('/home/stimuser/Desktop/PatternRecognition_Leonardo/Data_collection_nov_2020') #THIS IS YOUR DIRECTORY WHERE YOU PUT THE PROVIDED FOLDERS, PLEASE UPDATE THIS, THANKS
#logdir = ('/home/stimuser/Desktop/TempSeqAges')
logdir=('C:/Users/stimuser/Desktop/CognNeuroSci-Undervisning/2022/group3/StudyBuddiesEEG') 


#################### Load libraries and set directories ####################
import random
from random import shuffle
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import visual, core, sound, event, gui, monitors , logging
import itertools as it
import os
import numpy as np
import csv

# uncomment this if you need to use it in the MEG
from triggers import setParallelData
### setParallelData(0)

frate = 120 #60 #FREQUENCY RATE OF THE COMPUTER (I DON'T REMEMBER IF IT REFERS TO THE SCREEN OR THE AUDIO OR SOMETHING ELSE THOUGH.. 60 OR 120 REFERS TO THE STIMULUS COMPUTER IN THE MEG ROOM
prd = 1000/frate #CONVERSION IN MS

#################### Actual codes ####################

# quit key
def quitpd():
    logging.flush()
    core.quit()
event.globalKeys.add(key='escape',func=quitpd,name='shutdown')

#GUI for subject ID
ID = gui.Dlg(title = 'subj ID')
ID.addField('ID: ')
subID = ID.show()

#create csv file for log
filename = logdir + '/csv_files/Subj_' + subID[0] + '_Block_5_Visual.csv'
if os.path.exists(filename):
    print('THE FILE NAMED ' + 'Subj_' + subID[0] + '_Block_5_Visual.csv' + ' ALREADY EXIST!! PD')
else:
    logfile = open(filename,'w')
    logfile.write("subj;trial;response;RT \n")

    
    #create log file
    block_time = core.Clock()
    logging.setDefaultClock(block_time)
    filename = logdir + '/log_files/Subj_' + subID[0] +  '_Block_5_Visual.log'
    lastLog = logging.LogFile(filename, level=logging.INFO, filemode='a')
    
    # VECTOR SECTION
    old1 = (2,5,9,7,1)
    old1r = [[2,5,9,7,1]]
    #old2 = (9,3,1,6,4)
    new1t1 = [[2,1,4,5,9],[2,1,7,3,5],[2,1,3,5,8],[2,1,9,6,7],[2,3,4,8,6],[2,3,1,7,6],[2,3,5,8,4],[2,3,7,5,9],[2,4,5,6,1],[2,4,6,7,3],[2,4,7,8,5],[2,4,8,9,6],[2,5,4,7,9],[2,5,1,8,3],[2,5,9,4,7],[2,5,6,7,3],[2,6,8,5,4],[2,6,3,1,8],[2,6,1,9,5],[2,6,5,8,4],[2,7,3,5,6],[2,7,5,6,1],[2,7,6,9,3],[2,7,8,1,9],[2,8,5,1,4],[2,8,6,3,5],[2,8,1,7,3],[2,8,4,9,7],[2,9,7,1,3],[2,9,8,5,1],[2,9,3,6,7]]
    new1t3 = [[2,5,9,1,3], [2,5,9,1,4], [2,5,9,1,6], [2,5,9,1,7], [2,5,9,1,8], [2,5,9,3,1], [2,5,9,3,4], [2,5,9,3,6], [2,5,9,3,7], [2,5,9,3,8], [2,5,9,4,1], [2,5,9,4,3], [2,5,9,4,6], [2,5,9,4,7], [2,5,9,4,8], [2,5,9,6,1], [2,5,9,6,3], [2,5,9,6,4], [2,5,9,6,7], [2,5,9,7,1], [2,5,9,7,3], [2,5,9,7,4], [2,5,9,7,6], [2,5,9,8,1], [2,5,9,8,3], [2,5,9,8,4], [2,5,9,8,6], [2,5,9,0,1], [2,5,9,0,3], [2,5,9,0,4], [2,5,9,0,6]]

    rnd = random.sample(range(90),90) # Generate a random order for the new trial without repetition
    oldf = old1r * 20
    oldy = old1r * 30
    trig = []
    trig = oldf + new1t1 + new1t3 # empty list for all the stimuli
    trigy = oldy + new1t1 + new1t3

    
    #initializing RT variable to get RTs
    RT = core.Clock()
    block_time = core.Clock() #this should not be useful anymore..
    
    #preparing window for the screen
    win = visual.Window(fullscr = True, color = 'black')
    playlear = visual.TextStim(win,text = 'You will watch 1 sequence of numbers, repeated 20 times. \n\n Please try to memorize the sequence as much as you can. \n\n After each presentation, imagine the sequence in your mind. \n\n Press 1 to continue', color = 'white')
    playlear.draw()
    win.flip()
    
    event.waitKeys()
    fix_c = visual.TextStim(win,text = '+', color = 'white',height = 0.2)

    #LEARNING PHASE
    for muu in range (20):
        playlear = visual.TextStim(win,text = 'Trial number '+ str(muu + 1) + ' / 20', color = 'white')
        playlear.draw()
        win.flip()
        core.wait(1)
        for wavve, number in enumerate(old1):
            playlear = visual.TextStim(win,text = old1[wavve], color = 'white', height= 0.5)
            playlear.draw()
            win.callOnFlip(setParallelData, (wavve+1) * 10 + number + 100) #SENDING TRIGGER (TO MEG) #### (*!!!*) 10?????? 110-120-130-140-150
            #win.callOnFlip(print, (wavve+1) * 10 + number + 100) # FOR LOCAL TESTING
            win.flip()
            core.wait(0.35)
            playlear.draw()
            win.flip()
            core.wait(0.05)
            win.callOnFlip(setParallelData, 0)
            playlear.draw()
            win.flip()
            core.wait(0.30)
        win.flip()
        core.wait(1)
        core.wait(0.35)
        logging.flush()           
        playlear = visual.TextStim(win,text = 'Imagine', color = 'white',height = 0.2)
        playlear.draw()
        win.callOnFlip(setParallelData, 6)
        win.flip()
        core.wait(0.05)
        win.callOnFlip(setParallelData, 0)
        playlear.draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(5) 
    
    logfile.write("recognition \n")
    
    pausemex = visual.TextStim(win,text = 'Now you have a 20-second break \n\n You can relax :D', color = 'white')
    pausemex.draw()
    win.flip()
    core.wait(20)
    
    playrec = visual.TextStim(win,text = 'You will watch 90 sequences of numbers. \n\n For each sequence, press 1 if it is the sequence that you previously memorized, press 2 if it is a new sequence. \n\n Press 1 to continue', color = 'white')
    playrec.draw()
    win.flip()
    event.waitKeys()
    
    # Recognition phase 
    for bau in range (90):
        playlear = visual.TextStim(win,text = 'Trial number '+ str(bau + 1) + ' / 90', color = 'white')
        playlear.draw()
        win.flip()
        core.wait(1)
        if trigy[rnd[bau]] == old1r[0]:
            trs = True
        else:
            trs = False
        for wavve, number in enumerate(old1): # enumerate instead?? nummer (0-4) og number (id for tal). wave*10+number
            if wavve == 0:
                event.clearEvents(eventType='keyboard')
                RT.reset() # getting RTs only after the last dot.. if participants respond before the end of the numerical  sequence, their response will be still recorded and the RTs will be of about 1800ms (which corresponds to the end of the 5th number)
            # playlear = visual.TextStim(win,text = new1t1[rnd[bau]][wavve], color = 'white', height= 1.5)
            playlear = visual.TextStim(win,text = trigy[rnd[bau]][wavve], color = 'white', height= 0.5)
            if trs == True:
                win.callOnFlip(setParallelData, (wavve+1)*10+number) #SENDING TRIGGER (TO MEG)
            else:
                win.callOnFlip(setParallelData, (wavve+1)*10+number+150)
            playlear.draw()
            win.flip()
            core.wait(0.05)
            win.callOnFlip(setParallelData, 0)
            playlear.draw()
            win.flip()
            core.wait(0.30)
            if wavve == 0:
                win.callOnFlip(setParallelData, 0) #ENDING THE TRIGGER
                win.callOnFlip(print, 0) #ENDING THE TRIGGER (PRINTED VERSION FOR TESTING WITH LOCAL COMPUTER)  
        logging.flush()           
        # Declaring some list and variables for the loop
        rt = 0
        #event.clearEvents(eventType='keyboard')
        #RT.reset()
        resp = None
        while resp == None:
            fix_c.draw()
            win.flip()
            key = event.getKeys(keyList = ['1','2']) # Just 1 or 2 for old and new
            if len(key) > 0:
                rt = RT.getTime()
                resp = key[0][0]
            elif RT.getTime() > 2: # 2 seconds of maximum wait if subject does not reply (this is after the sound was played)
                resp = 'None'
                rt = RT.getTime()    
        logging.flush()           
        #writing RT, trial ID, subject's response
        lrow = '{};{};{};{}\n'
        lrow = lrow.format(subID[0],trigy[rnd[bau]], resp, round(rt*1000))
        logfile.write(lrow)
        core.wait(2)
    logfile.close()

#    
    #final message
    playlear = visual.TextStim(win,text = 'Thank you very much!', color = 'white')
    playlear.draw()
    win.flip()
    event.waitKeys(keyList = 'space')

####################
