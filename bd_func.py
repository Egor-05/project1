import sqlite3


def fill_func():
    with open('questions.txt') as f:
        lst = f.read().splitlines()
        conn = sqlite3.connect("questions_bd.sqlite")
        cursor = conn.cursor()
        for i in lst:
            cursor.execute("""INSERT INTO questions ( 
                              question,
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
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", i.split('|'))
        conn.commit()


fill_func()