import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()
conn.isolation_level = None

# Create Users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY,
             fullname TEXT NOT NULL,
             phone TEXT NOT NULL)''')

# Create Listings table
c.execute('''CREATE TABLE IF NOT EXISTS listings (
             listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER,
             photo TEXT NOT NULL,
             type TEXT NOT NULL,
             city TEXT NOT NULL,
             area TEXT,
             address TEXT NOT NULL,
             rooms INTEGER,
             price REAL NOT NULL,
             additional_info TEXT,
             listing_date DATE DEFAULT CURRENT_DATE NOT NULL,
             expiry_date DATE DEFAULT (date('now', '+30 days')) NOT NULL,
             active BOOLEAN DEFAULT 1,
             message_id INTEGER DEFAULT 0,
             FOREIGN KEY(user_id) REFERENCES users(user_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS rents (
                rent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                photo TEXT NOT NULL,
                type TEXT NOT NULL,
                city TEXT NOT NULL,
                area TEXT,
                address TEXT NOT NULL,
                rooms INTEGER,
                price REAL NOT NULL,
                additional_info TEXT,
                listing_date DATE DEFAULT CURRENT_DATE NOT NULL,
                expiry_date DATE DEFAULT (date('now', '+30 days')) NOT NULL,
                active BOOLEAN DEFAULT 1,
                message_id INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id))''')

# Create Subscriptions table
c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
             subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER,
             start_date DATE DEFAULT CURRENT_DATE NOT NULL,
             end_date TEXT DEFAULT (date('now', '+30 days')) NOT NULL,
             subscription_type TEXT DEFAULT 'free' NOT NULL,
             FOREIGN KEY(user_id) REFERENCES users(user_id))''')


# FOR USER TABLE <-------------------------------------------------------------------->
def add_user(user_id, fullname, phone):
    c.execute('INSERT INTO users (user_id, fullname, phone) VALUES (?, ?, ?)', (user_id, fullname, phone))
    return c.lastrowid

def get_user(user_id):
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return c.fetchone()


def update_user(user_id, fullname, phone):
    c.execute('UPDATE users SET fullname = ?, phone = ? WHERE user_id = ?', (fullname, phone, user_id))
    return True


def delete_user(user_id):
    c.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    return True

# END USER TABLE <-------------------------------------------------------------------->


#

# FOR LISTINGS TABLE <-------------------------------------------------------------------->

def add_listing(user_id, photo, type, city, area, address, rooms, price, additional_info, message_id):
    c.execute('INSERT INTO listings (user_id, photo, type, city, area, address, rooms, price, additional_info, message_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, photo, type, city, area, address, rooms, price, additional_info, message_id))
    return c.lastrowid

def set_message_id(listing_id, message_id):
    c.execute('UPDATE listings SET message_id = ? WHERE listing_id = ?', (message_id, listing_id))
    return True


def add_photo(listing_id, photo_url):
    c.execute('INSERT INTO photos (listing_id, photo_url) VALUES (?, ?)', (listing_id, photo_url))
    return c.lastrowid

def get_full_data_apartment(listing_id):
    try:
        c.execute('SELECT * FROM listings WHERE listing_id = ?', (listing_id,))
        data = c.fetchone()
        user_id = data[1]
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        return {
            'id': data[0],
            'photo': data[2],
            'type': data[3],
            'city': data[4],
            'area': data[5],
            'address': data[6],
            'rooms': data[7],
            'price': data[8],
            'additional_info': data[9],
            'listing_date': data[10],
            'owner': user[1],
            'phone': user[2]
        }
    except:
        return None

def get_apartment(listing_id):
    c.execute('SELECT * FROM listings WHERE listing_id = ?', (listing_id,))
    return c.fetchone()


def get_listings(user_id):
    c.execute('SELECT * FROM listings WHERE user_id = ?', (user_id,))
    return c.fetchall()


def get_photos(listing_id):
    c.execute('SELECT * FROM photos WHERE listing_id = ?', (listing_id,))
    return c.fetchall()


def delete_listing(listing_id):
    c.execute('DELETE FROM listings WHERE listing_id = ?', (listing_id,))
    c.execute('DELETE FROM photos WHERE listing_id = ?', (listing_id,))
    return True

def delete_subscription(user_id):
    c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
    return True

def change_listing_status(listing_id, status):
    c.execute('UPDATE listings SET active = ? WHERE listing_id = ?', (status, listing_id))
    return True

def get_active_listings():
    c.execute('SELECT * FROM listings WHERE active = 1')
    return c.fetchall()

def get_expired_listings():
    c.execute('SELECT * FROM listings WHERE active = 0')
    return c.fetchall()

def get_all_listings():
    c.execute('SELECT * FROM listings')
    return c.fetchall()

# END LISTINGS TABLE <-------------------------------------------------------------------->

#


# FOR RENTS TABLE <-------------------------------------------------------------------->

def add_rent(user_id, photo, type, city, area, address, rooms, price, additional_info, message_id):
    c.execute('INSERT INTO rents (user_id, photo, type, city, area, address, rooms, price, additional_info, message_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, photo, type, city, area, address, rooms, price, additional_info, message_id))
    return c.lastrowid

def get_rent(rent_id):
    c.execute('SELECT * FROM rents WHERE rent_id = ?', (rent_id,))
    return c.fetchone()

def get_full_data_rent(rent_id):
    try:
        c.execute('SELECT * FROM rents WHERE rent_id = ?', (rent_id,))
        data = c.fetchone()
        user_id = data[1]
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        return {
            'id': data[0],
            'photo': data[2],
            'type': data[3],
            'city': data[4],
            'area': data[5],
            'address': data[6],
            'rooms': data[7],
            'price': data[8],
            'additional_info': data[9],
            'listing_date': data[10],
            'owner': user[1],
            'phone': user[2]
        }
    except:
        return None

def set_rent_message_id(rent_id, message_id):
    c.execute('UPDATE rents SET message_id = ? WHERE rent_id = ?', (message_id, rent_id))
    return True

def get_rents_with_user_id(user_id):
    c.execute('SELECT * FROM rents WHERE user_id = ?', (user_id,))
    return c.fetchall()

def get_active_rents():
    c.execute('SELECT * FROM rents WHERE active = 1')
    return c.fetchall()

def get_expired_rents():
    c.execute('SELECT * FROM rents WHERE active = 0')
    return c.fetchall()

def get_all_rents():
    c.execute('SELECT * FROM rents')
    return c.fetchall()

def change_rent_status(rent_id, status):
    c.execute('UPDATE rents SET active = ? WHERE rent_id = ?', (status, rent_id))
    return True

def delete_rent(rent_id):
    c.execute('DELETE FROM rents WHERE rent_id = ?', (rent_id,))
    return True

# END RENTS TABLE <-------------------------------------------------------------------->

#

# FOR SUBSCRIPTIONS TABLE <-------------------------------------------------------------------->

def add_subscription(user_id, subscription_type):
    c.execute('INSERT INTO subscriptions (user_id, subscription_type) VALUES (?, ?)', (user_id, subscription_type))
    return c.lastrowid

def check_user_subscription(user_id):
    c.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,))
    return c.fetchone()[4]

def get_subscription(user_id):
    c.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,))
    return c.fetchone()


def change_subscription_type(user_id, subscription_type):
    c.execute('UPDATE subscriptions SET subscription_type = ? WHERE user_id = ?', (subscription_type, user_id))
    return True

# END SUBSCRIPTIONS TABLE <-------------------------------------------------------------------->