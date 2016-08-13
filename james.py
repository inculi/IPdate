import smtplib
import os

if not os.path.isfile(os.path.expanduser('~') + "\\email.dat"):
    print "No email credentials found. Please enter them now:"
    username = raw_input("gmail username: ")
    password = raw_input("gmail password: ")
    email = raw_input("email to send notifications to: ")
    file = open(os.path.expanduser('~') + '\\email.dat', 'w+')
    file.write(username)
    file.write('\n')
    file.write(password)
    file.write('\n')
    file.write(email)

username = ""
password = ""
email = ""

with open(os.path.expanduser('~') + "\\email.dat") as f:
    content = f.readlines()
    for x in range(0, 2):
        if "\n" in content[x]:
            content[x] = content[x].rsplit("\n")[0]
    username = content[0]
    password = content[1]
    email = content[2]
    print content
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(username, password)

msg = "IP addresses go here"
server.sendmail("", email, msg)
server.quit()
