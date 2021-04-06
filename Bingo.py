import csv
import random
import time
import os
from os import path
from PIL import Image, ImageDraw, ImageFont

def is_legal(ignore_list=[], checkee=[]):
    for x in ignore_list:
        if checkee.count(x) > 0:
            return False
    return True

def get_data(settings):
    dataarr = []
    headers = None
    ignored = get_setting_value(settings, 'Ignored').split(' ')
    filename = get_setting_value(settings, 'DataLocation')

    with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            line_count = 0
            for row in reader:
                line_count += 1
                if line_count == 1:
                    headers = row
                elif is_legal(ignored, row):
                    dataarr.append(row)

    return (dataarr, headers)

def draw_board(settings, entries=[]):
    width = get_setting_value(settings, 'ImageWidth')
    height = get_setting_value(settings, 'ImageHeight')
    padding = (get_setting_value(settings, 'PaddingX'), get_setting_value(settings, 'PaddingY'))
    offset = (get_setting_value(settings, 'OffsetX'), get_setting_value(settings, 'OffsetY'))
    boxsize = (get_setting_value(settings, 'BoxSizeX'), get_setting_value(settings, 'BoxSizeY'))

    img = Image.new('RGB', (width + padding[0], height + padding[1]), color=(get_setting_value(settings, 'BackGroundColorR'),get_setting_value(settings, 'BackGroundColorG'),get_setting_value(settings, 'BackGroundColorB')))
    if path.exists(get_setting_value(settings, 'CenterImage')):
        freeimg = Image.open(get_setting_value(settings, 'CenterImage'), 'r')
        freeimg.thumbnail(boxsize)
        img.paste(freeimg, (2 * boxsize[0] + offset[0] + boxsize[0] // 13, 2 * boxsize[1] + 75 + offset[1] - boxsize[1] // 2))

    d = ImageDraw.Draw(img)

    fontFound = False
    if path.exists(get_setting_value(settings, 'Font')):
        fontFound = True
        fnt = ImageFont.truetype(get_setting_value(settings, 'Font'), size=get_setting_value(settings, 'FontSize'))

    runnum = 0
    for x in range(0, 5):
        for y in range(0, 5):
            if fontFound:
                d.text((x * boxsize[0] + boxsize[0] // 2 + offset[0], y * boxsize[1] + boxsize[1] // 2 + offset[1]), entries[runnum], fill=(get_setting_value(settings, 'FontColorR'),get_setting_value(settings, 'FontColorG'),get_setting_value(settings, 'FontColorB')), font= fnt, align='center', anchor='mm')
            else:
                d.text((x * boxsize[0] + boxsize[0] // 2 + offset[0], y * boxsize[1] + boxsize[1] // 2 + offset[1]), entries[runnum], fill=(get_setting_value(settings, 'FontColorR'),get_setting_value(settings, 'FontColorG'),get_setting_value(settings, 'FontColorB')), align='center', anchor='mm')

            runnum += 1

    for x in range(0, 6):
        d.line([(0 + offset[0], x * boxsize[1] + offset[1]), (width + offset[0], x * boxsize[1] + offset[1])], fill=(get_setting_value(settings, 'LineColorR'),get_setting_value(settings, 'LineColorG'),get_setting_value(settings, 'LineColorB')), width=get_setting_value(settings, 'LineWidth'))

    for x in range(0, 6):
        d.line([(x * boxsize[0] + offset[0], 0 + offset[1]), (x * boxsize[0] + offset[0], height + offset[1])], fill=(get_setting_value(settings, 'LineColorR'),get_setting_value(settings, 'LineColorG'),get_setting_value(settings, 'LineColorB')), width=get_setting_value(settings, 'LineWidth'))

    if fontFound:
        d.text(( (width + padding[0]) / 2, offset[1] / 2), get_setting_value(settings, 'Title'), fill=(get_setting_value(settings, 'FontColorR'),get_setting_value(settings, 'FontColorG'),get_setting_value(settings, 'FontColorB')), font= fnt, align='center', anchor='mm')
    else:
        d.text(( (width + padding[0]) / 2, offset[1] / 2), get_setting_value(settings, 'Title'), fill=(get_setting_value(settings, 'FontColorR'),get_setting_value(settings, 'FontColorG'),get_setting_value(settings, 'FontColorB')), align='center', anchor='mm')

    return img

def swapPositions(listt, pos1, pos2):
    listt[pos1], listt[pos2] = listt[pos2], listt[pos1]
    return listt

def reshuffle_board(data=[]):
    random.shuffle(data)
    return swapPositions(data, 12, data.index(' '))

def get_indicies(use_last_run=True, data_amount=25):
    if use_last_run and path.exists('lastrun.txt'):
        file = open('lastrun.txt', 'r', encoding='utf-8')
        aslist = file.readline().split(' ')
        file.close()
        return map(int, aslist)

    rannums = list(range(0, data_amount))
    random.shuffle(rannums)
    rannums = rannums[:25]
    savethis = rannums

    file = open('lastrun.txt', 'w', encoding='utf-8')
    file.write(' '.join(map(str, savethis)))
    file.close()

    return rannums

def is_integer(number):
    try: 
        int(number)
        return True
    except ValueError:
        return False

def load_settings():
    if path.exists('settings.txt'):
        file = open('settings.txt', 'r')
        settingslines = file.readlines()
        settings = []
        for x in settingslines:
            if not x.startswith('#') and len(x) > 2:
                settings.append(x.split('='))
        
        return settings
    elif path.exists('defaultsettings.txt'):
        file = open('defaultsettings.txt', 'r')
        settingslines = file.readlines()
        settings = []
        for x in settingslines:
            if not x.startswith('#') and len(x) > 2:
                settings.append(x.split('='))
        
        return settings

def get_setting_value(settings=[], name=''):
    for x in settings:
        if x[0] == name and is_integer(x[1]):
            return int(x[1])
        elif x[0] == name:
            return x[1].strip()
    
    return -1

def main():
    settings = load_settings()
    data = get_data(settings)
    dataarr = data[0]

    rannums = get_indicies(get_setting_value(settings, 'UseLastRun') == 1, len(dataarr))

    randomentries = []

    # Shuffle the entries
    runnum = 0
    for x in rannums:
        runnum += 1
        if runnum != 13:
            randomentries.append(dataarr[x][0])
        else:
            randomentries.append(' ')

    # Ensure 10 chrs per line
    runnum = 0
    for x in randomentries:
        if len(x) > 10 and len(x) <= 20:
            x = x[:10] + '\n' + x[10:]
        elif len(x) > 20 and len(x) <= 30:
            x = x[:10] + '\n' + x[10:20] + '\n' + x[20:]
        elif len(x) > 30:
            x = x[:10] + '\n' + x[10:20] + '\n' + x[20:30] + '\n' + x[30:]
        
        randomentries[runnum] = x
        runnum += 1

    identifier = int(time.time())

    if not path.exists('generated'):
        os.mkdir('generated')

    for x in range(0, get_setting_value(settings, 'Count')):
        draw_board(settings, reshuffle_board(randomentries)).save('generated/' + str(identifier) + 'board' + str(x) + '.jpg', 'JPEG')

if __name__ == '__main__':
    main()