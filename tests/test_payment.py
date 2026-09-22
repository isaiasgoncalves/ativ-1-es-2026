import unittest
from unittest.mock import patch

from src.order import OrderBuilder, Product
from src.payment import PixPayment, PixProcessor, CreditCardPayment, CreditCardProcessor, PayPalPayment, PayPalProcessor


class TestPaymentProcessor(unittest.TestCase):
    def test_processa_pedido_com_pix(self):
        order = (
            OrderBuilder()
            .set_customer("Adrian")
            .set_payment_method("PIX")
            .add_product(Product("Fone de Ouvido QCY H3", 350.00))
            .add_product(Product("Copo de café nespresso", 99.90))
            .build()
        )

        with patch.object(PixPayment, "pay") as mock_pay:
            PixProcessor().process_order(order)

        self.assertEqual(order.payment_method, "PIX")
        mock_pay.assert_called_once_with(amount=449.90)
        
    def test_processa_pedido_com_cartao_de_credito(self):
        order = (
            OrderBuilder()
            .set_customer("Saulo")
            .add_product(Product("Notebook Dell Inspiron 15 Intel 16GB", 3549.99))
            .add_product(Product("Monitor Alienware 27' QuadHD 165Hz", 2279.99))
            .set_payment_method("Cartão de Crédito")
            .build()
        )

        with patch.object(CreditCardPayment, "pay") as mock_pay:
            CreditCardProcessor().process_order(order)

        self.assertEqual(order.payment_method, "Cartão de Crédito")
        mock_pay.assert_called_once_with(amount=5829.98)
        
    def test_processa_pedido_com_paypal(self):
        order = (
            OrderBuilder()
            .set_customer("Pedro")
            .set_payment_method("PayPal")
            .add_product(Product("Fritadeira a Ar Mondial", 350.00))
            .add_product(Product("Perfume Malbec", 99.90))
            .build()
        )

        with patch.object(PayPalPayment, "pay") as mock_pay:
            PayPalProcessor().process_order(order)

        self.assertEqual(order.payment_method, "PayPal")
        mock_pay.assert_called_once_with(amount=449.90)
        
        
        