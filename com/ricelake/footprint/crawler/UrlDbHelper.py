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
    if not inCheckedTable(url):
        cur.execute("INSERT INTO " + CHECKED_TABLE_NAME + " VALUES (\'" + escape(url) + "\')")
    
    
def addToUncheckedTable(url):
    if not inUnCheckedTable(url):
        cur.execute("INSERT INTO " + UNCHECKED_TABLE_NAME + " VALUES (\'" + escape(url) + "\')")
        
def deleteFromCheckedTable(url):
    t = (escape(url),)
    cur.execute("DELETE  FROM " + CHECKED_TABLE_NAME + " WHERE id=?", t)

def deleteFromUnheckedTable(url):
    t = (escape(url),)
    cur.execute("DELETE  FROM " + UNCHECKED_TABLE_NAME + " WHERE id=?", t)

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
    count = 0
    for row in result:
        count += 1
        print row
    print "totally " + str(count) + " tuples"
        
def showUnCheckedTable():
    result = cur.execute("select * from " + UNCHECKED_TABLE_NAME)
    for row in result:
        print row

def main():
    initDB()
    sina = "www.sina.com.cn"
    google = "www.google.com"
    dianping = "www.dianping.com"
    print "before add"
    showCheckedTable()
    
    print "after add"
    addToCheckedTable(sina)
    addToCheckedTable(sina)
    addToCheckedTable(sina)
    addToCheckedTable(google)
    showCheckedTable()
    
    print "after delete"
    deleteFromCheckedTable(sina)
    showCheckedTable()
    
    commit()
    
    
if __name__ == "__main__":
    main()


    
        


