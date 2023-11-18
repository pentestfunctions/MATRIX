#!/usr/bin/env python3
from urllib.parse import unquote 
import requests
import re
import argparse
import os
import sys
import time 
import random
import errno

start_time = time.time()


def main():
    if os.name == 'nt':
        os.system('cls')
    banner = """\u001b[36m

         ___                               _    __       
        / _ \___ ________ ___ _  ___ ___  (_)__/ /__ ____
       / ___/ _ `/ __/ _ `/  ' \(_-</ _ \/ / _  / -_) __/
      /_/   \_,_/_/  \_,_/_/_/_/___/ .__/_/\_,_/\__/_/   
                                  /_/     \u001b[0m               
                            
                           \u001b[32m - coded with <3 by Devansh Batham\u001b[0m 
    """
    print(banner)

    parser = argparse.ArgumentParser(description='ParamSpider a parameter discovery suite')
    parser.add_argument('-d','--domain' , help = 'Domain name of the taget [ex : hackerone.com]' , required=True)
    parser.add_argument('-s' ,'--subs' , help = 'Set False for no subs [ex : --subs False ]' , default=True)
    parser.add_argument('-l','--level' ,  help = 'For nested parameters [ex : --level high]')
    parser.add_argument('-e','--exclude', help= 'extensions to exclude [ex --exclude php,aspx]')
    parser.add_argument('-o','--output' , help = 'Output file name [by default it is \'domain.txt\']')
    parser.add_argument('-p','--placeholder' , help = 'The string to add as a placeholder after the parameter name.', default = "FUZZ")
    parser.add_argument('-q', '--quiet', help='Do not print the results to the screen', action='store_true')
    parser.add_argument('-r', '--retries', help='Specify number of retries for 4xx and 5xx errors', default=3)
    args = parser.parse_args()

    if args.subs == True or " True":
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"https://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    
    retry = True
    retries = 0
    while retry == True and retries <= int(args.retries):
             response, retry = connector(url)
             retry = retry
             retries += 1
    if response == False:
         return
    response = unquote(response)
   
    # for extensions to be excluded 
    black_list = []
    if args.exclude:
         if "," in args.exclude:
             black_list = args.exclude.split(",")
             for i in range(len(black_list)):
                 black_list[i] = "." + black_list[i]
         else:
             black_list.append("." + args.exclude)
             
    else: 
         black_list = [] # for blacklists
    if args.exclude:
        print(f"\u001b[31m[!] URLS containing these extensions will be excluded from the results   : {black_list}\u001b[0m\n")
    
    final_uris = param_extract(response , args.level , black_list, args.placeholder)
    save_func(final_uris , args.output , args.domain)

    if not args.quiet:
        print("\u001b[32;1m")
        print('\n'.join(final_uris))
        print("\u001b[0m")

    print(f"\n\u001b[32m[+] Total number of retries:  {retries-1}\u001b[31m")
    print(f"\u001b[32m[+] Total unique urls found : {len(final_uris)}\u001b[31m")
    if args.output:
        if "/" in args.output:
            print(f"\u001b[32m[+] Output is saved here :\u001b[31m \u001b[36m{args.output}\u001b[31m" )

        else:
            print(f"\u001b[32m[+] Output is saved here :\u001b[31m \u001b[36moutput/{args.output}\u001b[31m" )
    else:
        print(f"\u001b[32m[+] Output is saved here   :\u001b[31m \u001b[36moutput/{args.domain}.txt\u001b[31m")
    print("\n\u001b[31m[!] Total execution time      : %ss\u001b[0m" % str((time.time() - start_time))[:-12])

def param_extract(response, level, black_list, placeholder):

    ''' 
    Function to extract URLs with parameters (ignoring the black list extention)
    regexp : r'.*?:\/\/.*\?.*\=[^$]'
    
    '''

    parsed = list(set(re.findall(r'.*?:\/\/.*\?.*\=[^$]' , response)))
    final_uris = []
        
    for i in parsed:
        delim = i.find('=')
        second_delim = i.find('=', i.find('=') + 1)
        if len(black_list) > 0:
            words_re = re.compile("|".join(black_list))
            if not words_re.search(i):
                final_uris.append((i[:delim+1] + placeholder))
                if level == 'high':
                    final_uris.append(i[:second_delim+1] + placeholder)
        else:
            final_uris.append((i[:delim+1] + placeholder))
            if level == 'high':
                final_uris.append(i[:second_delim+1] + placeholder)
    return list(set(final_uris))

