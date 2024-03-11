# functions for calling errors
class NotEnoughAmount(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]


class InvalidWallet(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]


class InvalidType(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]

class NonExistentWallet(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]

class InvalidPubCode(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]


class InvalidAmount(Exception):
    def __init__(self, callback):
        self.callback = callback
    def __str__(self):
        return self.callback.json()["error"]

class UnknownError(Exception):
    def __str__(self):
        return "unknown error"




def unknown_error():
    raise Exception("unknown error")


def error(er):
    raise Exception(f"{er} error")
