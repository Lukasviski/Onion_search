import csv
import requests
from bs4 import BeautifulSoup
import re
import argparse
import sys
import os
import time

onion_pattern = re.compile(r'^(http://|https://)?[a-zA-Z0-9]+\.onion(/)?$')
session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
print("Connect to Tor")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'}
headers_csv = ['Engine', 'Title', 'Link']
default_output_file = "search_onion.csv"


def main():
    if os.name == 'nt':
        os.system('cls')

    credit = "- By Luk"
    for i, c in enumerate(credit):
        if i % 2 == 0:
            print("\u001b[35m\u001b[1m" + c, end="")
        else:
            print("\u001b[0m\u001b[1m" + c, end="")

    text = "\u001b[0m"

    banner = f"""
      \u001b[35m\u001b[1m_____                    ___ \u001b[0m
     \u001b[35m\u001b[1m/ ____|                   | | \u001b[0m                 \u001b[0m\u001b[1m(_)\u001b[0m
    \u001b[35m\u001b[1m| (___   ___  __ _ _ __ ___| |__ \u001b[0m     \u001b[0m\u001b[1m___  _ __  _  ___  _ __\u001b[0m
     \u001b[35m\u001b[1m\___ \ / _ \/ _` | '__/ __| '_ \ \u001b[0m   \u001b[0m\u001b[1m/ _ \| '_ \| |/ _ \| '_ \ \u001b[0m
     \u001b[35m\u001b[1m____) |  __/ (_| | | | (__| | | | \u001b[0m \u001b[0m\u001b[1m| (_) | | | | | (_) | | | |\u001b[0m
    \u001b[35m\u001b[1m|_____/ \___|\__,_|_|  \___|_| |_| \u001b[0m  \u001b[0m\u001b[1m\___/|_| |_|_|\___/|_| |_|\u001b[0m
                   {text}"""

    print(banner)
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", "-s", type=str, help="Text search.")

    parser.add_argument("--engine", "-e", type=str, default='full', help='Search engines, separated by comma(default: '
                                                                         'full): haystak, grams, kraken, torgle, '
                                                                         'exacacvaTor, submarine, danexio..')

    parser.add_argument("--output", "-o", type=str, default="search_onion.csv", help="Output file name (default: "
                                                                                     "search_onion.csv")
    args = parser.parse_args()

    output_file = args.output

    if os.path.exists(output_file):
        name, ext = os.path.splitext(output_file)
        count = 1
        new_filename = output_file
        while os.path.exists(new_filename):
            new_filename = f"{name}{count}{ext}"
            count += 1
        output_file = new_filename

    engines = args.engine.split(",")

    if 'full' in engines:
        engines = ["haystak", "grams", "kraken", "torgle", "excavaTor", "torDex", "submarine"]

    if args.search:
        search_text = args.search.replace(" ", "+")
    else:
        print("No arguments found.")
        print(parser.print_help())
        sys.exit()

    print(f"\n\nSelected engines: {engines}.\nSearch: {args.search}\n\n")

    for engine in engines:
        if engine == 'haystak':
            haystak(search_text, output_file)
        elif engine == 'grams':
            grams(search_text, output_file)
        elif engine == 'kraken':
            kraken(search_text, output_file)
        elif engine == 'torgle':
            torgle(search_text, output_file)
        elif engine == 'excavaTor':
            excavator(search_text, output_file)
        elif engine == 'torDex':
            tordex(search_text, output_file)
        elif engine == 'submarine':
            submarine(search_text, output_file)
        else:
            print(f"Unknown engine: {engine}")
        # elif engine == "danexio": Error 500
        #     results += danexio(args.search)

        print("Finished")


