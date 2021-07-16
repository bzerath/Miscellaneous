from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt

historic_path = r"C:\Users\bzera\OneDrive\Binance_ETHBTC_1h.csv"
window_size = 6
PERCENTAGE_DIFF = 0.6/100
RISK = 0.99


class Portefeuille:
    def __init__(self, ethereum: Decimal, bitcoin: Decimal):
        self.stock_ethereum = Decimal(ethereum)
        self.stock_bitcoin = Decimal(bitcoin)
        self._old_stock_ethereum = Decimal(0.)
        self._old_stock_bitcoin = Decimal(0.)

    def _buy_btc(self, taux_ethbtc: Decimal):
        return Decimal(self.stock_ethereum * taux_ethbtc)

    def _buy_eth(self, taux_ethbtc: Decimal):
        return Decimal(self.stock_bitcoin / taux_ethbtc)

    def buy_btc(self, taux_ethbtc: Decimal, secure=False):
        if secure:
            if not self.is_buying_btc_a_good_win(taux_ethbtc):
                return False
        if self.stock_ethereum > Decimal(0.):
            self.stock_bitcoin = self._buy_btc(taux_ethbtc)
            self._old_stock_ethereum = Decimal(self.stock_ethereum)
            self.stock_ethereum = Decimal(0.)
            return self.stock_bitcoin

    def buy_eth(self, taux_ethbtc: Decimal, secure=False):
        if secure:
            if not self.is_buying_eth_a_good_win(taux_ethbtc):
                return False
        if self.stock_bitcoin > Decimal(0.):
            self.stock_ethereum = self._buy_eth(taux_ethbtc)
            self._old_stock_bitcoin = Decimal(self.stock_bitcoin)
            self.stock_bitcoin = Decimal(0.)
            return self.stock_ethereum

    def is_buying_eth_a_good_win(self, taux_ethbtc: Decimal):
        print(taux_ethbtc, self._buy_eth(taux_ethbtc), self._old_stock_ethereum)
        return (self._buy_eth(taux_ethbtc)) > (self._old_stock_ethereum * Decimal(RISK))

    def is_buying_btc_a_good_win(self, taux_ethbtc: Decimal):
        return (self._buy_btc(taux_ethbtc)) > (self._old_stock_bitcoin * Decimal(RISK))


def moyenne(data: list) -> Decimal:
    return sum(data)/len(data)


def ca_a_baisse(hist: list, current_value: Decimal, previous_value: Decimal) -> bool:
    if current_value < moyenne(hist) \
            and 1-(current_value/moyenne(hist)) > PERCENTAGE_DIFF \
            and abs((data_cleaned[date]-previous_value)-1) > PERCENTAGE_DIFF:
        return True
    else:
        return False


def ca_a_monte(hist: list, current_value: Decimal, previous_value: Decimal) -> bool:
    if current_value > moyenne(hist) \
            and (current_value/moyenne(hist))-1 > PERCENTAGE_DIFF\
            and abs((data_cleaned[date]-previous_value)-1) > PERCENTAGE_DIFF:
        return True
    else:
        return False


def ca_bouge(hist: list, current_value: Decimal, previous_value: Decimal) -> bool:
    return ca_a_monte(hist, current_value, previous_value) or ca_a_baisse(hist, current_value, previous_value)


if __name__ == "__main__":
    etat = ""
    portefeuille = Portefeuille(ethereum=Decimal(1.),
                                bitcoin=Decimal(0.))

    with open(historic_path, "r") as fichier:
        data = fichier.readlines()

    data_to_draw = {"date": [],
                    "eth": [],
                    "btc": []}

    data_cleaned = {}
    for ligne in data[1:]:
        unix, date, symbol, _open, high, low, close, Volume_ETH, Volume_BTC, tradecount = ligne.split(",")
        try:
            current_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            current_date = datetime.strptime(date, '%Y-%m-%d %H-%p')
        except:
            print(date)
            raise
        if current_date > datetime.strptime("01-05-2021", "%d-%m-%Y"):
            data_cleaned[current_date] = Decimal((Decimal(_open) + Decimal(high) + Decimal(low) + Decimal(close))/4)

    # history = [data_cleaned[sorted(data_cleaned.keys())[0]]] * window_size
    # previous_value = data_cleaned[sorted(data_cleaned.keys())[0]]

    for i, date in enumerate(sorted(data_cleaned.keys())):
        taux_current = data_cleaned[date]
        if portefeuille.is_buying_eth_a_good_win(taux_current):
            portefeuille.buy_eth(taux_current)
            print("{}\t{}\t{}\t{}".format(date,
                                          round(taux_current, 7),
                                          portefeuille.stock_ethereum,
                                          portefeuille.stock_bitcoin))
        elif portefeuille.is_buying_btc_a_good_win(taux_current):
            portefeuille.buy_btc(taux_current)
            print("{}\t{}\t{}\t{}".format(date,
                                          round(taux_current, 7),
                                          portefeuille.stock_ethereum,
                                          portefeuille.stock_bitcoin))
        data_to_draw["date"].append(date)
        data_to_draw["eth"].append(portefeuille.stock_ethereum)
        data_to_draw["btc"].append(portefeuille.stock_bitcoin)

        # history[i % window_size] = data_cleaned[date]
        # previous_value = data_cleaned[date]

    fig, ax = plt.subplots()

    ax.plot(data_to_draw["date"],
            data_to_draw["btc"],
            "o",
            label="btc",
            c="orange")
    ax.plot(data_to_draw["date"],
            data_to_draw["eth"],
            "o",
            label="eth",
            c="blue")
    ax.legend()

    plt.gcf().set_size_inches(30, 18)
    plt.show()
