import sqlite3

con = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = con.cursor()

def insert_to_DB(vase_values):
    string_start = "INSERT INTO website_vase ("
    string_end = ""
    for key, value in vase_values.items():
        string_start += f"{str(key)}, "
        string_end += f"\"{str(value)}\", "
    string_start = string_start[:-2] + ") VALUES ("
    string_end = string_end[:-2] + ")"
    command = string_start + string_end
    cur.execute(command)
    con.commit()

def modify_record(id, vase_values):
    command = "UPDATE website_vase SET "
    for key, value in vase_values.items():
        if len(value) > 0 and key != "VASEID":
            command += f"{key}=\"{value}\", "
    print(list(vase_values.values())[0])
    command = command[:-2] + f" WHERE VASEID=\"{id}\""
    cur.execute(command)
    con.commit()