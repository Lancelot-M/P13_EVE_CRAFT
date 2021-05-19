import requests
import json

class EveOnline:
    categories_usfull = [4, 6, 7, 8, 9, 18, 22, 35, 43]

    def call_data(self):

        file = {}
        url = "https://esi.evetech.net/latest/universe/categories"
        params = {
            "datasource": "tranquility"
        }
        response = requests.get(url=url, params=params)
        response = response.json()
        for category in response:
            url = "https://esi.evetech.net/latest/universe/categories/{}"
            params = {
                "datasource": "tranquility"
            }
            response2 = requests.get(url=url.format(category), params=params)
            response2 = response2.json()
            file[category] = response2["name"]
            """
            for group in response["groups"]:
                url = "https://esi.evetech.net/latest/universe/groups/{}"
                params = {
                    "datasource": "tranquility"
                }
                group_response = requests.get(url=url.format(group), params=params)
                group_response = group_response.json()
                groups_list.append(group_response["name"])
            file[response["name"]] = [category, groups_list]
            """
        with open("categories_info.json", "w") as f:
            f.write(json.dumps(file, indent=4, sort_keys=True))

    def frig_bp(self):
        file = {}
        list_bp = []
        url = "https://esi.evetech.net/latest/universe/groups/105"
        params = {
            "datasource": "tranquility"
        }
        response = requests.get(url=url, params=params)
        response = response.json()
        for eve_type in response["types"]:
            url = "https://esi.evetech.net/latest/universe/types/{}"
            params = {
                "datasource": "tranquility"
            }
            type_respone = requests.get(url=url.format(eve_type), params=params)
            type_respone = type_respone.json()
            print(type_respone)
            exit()
            """
            list_bp.append(type_respone["name"])
        file["Frigate Blueprint - 105"] = list_bp
        print(file)   """  


if __name__ == "__main__":
    main = EveOnline()
    main.call_data()
    #main.frig_bp()