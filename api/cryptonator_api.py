from api import _Api

class Api(_Api):

    def __init__(self):
        super().__init__("CryptonatorApi")

    def _update_rate(self, xrate):
        rate = self._get_cryptonator_rate(xrate.from_currency, xrate.to_currency)
        return rate

    def _get_cryptonator_rate(self, from_currency, to_currency):
        aliases_map = {1000: "btc", 980: "uah", 643: "rub"}

        if from_currency not in aliases_map:
            raise ValueError(f"Invalid from_currency: {from_currency}")

        if to_currency not in aliases_map:
            raise ValueError(f"Invalid from_currency: {to_currency}")

        url_end = f"{aliases_map[from_currency]}-{aliases_map[to_currency]}"
        url = f"https://api.cryptonator.com/api/ticker/{url_end}"
        response = self._send_request(url=url, method="get")
        response_json = response.json()
        self.log.debug("Cryptonator response: %s" % response_json)
        rate = self._find_rate(response_json)

        return rate

    def _find_rate(self, response_data):
        if "ticker" not in response_data:
            raise ValueError(f"Not found ticker")

        if "price" not in response_data["ticker"]:
            raise ValueError(f"Not found ticker.price")
        
        return float(response_data["ticker"]["price"])











