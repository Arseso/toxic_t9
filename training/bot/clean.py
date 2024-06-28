import os
import psycopg2 as pg

cur = None


def get_data() -> list:
    global cur
    con = pg.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"))

    con.autocommit = True
    cur = con.cursor()
    cur.execute("SELECT id, sequence FROM data WHERE checked = FALSE")
    return cur.fetchall()


def interface(data: list) -> None:
    for idx, text in data:
        print("Is a valid sentence? [y/n]: {}".format(text))
        if input().lower() == "y":
            cur.execute("UPDATE data SET checked = TRUE WHERE id = {}".format(idx))
        else:
            cur.execute("DELETE FROM data WHERE id = {}".format(idx))


if __name__ == "__main__":
    interface(get_data())
