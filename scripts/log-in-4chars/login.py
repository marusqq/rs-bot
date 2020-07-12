__author__ = 'Marius'
__script__ = 'for logging 4 accounts'

import base64
import pyautogui as ag
import time 
from os import getcwd, listdir, path
import random as rn
import encode

SCREENS = 4

image_dir = getcwd() + '/pics/'

def moveToLocation(click_location, duration, clicks = None):

    ag.moveTo(click_location, duration = duration)

    time.sleep(round(rn.random(),2) + 0.2)
    if clicks is None:
        return click_location
    elif clicks.lower() == 'leftsingle':
        ag.click()
    elif clicks.lower() == 'leftdouble':
        ag.click(clicks = 2)
    elif clicks.lower() == 'rightsingle':
        ag.click(button='right')
    else:
        print('Cursor moved, but wrong click type string')
        return 'NAN'
        
    return click_location

def waitForLoad(image, item = 'item', press = True, clicks = 'leftsingle', output = False, maxLoadTime = 5, crash_if_not_found = False, wait_randomly = False):

    if wait_randomly:
        roll_the_dice(image)
    
    item = image[:-4]
    
    if item == 'trade_grum':
        duration = 0.1
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
                if output:
                    print('Failed loading', image)
                if crash_if_not_found:
                    quit()
                else:
                    return None

        image_found = ag.locateOnScreen(image_dir+image)

        if image_found is not None:
            if output:
                print (item + ' loaded!' + '\n')
            time.sleep(0.1)
            break
    if press:
        click_loc = moveToLocation(image_found, duration = duration, clicks = clicks)
    else:
        click_loc = image_found

    return click_loc

if not path.exists(getcwd() + '\logins.pass') or not path.exists(getcwd() + '\passwords.pass'):
    print('No logins.pass or passwords.pass in script dir')
    quit()
    
file_users = open(getcwd() + '\logins.pass', 'r')
file_passw = open(getcwd() + '\passwords.pass', 'r')

users = file_users.readlines()
passw = file_passw.readlines()

for i in range(len(users)):
    ok = waitForLoad('ok.png', press = True, crash_if_not_found = False)
    if ok is None:
        waitForLoad('existing.png', press = True, crash_if_not_found = False)

    ag.write(encode.decode(users[i].strip('\n')), interval = 0.25)
    ag.hotkey('enter')

    ag.write(encode.decode(passw[i].strip('\n')), interval = 0.25)
    ag.hotkey('enter')

print('Enjoy =)')
    #encode.decode(users[i].strip('\n'))
    #encode.decode(passw[i].strip('\n'))
    




