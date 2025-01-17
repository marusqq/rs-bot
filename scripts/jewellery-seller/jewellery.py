__author__ = 'Marius'
__script__ = 'for making pizzas'

'''reqs:
take the needed jeweleries and stand near grum in port sarim
start in last world and sort the worlds descending'''

##TODO:
    #1. Improve stock checking speed (somehow)
    #2. Implement dynamic inventory checks
    #3. Implement faster diamond jewellery selling
    #4. Implement selling for 10 [testing]
    #5. Make trading grum faster

import pyautogui as ag
import time 
from os import getcwd, listdir
import random as rn

image_dir = getcwd() + '/pics/'
wait_chance = 0.3 #30%

#Steps:
#1. Find Grum
#   1.1. rightclick him
#   1.2. trade him

#2. Find the right jewellery to sell to him
#   2.1 find any jewelerry that is under 7 stock (under 10 for gold ring / gold necklace / gold amulet)
#   2.2 right click in inventory to sell it

#3. Jump worlds and repeat from #1

image_dir = getcwd() + '/pics/'


jewellery_thingies = ['ring', 'necklace', 'amulet']
shiny_thingies = ['gold', 'sapphire', 'emerald', 'ruby', 'diamond']

used_jew_file = open('used_jewellery.jew', 'r')
jewellery = used_jew_file.readlines()
for jew in reversed(jewellery):
    if '#' in jew:
        jewellery.remove(jew)

new_jewellery  = []
for jew in jewellery:
    new_jewellery.append(jew.rstrip('\n'))
jewellery = new_jewellery

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
    
    if 'grum' in item:
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

def roll_the_dice(image):
    if rn.random() <= wait_chance:
        waiting_time = rn.randint(1,10)
        print('Waiting randomly for', waiting_time, 'before', image)
        time.sleep(waiting_time)

def look_for_grum():

    list = listdir(image_dir + 'findgrum/')
    grum_photos = len(list)
      
    while grum_photos > 0:
        path = 'findgrum/grum' + str(grum_photos) + '.png'
        grum = waitForLoad(path, press = True, clicks = 'rightsingle', output = True, maxLoadTime = 1)

        if grum is not None:
            grum_trade = waitForLoad('trade_grum.png', press = True, clicks = 'leftsingle', output = False, maxLoadTime = 2)
            if grum_trade is None:
                return False
            return True

        grum_photos -= 1

    return False     

def look_for_stock(out = False):
    to_buy = []

    print('Calculating what to sell now... You can have the mouse for now :)')
    #ring, necklace, amulet
    for jewel in jewellery_thingies:
        if out:
            print('looking for', jewel)
        stock_pics = listdir(image_dir + 'stock/' + jewel + '/')
        image_path = 'stock/' + jewel + '/'
        
        for photo in stock_pics:

            item = photo.split('_')
            
            if item[1] + '_' + item[2][:-4] in jewellery:
                if waitForLoad(image_path + photo, press = False, maxLoadTime = 0.1, output=False):
                    if item[1] == 'gold':
                        max_sell = 10
                    else:
                        max_sell = 7
                    
                    to_buy.append(str(max_sell - int(item[0])) + '_' + item[1] + '_' + item[2][:-4])
    
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('Starting to sell in 3 seconds!')
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')

    time.sleep(3)
    
    return to_buy

def sell(items_to_sell):

    for item in items_to_sell:

        if 'ring' in item:
            photo_path = 'stock/rings.png'

        elif 'amulet' in item:
            photo_path = 'stock/amulets.png'

        elif 'necklace' in item:
            photo_path = 'stock/necklaces.png'
        
        column = waitForLoad(photo_path, press = False)
        if column is None:
            quit('robe / hat / robes are not found!')
        custom_left = 20
        
        if 'gold' in item:
            custom_top = 50 
        elif 'sapphire' in item:
            custom_top = 90
        elif 'emerald' in item:
            custom_top = 130
        elif 'ruby' in item:
            custom_top = 160
        elif 'diamond' in item:
            custom_top = 200
        else:
            print('nothing is found! something went bad')
        
        loc = [column.left+custom_left, column.top+custom_top]
        #ag.moveTo(loc, duration = 0.2)
        
        quantity = item.split('_')
        quantity_to_sell(int(quantity[0]), loc)

    return

def quantity_to_sell(quantity, loc):
    
    while quantity > 0:
        ag.moveTo(loc, duration = 0.2)
        ag.click(button = 'right')
        if quantity == 10:
            press = waitForLoad('sell10.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            if press is None:
                waitForLoad('sell10_highlighted.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            quantity -= 10
        elif quantity >= 5:
            press = waitForLoad('sell5.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            if press is None:
                waitForLoad('sell5_highlighted.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            quantity -= 5
        else:
            press = waitForLoad('sell1.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            if press is None:
                waitForLoad('sell1_highlighted.png', press = True, clicks = 'leftsingle', wait_randomly = False)
            quantity -= 1
    return
    
def jump_worlds():

    waitForLoad('exit_store.png', press = True)
    failed_world = 0
    jumped = False

    this_world = waitForLoad('green_world_change.png', press = False)

    while not jumped:
        
        #ag.alert(text='Change the world and press ok', title='', button='OK')
        
        X_button = waitForLoad('exit_store.png', press = False)
        up_arrow = [X_button.left + 6, X_button.top + 41]
        ag.moveTo(up_arrow, duration = 0.2)
        ag.mouseDown()
        ag.click()

        next_world = [this_world.left, this_world.top + 2] #+ failed_world]
        ag.moveTo(next_world, duration = 0.3)
        ag.click()

        if waitForLoad('please_wait.png', press = False) is not None:
            print('jumping worlds!')
            jumped = True
            failed_world = -20

    return 

def info_about_selling(sell):
    print('-------------------------------------')
    print('Selling:')
    for item in sell:
        splitted = item.split('_')
        print(splitted[1].capitalize(), splitted[2] + ':' + splitted[0])
    print('-------------------------------------')

def jewellery_bot():
    
    while True:
        grum_found = False
        while not grum_found:
            grum_found = look_for_grum()

        what_to_sell = look_for_stock(False)
        info_about_selling(what_to_sell)
        sell(what_to_sell)
        jump_worlds()
        time.sleep(2)

    return

jewellery_bot()