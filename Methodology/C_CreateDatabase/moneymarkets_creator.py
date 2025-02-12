import json
import os
from tqdm import tqdm


def fill_data_points_moneymarkets(data_symbol, options=None):
    if options is None:
        options = {}
    try:
        options['short_name'] = data_symbol['quoteType']['shortName']
    except (TypeError, KeyError):
        options['short_name'] = None
    try:
        options['long_name'] = data_symbol['quoteType']['longName']
    except (TypeError, KeyError):
        options['long_name'] = None
    try:
        options['currency'] = data_symbol['price']['currency']
    except (TypeError, KeyError):
        options['currency'] = None
    try:
        options['market'] = data_symbol['quoteType']['market']
    except (TypeError, KeyError):
        options['market'] = None
    try:
        options['exchange'] = data_symbol['quoteType']['exchange']
    except (TypeError, KeyError):
        options['exchange'] = None
    return options


def make_directories_and_fill_json_moneymarkets(data, directory_name):
    try:
        market_dictionaries = {}
        symbols_dictionaries = {}
        Errors = {}
        os.mkdir(directory_name)
    except FileExistsError:
        return print(directory_name + " already exists. Please delete or rename the directory "
                                      "before continuing")

    print("Creating folder structure")
    for symbol in tqdm(data):
        options = fill_data_points_moneymarkets(data[symbol])
        symbols_dictionaries[symbol] = options

        try:
            market = data[symbol]['quoteType']['market']

            if market not in market_dictionaries and market is not None:
                if len(market) > 0:
                    market_dictionaries[market] = {}

            market_dictionaries[market][symbol] = options
        except (TypeError, KeyError) as e:
            Errors[symbol + ' Category'] = "Could not be categorized due to: " + str(e)

    print('Filling folders with data..')
    for market in tqdm(market_dictionaries.keys()):
        market_new = market.replace('/', ' ')
        with open(directory_name + '/' + market_new + '.json', 'w') as handle:
            json.dump(market_dictionaries[market], handle, indent=4)
    with open(directory_name + '/_' + directory_name + ".json", 'w') as handle:
        json.dump(symbols_dictionaries, handle, indent=4)

    if Errors:
        print("A couple of tickers were not able to be categorized. Please check the output of this function.")
        return Errors
