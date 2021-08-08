import requests
import re
from bs4 import BeautifulSoup


def taichung_COVID_vaccine_clinic(website="https://www.cdc.gov.tw/Category/MPage/BUp9U5cp5G6eltxz9yuoOQ"):
    """
    This function takes url as input, and construct a dictionary filtered by names of district in Taichung, it may cause
    various issues if users do not use the defaut url as input.
    :param website:
    :return: A dictionary with keys of names of districts and values a list of info of clinics that provide COVID-19
             vaccination
    """
    url = website
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.find_all("div", class_="panel-body")

    clinic_sorted_by_dist_dict = dict()

    for clinic in result:

        clinic = clinic.text.split("\n")
        # No need to split <br> tag since BS already dealt with it.

        trash_lst = ["\r", "\u2003", "連結", "\xa0"]
        trash_set = set(trash_lst)

        # print(clinic)
        # To show the data structure and the actual output extracted from the demanded class.

        temp_clinic_lst = list()
        temp_clinic_dict = dict()

        for info in clinic:
            trash_flag = False
            for trash in trash_set:
                if len(info) == 0 or info[0] == " " or trash in info:
                    # Tick out unnecessary information
                    trash_flag = True
                    continue

            if not trash_flag:
                temp_clinic_lst.append(info)

                split_info = re.split('[:：]', info, 1)
                # Note that there are full and half type semicolon, we need to split the string as either one appears.
                # Also, the reason we split it once is cuz semicolon is also used in clock format; it may cause errors
                # later on.

                info_category, info_data = split_info
                info_category = info_category.strip()
                info_data = info_data.strip()

                temp_clinic_dict[info_category] = info_data

        # We sort these areas by district.
        if "鄉鎮市區" in temp_clinic_dict:
            if temp_clinic_dict["鄉鎮市區"] not in clinic_sorted_by_dist_dict:
                clinic_sorted_by_dist_dict[temp_clinic_dict["鄉鎮市區"]] = list()
            else:
                clinic_sorted_by_dist_dict[temp_clinic_dict["鄉鎮市區"]].append(temp_clinic_dict)
            # if "醫療院所名稱" in temp_clinic_dict:
            #     print(temp_clinic_dict["醫療院所名稱"], temp_clinic_dict["鄉鎮市區"])

    return clinic_sorted_by_dist_dict


def main():
    """

    This is the main function, we first enter the district we desire, and then will return a list of dictionaries,
    providing various information about the clinics, including names, addresses, contact numbers, and etc..

    Since there are a number of clinics fail providing their contact info, I didn't show them up in the display session.

    For more information about vaccination in Taichung, please visit
    https://www.cdc.gov.tw/Category/MPage/BUp9U5cp5G6eltxz9yuoOQ.

    :return:
    """
    clinics_in_dist = taichung_COVID_vaccine_clinic()

    district = input("請輸入地區: ")
    while True:
        if district in clinics_in_dist:
            total_clinic_count = len(clinics_in_dist[district])
            if total_clinic_count:
                print("\n搜索到 {:^5d} 間診所\n".format(total_clinic_count))

                print("{:<40s}{:^40s}{:>40s}".format('醫療院所名稱', '地址', '洽詢電話'))
                bad_contact_clinic_count = 0
                for clinic in clinics_in_dist[district]:
                    if '醫療院所名稱' in clinic and '地址' in clinic and '洽詢電話' in clinic:
                        print("{:<40s}{:^40s}{:>40s}".format(clinic['醫療院所名稱'], clinic['地址'], clinic['洽詢電話']))
                    else:
                        bad_contact_clinic_count += 1

                if bad_contact_clinic_count:
                    print("有 {:^5d} 診間信息有缺漏， 詳情請至"
                          "https://www.cdc.gov.tw/Category/MPage/BUp9U5cp5G6eltxz9yuoOQ 查詢"
                          .format(bad_contact_clinic_count))
            else:
                print("\n目前區域無施打新冠疫苗診所，請搜群其他區域")
        else:
            print("\n查無此地區")

        desire = input("\n繼續查詢？(y/n) ")
        if desire.lower() == 'n':
            print("\n感謝您的查詢，再見。")
            break
        district = input("\n請重新輸入地區: ")


if __name__ == "__main__":
    main()
