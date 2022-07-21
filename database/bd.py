import sqlite3 as sql


def createDB():
    conn = sql.connect("BaseDatos.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE publicacion (
        id integer primary key AUTOINCREMENT,
        contenido text,
        listo integer
    )""")
    conn.commit()
    conn.close()


def addValues():
    conn = sql.connect("BaseDatos.db")
    cursor = conn.cursor()
    data = [
        (1, "Hola Mundo", 0)
    ]
    cursor.executemany("""INSERT INTO publicacion VALUES (?, ?, ?)""", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    addValues()
