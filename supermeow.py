import requests
import time
import random
import threading
import json
import os
import logging
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

FILE_SESI = 'sessions.json'
lock = threading.Lock()

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format=f'{Fore.GREEN}%(asctime)s{Style.RESET_ALL} | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Menghilangkan log level INFO dari output
logging.getLogger().setLevel(logging.WARNING)

def print_ascii_art():
    art = """
░██████╗██╗░░░██╗██████╗░███████╗██████╗░███╗░░░███╗███████╗░█████╗░░██╗░░░░░░░██╗  ██████╗░░█████╗░████████╗
██╔════╝██║░░░██║██╔══██╗██╔════╝██╔══██╗████╗░████║██╔════╝██╔══██╗░██║░░██╗░░██║  ██╔══██╗██╔══██╗╚══██╔══╝
╚█████╗░██║░░░██║██████╔╝█████╗░░██████╔╝██╔████╔██║█████╗░░██║░░██║░╚██╗████╗██╔╝  ██████╦╝██║░░██║░░░██║░░░
░╚═══██╗██║░░░██║██╔═══╝░██╔══╝░░██╔══██╗██║╚██╔╝██║██╔══╝░░██║░░██║░░████╔═████║░  ██╔══██╗██║░░██║░░░██║░░░
██████╔╝╚██████╔╝██║░░░░░███████╗██║░░██║██║░╚═╝░██║███████╗╚█████╔╝░░╚██╔╝░╚██╔╝░  ██████╦╝╚█████╔╝░░░██║░░░
╚═════╝░░╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░  ╚═════╝░░╚════╝░░░░╚═╝░░░
┌──────────────────────────┐
│ By ZUIRE AKA SurrealFlux │
└──────────────────────────┘
    """
    print(art)

def muat_sesi():
    if os.path.exists(FILE_SESI):
        with open(FILE_SESI, 'r') as file:
            return json.load(file)
    return []

def simpan_sesi(sesi):
    with open(FILE_SESI, 'w') as file:
        json.dump(sesi, file, indent=2)

