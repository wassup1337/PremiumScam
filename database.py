import sqlite3

conn = sqlite3.connect('database.db')
print('База данных создана и подключена')

cursor = conn.cursor()

if cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users"').fetchone() is None:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            chance REAL DEFAULT 0.0,
            count_refs INTEGER DEFAULT 0,
            referral_id INTEGER DEFAULT NULL,
            rolled INTEGER DEFAULT 0
        )
    ''')
    print('Таблица "users" создана')
else:
    print('Выполнено подключение к таблице "users".')
    
conn.commit()
conn.close()
print('База данных успешно инициализирована.')


def add_user(user_id, username, referral_id=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, username, chance, count_refs, referral_id, rolled) VALUES (?, ?, ?, ?, ?, ?)', 
                   (user_id, username, 0.0, 0, referral_id, 0))
    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return bool(result)

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT * FROM users').fetchall()
    conn.close()
    return result

def increment_chance(user_id, chance):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET chance = chance + ? WHERE id = ?', (chance, user_id))
    conn.commit()
    conn.close()

def detele_chances(user_id, chance):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET chance = ? WHERE id = ?', (chance, user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return result

def get_user_count():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT COUNT(*) FROM users').fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_chance(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT chance FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_rolled(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT rolled FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_zero_referrals():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT * FROM users WHERE count_refs = 0').fetchall()
    conn.close()
    return result

def increment_referrals(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET count_refs = count_refs + 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()