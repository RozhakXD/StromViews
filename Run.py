#!/usr/bin/env python3 -W ignore::DeprecationWarning
import shutup; shutup.please()
import requests, json, time, os, re, sys, subprocess
from rich.panel import Panel
from rich import print
from rich.console import Console

# Banner
def Banner():
    if 'win' in str(sys.platform).lower():
        os.system('cls')
    else:
        os.system('clear')
    Console(width=45, style="bold plum4").print(Panel("""[bold red] ╦ ╦  ╔╦╗┌─┐┌┬┐┌─┐         
[bold red]╚╦╝  ║║║├─┤ │ ├┤           
[bold white]  ╩[bold green] ❷[bold white] ╩ ╩┴ ┴ ┴ └─┘          
[bold yellow] Coded by Rozhak""", title="[bold plum4]Version 1.7"), justify="center")
    return 0
# Pengguna
def Pengguna():
    with requests.Session() as r:
        url = ('https://justpaste.it/awt8i')
        response = r.get(url).text
    return {
        'Jumlah': re.search('"onlineText":"(\d+)"', str(response)).group(1),
        'Online': re.search('"viewsText":"(\d+)"', str(response)).group(1)
    }
# Menu
def Menu():
    Banner()
    try:
        jumlah, online = Pengguna()['Jumlah'], Pengguna()['Online']
        Console(width=45, style="bold plum4").print(Panel(f"[bold white]Jumlah User :[bold green] {jumlah}/{online}", title="👋"))
    except Exception as e:
        Console(width=45, style="bold plum4").print(Panel(f"[italic red]{str(e).title()}!", title="😡"));sys.exit()
    Console(width=45, style="bold plum4").print(Panel("""[bold green]1[bold white]. Cari Musik Berdasarkan Query
[bold green]2[bold white]. Download Musik Dari Youtube
[bold green]3[bold white]. Play Musik Yang Sudah Di Download
[bold green]4[bold white]. Keluar Dari Program""", title="😁"))
    Console().print("[bold white]╭──([bold green]Pilih Salah Satu[bold white])")
    zhak = Console().input("[bold white]╰─> ")
    if zhak == '1' or zhak == '01':
        try:
            Console(width=45, style="bold plum4").print(Panel("[italic white]Silahkan Masukan Query Atau Judul Music, Misalnya :[italic green] Tiara Raffa Affar", title="🙂"))
            Console().print("[bold white]╭──([bold green]Query[bold white])")
            query = Console().input("[bold white]╰─> ")
            Cari(query)
        except Exception as e:
            Console(width=45, style="bold plum4").print(Panel(f"[italic red]{str(e).title()}!", title="😡"));sys.exit()
    elif zhak == '2' or zhak == '02':
        try:
            Console(width=45, style="bold plum4").print(Panel("[italic white]Silahkan Masukan Url Video Dari Youtube Pastikan Benar, Misalnya :[italic green] youtube.com/watch?v=yd2FeKDN0v4", title="🙂"))
            Console().print("[bold white]╭──([bold green]Url[bold white])")
            url = Console().input("[bold white]╰─> ")
            if 'https://www.youtube.com/watch?v=' in str(url):
                Download(url)
            elif 'youtube.com/watch?v=' in str(url):
                Download(f'https://www.{url}')
            else:
                Console(width=45, style="bold plum4").print(Panel("[italic red]Harap Masukan Link Video Dengan Benar Dan Sesuai Contoh!", title="😡"));sys.exit()
        except Exception as e:
            Console(width=45, style="bold plum4").print(Panel(f"[italic red]{str(e).title()}!", title="😡"));sys.exit()
    elif zhak == '3' or zhak == '03':
        try:
            music = os.listdir('Music')
            count = 0
            for z in music:
                count += 1
                Console(width=45, style="bold plum4").print(Panel(f"[bold green]{count}[bold white]. {z}", title="✔️"))
            Console().print("[bold white]╭──([bold green]Pilih Musik[bold white])")
            musik = int(Console().input("[bold white]╰─> "))
            if musik == 1:
                judul = music[0]
            else:
                mana = (musik - 1)
                judul = music[mana]
            Console(width=45, style="bold plum4").print(Panel("[bold green]Playing[bold white] ⇆ㅤ||◁ㅤ❚❚ㅤ▷ || ↻               ", title="😎"), justify="center")
            Calling(f'play Music/{judul}')
            Console().input("[bold white][[bold green]Kembali[bold white]]");time.sleep(2.5);Menu()
        except Exception as e:
            Console(width=45, style="bold plum4").print(Panel(f"[italic red]{str(e).title()}!", title="😡"));sys.exit()
    elif zhak == '4' or zhak == '04':
        Console(width=45, style="bold plum4").print(Panel("[italic white]Selamat Tinggal Bro, Terimakasih Telah Menggunakan Tools Saya!", title="🙂"));sys.exit()
    else:
        Console(width=45, style="bold plum4").print(Panel(f"[italic red]Pilihan {zhak.title()} Yang Kamu Masukan Tidak Ada Di Dalam Menu!", title="😡"));sys.exit()
