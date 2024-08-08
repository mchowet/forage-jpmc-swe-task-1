import unittest
import random
from client3 import getDataPoint, getRatio


class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            self.assertEqual(getDataPoint(quote),
                             (quote['stock'],
                              quote['top_bid']['price'],
                              quote['top_ask']['price'],
                              round((quote['top_bid']['price'] + quote['top_ask']['price']) / 2, 2)))

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            self.assertEqual(getDataPoint(quote),
                             (quote['stock'],
                              quote['top_bid']['price'],
                              quote['top_ask']['price'],
                              round((quote['top_bid']['price'] + quote['top_ask']['price']) / 2, 2)))

    def test_getDataPoint_calculatePriceBidZero(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 0.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 0.0, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            self.assertEqual(getDataPoint(quote),
                             (quote['stock'],
                              quote['top_bid']['price'],
                              quote['top_ask']['price'],
                              round((quote['top_bid']['price'] + quote['top_ask']['price']) / 2, 2)))

    def test_getRatio_PriceAHigher(self):
        prices = [
            {'a': 5.0,       'b': 3.0},
            {'a': 5.1,       'b': 5.01},
            {'a': 5.001,     'b': 5.0001},
            {'a': 50005.0,   'b': 0.1},
            {'a': 2222222.1, 'b': 2222222.0},
        ]
        for price_pair in prices:
            self.assertGreater(getRatio(price_pair['a'], price_pair['b']), 1)

    def test_getRatio_PriceBHigher(self):
        prices = [
            {'b': 5.0, 'a': 3.0},
            {'b': 5.1, 'a': 5.01},
            {'b': 5.001, 'a': 5.0001},
            {'b': 50005.0, 'a': 0.1},
            {'b': 2222222.1, 'a': 2222222.0},
        ]

        for price_pair in prices:
            self.assertLess(getRatio(price_pair['a'], price_pair['b']), 1)

    def test_getRatio_PriceAZero(self):
        prices = [
            {'b': 5.0, 'a': 0},
            {'b': 5.1, 'a': 0.0},
            {'b': 5.001, 'a': 0},
            {'b': 50005.0, 'a': 0.0},
            {'b': 2222222.1, 'a': 0.0},
        ]

        for price_pair in prices:
            self.assertEqual(getRatio(price_pair['a'], price_pair['b']), 0.0)

    def test_getRatio_PriceBZero(self):
        prices = [
            {'a': 5.0, 'b': 0},
            {'a': 5.1, 'b': 0.00},
            {'a': 2222222.1, 'b': 0.0},
        ]

        for price_pair in prices:
            self.assertEqual(getRatio(price_pair['a'], price_pair['b']), -1)

    def test_getRatio_PricesZero(self):
        prices = [
            {'a': 0, 'b': 0.0},
            {'a': 0.0, 'b': 0},
            {'a': 0, 'b': 0},
            {'a': 0.0000, 'b': 0.0},
        ]

        for price_pair in prices:
            self.assertEqual(getRatio(price_pair['a'], price_pair['b']), -1)

    def test_getRatio_PricesEqual(self):
        prices = [0.01, 1.3, 10.10, 44.44, 99, 122.22, 300.30, 400]
        test_count = 8
        for price in prices:
            self.assertEqual(getRatio(price, price), 1)
        for _ in range(test_count):
            price = random.normalvariate() * 500 + 0.001
            self.assertEqual(getRatio(price, price), 1)


if __name__ == '__main__':
    unittest.main()
