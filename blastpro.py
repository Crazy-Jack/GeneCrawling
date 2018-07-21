import requests
from bs4 import BeautifulSoup as Bsoup 
import re
import sys
import datetime


# get all the blastinfo url

# get first 300
def get_soup(url):
    url_o = requests.get(url)
    soup = Bsoup(url_o.text, 'html.parser')
    return soup


def get_soups(urls):
    soups = []
    for url in urls:
        url_o = requests.get(url)
        soup = Bsoup(url_o.text, 'html.parser')
        soups.append(soup)
    return (soups)

# get GI code and number
def extract(soups):
    IDs = {}
    for soup in soups:
        a = soup.find_all('a')
        for e in a:
            name = e.get_text()
            if name[:1] == 'G':
                gen = [m for m in e['href'].split('&') if m[:13] == 'GeneticelemID'][0]
                num = gen.split('=')[1]
                IDs[name] = str(num)
    return (IDs)


def url_builder(IDs, model_url):
    Urls = {}
    for i in IDs:
        Urls[i] = model_url + IDs[i]
    return Urls

# get all of them

def get_all_url(model_url, pages):
    all_URLs = []
    for r in range(pages[0], pages[1]):
        url = model_url + str(r*300)
        all_URLs.append(url)
    return all_URLs


# extrac info
def ichild(i, tag):
    return list(tag.children)[i]

def find_everything(len_tag):
    # for each block, find GI#, length, score, Identity
    leng_div = len_tag.parent.parent.parent
    num_div = leng_div.previous_sibling.previous_sibling
    info_div = leng_div.next_sibling.next_sibling.next_sibling.next_sibling

    # get length
    length_tag = ichild(1, ichild(2, ichild(1, leng_div)))
    length = length_tag.get_text() # type is str

    # get num
    num_tag = ichild(1, ichild(0, ichild(1, ichild(1, num_div))))
    num = num_tag.get_text()

    # get score
    score_tag = ichild(1, ichild(1, info_div))
    ret = score_tag.get_text()
    pattern = re.compile(r'\d+\.\d*')
    score_try = pattern.findall(ret)
    if len(score_try) != 0:
    	score = score_try[0]
    else:
    	score = -1
    # get identity
    id_tag = ichild(1, ichild(3, info_div))
    idtext = id_tag.get_text()
    rp = re.compile(r"\d+%")
    Id_try = rp.findall(idtext)
    if len(Id_try) != 0:
    	Identity = Id_try[0][:-1]
    else:
    	Identity = -1

    return (num, (length, score, Identity))



def get_all_info(soup):
    # find p tag with text "Length:"
    len_tags = soup('p', text="Length:")
    # get info from each of them
    info = {}
    for tag in len_tags:
        result = find_everything(tag)
        info[result[0]] = result[1]
    return info

    
def all_page(urls):
    differnt_GIs_info = {}
    count = 0
    oldtime = []
    lens = len(urls)
    for url in urls:
        start = datetime.datetime.now().timestamp()
        URL = urls[url]
        soup = get_soup(URL)
        dic = get_all_info(soup)
        differnt_GIs_info[url] = dic
        count += 1
        end = datetime.datetime.now().timestamp()
        oldtime.append(end - start)
        print(str(count) + '/' + str(lens) +'\t'+ '(' + str(url) + ')' + " is finished"+'\t'+'('+str(estimate_time(oldtime, count, lens))+' mins )')
    return differnt_GIs_info

def estimate_time(oldtime, count, lens_urls):
    aver = sum(oldtime)/len(oldtime)
    esti = (lens_urls - count) * aver
    return round(esti / 60, 2)
    



def clean_data(result_dic, min_score=100, ind_edge=30):
    new_data = {}
    for each_GI in result_dic:
        each_set = result_dic[each_GI]
        if len(each_set) != 0:
            if len(each_set[each_GI]) != 0:
                length = each_set[each_GI][0] 
            else:
                length = -1
            count = 0
            for e in each_set:
                value = each_set[e]
                score = float(value[1])
                identity = float(value[2])
                if score >= min_score and identity >= ind_edge:
                    count += 1
            new_data[each_GI] = (length, count)
    return new_data


def write_to_table(dic, pages):
    with open('data'+str(pages[0])+'_'+str(pages[1])+'.txt', 'w') as f:
        f.write('GI number' + '\t' + 'Length' + '\t' + "Count" + '\n')
        for e in dic:
            f.write(str(e) + '\t' + str(dic[e][0]) + '\t' + str(dic[e][1]) + '\n')




def main(argv):
	# settings
    model_url_list = "http://pedant.helmholtz-muenchen.de/pedant3htmlview/pedant?Method=geneticelements&Db=p3_p116_Ara_thali&GeneticelemType=all&Offset="
    model_url_page = "http://pedant.helmholtz-muenchen.de/pedant3htmlview/pedant?Method=ReportGeneData&Db=p3_p116_Ara_thali&Name=blastpself&GeneticelemID="
    pages = [int(argv[1]), int(argv[2])]
    URLs = get_all_url(model_url_list, pages=pages)
    soups = get_soups(URLs)
    IDs = extract(soups)
    urls = url_builder(IDs, model_url_page)

    result_dic = all_page(urls)
    clean = clean_data(result_dic)
    write_to_table(clean, pages)


if __name__ == "__main__":
    main(sys.argv)
    #pass

