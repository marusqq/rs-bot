__author__ = 'Marius'
__script__ = 'default'

'''reqs:
fill required stuff for the script'''

import pyautogui as ag
import time 
from os import getcwd
import random as rn

#workflow
#
#
#
#
#
#

image_dir = getcwd() + '/pics/'
pizza_in_one_try = 9
wait_chance = 0.3 #30%

def moveToLocation(click_location, duration, clicks = None):

    ag.moveTo(click_location, duration = duration)

    time.sleep(round(rn.random(),2) + 0.2)

    if clicks is None:
        return click_location
    elif clicks == 'leftsingle':
        ag.click()
    elif clicks == 'leftdouble':
        ag.click(clicks = 2)
    elif clicks == 'rightsingle':
        ag.click(button='right')
    else:
        return 'Cursor moved, but wrong click type string'
        
    return click_location

def waitForLoad(image, item = 'item', press = True, clicks = 'leftsingle', output = False, maxLoadTime = 5):

    roll_the_dice(image)
    
    item = image[:-4]
    
    if item == 'banker_shoulder':
        duration = 0.6
    elif item in ['bank_banker','items_to_bank', 'bucket_of_water']:
        duration = 0.2
    else:
        duration = 0.4

    #wait for the item to load
    if maxLoadTime is not None:
        startTime = time.time()
    if output:
        print ('Loading ' + item)
    while True:
        if maxLoadTime is not None:
            loadingTime = time.time()
            total = loadingTime - startTime
            if int(total) > maxLoadTime:
                print('Failed loading', image)
                quit()
        image_found = ag.locateOnScreen(image_dir+image)
        if image_found is not None:
            if output:
                print (item + ' loaded!' + '\n')
            time.sleep(0.1)
            break
    if press:
        click_loc = moveToLocation(image_found, duration = duration, clicks = clicks)
    return click_loc

def roll_the_dice(image):
    if rn.random() <= wait_chance:
        waiting_time = rn.randint(1,10)
        print('Waiting randomly for', waiting_time, 'before', image)
        time.sleep(waiting_time)

def print_info(script_start_time):

    script_time = time.time()
    seconds_running = round((script_time - script_start_time),2)
    print('---------------------------------------')
    print('Script has been running for', seconds_running, 'seconds')
    print('---------------------------------------')

    if seconds_running > (3600 + 1800):
        quit("Script has passed one and a half hour mark. Quitting...")

    return

#custom functions go below

def bot():
    script_start_time = time.time()
    #set default values for bot


    #start bot
    while True:
        #custom logic here

        print_info(script_start_time)


bot()


