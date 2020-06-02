import time
import requests
import pickle
import json
import csv
import os

with open("config.json") as config:
    CONFIG = json.load(config)


def recurcive_file_list(dir_name):
    """
    :param dir_name: a directory name
    :return: an array of all files recurcively checked within the directory you're in
    """
    list_of_file = os.listdir(dir_name)
    all_files = []
    for file in list_of_file:
        if file in ["venv", ".idea"]:  # directories no ordinary person would be messing with
            continue
        full_path = os.path.join(dir_name, file)
        if os.path.isdir(full_path):
            all_files = all_files + recurcive_file_list(full_path)
        else:
            all_files.append(full_path)

    return all_files


def updater():
    """
    Logs into cardsphere and sets up for update_if_old.
    If you wanted to update_if_old for other functions you could add them at the bottom
    """
    with requests.Session() as sesh:
        payload = {"email": CONFIG["email"],
                   "password": CONFIG["password"]}

        login = sesh.post("https://www.cardsphere.com/login", data=payload)
        if str(login.url) != "https://www.cardsphere.com/":
            print("FUCK THE LOGIN FUCKED UP")
        else:
            print("Successfully logged in")

        update_if_old(sesh, "cs_offers.p", load_cs_top_offers)


def update_if_old(sesh, save_name, func):
    """
    Attempt to load save_name and check how old it is. If it's too old or it's not there, it'll call the function
    func(), which should be a function that gets info for saving, then saves to save_name.

    :param sesh: the requests session you're in
    :param save_name: str of the address of the save you're in
    :param func the function to call for updating your save

    """
    fail_flag = 0
    try:
        save = pickle.load(open(save_name, "rb"))
        if time.time() - int(save['last_checked']) > CONFIG["update_delay"]:  # two days old
            # print("long time since last load")
            print("%f hours passed since load" % ((time.time() - int(save['last_checked']))/60/60))
            fail_flag = 1
        else:
            print("Using pickled save for %s" % save_name)
    except FileNotFoundError:
        print("No %s pickle found or something broke while trying" % save_name)
        fail_flag = 1

    if fail_flag == 1:
        print("Running %s" % str(func))
        save = func(sesh)
        print("Saving %s" % save_name)
        pickle.dump(save, open(save_name, "wb"), 2)


def load_cs_top_offers(sesh):
    """
    get data from cardsphere's offers rest api and converts it into an array of offers that can be saved locally and
    more easily worked with without needing to get further data from servers

    :param sesh: the requests session you're in
    :return: a dict {"offer_array": [offers scraped from CS],
                    "last_checked": time since epoch at start of scraping CS offers}
    """

    # this chugs along a bit. Should I find a way to be more efficient?

    offer_array = []
    last_checked = time.time()

    for i in range(0, CONFIG["scrape_max"], 100):  # 130001
        if i % 500 == 0:
            print("SEARCHING %i " % i)
        while True:
            try:
                rest = sesh.get("https://www.cardsphere.com/rest/v1/offers?offset=" + str(i) +
                                "&order=maxabs&country=AF,AX,AL,DZ,AS,AD,AO,AI,AQ,AG,AR,AM,AW,AU,AT,AZ,BS,BH,BD,BB,BY,"
                                "BE,BZ,BJ,BM,BT,BO,BQ,BA,BW,BV,BR,IO,BN,BG,BF,BI,CV,KH,CM,CA,KY,CF,TD,CL,CN,CX,CC,CO,KM"
                                ",CD,CG,CK,CR,CI,HR,CU,CW,CY,CZ,DK,DJ,DM,DO,EC,EG,SV,GQ,ER,EE,ET,FK,FO,FJ,FI,FR,GF,PF,"
                                "TF,GA,GM,GE,DE,GH,GI,GR,GL,GD,GP,GU,GT,GG,GW,GN,GY,HT,HM,VA,HN,HK,HU,IS,IN,ID,IR,IQ,"
                                "IE,IM,IL,IT,JM,JP,JE,JO,KZ,KE,KI,KP,KR,KW,KG,LA,LV,LB,LS,LR,LY,LI,LT,LU,MO,MK,MG,MW,"
                                "MY,MV,ML,MT,MH,MQ,MR,MU,YT,MX,FM,MD,MC,MN,ME,MS,MA,MZ,MM,NA,NR,NP,NL,NC,NZ,NI,NE,NG,"
                                "NU,NF,MP,NO,OM,PK,PW,PS,PA,PG,PY,PE,PH,PN,PL,PT,PR,QA,RE,RO,RU,RW,BL,SH,KN,LC,MF,PM,"
                                "VC,WS,SM,ST,SA,SN,RS,SC,SL,SG,SX,SK,SI,SB,SO,ZA,GS,SS,ES,LK,SD,SR,SJ,SZ,SE,CH,SY,TW,"
                                "TJ,TZ,TH,TL,TG,TK,TO,TT,TN,TR,TM,TC,TV,UG,UA,AE,GB,USMIL,UM,US,UY,UZ,VU,VE,VN,VG,VI,"
                                "WF,EH,YE,ZM,ZW&kind=S,D&language=EN,CT,CS,FR,DE,IT,JA,KO,PT,RU,ES")
                # time.sleep(1)
                if rest.status_code == 200:
                    break
                else:
                    print("CS top offer offset %s broke" % i)
                    print("Error code: %i" % rest.status_code)
                    time.sleep(20)

            except:
                print("CS top offer offset %s broke" % i)
                pass

        time.sleep(.5)

        part_offer_array = json.loads(rest.content)

        if len(part_offer_array) == 0:
            break

        for j in part_offer_array:
            # print(j)
            offer_array.append(j)

    save = {
        "offer_array": offer_array,
        "last_checked": last_checked,
    }

    return(save)


