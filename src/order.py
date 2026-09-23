"""Produto, pedido e Builder de pedido.

Os valores monetários usam ``float`` para manter o exemplo simples. Em um
sistema real, um tipo decimal seria mais apropriado.
"""

from .app_config import AppConfig

# Definindo produto

class Product:
    def __init__(self, name: str, price: float):    
        self.name = name
        self.price = float(price)
        
    def __str__(self):
        return f"Produto: {self.name}\nValor:R${self.price:.2f}"
        
# Classe de Pedido        

class Order:
    def __init__(self,
                 customer: str,
                 products: list[Product] | None = None,
                 address: str | None = None,
                 coupon: str | None = None,
                 payment_method: str | None = None,
                 obs: str | None = None):
        
        self.customer = customer
        self.products = list(products) if products is not None else []
        self.address = address
        self.coupon = coupon
        self.payment_method = payment_method
        self.obs = obs
        
    def total(self):
        """Retorna os preços de todos os produtos de um pedido somados"""
        return sum(product.price for product in self.products)
    
    def __str__(self):
        """Retorna uma representação textual do pedido em formato de recibo."""
        
        width = 45
        name_width = 35
        value_width = width - name_width - 1
        currency = AppConfig().currency
        lines = [
            "=" * width,
            "PEDIDO".center(width),
            "=" * width,
            f"Cliente:  {self.customer}",
            f"Endereço: {self.address or '[Não informado]'}",
            "-" * width,
            (
                f"{'PRODUTO':<{name_width}} "
                f"{f'VALOR ({currency})':>{value_width}}"
            ),
            "-" * width,
        ]
        for product in self.products:
            name = product.name[:name_width]

            lines.append(
                f"{name:<{name_width}} "
                f"{product.price:>{value_width}.2f}"
            )
        lines.extend(
            [
                "-" * width,
                (
                    f"{'TOTAL DO PEDIDO':<{name_width}} "
                    f"{self.total():>{value_width}.2f}"
                ),
                "=" * width,
                f"Forma de pagamento: {self.payment_method or '[Não informada]'}",
                f"Cupom:              {self.coupon or '[Não informado]'}",
                f"Observação:         {self.obs or '[Nenhuma]'}",
                "=" * width,
            ]
        )
        return "\n".join(lines)
        
# Builder de pedido

class OrderBuilder:
    def __init__(self):
        self.customer = None
        self.products = []
        self.address = None
        self.coupon = None
        self.payment_method = None
        self.obs = None
        
    def set_customer(self, customer: str):
        self.customer = customer
        return self
    
    def set_address(self, address: str):
        self.address = address
        return self
    
    def set_coupon(self, coupon):
        self.coupon = coupon
        return self
    
    def set_payment_method(self, payment_method: str):
        self.payment_method = payment_method
        return self
    
    def set_obs(self, obs):
        self.obs = obs
        return self
    
    def set_products(self, products: list[Product]):
        """Substitui lista de produtos por uma nova fornecida"""
        self.products = products.copy() # Substituindo por cópia
        return self
        
    def add_product(self, product: Product):
        """Adiciona um produto à lista do pedido em construção."""
        self.products.append(product)
        return self
        
    def build(self):
        """Verifica se foi definido um cliente, e gera o objeto Order com base nos parâmetros dados"""
        
        if self.customer is None:
            raise ValueError("O pedido precisa ter um cliente para ser criado")
        
        return Order(
            customer=self.customer,
            products=self.products.copy(), # Caso reutilizemos a lista de produtos de novo
            address=self.address,
            coupon=self.coupon,
            payment_method=self.payment_method,
            obs=self.obs
        )
        
if __name__ == "__main__":
    
    """Testando"""
    
    order = (OrderBuilder()
             .set_customer("Luis Bueno")
             .set_address("Rua Bambina 67, Botafogo")
             .set_payment_method("pix")
             .add_product(Product("Engenharia de IA - Chip Huyen", 129.99))
             .add_product(Product("Dom Casmurro - Machado de Assis", 49.99))
             .add_product(Product("Teclado Mecânico Aula F87", 349.99))
             .add_product(Product("KitKat sabor limão", 5.99))
             .build())
    
    print(order)
