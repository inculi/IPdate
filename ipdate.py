import urllib2
import os
import subprocess
import platform
import smtplib

def get_pub_ip():
    print("Finding public IP. Consulting amazonaws...")
    try:
        data = urllib2.urlopen("http://checkip.amazonaws.com")
        ip = data.read().replace("\n","")
        return ip
    except:
        print("There was an error, most likely with your internet or urllib2.")
        return urllib2.URLError

def get_priv_ip():
    print("Finding private IP. Checking network interfaces...")
    if platform.system() == 'Darwin': # OS X
        interfaces = ['en0','en1'] # en0 is ethernet, en1 is wireless.
        for interface in interfaces:
            try:
                command = str("ipconfig getifaddr "+interface)
                output = subprocess.check_output(command, shell=True).replace("\n","")
                print("Found IP on "+interface+": " + output)
                return output
            except:
                pass

        # If it makes it to here, it couldn't find anything and we have a problem.
        print("No private addresses found. Consult ifconfig.")
        return 1

    elif platform.system() == 'Windows': # Windows
        import socket # we only need this if using windows. left here 4 optimiz.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        priv_ip = s.getsockname()[0]
        print("Found IP: " + priv_ip)
        return priv_ip

    elif platform.system() == 'Linux': # Linux
        output = subprocess.check_output("hostname -I", shell=True).replace("\n","")
        print("Found IP: " + output)
        return output

    else:
        print("You must have a strange OS. What does platform.system() return?")

if platform.system() == 'Darwin' or platform.system() == 'Linux':
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
    msg += "Public: " + get_pub_ip() + "\n"
    msg += "Private: " + get_priv_ip() + "\n"
    msgFile.write(msg)
    msgFile.close()

    print("Sending email to "+email+". Make sure to check your Junk folder.")
    os.system("sendmail " + email + " < msg.txt")
    print("Message sent.")
elif platform.system() == 'Windows':
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
    msg += "Public: " + get_pub_ip() + "\n"
    msg += "Private: " + get_priv_ip() + "\n"

    server.sendmail("", email, msg)
    server.quit()
