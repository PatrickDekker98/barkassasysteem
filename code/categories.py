from main import *


def getCategories():
    cursor.execute("SELECT * FROM category WHERE datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()


def getCategory(categoryId):
    cursor.execute("SELECT * FROM category WHERE categoryId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))", [categoryId])
    return cursor.fetchone()


def addCategory(name):
    cursor.execute("INSERT INTO category (name) VALUES (?)", [name])
    conn.commit()
    return cursor.rowcount == 1


def updateCategory(categoryId, name):
    print(categoryId)
    print(name)
    cursor.execute("UPDATE category SET name = ? WHERE categoryId = ?", [name, categoryId])
    conn.commit()
    return cursor.rowcount == 1


def deleteCategory(categoryId):
    cursor.execute("UPDATE category SET datetimeEnd = datetime('now', 'localtime') WHERE categoryId = ?", [categoryId])
    conn.commit()
    return cursor.rowcount == 1


# print(deleteCategory(4))
# print(getCategories())
