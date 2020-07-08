__author__ = 'Marius'
__script__ = 'for making pizzas'

'''reqs:
set the default bank deposit value to 9,
have pizzas, buckets of water in bank
also dont use the fullscreen version'''

import pyautogui as ag
import time 
from os import getcwd
import random as rn

#workflow
#1. banker
    #1.0 open bank
    #   if not the first time: put items to bank
    #1.1 take flour
    #1.2 take water
    #1.3 close bank

#2. inventory
    #2.1 press on flour
    #2.2 press on water
    #2.3 press space
    #2.4 wait for finish

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
    
    


def bank(deposit):
    waitForLoad('banker_shoulder.png', clicks = 'rightsingle')
    #ag.click(x = 1291, y = 2633, button = 'right')
    waitForLoad('bank_banker.png', clicks = 'leftsingle')

    if deposit:
        waitForLoad('items_to_bank.png', clicks = 'leftsingle')

    bucket = waitForLoad('bucket_of_water.png', clicks = 'leftsingle')
    time.sleep(round(rn.random(),2) * 1.5 + 0.3)
    flour_loc = [bucket.left-50, bucket.top]
    ag.moveTo(flour_loc, duration = 0.2)
    ag.click(flour_loc)

    #waitForLoad('flour.png', clicks = 'leftsingle')

    waitForLoad('close_bank.png', clicks = 'leftsingle')

    return True

def make_pizza():

    bucket = waitForLoad('bucket_of_water_inventory.png', clicks = 'leftsingle')
    time.sleep(round(rn.random(),2) * 1.5 + 0.3)
    
    flour_loc = [bucket.left+50, bucket.top+10]
    ag.moveTo(flour_loc, duration = 0.2)
    ag.click(flour_loc)
    
    
    time.sleep(round(rn.random(),2) + 0.9)
    waitForLoad('pizza.png', clicks = 'leftsingle')

    time.sleep(round(rn.random(),2) + 7.2)

    return

def print_info(script_start_time, pizzas):

    pizzas += pizza_in_one_try
    script_time = time.time()

    print('---------------------------------------')
    print(pizza_in_one_try,'new pizza pads formed and deposited to bank.')
    print(pizzas, 'farmed in this session.')
    print('Script has been running for', round((script_time - script_start_time),2), 'seconds')
    print('---------------------------------------')

    return pizzas


def pizza_bot():
    deposit = False
    script_start_time = time.time()
    pizza_count = 0
    while True:
        deposit = bank(deposit)
        make_pizza()
        pizza_count = print_info(script_start_time, pizza_count)


pizza_bot()


