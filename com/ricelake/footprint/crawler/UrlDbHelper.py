import sqlite3
from cgi import escape

DB_NAME = "sqlite.db"
CHECKED_TABLE_NAME = "checked"
UNCHECKED_TABLE_NAME = "unchecked"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()


def initDB():
    create_table_stmt = "CREATE TABLE IF NOT EXISTS %s (id TEXT);"%CHECKED_TABLE_NAME
    create_index = "CREATE INDEX IF NOT EXISTS idx_id ON %s (id);"%CHECKED_TABLE_NAME
    cur.execute(create_table_stmt)
    cur.execute(create_index)
    conn.commit()
    
    create_table_stmt = "CREATE TABLE IF NOT EXISTS %s (id TEXT);"%UNCHECKED_TABLE_NAME
    create_index = "CREATE INDEX IF NOT EXISTS idx_id ON %s (id);"%UNCHECKED_TABLE_NAME
    cur.execute(create_table_stmt)
    cur.execute(create_index)
    conn.commit()
    
def addToCheckedTable(url):
    cur.execute("INSERT INTO " + CHECKED_TABLE_NAME + " VALUES (\'" + escape(url) + "\')")
    
    
def addToUncheckedTable(url):
    cur.execute("INSERT INTO " + UNCHECKED_TABLE_NAME + " VALUES (\'" + escape(url) + "\')")

def commit():
    conn.commit()
    
def inCheckedTable(url):
    t = (escape(url),)
    result = cur.execute("SELECT * FROM " + CHECKED_TABLE_NAME +" WHERE id=?", t)
    return result.fetchone() != None

def inUnCheckedTable(url):
    t = (escape(url),)
    result = cur.execute("SELECT * FROM " + UNCHECKED_TABLE_NAME +" WHERE id=?", t)
    return result.fetchone() != None

def showCheckedTable():
    result = cur.execute("select * from " + CHECKED_TABLE_NAME)
    for row in result:
        print row
        
def showUnCheckedTable():
    result = cur.execute("select * from " + UNCHECKED_TABLE_NAME)
    for row in result:
        print row

def main():
    initDB()
    sina = "www.sina.com.cn"
    google = "www.google.com"
    dianping = "www.dianping.com"
    showCheckedTable()
    print inCheckedTable(sina)
    addToCheckedTable(sina)
    print inCheckedTable(sina)
    showCheckedTable()
#    conn.commit()
#    addToCheckedTable(dianping)
#    addToCheckedTable(google)
#    addToUncheckedTable([sina])
#    addToUncheckedTable([sina])
    
#    print "checked"
#    showCheckedTable()
#    print "unchecked"
#    showUnCheckedTable()
        
    
if __name__ == "__main__":
    main()


    
        


