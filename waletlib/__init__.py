import pip._internal as pip
url = "http://127.0.0.1:8080"

def import_lib(name):
    try:
        return __import__(name)
    except ImportError:
        pip.main(['install', name])
    return __import__(name)


if __name__ == '__main__':
    numpy = import_lib('requests')






import requests as r
from waletlib.error import *



def create_wallet(wallet_type="0.01") -> tuple:
    # function for creating a wallet
    payloud = {"wallet_type": wallet_type}
    callback = r.get(url + "/wallet/create/", params=payloud)
    if callback.json()["code"] == 200:
        return {"pub": callback.json()["pub"], "priv": callback.json()["priv"]}

    elif callback.json()["code"] == 520:
        raise UnknownError()

    else:
        if callback.json()["error"] == "invalid wallet":
            raise InvalidType(callback)
        elif callback.json()["error"] == "invalid type":
            raise InvalidType(callback)



class wallet:
    def __init__(self, pub: str, priv: str) -> None:
        self.pub = pub
        self.priv = priv
        self.link = url
        self.wallet_type = "0.01"

    def check_amount(self) -> int:
        # function for checking amount

        payload = {"pub": self.pub, "priv": self.priv}
        callback = r.get(self.link + "/wallet/amount/", params=payload)

        if callback.json()["code"] == 200:
            return callback.json()["amount"]

        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "there is no such wallet":
                raise NonExistentWallet(callback)
            elif callback.json()["error"] == "invalid type":
                raise InvalidType(callback)



    def send_amount(self, to: str, amount: int) -> None:
        # function for making transfers

        payload = {"to_pub": to, "from_pub": self.pub, "from_priv": self.priv, "amount": amount}
        callback = r.get(self.link + "/amount/send/", params=payload)

        if callback.json()["code"] == 200:
            return payload

        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "invalid to_pub wallet code":
                raise InvalidPubCode(callback)
            elif callback.json()["error"] == "invalid amount":
                raise InvalidAmount(callback)
            elif callback.json()["error"] == "not enough amount":
                raise NotEnoughAmount(callback)
            elif callback.json()["error"] == "invalid type":
                raise InvalidType(callback)





    def check_transaction(self):
        # function for check transaction

        payload = {"priv": self.priv, "pub": self.priv}
        callback = r.get(self.link + "/wallet/transactions/", params=payload)

        if callback.json()["code"] == 200:
            return callback.json()["transaction"]


        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "invalid type":
                raise InvalidType(callback)
