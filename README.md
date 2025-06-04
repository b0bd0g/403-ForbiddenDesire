# 403-ForbiddenDesire
A 403 fuzzer using a variety of techniques


![Image](pictures/forbidden.png)

## Techniques implemented:

-**Path Fuzzing** - modifies the path to the target file to include various characters and symbols

-**Header Fuzzing** - adds header fields like `X-Forwarded-For`, `Referer` etc and attempts to make requests appear to come from unexpected sources. Also includes the use of duplicate host headers to see if web server treats them as valid

-**Content Length Mismatch** - creates a discrepancy between the `Content-Length` header and the actual length of data included (both over and underlength data)

-**Oversize Data** - includes a large peice of data with the request

-**Incorrect Chunking** - includes data that is chunked incorrectly in the request

-**User Agent Fuzzing** - tries multiple user agents to see if any return a response code other than 403. The user agent list is the one from SecLists (include link). Given the number of user agents it will only print ones that have a response code other than 403.

-**Remote File Inclusion** - this requires that the attacker machine has PHP installed and that `allow_url_fopen` is enabled to allow Remote File Inclusion. It will start a PHP server and attempt to fetch the target URL by way of Remote File Inclusion from that PHP Server. **NOTE:** the RFI method is not included in the `--all` flag and must be specifically called. 

## Features

-**Proxy Support** - supports the use of a proxy so that traffic can be analyzed with something like Burp Suite.

-**Custom Headers** - includes support for a custom user agent (or it will choose a random one from the SecLists list) as well as support for full custom headers that can be read from an external file.

-**Custom Data** - custom data can be included with the request either inserted as an argument or read from a file.

-**Content Length Comparison** - it will automatically determine the size of a 403 response and if any responses are more than 50 bytes smaller/larger it will flag those responses

-**HTTP and HTTPS Support** - by default it will try to determine whether to use HTTP or HTTPS from the format of the target URL that is given, however HTTPS can be explicitly set

-**Request Timeout** - ability to set a time out in milliseconds between requests to avoid overloading target servers and having IPs blacklisted.

-**Custom 403 Page** - If a site does not explicitly return a 403 response but rather redirects to a custom page when a forbidden resource is requested, this will follow the redirect and parse the resulting page for the specified string. For example if the page says "You are not allowed to access this resource" use `--custom "not allowed to access" and it will look for that string in the return. **NOTE:** this is considered an experimental feature and has not been fully tested

-**GET and POST Supported** - currently GET and POST are the only two supported request methods. POST requests do not play well with the proxy feature so your mileage may vary if you try to use both at the same time.

### Normal vs Standalone Versions

The normal version uses external files located in the `Resources` folder for User Agent Fuzzing/modification, Path Fuzzing and Header Fuzzing. The standalone has all of those included inside the python file so that the only file required for it to run is the `403_standalone.py`. As such the Standalone version includes less User Agents in its list.

The exception to this is the Remote File Inclusion method which requires the contents of the PHP folder for both the normal and standalone versions. If using Standalone do not use the `--rfi` method if you don't have the PHP folder handy.

## Usage

The `--all` flag implements all of the fuzzing options **EXCEPT FOR REMOTE FILE INCLUSION**. To use RFI, you must specify the `--rfi` flag explicitly.

```
usage: 403_revised.py [--help] [-t] [--all] [--rfi] [-P] [-H] [-L] [-O] [-C]
                      [-U] [-u] [-r] [-h] [-m {GET,POST}] [-s] [-p] [-to] [-d]
                      [-df] [--custom]

options:
  --help         Show this help message and exit

Fuzzing Options:
  -t             url of target file
  --all          perform all fuzzing techniques except for remote file
                 inclusion (path fuzzing, header fuzzing, content length
                 mismatch, oversize data, remote file inclusion and chunking)
  --rfi          start a PHP server and attempt access via Remote File
                 Inclusion. Requires PHP to be installed locally and
                 configured to allow for RFI
  -P             use path fuzzing
  -H             use header fuzzing
  -L             use content length mismatch
  -O             use oversize data in request
  -C             use incorrectly formatted chunked data
  -U             use user agent fuzzing

Header Options:
  -u             define a custom user-agent
  -r             use a random user agent
  -h             use file to define custom headers
  -m {GET,POST}  select method to use - default is GET

Network Options:
  -s             Force HTTPS. By default it tries to read HTTP/S from the url
                 prefix. If not set, defaults to HTTP
  -p             send requests through proxy (this does not play well with
                 POST requests). Format http://[IP]:[PORT] eg.
                 http://127.0.0.1:8080
  -to            set the timeout between requests in milliseconds

Data Options:
  -d             data to include with request
  -df            get data to include with request from file

Experimental Options:
  --custom       if a standard 403 page is not returned and instead a redirect
                 is made to a custom page, text to look for on custom page
                 which denotes forbidden access
```
