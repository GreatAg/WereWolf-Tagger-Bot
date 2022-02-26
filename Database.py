import psycopg2

conn = psycopg2.connect(host=##, database=##, user=##, password=##)

c = conn.cursor()

# c.execute("""CREATE TABLE activegps (
#             groupid int
#             )""")


# conn.commit()
#
# conn.close()

def getactivegaps():
    with conn:
        c.execute("SELECT groupid FROM aliag_db.taggergps")
        return c.fetchall()


def activegap(chat_id):
    chat_id = int(chat_id)
    with conn:
        c.execute(f"SELECT groupid FROM aliag_db.taggergps WHERE groupid = {chat_id}")
        isthere = len(c.fetchall())
    if isthere == 0:
        with conn:
            c.execute(f"INSERT INTO aliag_db.taggergps VALUES ({chat_id})")
            return "Group added to database seccesfully🟢"
    else:
        return "Group has been activated before!"


def deactivegap(chat_id):
    chat_id = int(chat_id)
    with conn:
        c.execute(f"SELECT groupid FROM aliag_db.taggergps WHERE groupid = {chat_id}")
        isthere = len(c.fetchall())
    if isthere != 0:
        with conn:
            c.execute(f"DELETE FROM aliag_db.taggergps WHERE groupid = {chat_id}")
        return "Group remove from database seccesfully🔴"
    else:
        return "Group isn\'t active!"


def isactive(chat_id):
    chat_id = int(chat_id)
    with conn:
        c.execute(f"SELECT groupid FROM aliag_db.taggergps WHERE groupid = {chat_id}")
        isthere = len(c.fetchall())
    if isthere == 0:
        return False
    else:
        return True



