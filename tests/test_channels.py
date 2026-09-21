"""Testes das famílias de canal (Abstract Factory) -- questão 4."""

import unittest

from src.channels import (
    MobileCheckout,
    MobileFactory,
    MobileNotification,
    WebCheckout,
    WebFactory,
    WebNotification,
)
from src.order_service import OrderService
from src.order import Order, OrderBuilder, Product


class TestWebFactory(unittest.TestCase):
    def test_cria_checkout_e_notificacao_web(self):
        factory = WebFactory()

        self.assertIsInstance(factory.create_checkout(), WebCheckout)
        self.assertIsInstance(factory.create_notification(), WebNotification)

    def test_checkout_web_menciona_cliente_e_total(self):
        checkout = WebCheckout()
        order = (OrderBuilder()
            .set_customer("Ana")
            .set_products([
                Product("Produto A", 70.0),
                Product("Produto B", 30.0)
                ])
            .build())

        message = checkout.show(order)

        self.assertIn("Ana", message)
        self.assertIn("100.0", message)


class TestMobileFactory(unittest.TestCase):
    def test_cria_checkout_e_notificacao_mobile(self):
        factory = MobileFactory()

        self.assertIsInstance(factory.create_checkout(), MobileCheckout)
        self.assertIsInstance(factory.create_notification(), MobileNotification)

    def test_notificacao_mobile_menciona_cliente(self):
        notification = MobileNotification()
        order = (OrderBuilder()
            .set_customer("Beto")
            .set_products([
                Product("Produto C", 50.0)
                ])
            .build())

        message = notification.send(order)

        self.assertIn("Beto", message)


class TestFamiliasPorCanalSaoIndependentes(unittest.TestCase):
    def test_web_e_mobile_produzem_tipos_diferentes(self):
        web = WebFactory()
        mobile = MobileFactory()

        self.assertNotEqual(type(web.create_checkout()), type(mobile.create_checkout()))
        self.assertNotEqual(
            type(web.create_notification()), type(mobile.create_notification())
        )


class TestComportamentoAdicionalDeFactory(unittest.TestCase):
    """Teste adicional da questão 7 (criação de objetos por uma fábrica).

    Comportamento verificado: cada chamada a create_checkout() devolve uma
    nova instância, isto é, a fábrica não reaproveita/cacheia o produto.
    Resultado esperado: duas chamadas sucessivas produzem objetos distintos.
    Importância: se a fábrica devolvesse sempre o mesmo objeto, pedidos
    concorrentes acabariam compartilhando estado do checkout indevidamente.
    """

    def test_fabrica_cria_uma_nova_instancia_a_cada_chamada(self):
        factory = WebFactory()

        checkout_1 = factory.create_checkout()
        checkout_2 = factory.create_checkout()

        self.assertIsNot(checkout_1, checkout_2)


if __name__ == "__main__":
    unittest.main()
