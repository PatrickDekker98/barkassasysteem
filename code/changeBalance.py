from main import *

def raiseBalance(customerId):
    'berekent tijd in epoch, vraagt het huidige balans op van de klant, berekent nieuwe balans. schrijft naar de db.'

    epoch = datetime.datetime(1970, 1, 1)
    i = datetime.datetime.now()

    delta_time = int((i - epoch).total_seconds()) #tijd in epoch

    amountIn = askAmount()

    cursor.execute("SELECT balance FROM customer WHERE customerId = ?", customerId)
    customerBalance = cursor.fetchone()[0]

    newBalance = customerBalance + amountIn

    cursor.execute('INSERT INTO balanceRaising (amount, datetime) VALUES (?,?)', (amountIn, delta_time))
    cursor.execute('UPDATE customer SET balance = ? WHERE customerId = ?', (newBalance, customerId))

    conn.commit()
    conn.close()


def askAmount():
    'fetched de balans verhoging van een GUI entry element'

    amountInput = Entry.get()

    return amountInput