def klaim_hadiah(param_klaim, username_telegram, id_thread):
    headers = {
        'accept': 'application/json; indent=2',
        'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://lfg.supermeow.vip',
        'priority': 'u=1, i',
        'referer': 'https://lfg.supermeow.vip/',
        'sec-ch-ua': '""',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, seperti Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
    }

    url_klaim = 'https://api.supermeow.vip/meow/claim?' + param_klaim

    while True:
        try:
            response = requests.post(url_klaim, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()
        except requests.exceptions.HTTPError as http_err:
            with lock:
                logging.error(f"HTTP error occurred: {http_err}")
            time.sleep(60)  # Wait 60 seconds before retrying
            continue
        except requests.exceptions.RequestException as req_err:
            with lock:
                logging.error(f"Error during request: {req_err}")
            time.sleep(60)  # Wait 60 seconds before retrying
            continue
        except json.JSONDecodeError as json_err:
            with lock:
                logging.error(f"JSON decode error: {json_err}")
            time.sleep(60)  # Wait 60 seconds before retrying
            continue

        saldo = data.get('balance', 'N/A')
        with lock:
            logging.warning(f'{Fore.YELLOW}Akun: {id_thread} | Telegram: {username_telegram} | Saldo Anda: {Fore.YELLOW}{saldo}{Style.RESET_ALL}')
        
        tunda_acak = random.randint(3700, 4000)
        tunda = tunda_acak
        while tunda > 0:
            menit, detik = divmod(tunda, 60)
            jam, menit = divmod(menit, 60)
            with lock:
                print(f"{Fore.YELLOW}Akun: {id_thread} | Telegram: {username_telegram} | Klaim Berikutnya Dalam : {jam:02d}:{menit:02d}:{detik:02d}    ", end='\r')
            time.sleep(1)
            tunda -= 1
        print("\n")

def tambah_sesi(sesi):
    param = input('Masukkan Data Parameter contoh "telegram=68xxxx" : ')
    username_telegram = input('Masukkan Nama Telegram Anda: ')
    id_sesi = len(sesi) + 1
    sesi.append({'param': param, 'username_telegram': username_telegram, 'id_sesi': id_sesi})
    simpan_sesi(sesi)
    print(f'{Fore.BLUE}Sesi {id_sesi} ditambahkan.')

def jalankan_sesi(sesi):
    if not sesi:
        print(f"{Fore.RED}Tidak ada sesi yang tersedia.")
        return
    
    print(f"\n{Fore.CYAN}Daftar Sesi yang Tersedia:")
    for session in sesi:
        print(f"{Fore.CYAN}ID: {session['id_sesi']} | Telegram: {session['username_telegram']}")

    pilihan_id = input(f"{Fore.CYAN}Masukkan ID sesi yang ingin dijalankan (pisahkan dengan koma untuk beberapa sesi): ")
    id_sesi_list = [int(id.strip()) for id in pilihan_id.split(",")]

    threads = []
    for id_sesi in id_sesi_list:
        session = next((s for s in sesi if s['id_sesi'] == id_sesi), None)
        if session:
            try:
                param_klaim = session['param']
                username_telegram = session['username_telegram']
                thread = threading.Thread(target=klaim_hadiah, args=(param_klaim, username_telegram, id_sesi), name=f"Sesi-{id_sesi}")
                threads.append(thread)
                thread.start()
            except KeyError as e:
                logging.error(f"Data sesi tidak valid: {session}. Kesalahan: {e}")
        else:
            logging.error(f"Sesi dengan ID {id_sesi} tidak ditemukan.")
    
    for thread in threads:
        thread.join()

def perbarui_id_sesi(sesi):
    for i, session in enumerate(sesi):
        session['id_sesi'] = i + 1
    simpan_sesi(sesi)

def hapus_sesi(sesi):
    if not sesi:
        print(f"{Fore.RED}Tidak ada sesi yang tersedia.")
        return
    
    print(f"\n{Fore.CYAN}Daftar Sesi yang Tersedia:")
    for session in sesi:
        print(f"{Fore.CYAN}ID: {session['id_sesi']} | Telegram: {session['username_telegram']}")

    pilihan_id = input(f"{Fore.CYAN}Masukkan ID sesi yang ingin dihapus (pisahkan dengan koma untuk beberapa sesi): ")
    id_sesi_list = [int(id.strip()) for id in pilihan_id.split(",")]

    for id_sesi in sorted(id_sesi_list, reverse=True):  # Urutkan secara terbalik untuk menghindari perubahan indeks
        session = next((s for s in sesi if s['id_sesi'] == id_sesi), None)
        if session:
            indeks_sesi = next((index for (index, d) in enumerate(sesi) if d["id_sesi"] == id_sesi), None)
            if indeks_sesi is not None:
                del sesi[indeks_sesi]
                perbarui_id_sesi(sesi)
                print(f'{Fore.RED}Sesi {id_sesi} dihapus.')
            else:
                print(f'{Fore.RED}Sesi {id_sesi} tidak ditemukan.')
        else:
            print(f"{Fore.RED}Sesi dengan ID {id_sesi} tidak ditemukan.")

def main():
    print_ascii_art()
    sesi = muat_sesi()
    while True:
        print(f"\n{Fore.WHITE}1. Tambah Sesi")
        print(f"{Fore.WHITE}2. Jalankan Sesi")
        print(f"{Fore.WHITE}3. Hapus Sesi")
        print(f"{Fore.WHITE}4. Keluar")
        pilihan = input(f"{Fore.WHITE}Pilih opsi: ")
        if pilihan == '1':
            tambah_sesi(sesi)
        elif pilihan == '2':
            jalankan_sesi(sesi)
        elif pilihan == '3':
            hapus_sesi(sesi)
        elif pilihan == '4':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