# Cari
def Cari(query):
    with requests.Session() as r:
        url = ('https://www.googleapis.com/youtube/v3/search/')
        r.headers.update({
            'Host': 'www.googleapis.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'id,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': None,
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        })
        params = {
            'q': query,
            'maxResults': '5',
            'key': json.loads(open('Data/Apikey.json','r').read())['Apikey'],
            'type': 'video',
            'order': 'viewCount'
        }
        response = r.get(url, params = params)
        count = 0
        for x in json.loads(response.text)['items']:
            url = ('youtube.com/watch?v={}'.format(x['id']['videoId']))
            count += 1
            Console(width=45, style="bold plum4").print(Panel(f"[bold green]{count}[bold white]. {url}", title="✔️"))
        Console().input("[bold white][[bold green]Kembali[bold white]]");time.sleep(2.5);Menu()
# Download
def Download(youtube_url):
    with requests.Session() as r:
        url = ('https://www.y2mate.com/mates/id365/mp3/ajax')
        r.headers.update({
            'Host': 'www.y2mate.com',
            'accept-language': 'id,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.y2mate.com',
            'referer': 'https://www.y2mate.com/id365/youtube-mp3',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        })
        data = {
            'url': youtube_url,
            'q_auto': '0',
            'ajax': '1'
        }
        response = r.post(url, data = data).text
        if "\"status\":\"success\"" in str(response):
            mp3_type = re.search('mp3_type = \'(\d+)\';', str(response)).group(1)
            k__id = str(re.search('k__id = (.*?);', str(response)).group(1)).replace('\\"','')
            judul = str(re.search('k_data_vtitle = (.*?);', str(response)).group(1)).replace('\\"','')
            k_data_vid = str(re.search('k_data_vid = (.*?);', str(response)).group(1)).replace('\\"','')
            url = ('https://www.y2mate.com/mates/mp3Convert')
            r.headers.clear()
            r.headers.update({
                'Host': 'www.y2mate.com',
                'accept-language': 'id,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'referer': 'https://www.y2mate.com/id/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            })
            data = {
                'type': 'youtube',
                '_id': k__id,
                'v_id': k_data_vid,
                'ajax': '1',
                'token': '',
                'ftype': 'mp3',
                'fquality': mp3_type
            }
            response = r.post(url, data = data).text
            if "\"status\":\"success\"" in str(response):
                r.headers.clear()
                url = str(re.search('href=(.*?) rel', str(response)).group(1)).replace('\\"','').replace('\\','')
                r.headers.update({
                    'Content-Type': 'audio/mpeg',
                    'X-Powered-By': 'PHP/5.4.16',
                    'Cache-Control': 'public, must-revalidate, post-check=0, pre-check=0',
                    'Accept-Ranges': 'bytes'
                })
                response = requests.get(url, verify = False)
                files = judul.replace(' ','_').replace('(','').replace(')','').replace('-','_')
                with open(f"Music/{files}.mp3", 'wb') as c:
                    c.write(response.content)
                c.close()
                Console(width=45, style="bold plum4").print(Panel(f"""[bold green]1[bold white]. Judul   :[bold green] {judul.title()}
[bold green]2[bold white]. VideoID : {k_data_vid}
[bold green]3[bold white]. Saved   :[bold yellow] Music/{files}.mp3
[bold green]4[bold white]. Quality : {mp3_type}""", title="✔️"))
                Console().input("[bold white][[bold green]Kembali[bold white]]");time.sleep(2.5);Menu()
            else:
                Console(width=45, style="bold plum4").print(Panel("[italic red]Gagal Mendownload Music, Mungkin Link Video Tidak Valid!", title="😡"));sys.exit()
        else:
            Console(width=45, style="bold plum4").print(Panel("[italic red]Gagal Mendownload Music, Mungkin Link Video Tidak Valid!", title="😡"));sys.exit()
# Calling
def Calling(url, *args, **kwargs):
    process = subprocess.Popen(
        url,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    pass

if __name__ == '__main__':
    if os.path.exists("Data") == False or os.path.exists("Music") == False:
        os.system('nkdir Data && mkdir Music');Menu()
    else:
        os.system('git pull');Menu()