import requests
import pandas as pd


def fetch_info(cookies: dict, headers: dict, json: dict):
    # fetch first json for max_pages
    response = requests.post(
        "https://www.era.pt/API/ServicesModule/Property/Search",
        cookies=cookies,
        headers=headers,
        json=json_data,
    ).json()

    return response


def fetch_all(response: dict):
    # scrape every page property list
    house_list = []
    max_pages = response["TotalPages"]
    for page in range(1, max_pages + 1):
        print(f"Fetching for page {page}/{max_pages}")
        json_data["page"] = str(page)
        resp = requests.post(
            "https://www.era.pt/API/ServicesModule/Property/Search",
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).json()
        house_list += [i for i in resp["PropertyList"]]
        if page % 100 == 0:
            save(house_list)

    return house_list


def save(house_list: list[dict]):
    df = pd.DataFrame(house_list)
    print(f"Saving df with shape: {df.shape}")
    df.to_csv("../../data/raw/raw_houses.csv")


def main():

    resp = fetch_info(cookies, headers, json_data)
    house_list = fetch_all(resp)

    return save(house_list)


if __name__ == "__main__":

    cookies = {
        "dnn_IsMobile": "False",
        ".ASPXANONYMOUS": "cn3IX2_OyOWznnN4kNCgLLei_Lw6dgvFjiwGd1NzaW4PwvJHc6Z_P-j2KE-d6tSJuarQjEtW15Dba0lP1Emt4uBREXIRalh8M87Et7GN014UI-ye0",
        "language": "pt-PT",
        "__RequestVerificationToken": "CTbdNiC1LxzEFbTfr5BYOHCL9D4BQEJqaJ0INVO57Pb1UIylOoYw88GNUCSLroO4t-gJ-w2",
        "Live_CC": "2023-08-11T00:40:36.938Z",
        "_gcl_au": "1.1.905848513.1691714437",
        "_gid": "GA1.2.1181917828.1691714437",
        "_gat_UA-33005389-9": "1",
        "ln_or": "eyIyODc2MjgyIjoiZCJ9",
        "_fbp": "fb.1.1691714437345.1646749527",
        "_hjFirstSeen": "1",
        "_hjIncludedInSessionSample_1712566": "0",
        "_hjSession_1712566": "eyJpZCI6IjQ5NWRlNGZkLWFhM2ItNGY5YS1hNjY3LTIyNzhiMzgzZjVlMSIsImNyZWF0ZWQiOjE2OTE3MTQ0MzczNjQsImluU2FtcGxlIjpmYWxzZX0=",
        "_hjAbsoluteSessionInProgress": "0",
        "G_ENABLED_IDPS": "google",
        "ServicesToken": "dnLX9QptQKXbg37dNvr1NoGSElkTzQTXSAWOaQRMJlIdnMMp2l7IK6qxIs8s9p95c2AxUgXte3Vvi6RBNivawnnFhhPCM8SeaW1S8LJIdOYKdUC7KIspCvDN8/S8Y1nszNWEtpNdoRfCl0NHMu+wSZDlsyekyPmSD9oWz25UY5IFa/HnV7liwIJAkl2IV0pvbDx+rzDnCv9//XqLRAw8vC7qMIdehyl7Lx6G/dmL7L1P+K5xwjFs2rq2VG/RSGy5EaQHlQsLdATTtJCrJ3RCSf1bjlMm+jHHcPPxltTfkKY=",
        "glt": "1",
        "_ga": "GA1.1.1674681119.1691714437",
        "_hjSessionUser_1712566": "eyJpZCI6IjY1MGFjMTMxLTQwNDYtNWJlYi1hNjI4LTBhYWZhMzEwYjM0NyIsImNyZWF0ZWQiOjE2OTE3MTQ0MzczNTgsImV4aXN0aW5nIjp0cnVlfQ==",
        "Search": "RFROt0E7j1+mdYRbjwZkmsTRpAyMVEZd4q4HeaoGVw8CNKyglgJnzj7a5E/gP3H48bS1C/obmCcr2S2P0coPsW/GCCeddipmzhdg9Xgl8v94xSqBPzE/04/LOdOUBjas6j/zCAz9DGdng1QoYZmCnL24qs5YxZrmtRAy5CXilzDf74ux6rCYLEd6/OwnwMHInUexEj6+0v9Tibx+zY5DajjYdpyKjXY79MDwcB241j6cBFN3/8nTAtQ63dlllYiDvw9SNlIWR+eNjBFGYaxsXN5rFsP/wZLTbLgC0EcKaKv3ZWPbCXVXElMptCk7vVy3BVyFICCrZs00ORmNSNdoOZGwziYHvsotDKXleztamEl+z2SRqkq3j61Be4guaNAb+tmsWUVXOANI8eAgoMHKSklQFMAVjs9gACjIfx92XTkjC+tWPuiklkkhwdTTQjk1n4PZwIxi+JzCmrDHwicsledOVpbEYhfrxpDP4oWNNlh8ymxrEZk6riFq84kXgBwmE2fzFE4mFEHyOaBibefD8J1J7BZfBpGlzB5Y4q2A5SujEcbMxfEak+AzbTqlRWOAagtYu8ISNfW+92mcdCyI7tUoqlwGXVad/YwbhC/DuQ6b8YcfuqmEfOwc+MtI8c1UdwJETQXqw0Dk9K0fwIiwovBGKPSN4ihz4EKY2oCCu22QSofPNYvN7m7y+83WNWcijm7KmnL/j/sJVw7D53O4Ww==",
        "_ga_Q0QJSN667Y": "GS1.1.1691714437.1.1.1691714448.49.0.0",
        "cto_bundle": "9PxE1l9hOVhKR0s1TE5SVHF4bUJpZjZyTnRKTUFnbU1pNWp3SEllODBZeDh4NVRsQUp0NTR4ck9WT3pGM29hS2ltRiUyRjdQV2VXU1k5U3R6Q2RWTDlyelgyS0hYbiUyQldyWEJCaE45ZVMzeThWbGdQZk5CJTJGZEk0S05Ddm4wOVpYWVJockF3ag",
    }
    headers = {
        "authority": "www.era.pt",
        "accept": "*/*",
        "accept-language": "pt-PT,pt;q=0.9",
        "content-type": "application/json",
        # 'cookie': 'dnn_IsMobile=False; .ASPXANONYMOUS=cn3IX2_OyOWznnN4kNCgLLei_Lw6dgvFjiwGd1NzaW4PwvJHc6Z_P-j2KE-d6tSJuarQjEtW15Dba0lP1Emt4uBREXIRalh8M87Et7GN014UI-ye0; language=pt-PT; __RequestVerificationToken=CTbdNiC1LxzEFbTfr5BYOHCL9D4BQEJqaJ0INVO57Pb1UIylOoYw88GNUCSLroO4t-gJ-w2; Live_CC=2023-08-11T00:40:36.938Z; _gcl_au=1.1.905848513.1691714437; _gid=GA1.2.1181917828.1691714437; _gat_UA-33005389-9=1; ln_or=eyIyODc2MjgyIjoiZCJ9; _fbp=fb.1.1691714437345.1646749527; _hjFirstSeen=1; _hjIncludedInSessionSample_1712566=0; _hjSession_1712566=eyJpZCI6IjQ5NWRlNGZkLWFhM2ItNGY5YS1hNjY3LTIyNzhiMzgzZjVlMSIsImNyZWF0ZWQiOjE2OTE3MTQ0MzczNjQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; G_ENABLED_IDPS=google; ServicesToken=dnLX9QptQKXbg37dNvr1NoGSElkTzQTXSAWOaQRMJlIdnMMp2l7IK6qxIs8s9p95c2AxUgXte3Vvi6RBNivawnnFhhPCM8SeaW1S8LJIdOYKdUC7KIspCvDN8/S8Y1nszNWEtpNdoRfCl0NHMu+wSZDlsyekyPmSD9oWz25UY5IFa/HnV7liwIJAkl2IV0pvbDx+rzDnCv9//XqLRAw8vC7qMIdehyl7Lx6G/dmL7L1P+K5xwjFs2rq2VG/RSGy5EaQHlQsLdATTtJCrJ3RCSf1bjlMm+jHHcPPxltTfkKY=; glt=1; _ga=GA1.1.1674681119.1691714437; _hjSessionUser_1712566=eyJpZCI6IjY1MGFjMTMxLTQwNDYtNWJlYi1hNjI4LTBhYWZhMzEwYjM0NyIsImNyZWF0ZWQiOjE2OTE3MTQ0MzczNTgsImV4aXN0aW5nIjp0cnVlfQ==; Search=RFROt0E7j1+mdYRbjwZkmsTRpAyMVEZd4q4HeaoGVw8CNKyglgJnzj7a5E/gP3H48bS1C/obmCcr2S2P0coPsW/GCCeddipmzhdg9Xgl8v94xSqBPzE/04/LOdOUBjas6j/zCAz9DGdng1QoYZmCnL24qs5YxZrmtRAy5CXilzDf74ux6rCYLEd6/OwnwMHInUexEj6+0v9Tibx+zY5DajjYdpyKjXY79MDwcB241j6cBFN3/8nTAtQ63dlllYiDvw9SNlIWR+eNjBFGYaxsXN5rFsP/wZLTbLgC0EcKaKv3ZWPbCXVXElMptCk7vVy3BVyFICCrZs00ORmNSNdoOZGwziYHvsotDKXleztamEl+z2SRqkq3j61Be4guaNAb+tmsWUVXOANI8eAgoMHKSklQFMAVjs9gACjIfx92XTkjC+tWPuiklkkhwdTTQjk1n4PZwIxi+JzCmrDHwicsledOVpbEYhfrxpDP4oWNNlh8ymxrEZk6riFq84kXgBwmE2fzFE4mFEHyOaBibefD8J1J7BZfBpGlzB5Y4q2A5SujEcbMxfEak+AzbTqlRWOAagtYu8ISNfW+92mcdCyI7tUoqlwGXVad/YwbhC/DuQ6b8YcfuqmEfOwc+MtI8c1UdwJETQXqw0Dk9K0fwIiwovBGKPSN4ihz4EKY2oCCu22QSofPNYvN7m7y+83WNWcijm7KmnL/j/sJVw7D53O4Ww==; _ga_Q0QJSN667Y=GS1.1.1691714437.1.1.1691714448.49.0.0; cto_bundle=9PxE1l9hOVhKR0s1TE5SVHF4bUJpZjZyTnRKTUFnbU1pNWp3SEllODBZeDh4NVRsQUp0NTR4ck9WT3pGM29hS2ltRiUyRjdQV2VXU1k5U3R6Q2RWTDlyelgyS0hYbiUyQldyWEJCaE45ZVMzeThWbGdQZk5CJTJGZEk0S05Ddm4wOVpYWVJockF3ag',
        "moduleid": "410",
        "origin": "https://www.era.pt",
        "referer": "https://www.era.pt/comprar?ob=1&tp=1,2&page=1&ord=3",
        "requestverificationtoken": "a-O4381lPrhF-qBK4zus03XCflrWmJG0-1OegjdRSVsD8AbK5c4IgHkEfhR9baDc8Xn48A2",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "tabid": "36",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    json_data = {
        "businessTypeId": [
            1,
        ],
        "propertiesTypeId": [
            1,
            2,
        ],
        "locationId": [],
        "shape": None,
        "bounds": None,
        "floor": [],
        "eraBenefits": [],
        "otherFeatures": [],
        "propertyState": [],
        "validatePropertyReference": None,
        "sellPrice": None,
        "rentPrice": None,
        "subleasePrice": None,
        "netArea": None,
        "landArea": None,
        "rooms": None,
        "wcs": None,
        "parking": None,
        "onlyDevelopments": False,
        "page": "1",
        "order": "3",
    }

    main()
