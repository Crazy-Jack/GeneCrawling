from bs4 import BeautifulSoup as Bsoup
import requests
import socket1
import os
import datetime
import sys

def get_soup(url):
    url_o = requests.get(url)
    soup = Bsoup(url_o.text, 'html.parser')
    return soup

def extract(soup):
    IDs = {}
    a = soup.find_all('a')
    for e in a:
        name = e.get_text()
        if name[:1] == 'G':
            gen = [m for m in e['href'].split('&') if m[:13] == 'GeneticelemID'][0]
            num = gen.split('=')[1]
            IDs[name] = str(num)
    return (IDs)

def main(argv):
	model_id_url = "http://pedant.helmholtz-muenchen.de/pedant3htmlview/pedant?Method=geneticelements&Db=p3_p116_Ara_thali&GeneticelemType=all&Offset="
	model_bio_url = "https://pedant.helmholtz-muenchen.de/pedant3htmlview/pedant?Method=ReportGeneData&Db=p3_p116_Ara_thali&Name=blastpself&GeneticelemID="
	host = "146.107.217.21"
	filepath = './data-' + str(datetime.datetime.now())
	os.mkdir(filepath)
	os.chdir(filepath)
	now_sum = 0
	total_info_pages = int(argv[2]) - int(argv[1])
	start_page, end_page = int(argv[1]), int(argv[2])
	page_done = 0
	countg = 0
	for i in range(start_page, end_page):
		path = './page-'+str(i)
		os.mkdir(path)
		os.chdir(path)
		url =  model_id_url + str(i*300)
		IDsoup = get_soup(url)
		IDs = extract(IDsoup)
		count = 0
		for iid in IDs:
			IDnum = IDs[iid]
			count, countg = count + 1, countg + 1
			timedelta = socket1.everyconnect(IDnum, model_bio_url, host)
			now_sum = timedelta + now_sum
			if countg == 0:
				esti = 0
			else: esti = (now_sum / countg) * ((len(IDs) - count) + (total_info_pages - page_done) * len(IDs))
			print("close socekt of " + str(IDnum) +': ' + str(count) + '/' + str(len(IDs)) + '/' + str(i) + ' estimate: ' + str(round(esti/60, 2)) + ' mins')
		os.chdir('../')
		page_done += 1

if __name__ == "__main__":
	main(sys.argv)





