import time
import datetime
from matplotlib import pyplot as plt

import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError


def get_historical_data(symbol, n_years=1, n_max_trials=5):
    data = None
    end = datetime.date.today()
    start = datetime.date(end.year - n_years, 1, 1)

    try:
        data = web.DataReader(symbol, "yahoo", start, end)
    except RemoteDataError as e:
        print("Couldn't get data from Yahoo.")

        n_trials = 1
        while data is None:
            print("Retrying in 1 second...")
            time.sleep(1)

            try:
                data = web.DataReader(symbol, "yahoo", start, end)
            except RemoteDataError as e:
                print("Couldn't get data from Yahoo.")

            n_trials += 1
            if n_trials > n_max_trials:
                raise(e)

    return data


def main():

    data = get_historical_data("AAPL", n_years=5)
    print("The shape of the data is : {}".format(data.shape))

    ax1 = plt.subplot(211)
    data[["Open", "High", "Low", "Close"]].plot(ax=ax1)
    ax2 = plt.subplot(212, sharex=ax1)
    data["Volume"].plot(ax=ax2)
    plt.show()


if __name__ == '__main__':
    main()
