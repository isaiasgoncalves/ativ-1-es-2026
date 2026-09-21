"""Testes de Pedido e Produto -- Builder"""

import unittest
from src.order import Order, OrderBuilder, Product

class TestOrderBuilder(unittest.TestCase):
    
    def setUp(self):
        self.keyboard = Product("Teclado", 350.00)
        self.mouse = Product("Mouse", 99.90)
        
    def test_construcao_com_dois_produtos(self):
        order = (
            OrderBuilder()
            .set_client("Luis Bueno")
            .add_product(self.keyboard)
            .add_product(self.mouse)
            .build()
        )
        
        self.assertIsInstance(order, Order)
        self.assertEqual(order.client, "Luis Bueno")
        self.assertEqual(len(order.products), 2)
        self.assertIn(self.keyboard, order.products)
        self.assertIn(self.mouse, order.products)
        self.assertAlmostEqual(order.total(), 449.90)
        
    def test_construcao_com_atributos_opcionais(self):
        order = (
            OrderBuilder()
            .set_client("Luis Bueno")
            .set_address("Rua Exemplo, 42")
            .set_coupon("DESCONTO10")
            .set_payment_method("pix")
            .set_obs("Entregar à tarde")
            .add_product(self.keyboard)
            .build()
        )

        self.assertEqual(order.address, "Rua Exemplo, 42")
        self.assertEqual(order.coupon, "DESCONTO10")
        self.assertEqual(order.payment_method, "pix")
        self.assertEqual(order.obs, "Entregar à tarde")
        
    def test_construcao_sem_cliente_e_rejeitada(self):
        builder = OrderBuilder().add_product(self.keyboard)

        with self.assertRaises(ValueError):
            builder.build()
            
    def test_pedido_construido_nao_muda_ao_reutilizar_builder(self):
        builder = (
            OrderBuilder()
            .set_client("Luis Bueno")
            .add_product(self.keyboard)
        )

        first_order = builder.build()

        builder.add_product(self.mouse)
        second_order = builder.build()

        self.assertEqual(len(first_order.products), 1)
        self.assertEqual(len(second_order.products), 2)
        self.assertNotIn(self.mouse, first_order.products)
            
if __name__ == "__main__":
    unittest.main()