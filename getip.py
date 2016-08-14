import urllib2
import os
import subprocess
import platform

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

    elif platform.system() == 'Windows': # OS X
        import socket # we only need this if using windows. left here 4 optimiz.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        priv_ip = s.getsockname()[0]
        print("Found IP: " + priv_ip)
        return priv_ip

    elif platform.system() == 'Linux': # OS X
        output = subprocess.check_output("hostname -I", shell=True).replace("\n","")
        print("Found IP: " + output)
        return output

    else:
        print("You must have a strange OS. What does platform.system() return?")
