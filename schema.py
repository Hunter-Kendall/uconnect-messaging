import sqlite3
conn = sqlite3.connect('Uconnect.db')
c = conn.cursor()

c.execute('''CREATE TABLE Users
            (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             password TEXT NOT NULL,
             name TEXT NOT NULL,
             tagline TEXT NOT NULL)''')
conn.commit()
c.execute('''CREATE TABLE Groups
            (group_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL)''')
conn.commit()
c.execute('''CREATE TABLE Group_Members
            (group_id INTEGER NOT NULL,
             user_id INTEGER NOT NULL,
             current_ip TEXT NOT NULL,
             online INTEGER NOT NULL,
             PRIMARY KEY(group_id, user_id),
             CONSTRAINT FK_group_id FOREIGN KEY (group_id)
             REFERENCES Groups(group_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION,
             CONSTRAINT FK_user_id FOREIGN KEY (user_id)
             REFERENCES Users(user_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION)''')
conn.commit()
c.execute('''CREATE TABLE Messages
            (message_num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             group_id INTEGER NOT NULL,
             user_id INTEGER NOT NULL,
             group_message_num INTEGER NOT NULL,
             CONSTRAINT FK_group_id FOREIGN KEY (group_id)
             REFERENCES Groups(group_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION,
             CONSTRAINT FK_user_id FOREIGN KEY (user_id)
             REFERENCES Users(user_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION)''')

conn.commit()
conn.close()