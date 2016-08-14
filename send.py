import os
import getip

# check to see if we have the previous email recip. saved.
# if not, ask for the email.
if not os.path.isfile(os.path.expanduser('~') + "/myemail.dat"):
    email = raw_input("What email should this send to?\n > ")
    emailFile = open(os.path.expanduser('~') + '/myemail.dat', 'w+')
    emailFile.write(email)
    emailFile.close() # save

else:
    emailFile = open(os.path.expanduser('~') + '/myemail.dat', 'r')
    email = emailFile.readline()

# compose message with IP information
msgFile = open("msg.txt", "w+")
msg = "To: " + email + "\n"
msg += "Subject: Updated IP Information\n\n" # text that we shall append the infomation to
msg += "Public: " + getip.get_pub_ip() + "\n"
msg += "Private: " + getip.get_priv_ip() + "\n"
msgFile.write(msg)
msgFile.close()

print("Sending email to "+email+". Make sure to check your Junk folder.")
os.system("sendmail " + email + " < msg.txt")
print("Message sent.")