def haystak(search, output_file):
    base_url = f'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q={search}&offset='
    offset = 0
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        num_attempts = 0
        while num_attempts < 3:
            url = base_url + str(offset)
            try:
                response = session.get(url, headers=headers)
                response.raise_for_status()
            except Exception as e:
                print("Haystak. Error:", e)
                num_attempts += 1
                if num_attempts < 3:
                    print("Retrying in 10 seconds...")
                    time.sleep(10)
                    continue
                else:
                    print("Maximum number of attempts reached. Exiting...")
                    break
            else:
                print("Connected to haystak. Status code:", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                last_link = None
                print(url)
                while True:
                    results = soup.find_all('div', {'class': 'result'}, start=last_link)
                    if not results:
                        break
                    for result in results:
                        link = result.find('a', href=True)['href']
                        title = result.find('a').text
                        writer.writerow(['haystak', title, link])
                        last_link = link
                        print(title, ":", link)
                offset += 20
                if not last_link:
                    print("No more links.")
                    break


def grams(search, output_file):
    base_url = f'http://grams64rarzrk7rzdaz2fpb7lehcyi7zrrf5kd6w2uoamp7jw2aq6vyd.onion/search?key={search}&q=Search&page='
    page = 1
    last_output = None
    repetitions = 0
    while True:
        url = base_url + str(page)
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Grams. Error. Status code: ", response.status_code)
            break
        else:
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                print("Connect to grams. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                last_link = None
                output = ''
                while True:
                    link_header = soup.find_all('font', {'class': 'link-header'}, start=last_link)
                    if link_header:
                        for href in link_header:
                            title = href.text.strip()
                            if href.a:
                                link = href.a['href']
                                print(title, " : ", link)
                                writer.writerow(['grams', title, link])
                    if output == last_output:
                        repetitions += 1
                    else:
                        repetitions = 0
                        last_output = output
                    if repetitions >= 2:
                        print('Repeated output. Stopping.')
                        break
                    page += 1


def kraken(search, output_file):
    page = 1
    base_url = f'http://krakenai2gmgwwqyo7bcklv2lzcvhe7cxzzva2xpygyax5f33oqnxpad.onion/search/?q={search}&PAGEN_1='
    last_output = None
    repetitions = 0
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        while True:
            url = base_url + str(page)
            response = session.get(url, headers=headers)
            if response.status_code != 200:
                print("kraken. Error. Status code: ", response.status_code)
                break
            else:
                writer = csv.writer(file)
                print("Connect to kraken. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                output = ''
                last_link = None
                while True:
                    links = soup.find_all('a', attrs={'target': '_blank', 'class': 'title'}, start=last_link)
                    if not links:
                        print("Not have more links.")
                        break
                    for link in links:
                        title = link.text.strip()
                        link_h = link['href']
                        print(title, " : ", link_h)
                        writer.writerow(['kraken', title, link])
                        output += link['href'] + '\n'
                        last_link = link['href']
                if not last_link:
                    break
                if output == last_output:
                    repetitions += 1
                else:
                    repetitions = 0
                    last_output = output
                if repetitions >= 2:
                    print('Repeated output. Stopping.')
                    break
                page += 1


def torgle(search, output_file):
    page = 0
    base_url = f'http://iy3544gmoeclh5de6gez2256v6pjh4omhpqdh2wpeeppjtvqmjhkfwad.onion/torgle/?query={search}&page='
    last_output = None
    repetitions = 0
    while True:
        url = base_url + str(page)
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Torgle. Error. Status code: ", response.status_code)
            break
        else:
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                print("Connect to Torgle. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                output = ''
                last_link = None
                while True:
                    links = soup.find_all('a', attrs={'target': '_blank'}, start=last_link)
                    titles = soup.find_all('td', attrs={'valign': 'top'})
                    if not titles:
                        print("Not have more links.")
                        break
                    if not links:
                        print("Not have more links.")
                        break
                    for link, title in zip(links, titles):
                        parent = link.findParent('i')
                        find_title = title.find('b')
                        find_title_tag = find_title.text.strip()
                        if parent and parent.text.strip() == link['href']:
                            print(find_title_tag, " : ", link['href'])
                            writer.writerow(['torgle', find_title_tag, parent])
                        output += link['href'] + '\n'
                        last_link = link['href']
                if not last_link:
                    break
                if output == last_output:
                    repetitions += 1
                else:
                    repetitions = 0
                    last_output = output
                if repetitions >= 2:
                    print('Repeated output. Stopping.')
                    break
                page += 1


def excavator(search, output_file):
    page = 0
    base_url = f'http://2fd6cemt4gmccflhm6imvdfvli3nf7zn6rfrwpsy7uhxrgbypvwf5fad.onion/search/{search}/?per_page='
    last_output = None
    repetitions = 0
    while True:
        url = base_url + str(page)
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Excavator. Error. Status code: ", response.status_code)
            break
        else:
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                print("Connected to ExcavaTor. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                output = ''
                last_link = None
                for parent_h6 in soup.find_all('h6', class_='text-truncate'):
                    link = parent_h6.find('a')
                    title = link.text.strip()
                    if link:
                        print(title, " : ", link)
                        writer.writerow(['excavaTor', title, link])
                    # file.flush()
                    last_link = parent_h6
            if not last_link:
                print("Not have more links.")
                break
            if output == last_output:
                repetitions += 1
            else:
                repetitions = 0
                last_output = output
            if repetitions >= 2:
                print('Repeated output. Stopping.')
                break
            page += 20


def tordex(search, output_file):
    page = 1
    base_url = f'http://tordexu73joywapk2txdr54jed4imqledpcvcuf75qsas2gwdgksvnyd.onion/search?query={search}&page='
    last_output = None
    repetitions = 0
    while True:
        url = base_url + str(page)
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Tordex. Error. Status code: ", response.status_code)
            break
        else:
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                print("Connect to torDex. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                output = ''
                last_link = None
                while True:
                    links = soup.find_all('h5', attrs={'id': 'title'}, start=last_link)
                    if not links:
                        print("Not have more links.")
                        break
                    for link in links:
                        link_a = link.find('a')['href']
                        title = link.text.strip()
                        print(title, " : ", link_a)
                        writer.writerow(['torDex', title, link_a])
                        output += link_a
                        last_link = link_a
                if not last_link:
                    break
                if output == last_output:
                    repetitions += 1
                else:
                    repetitions = 0
                    last_output = output
                if repetitions >= 2:
                    print('Repeated output. Stopping.')
                    break
                page += 1


def submarine(search, output_file):
    page = 0
    base_url = f'http://no6m4wzdexe3auiupv2zwif7rm6qwxcyhslkcnzisxgeiw6pvjsgafad.onion/search.php?term={search}&page='
    last_output = None
    repetitions = 0
    while True:
        url = base_url + str(page)
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Submarine. Error. Status code: ", response.status_code)
            break
        else:
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                print("Connect to Submarine. Status code: ", response.status_code)
                html = response.content
                soup = BeautifulSoup(html, "html.parser")
                print(url)
                output = ''
                last_link = None
                while True:
                    links = soup.find_all('h4', attrs={'class': 'link-header'}, start=last_link)
                    if not links:
                        print("Not have more links.")
                        break
                    for link in links:
                        title = link.text.strip()
                        link_a = link.find('a')['href']

                        print(title, " : ", link_a)
                        writer.writerow(['submarine', title, link_a])
                        output += link_a
                        last_link = link_a
                if not last_link:
                    break
                if output == last_output:
                    repetitions += 1
                else:
                    repetitions = 0
                    last_output = output
                if repetitions >= 2:
                    print('Repeated output. Stopping.')
                    break
                page += 1


if __name__ == "__main__":
    main()
