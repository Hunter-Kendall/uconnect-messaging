import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user = "uconnect",
    password = "csci400@HC")
c = conn.cursor()
#creating a fresh database
# c.execute("DROP DATABASE Uconnect")
c.execute("CREATE DATABASE Uconnect")
c.execute("USE Uconnect")


c.execute('''CREATE TABLE Users
            (user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
             username VARCHAR(16) NOT NULL,
             password VARCHAR(25) NOT NULL,
             name VARCHAR(16) NOT NULL,
             tagline CHAR(5) NOT NULL)''')
conn.commit()
c.execute('''CREATE TABLE Group_Chat
            (group_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
             name VARCHAR(16) NOT NULL,
             join_code CHAR(10) NOT NULL)''')
conn.commit()
c.execute('''CREATE TABLE Group_Members
            (group_id INT NOT NULL,
             user_id INT NOT NULL,
             online INT NOT NULL,
             PRIMARY KEY(group_id, user_id),
             CONSTRAINT FK_group_id FOREIGN KEY (group_id)
             REFERENCES Group_chat(group_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION,
             CONSTRAINT FK_user_id FOREIGN KEY (user_id)
             REFERENCES Users(user_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION)''')
conn.commit()
c.execute('''CREATE TABLE Messages
            (message_num INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
             group_id INT NOT NULL,
             user_id INT NOT NULL,
             group_message_num INT NOT NULL,
             message VARCHAR(500) NOT NULL, 
             CONSTRAINT FK_group_members_group_id FOREIGN KEY (group_id)
             REFERENCES Group_Members(group_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION,
             CONSTRAINT FK_group_members_user_id FOREIGN KEY (user_id)
             REFERENCES Group_Members(user_id)
             ON DELETE NO ACTION ON UPDATE NO ACTION)''')

conn.commit()
conn.close()
