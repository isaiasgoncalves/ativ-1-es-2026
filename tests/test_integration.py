"""Testes de integração de OrderService -- questão 6.

TODO: Substituir _FakePaymentProcessor pela classe implementada pelo Isaías
"""

import unittest

from src.channel_registry import _factories, get_channel_factory, register_factory
from src.channels import MobileFactory, WebFactory
from src.event_logger import EventLogger
from src.kiosk_channel import KioskFactory
from src.order_service import OrderService
from src.order_service import OrderService
from src.order import Order, OrderBuilder, Product


class _FakePaymentProcessor:
    def __init__(self):
        self.processed = []

    def process_order(self, order):
        self.processed.append(order)


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
            .build())
        payment_processor = _FakePaymentProcessor()
        logger = EventLogger()
        service = OrderService(payment_processor, get_channel_factory("WEB"), logger)

        checkout_message, notification_message = service.process_order(order)

        self.assertIn("Carla", checkout_message)
        self.assertIn("Carla", notification_message)
        self.assertIn(order, payment_processor.processed)
        self.assertEqual(len(logger.events), 3)

    def test_fluxo_completo_canal_kiosk_sem_alterar_order_service(self):
        order = (OrderBuilder()
            .set_customer("Diego")
            .set_products([
                Product("Produto B", 75.0)
                ])
            .build())
        payment_processor = _FakePaymentProcessor()
        service = OrderService(payment_processor, get_channel_factory("KIOSK"))

        checkout_message, notification_message = service.process_order(order)

        self.assertIn("Diego", checkout_message)
        self.assertIn("KIOSK", checkout_message)
        self.assertIn(order, payment_processor.processed)

    def test_order_service_apenas_delega_pagamento_ao_colaborador(self):
        """OrderService não decide qual mecanismo de pagamento usar: só
        chama o PaymentProcessor injetado."""

        order = (OrderBuilder()
            .set_customer("Erika")
            .set_products([
                Product("Produto C", 10.0)
                ])
            .build())
        payment_processor = _FakePaymentProcessor()
        service = OrderService(payment_processor, get_channel_factory("MOBILE"))

        service.process_order(order)

        self.assertEqual(payment_processor.processed, [order])


if __name__ == "__main__":
    unittest.main()
