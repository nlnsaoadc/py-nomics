from unittest import TestCase, mock

from nomics.nomics import KeyTypeError, Nomics


class NomicsTestCase(TestCase):
    def setUp(self):
        self.api = Nomics(key="123test", paid_plans=True)
        self.api_unpaid_plans = Nomics(key="123test", paid_plans=False)

    @mock.patch(
        "requests.get", return_value=mock.Mock(status_code=200, json=lambda: {})
    )
    def test_get(self, mock_get):
        self.api._get("test")
        mock_get.assert_called_once_with(
            url="https://api.nomics.com/test",
            params={"key": "123test"},
        )

    @mock.patch("nomics.nomics.logger.warning")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=lambda: {"message": "Not Found"},
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status(self, mock_get, mock_log):
        with self.assertRaises(Exception) as context:
            self.api._get("test")
        self.assertEqual(
            "404 404 Not Found Message",
            str(context.exception),
        )
        mock_log.assert_called_once()

    @mock.patch("nomics.nomics.logger.info")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=mock.Mock(side_effect=Exception("")),
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status_fail_silently(self, mock_get, mock_log):
        self.api.fail_silently = True
        self.assertEqual(self.api._get("test"), None)
        mock_log.assert_called_once()

    @mock.patch("nomics.nomics.logger.error")
    @mock.patch("nomics.nomics.Nomics._get")
    def test_wrong_key_type(self, mock_get, mock_log):
        try:
            self.api_unpaid_plans.get_exchange_markets_ticker()
        except KeyTypeError as error:
            self.assertEqual(type(str(error)), str)
        mock_log.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currencies_ticker(self, mock_get):
        self.api.get_currencies_ticker(ids=[""], interval=[""], convert="USD")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currencies_sparkline(self, mock_get):
        self.api.get_currencies_sparkline(ids="", start="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_market(self, mock_get):
        self.api.get_market()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_marketcap_history(self, mock_get):
        self.api.get_marketcap_history(start="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_global_volume_history(self, mock_get):
        self.api.get_global_volume_history()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_rates(self, mock_get):
        self.api.get_exchange_rates()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_rates_history(self, mock_get):
        self.api.get_exchange_rates_history()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_global_ticker(self, mock_get):
        self.api.get_global_ticker(convert=True)
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currency_highlights(self, mock_get):
        self.api.get_currency_highlights(currency="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_supply_history(self, mock_get):
        self.api.get_supply_history(currency="", start="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_highlights(self, mock_get):
        self.api.get_exchange_highlights(exchange="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchanges_ticker(self, mock_get):
        self.api.get_exchanges_ticker()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchanges_volume_history(self, mock_get):
        self.api.get_exchanges_volume_history(exchange="", start="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_metadata(self, mock_get):
        self.api.get_exchange_metadata()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_market_highlights(self, mock_get):
        self.api.get_market_highlights(base="", quote="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_markets_ticker(self, mock_get):
        self.api.get_exchange_markets_ticker()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_aggregated_ohlcv_candles(self, mock_get):
        self.api.get_aggregated_ohlcv_candles(interval="", currency="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_exchange_ohlcv_candles(self, mock_get):
        self.api.get_exchange_ohlcv_candles(interval="", exchange="", market="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_aggregated_pair_ohlcv_candles(self, mock_get):
        self.api.get_aggregated_pair_ohlcv_candles(
            interval="", base="", quote=""
        )
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_trades(self, mock_get):
        self.api.get_trades(exchange="", market="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_order_book_snapshot(self, mock_get):
        self.api.get_order_book_snapshot(exchange="", market="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_order_book_batches(self, mock_get):
        self.api.get_order_book_batches(exchange="", market="")
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currency_predictions_ticker(self, mock_get):
        self.api.get_currency_predictions_ticker()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currency_predictions_history(self, mock_get):
        self.api.get_currency_predictions_history()
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currencies(self, mock_get):
        self.api.get_currencies(ids=[""], attributes=[""])
        mock_get.assert_called_once()

    @mock.patch("nomics.nomics.Nomics._get")
    def test_get_currencies_predictions_ticket(self, mock_get):
        self.api.get_currencies_predictions_ticket(ids=[""])
        mock_get.assert_called_once()
