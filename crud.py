import sqlite3

def add_contact(fname, lname, address, email, phone, category, notes, last_interaction):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("""INSERT INTO contacts 
        (first_name, last_name, address, email, phone, category, notes, last_interaction) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (fname, lname, address, email, phone, category, notes, last_interaction))
    conn.commit()
    conn.close()

def get_all_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    data = c.fetchall()
    conn.close()
    return data

def update_contact(id, fname, lname, address, email, phone, category, notes, last_interaction):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("""UPDATE contacts SET 
        first_name=?, last_name=?, address=?, email=?, phone=?, 
        category=?, notes=?, last_interaction=? 
        WHERE id=?""",
        (fname, lname, address, email, phone, category, notes, last_interaction, id))
    conn.commit()
    conn.close()


def delete_contact(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
