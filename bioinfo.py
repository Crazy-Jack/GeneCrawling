import requests
from bs4 import BeautifulSoup



myurl = 'http://pedant.helmholtz-muenchen.de/pedant3htmlview/pedant?Method=ReportGeneData&Db=p3_p116_Ara_thali&Name=blastpself&GeneticelemID=90'

a = requests.get(myurl)

soup = BeautifulSoup(a.text, 'lxml')

print(soup)




















def main():
	pass

if __name__ == "__main__":
	main()