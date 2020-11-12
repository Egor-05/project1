import sqlite3


def fill_func():
    with open('questions.txt') as f:
        lst = f.read().splitlines()
        conn = sqlite3.connect("questions_bd.sqlite")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                          id           INTEGER      PRIMARY KEY AUTOINCREMENT
                                                    UNIQUE,
                          question     VARCHAR,
                          person       VARCHAR (40),
                          picture      VARCHAR (30),
                          answer1      VARCHAR (20),
                          eco_index1   INTEGER,
                          beh_index1   INTEGER,
                          army_index1  INTEGER,
                          money_index1 INTEGER,
                          answer2      VARCHAR (20),
                          eco_index2   INTEGER,
                          beh_index2   INTEGER,
                          army_index2  INTEGER,
                          money_index2 INTEGER
                          )""")
        conn.commit()
        cursor.execute("""DELETE from questions""")
        conn.commit()
        for i in lst:
            cursor.execute("""INSERT INTO questions ( 
                              question,
                              person,
                              picture,
                              answer1,
                              eco_index1,
                              beh_index1,
                              army_index1,
                              money_index1,
                              answer2,
                              eco_index2,
                              beh_index2,
                              army_index2,
                              money_index2)
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", i.split('|'))
        conn.commit()


fill_func()