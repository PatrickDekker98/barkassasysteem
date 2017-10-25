from main import *


def getCategories():
    cursor.execute("SELECT * FROM category WHERE datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()


def getCategory(categoryId):
    cursor.execute("SELECT * FROM category WHERE categoryId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))", [categoryId])
    return cursor.fetchone()


def deleteCategory(categoryId):
    print(categoryId)
    cursor.execute("UPDATE category SET datetimeEnd = datetime('now', 'localtime') WHERE categoryId = ?", [categoryId])
    return cursor.rowcount == 1


print(deleteCategory(4))
