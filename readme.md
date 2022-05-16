# Uconnect
### A Group Messaging Web App

**website link:** https://uconnect-messaging.herokuapp.com/

*Email me when grading to make sure that my pc is on so it can connect to the database.*

*Join code with example data:* **qQrZcZmOtC**

---
## What I Worked On

In my project I worked on a group messaging website I called Uconnect. What originally started as a tutorial for a group chat using socket.io and flask web server hosted by heroku. Then I expanded this simple app to be able to have accounts, save messages, have multiple groups and more.

#### Librarys Used
The librarys I used in this project are socket.io, flask, gunicorn, MySQL-python-connector, and it was hosted by Heroku. Socket.io Is a web socket library compatible between JavaScript and Python. Flask is a simple web framework that is easy to expand apon. Gunicorn is responsible for running the flask server and threading it. Heroku is a website hosting service for developers and has a free hosting for low power websites. 

## Objectives and Success

**My objectives when starting this project:**

- Create a threaded webserver.
- Implement a MySQL database.
- Save messages to the database.
- Allow users to create accounts and login.
- Allow users to create and join groups.
- Allow users to view older messages.
- Show who is curretly connected to the group.
- Make sure everything was syncornized across all clients.
  
**My Successes/Failures:**

I had success in all objectives except 2. The first is the threaded webserver. I was not able to create a threaded webserver because to do that on heroku I would need to pay money. The other failure is seeing who is online (Who is viewing that group). When some one shuts down with the browser open it does not update that they are offline and will just leave them on the online list. Any other event like browser close or go back a page it will update the list.

**Not my Objectives but Failures:**

There is also not a whole lot of security when it comes to encryption. since there was alot to implelemt and not enough time there is not password encryption, so passwords are stored in the data base as the way they were typed. 

If i was to do this project over again I would also not use my local mysql database. This is because i had to open a port on my network and put my ip, username and password into the database commands file that is stored on the heroku repository.

I wanted to make the website look nice with css, but ran out of time.

## Networking Principles Implemented

In my project I used sockets that sent strings of data from the client to the server and vice versa. The problem with these sockets is that they could only send one parameter of data. My solution was to implement a form of marshalling where I combined all parameters of the function on the server into one string to be sent. The parameters are seperated by a series of random character that would not be normally used. Then on the server, it would split based on the random series and then the server would runs its function and return its data in the same way. The marshalling occurs when the client combines the data into a string only translatable by that function of the server. This would be a form of cannonical marshalling between the functions being used and not between the whole client since it is a different split sequence for each 
function.


My project is based on the application layer of the OSI model and also uses some transport layer protocols.
**Protocols Used:**

- TCP for socket transfer.
- HTTPS for webpage distribution.

Even thought the messages are sent over TCP I still check the message number in the client to make sure all messages displayed are in order and for the right user.

## Contributions to This Project
What the web page started with was a username field, connect button, disconnect button, message field, send button, a chat box, and a basic web server.

**What I Added:**
- Added user accounts.
- Login page
- Register page
- Create group page
- The ability to register/login/create groups.
- Saving messages.
- Viewing older messages.
- Select wich group to join/view.
- The ability to see who is online in that group.
- Added/connected the database.
  - Made sure that there cannot be duplicate people wo i added the taglines that if 

## References

- Group chat tutorial: https://medium.com/geekculture/making-your-own-chatroom-sockets-in-python-javascript-html-ac14c2870064
- Saving data across webpages: https://stackoverflow.com/questions/17309199/how-to-send-variables-from-one-file-to-another-in-javascript/17309679#17309679
