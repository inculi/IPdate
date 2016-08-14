import smtplib
import os
import getip

# ===========================   IGNORE THIS FILE   =============================
# This is currently the development file for email on Windows.
# ===========================   IGNORE THIS FILE   =============================

if not os.path.isfile(os.path.expanduser('~') + "/email.dat"):
    print "No email credentials found. Please enter them now:"
    username = raw_input("gmail username: ")
    password = raw_input("gmail password: ")
    email = raw_input("email to send notifications to: ")
    f = open(os.path.expanduser('~') + '/email.dat', 'w+')
    f.write(username+'\n'+password+'\n'+email)
    f.close()

with open(os.path.expanduser('~') + "/email.dat") as f:
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

msg = "To: " + email + "\n"
msg += "Subject: Updated IP Information\n\n" # text that we shall append the infomation to
msg += "Public: " + getip.get_pub_ip() + "\n"
msg += "Private: " + getip.get_priv_ip() + "\n"

server.sendmail("", email, msg)
server.quit()
