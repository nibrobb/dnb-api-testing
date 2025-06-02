import json
import os
from enum import Enum

from requests import get

# https://developer.dnb.no/

class Environment(str, Enum):
    TEST = "TEST"
    LIVE = "LIVE"

ENV = {
    Environment.LIVE: "https://developer-api.dnb.no",
    Environment.TEST: "https://developer-api-testmode.dnb.no",
}

class Currency(str, Enum):
    NOK = "NOK"
    SEK = "SEK"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"


def get_quote(
    environment: Environment = Environment.TEST,
    quote_currency: Currency = Currency.NOK,
):
    """
    :param environment: "test" or "live"
    :param quote_currency: ISO 4217
    """
    base_url = ENV[environment]

    response = get(
        url=base_url + f"/v2/convert/{quote_currency.value}",
        headers={"x-api-key": os.environ.get(f"TEST_APP_{environment.value}_API_KEY")}
    )

    return response.json()


def get_convert(
    environment: Environment = Environment.TEST,
    buy_currency: Currency = Currency.EUR,
    sell_currency: Currency = Currency.NOK,
):
    """
    :param environment: "test" or "live"
    :param buy_currency: ISO 4217
    :param sell_currency: ISO 4217
    """
    base_url = ENV[environment]

    response = get(
        url=base_url + f"/v2/{buy_currency.value}/convert/{sell_currency.value}",
        params={"buyAmount": 1},
        headers={"x-api-key": os.environ.get(f"TEST_APP_{environment.value}_API_KEY")}
    )

    return response.json()


if __name__ == "__main__":
    # 02.06.2025:
    #   Test does not work because their SSL certificate is expired
    #   Live does not work because I am not authorized

    res = json.dumps(get_convert(Environment.LIVE), indent=2)
    print(res)

    res = json.dumps(get_quote(Environment.LIVE), indent=2)
    print(res)

    res = json.dumps(get_convert(Environment.TEST), indent=2)
    print(res)

    res = json.dumps(get_quote(Environment.TEST), indent=2)
    print(res)