def beat_other_offers():
    curr_file = ""
    for filename in recurcive_file_list(os.getcwd()):
        if "cardsphere_wants" in filename and ".csv" in filename:
            curr_file = filename
            break

    with open(curr_file, encoding="utf8") as raw_file:
        cs_offers = pickle.load(open("cs_offers.p", "rb"))["offer_array"]
        reader = csv.reader(raw_file, delimiter=",")
        save_arr = []
        start = True
        for i in reader:
            if start:
                start = False
                continue
            breakflag = False
            offer_to_beat = 0.02
            percent_to_beat = 1
            for j in cs_offers:
                if j["cardName"] == i[1]:
                    for k in j['sets']:
                        if k['name'] in i[2]:
                            for m in j['conditions']:
                                cond_dict = {40: 'NM',
                                             30: 'SP',
                                             20: 'MP',
                                             10: 'HP'}

                                if cond_dict[m] in i[3]:
                                    for n in j['languages']:
                                        if n in i[4]:
                                            for p in j['finishes']:
                                                if p in i[5]:
                                                    if (not j['userDisplay'] in CONFIG["user_blacklist"]
                                                            and not j['userId'] in CONFIG["user_blacklist"]
                                                            and (j['userDisplay'] in CONFIG["user_whitelist"]
                                                                 or j['userId'] in CONFIG["user_whitelist"]
                                                                 or CONFIG['user_whitelist'] == [])):
                                                        if (not j['country'] in CONFIG["country_blacklist"]
                                                                and not j['countryName'] in CONFIG["country_blacklist"]
                                                                and (j['country'] in CONFIG["country_whitelist"]
                                                                     or j['countryName'] in CONFIG["country_whitelist"]
                                                                     or CONFIG['user_whitelist'] == [])):

                                                            print(i)
                                                            print(j)
                                                            offer_to_beat = float(j['maxIndex'] + j['maxEff'])/100.0
                                                            offer_to_beat += 0.02
                                                            percent_to_beat = 100 + int(j['maxRelEff']*100)
                                                            percent_to_beat += 1
                                                            print(offer_to_beat)
                                                            print(percent_to_beat)
                                                            breakflag = True
                                                            break
                if breakflag:
                    break
            i_copy = i
            i_copy[8] = percent_to_beat
            i_copy[9] = offer_to_beat
            save_arr.append(i_copy)

    with open("output.csv", "w", encoding="utf8") as output:
        output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        output_writer.writerow(["Quantity", "Name", "Sets", "Conditions",
                                "Languages", "Finishes", "Paused", "Tags", "Offer", "Limit"])
        for i in save_arr:
            output_writer.writerow(i)


if __name__ == "__main__":
    updater()
    beat_other_offers()
