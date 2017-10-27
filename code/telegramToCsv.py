#from main import *

def write2csv(telegramId, msg):
    'Writes a telegram ID and the message to a CSV file'

    import csv

    with open('telegramBerichten.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow([telegramId, msg])
