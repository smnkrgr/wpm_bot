from src.Event import Event
import requests
import os
import sys
import json
import typing
import pickle


class Helper():

    @staticmethod
    def print_header() -> None:
        print("")
        print("            __  __            _____      _              _ _")
        print("     /\    / _|/ _|          / ____|    | |            (_) |")
        print("    /  \  | |_| |_ ___ _ __ | (___   ___| |__  _ __ ___ _| |__")
        print("   / /\ \ |  _|  _/ _ \ '_ \ \___ \ / __| '_ \| '__/ _ \ | '_ \\")
        print("  / ____ \| | | ||  __/ | | |____) | (__| | | | | |  __/ | |_) |")
        print(" /_/    \_\_|_|_|_\___|_| |_|_____/ \___|_|_|_|_|_ \___|_|_.__/")
        print(" \ \        / /  __ \|  \/  | |  _ \ / __ \__   __|")
        print("  \ \  /\  / /| |__) | \  / | | |_) | |  | | | |")
        print("   \ \/  \/ / |  ___/| |\/| | |  _ <| |  | | | |")
        print("    \  /\  /  | |    | |  | | | |_) | |__| | | |")
        print("     \/  \/   |_|    |_|  |_| |____/ \____/  |_|")
        print("")

    @staticmethod
    def authorize_identity(email, password) -> typing.Tuple[str, str]:
        Event("Authorizing account: " + email)
        headers = {
            'User-Agent': 'Klappradtour des Kreises',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'x-client-version': 'Firefox/JsCore/9.6.0/FirebaseCore-web',
            'Origin': 'https://monkeytype.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }
        params = {
            'key': 'AIzaSyB5m_AnO575kvWriahcF1SFIWp8Fj3gQno',
        }
        json_data = {
            'returnSecureToken': True,
            'email': email,
            'password': password,
        }
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
        try:
            response = requests.post(url, headers=headers, params=params, json=json_data)
            json_response = json.loads(response.text)
            name, token = json_response['displayName'], json_response['idToken']
            Event("Account authorized!", is_success=True)
            Event("Display name: " + name, level=1)
            Event("Token retrieved!", level=1)
            return name, token
        except Exception as e:
            message = "Authorization failed: " + str(e)
            Event(message, is_error=True, exit=True)

    @staticmethod
    def get_typing_data(token) -> dict:
        Event("Requesting typing data...")
        headers = {
            'User-Agent': 'Klappradtour des Kreises',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Authorization': "Bearer " + token,
            'Origin': 'https://monkeytype.com',
            'Connection': 'keep-alive',
            'Referer': 'https://monkeytype.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }
        try:
            url = 'https://api.monkeytype.com/results'
            response = requests.get(url, headers=headers)
            json_response = json.loads(response.text)
            typing_data = json_response['data']
            Event("Typing data retrieved!", is_success=True)
            Event(str(len(typing_data)) + " typing tests retrieved!", level=1)
            return typing_data
        except Exception as e:
            message = "Requesting typing data failed: " + str(e)
            Event(message, is_error=True, exit=True)

    @staticmethod
    def save_dict(path, dictionary) -> None:
        try:
            with open(path, "wb") as fp:
                pickle.dump(dictionary, fp)
        except Exception as e:
            message = "Saving the dictionary failed: " + str(e)
            Event(message, is_error=True, exit=True)

    @staticmethod
    def parse_conf_list(value) -> list:
        return list(filter(None, (x.strip() for x in value.splitlines())))

    @staticmethod
    def load_dict(path) -> dict:
        dictionary = {}
        try:
            with open(path, "rb") as fp:
                dictionary = pickle.load(fp)
        except Exception as e:
            message = "Saving the dictionary failed: " + str(e)
            Event(message, is_error=True, exit=True)
        return dictionary


# Print header upon import
Helper.print_header()
