import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

def get_listing():
    c.execute("SELECT * FROM listings")
    data = c.fetchall()
    json_data = {}
    for i in data:
        json_data[i[0]] = {
            "id": i[0],
            "type": i[1],
            "city": i[2],
            "area": i[3],
            "address": i[4],
            "rooms": i[5],
            "price": i[6],
            "additional_info": i[7],
            "owner": i[8],
            "phone": i[9]
        }
    return json_data  # Return the created dictionary

def get_user(user_id):
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return c.fetchone()

def get_subscription(user_id):
    c.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,))
    return c.fetchone()[4]

print(get_subscription(217775483))