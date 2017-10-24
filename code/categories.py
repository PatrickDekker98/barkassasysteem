from main import *


def getCategories():
    cursor.execute("SELECT * FROM category WHERE datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()


def getCategory(categoryId):
    cursor.execute("SELECT * FROM category WHERE categoryId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))", [categoryId])
    return cursor.fetchone()

print(getCategory(3))
