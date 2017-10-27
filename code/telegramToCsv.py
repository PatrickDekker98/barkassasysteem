# De functie in dit script schrijft het telegram ID
# en het betreffende bericht naar een CSV bestand
# ~ Nico van Bentum

from main import *

def write2csv(telegramId, msg):
    '''neemt een telegramID en een bericht, opent en write TeleGramBerichten.csv,
    schrijft id en bericht naar tel~.csv'''

    import csv

    with open('telegramBerichten.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow([telegramId, msg])
