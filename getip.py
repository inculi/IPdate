import urllib2

def get_ip():
    try:
        data = urllib2.urlopen("http://checkip.amazonaws.com")
        ip = data.read().replace("\n","")
        return ip
    except:
        print("There was an error.")
        return urllib2.URLError

test()
