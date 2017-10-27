#from main import *

def write2csv(telegramId, msg):
    'schrijft telegram ID en bericht weg naar een CSV file'

    import csv

    with open('telegramBerichten.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow([telegramId, msg])
