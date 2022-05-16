import mysql.connector
import random
import string
import copy
class DB_Commands():
    def __init__(self):
        self.conn = mysql.connector.connect(
                host = "38.240.241.204",
                user = "uconnect",
                password = "csci400@HC",
                database = "Uconnect"
        )
        #str(input("Password: "))
        self.c = self.conn.cursor()

    '''
    Have to connect to database in every "command" so the data base will be written to.
    '''
    def on_viewing(self, group_id):
        msg_count, group_id = group_id.split("+-+-=_=")
        self.c.execute(f'''SELECT  group_id, Messages.user_id, name, tagline, group_message_num, message FROM Messages, Users WHERE group_id = {group_id} AND Messages.user_id = Users.user_id ORDER BY group_message_num DESC LIMIT {msg_count}''')
        past_messages = self.c.fetchall()
        return past_messages

    def on_notify(self, user):
        name, tagline, group_id, status, user_id = user.split("@@@@@")
        #checking if joinging or leaving
        if status == "1":

            #reconnecting users are set to 1 in the online columns
            self.c.execute(f"""UPDATE Group_Members SET online = 1 WHERE user_id = {user_id} AND group_id = {group_id}""")
            self.conn.commit()
            print(f"[User Reconnected]: {name}")
        else:
            #on leave set online status to 0 for all groups
            self.c.execute(f"""UPDATE Group_Members SET online = 0 WHERE user_id = {user_id}""")
            self.conn.commit()
            
            print(f"[User disconnected]: {name}")
        self.c.execute(f'''SELECT name, tagline, group_id from Users, Group_Members WHERE Group_Members.user_id = Users.user_id AND Online = 1''')
        online = self.c.fetchall()
        all_online = ""
        first = True
        for on in online:
            if first:
                all_online = f"{on[0]}@@@@@ {on[1]}@@@@@{on[2]}"
                first = False
            else:
                all_online = f"{all_online}[123[32[{on[0]}@@@@@ {on[1]}@@@@@{on[2]}"
        return all_online

    def on_send(self, group_id, message):
        name = message[1:].split("]")[0]
        message = message.split(": ")[1]
        self.c.execute(f'''SELECT user_id FROM Users WHERE name = "{name[:-6]}" AND tagline = "{name[-5:]}"''')
        id_fetch = self.c.fetchone()[0]
        print(id_fetch)
        self.c.execute(f'''SELECT MAX(group_message_num) FROM Messages WHERE group_id = {group_id}''')
        group_message_num = self.c.fetchone()[0]
        print(type(group_message_num))
        if isinstance(group_message_num, int):
            pass
        else:
            group_message_num = 0
        #add multiple groups
        self.c.execute(f"""INSERT INTO Messages (group_id, user_id, group_message_num, message) VALUES ({group_id}, {id_fetch}, {group_message_num + 1}, '{message}')""")
        self.conn.commit()
        return f"{group_id}|@@@|[{name}]: {message}|@@@|{group_message_num + 1}"

    def on_login(self, username_password):
        username, password = username_password.split(":)-+-(:")
        self.c.execute(f"""SELECT username, password, name, tagline, user_id FROM Users WHERE username = '{username}' AND password = '{password}' """)
        user = self.c.fetchone()
        if isinstance(user, tuple):
            self.c.execute(f"""SELECT Group_Members.group_id, name FROM Group_Members, Group_Chat WHERE user_id = {user[4]} and Group_Members.group_id = Group_Chat.group_id""")
            groups = self.c.fetchall()

            first = True
            group_names = ""
            group_list = ""
            for group in groups:

                if first:
                    group_list = f"{group[0]}"
                    group_names = f"{group[1]}"
                    first = False
                else:
                    group_list = f"{group_list}|+|+{group[0]}"
                    group_names = f"{group_names}|-|-{group[1]}"


            #if a tuple is returned it means that user is registered. 
        
            return f"{user[3]}|_|{user[2]}|_|{user[4]}:@@@@@@@@@:{group_list}:@@@@@@@@@:{group_names}"
        else:
            return 'Username or Password is incorrect.'
    
    def on_register(self, username_password_chatname):
        chatname, username, password  = username_password_chatname.split(":)+=+(:")
        self.c.execute(f"""SELECT username FROM Users WHERE username = '{username}' """)
        check_username = self.c.fetchone()
        if isinstance(check_username, tuple):
            #Error 1 means that the login name is taken
            check_username = "Error 1"
        else: 
            check_username = "Login name available"
        #getting the tagline

        self.c.execute(f"""SELECT name FROM Users WHERE name = '{chatname}' """)
        check_chatname = self.c.fetchall()
        if isinstance(check_chatname, tuple):
            if len(check_chatname) + 1 > 9:
                tagline = f"#00{len(check_chatname) + 1}"
            elif len(check_chatname) + 1 > 99:
                tagline = f"#0{len(check_chatname) + 1}"
            elif len(check_chatname) + 1 > 999:
                tagline = f"#{len(check_chatname) + 1}"
            elif len(check_chatname) + 1 > 9999:
                #error 2 means that there are too many accounts with that chat name
                check_username = "Error 2"
            else:
                tagline = f"#000{len(check_chatname) + 1}"
        else:
            tagline = "#0001"
        
        #now all the data is safe to insert
        self.c.execute(f"""INSERT INTO Users (username, password, name, tagline) VALUES ('{username}', '{password}', '{chatname}', '{tagline}')""")
        self.conn.commit()
        #check_username has 3 states error 1, error 2 and Login name available
        return check_username

    def on_create(self, new_group):
        new_group, user_id = new_group.split("!@#$%!%@$#")
        self.c.execute(f"""SELECT name FROM Group_Chat WHERE name = '{new_group}'""")
        group_status = self.c.fetchone()
        #upper case and lowercase letters
        letters = string.ascii_letters
        #creating new join code
        join_code = ''.join(random.choice(letters) for i in range(10))
        taken = True
        self.c.execute(f"""SELECT join_code From Group_Chat WHERE join_code = '{join_code}'""")
        code_check = self.c.fetchone()
        while taken:
            if isinstance(code_check, tuple):
                join_code = ''.join(random.choice(letters) for i in range(10))
            else:
                taken = False

        #checks group name existance
        if isinstance(group_status, tuple):
            #error 3 means group name already exists
            return "Error 3"
        else:
            self.c.execute(f"""INSERT INTO Group_Chat (name, join_code) VALUES ('{new_group}', '{join_code}')""")
            self.conn.commit()
            self.c.execute(f"""SELECT group_id FROM Group_Chat WHERE name = '{new_group}' AND join_code = '{join_code}'""")
            group_id = self.c.fetchone()[0]
            self.c.execute(f"""INSERT INTO Group_Members (group_id, user_id, online) VALUES ({group_id}, {user_id}, 1)""")
            self.conn.commit()
            return f"{group_id}[12@#$@{new_group}"

    def on_join(self, join_code):
        user_id, join_code = join_code.split("::::")
        self.c.execute(f"""SELECT group_id, name FROM Group_Chat WHERE join_code = '{join_code}'""")
        group_id = self.c.fetchone()
        # checks if join code is valid
        if isinstance(group_id, tuple):
            self.c.execute(f"""SELECT user_id FROM Group_Members WHERE group_id = {group_id[0]} AND user_id = {user_id}""")
            user_check = self.c.fetchone()
            #checks if the user is already in the group
            if isinstance(user_check, tuple):
                #error 5 is if the user is already in  the group
                return "Error 5"
            else:
                #if join code is valid then we can insert the user into the group
                self.c.execute(f"""INSERT INTO Group_Members (group_id, user_id, online) VALUE ({group_id[0]}, {user_id}, 0)""")
                return f"{group_id[0]}[12@#$@{group_id[1]}"
        else:
            #if the room code doesnt exist it returns error 4
            return "Error 4"

    def on_room_code(self, group_id):
        self.c.execute(f"""SELECT join_code FROM Group_Chat WHERE group_id = {group_id}""")
        join_code = self.c.fetchone()[0]
        return join_code


        


