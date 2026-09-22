"""Testes de integração de OrderService -- questão 6."""

import unittest
from unittest.mock import patch

from src.channel_registry import _factories, get_channel_factory, register_factory
from src.channels import MobileFactory, WebFactory
from src.event_logger import EventLogger
from src.kiosk_channel import KioskFactory
from src.order_service import OrderService
from src.order import OrderBuilder, Product
from src.payment import PixPayment, PixProcessor


class TestIntegracaoOrderService(unittest.TestCase):
    def setUp(self):
        _factories.clear()
        register_factory("WEB", WebFactory())
        register_factory("MOBILE", MobileFactory())
        register_factory("KIOSK", KioskFactory())

    def test_fluxo_completo_canal_web(self):
        order = (OrderBuilder()
            .set_customer("Carla")
            .set_products([
                Product("Produto A", 120.0)
                ])
            .set_payment_method("PIX")
            .build())
        logger = EventLogger()
        service = OrderService(PixProcessor(), get_channel_factory("WEB"), logger)

        with patch.object(PixPayment, "pay") as mock_pay:
            checkout_message, notification_message = service.process_order(order)

        self.assertIn("Carla", checkout_message)
        self.assertIn("Carla", notification_message)
        mock_pay.assert_called_once_with(amount=120.0)
        self.assertEqual(len(logger.events), 3)

    def test_fluxo_completo_canal_kiosk_sem_alterar_order_service(self):
        order = (OrderBuilder()
            .set_customer("Diego")
            .set_products([
                Product("Produto B", 75.0)
                ])
            .set_payment_method("PIX")
            .build())
        service = OrderService(PixProcessor(), get_channel_factory("KIOSK"))

        with patch.object(PixPayment, "pay") as mock_pay:
            checkout_message, notification_message = service.process_order(order)

        self.assertIn("Diego", checkout_message)
        self.assertIn("KIOSK", checkout_message)
        mock_pay.assert_called_once_with(amount=75.0)

    def test_order_service_apenas_delega_pagamento_ao_colaborador(self):
        """OrderService não decide qual mecanismo de pagamento usar: só
        chama o PaymentProcessor injetado."""

        order = (OrderBuilder()
            .set_customer("Erika")
            .set_products([
                Product("Produto C", 10.0)
                ])
            .set_payment_method("PIX")
            .build())
        payment_processor = PixProcessor()
        service = OrderService(payment_processor, get_channel_factory("MOBILE"))

        with patch.object(PixProcessor, "process_order") as mock_process_order:
            service.process_order(order)

        mock_process_order.assert_called_once_with(order)


if __name__ == "__main__":
    unittest.main()
