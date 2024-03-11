import sqlite3

con = sqlite3.connect('user_wallet.db', check_same_thread=False)
cur = con.cursor()
table = '''
    CREATE TABLE IF NOT EXISTS wallet_table (
        id TEXT,
        pub_key TEXT,
        priv_key TEXT,
        wallet_name TEXT
    )
    '''
cur.executescript(table)



def check_wallets(user_id):
    sqlite_connection = sqlite3.connect('user_wallet.db')
    cur = sqlite_connection.cursor()
    cur.execute("SELECT wallet_name, pub_key, priv_key FROM wallet_table WHERE id = ?", (user_id, ))
    s = cur.fetchall()
    return s


def add_wallet(wallet_name, user_id, pub_key, priv_key):
    sqlite_connection = sqlite3.connect('user_wallet.db')
    cur = sqlite_connection.cursor()
    cur.execute("INSERT INTO wallet_table (id, pub_key, priv_key, wallet_name) VALUES (?,?,?,?)", (str(user_id), str(pub_key), str(priv_key), str(wallet_name)))
    sqlite_connection.commit()
    sqlite_connection.close()


def get_wallet(user_id, pub_key):
    sqlite_connection = sqlite3.connect('user_wallet.db')
    cur = sqlite_connection.cursor()
    cur.execute("SELECT * FROM wallet_table WHERE id = ? and pub_key = ?", (user_id, pub_key))
    return cur.fetchone()


def delete_wallet(user_id, pub_key):
    sqlite_connection = sqlite3.connect('user_wallet.db')
    cur = sqlite_connection.cursor()
    cur.execute("DELETE FROM wallet_table WHERE id = ? and pub_key = ?", (str(user_id), str(pub_key)))
    sqlite_connection.commit()
    sqlite_connection.close()
