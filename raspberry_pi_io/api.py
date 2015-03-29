import requests


class InvalidDeviceConfigResponse(Exception):
    pass


class DeviceConfig(object):

    def __init__(self, api, user_email, user_key, device_id):
        self.url = "{0}/pin-config".format(api)
        self.headers = {
            'io-user-email': user_email,
            'io-user-key': user_key,
            'io-device-id': device_id
        }

    def get(self):
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            if r.status_code == 403:
                raise InvalidDeviceConfigResponse("Not authorized")
            if r.status_code == 401:
                raise InvalidDeviceConfigResponse("Authentication failed")
            raise InvalidDeviceConfigResponse("Pin Config request failed")
        return r.json()
