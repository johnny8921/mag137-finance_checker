import ccxt.pro as ccxt
import asyncio



class FinanceWatcher:
    _orderbooks = {}

    currency_holder = {}

    def _when_orderbook_changed(self, exchange_spot, symbol, orderbook):
        # это обычная функция обработчика, она вызывается при обновлении любой книги заказов
        # у нее есть доступ как к книге заказов, которая была обновлена, а также остальные книги заказов
        # распечатайте здесь только одну книгу заказов
        book = {}
        book['datetime'] = orderbook['datetime']
        book['asks'] = orderbook['asks'][0]
        book['bids'] = orderbook['bids'][0]

        currency_holder['lastUpdate'] = exchange_spot.iso8601(exchange_spot.milliseconds())
        currency_holder[symbol] = book

        print(currency_holder)
        #  или распечатайте все книги заказов, на которые уже была оформлена подписка -на
        # for symbol, orderbook in orderbooks.items():
        # print(orderbook['datetime'], symbol, orderbook['asks'][0], orderbook['bids'][0])


    async def watch_one_orderbook(exchange_spot, symbol):
        # a call cost of 1 in the queue of subscriptions
        # means one subscription per exchange.rateLimit milliseconds
        your_delay = 1
        await exchange_spot.throttle(your_delay)
        while True:
            try:
                _orderbooks[symbol] = await exchange_spot.watch_order_book(symbol)
                _when_orderbook_changed(exchange_spot, symbol, orderbook)
            except Exception as e:
                print(type(e).__name__, str(e))


    async def watch_some_orderbooks(exchange_spot, symbol_list):
        loops = [watch_one_orderbook(exchange_spot, symbol) for symbol in symbol_list]
        # let them run, don't for all tasks cause they execute asynchronously
        # don't print here
        await asyncio.gather(*loops)


    async def _print_currency_dict():
        while True:
            print()
        pass


    async def main():
        exchange_spot = ccxt.binance()
        await exchange_spot.load_markets()
        await watch_some_orderbooks(exchange_spot, ['ZEN/USDT', 'RUNE/USDT', 'AAVE/USDT', 'SNX/USDT'])
        await exchange_spot.close()


# st.write(out)
asyncio.run(main())
