from main import *


def getCategories():
    'Fetches all active categories from the database'
    cursor.execute("SELECT * FROM category WHERE datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()


def getCategory(categoryId):
    'Fetches all information about a particular category from the database, when provided with this categories ID'
    cursor.execute("SELECT * FROM category WHERE categoryId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))", [categoryId])
    return cursor.fetchone()


def getCategoryId(categoryName):
    'Returns a categories ID from the database, when provided with its Name'
    cursor.execute("SELECT categoryId FROM category WHERE name = ?",[categoryName])
    return cursor.fetchone()[0]


def addCategory(name):
    'Adds a new catagory into the database, by name'
    cursor.execute("INSERT INTO category (name) VALUES (?)", [name])
    conn.commit()
    return cursor.rowcount == 1


def updateCategory(categoryId, name):
    'Updates the name of a category by categoryID in the database'
    cursor.execute("UPDATE category SET name = ? WHERE categoryId = ?", [name, categoryId])
    conn.commit()
    return cursor.rowcount == 1


def deleteCategory(categoryId):
    '"Deletes" a productCategory by setting the datetimeEnd to today in the database'
    cursor.execute("UPDATE category SET datetimeEnd = datetime('now', 'localtime') WHERE categoryId = ?", [categoryId])
    conn.commit()
    return cursor.rowcount == 1