def connector(url):
    result = False
    user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
 
    try:
        # TODO control request headers in here
            response = requests.get(url,headers=headers ,timeout=30)
            result = response.text
            retry = False
            response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
            retry = False
            print("\u001b[31;1mCan not connect to server. Check your internet connection.\u001b[0m")
    except requests.exceptions.Timeout as e:
            retry = True
            print("\u001b[31;1mOOPS!! Timeout Error. Retrying in 2 seconds.\u001b[0m")
            time.sleep(2)
    except requests.exceptions.HTTPError as err:
            retry = True
            print(f"\u001b[31;1m {err}. Retrying in 2 seconds.\u001b[0m")
            time.sleep(2)
    except requests.exceptions.RequestException as e:
            retry = True
            print("\u001b[31;1m {e} Can not get target information\u001b[0m")
            print("\u001b[31;1mIf you think this is a bug or unintentional behaviour. Report here : https://github.com/devanshbatham/ParamSpider/issues\u001b[0m")
    except KeyboardInterrupt as k:
            retry = False
            print("\u001b[31;1mInterrupted by user\u001b[0m")
            raise SystemExit(k)
    finally:
            return result, retry

def save_func(final_urls , outfile , domain):
    if outfile:
        if "/" in outfile:
            filename = f'{outfile}'
        else : 
            filename = f'output/{outfile}'
    else :
        filename = f"output/{domain}.txt"
    
    if os.path.exists(filename):
        os.remove(filename)

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: 
            if exc.errno != errno.EEXIST:
                raise
    
    
    for i in final_urls:
        with open(filename, "a" , encoding="utf-8") as f:
            f.write(i+"\n")

{
    "flags" : "-HanrE",
    "patterns" : [
    "callback=",
    "jsonp=",
    "api_key=",
    "api=",
    "password=",
    "email=",
    "emailto=",
    "token=",
    "username=",
    "csrf_token=",
    "unsubscribe_token=",
    "p=",
    "q=",
    "query=",
    "search=",
    "id=",
    "item=",
    "page_id=",
    "secret=",
    "url=",
    "from_url=",
    "load_url=",
    "file_url=",
    "page_url=",
    "file_name=",
    "page=",
    "folder=",
    "folder_urllogin_url=",
    "img_url=",
    "return_url=",
    "return_to=",
    "next=",
    "redirect=",
    "redirect_to=",
    "logout=",
    "checkout=",
    "checkout_url=",
    "goto=",
    "next_page=",
    "file=",
    "load_file=",
    "cmd=",
    "ip=",
    "ping=",
    "lang=",
    "edit=",
    "LoginId=",
    "size=",
    "signature=",
    "passinfo="
    ]
    }

{

    "flags" : "-HanrE",
    "patterns" : [
    "url=",
    "from_url=",
    "load_url=",
    "file_url=",
    "page_url=",
    "file_name=",
    "page=",
    "folder=",
    "folder_url=",
    "login_url=",
    "img_url=",
    "return_url=",
    "return_to=",
    "next=",
    "redirect=",
    "redirect_to=",
    "logout=",
    "checkout=",
    "checkout_url=",
    "goto=",
    "next_page=",
    "file=",
    "load_file="
    ]
    }

{
    "flags" : "-HanrE",
    "patterns" : [
"index.php",
"license.txt",
"readme.html",
"wp-activate.php",
"wp-admin",
"wp-app.php",
"wp-blog-header.php",
"wp-comments-post.php",
"wp-config-sample.php",
"wp-content",
"wp-cron.php",
"wp-links-opml.php",
"wp-load.php",
"wp-login.php",
"wp-mail.php",
"wp-pass.php",
"wp-register.php",
"wp-settings.php",
"wp-signup.php",
"wp-trackback.php",
"xmlrpc.php"
]
}

{
    "flags" : "-HanrE",
    "patterns" : [
    "callback=",
    "jsonp=",
    "api_key=",
    "api=",
    "password=",
    "email=",
    "emailto=",
    "token=",
    "username=",
    "csrf_token=",
    "unsubscribe_token=",
    "p=",
    "q=",
    "query=",
    "search=",
    "id=",
    "item=",
    "page_id="
    ]
    }

if __name__ == "__main__":
    main()