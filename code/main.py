import sqlite3 as sql
import tkinter
import datetime

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()


def printGui(message):
    """Print a message in the GUI"""
    print("GUI message:", message)  # print in python console, for now


def inputGui(question):
    """Ask for input in GUI"""
    return input(question)  # use python console input, for now
