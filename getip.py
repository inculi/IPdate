import urllib2
import os
import subprocess

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

    # en0
    try:
        en0 = subprocess.check_output("ipconfig getifaddr en0", shell=True).replace("\n","")
        print("Found IP on en0 (Ethernet): " + en0)
        return en0
    except:
        pass

    # en1
    try:
        en1 = subprocess.check_output("ipconfig getifaddr en1", shell=True).replace("\n","")
        print("Found IP on en1 (Wireless): " + en1)
        return en1
    except:
        print("No private addresses found. Consult ifconfig.")
        return 1
