"""Classes de Pagamento -- Factory Method"""

from abc import ABC, abstractmethod
from .order import Order

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        ...
        
class PixPayment(Payment):
    def pay(self, amount: float):
        print(f"Pagamento via PIX no valor de {amount:.2f}")
        
class CreditCardPayment(Payment):
    def pay(self, amount: float):
        print(f"Pagamento via Cartão de Crédito no valor de {amount:.2f}")
        
class BoletoPayment(Payment):
    def pay(self, amount: float):
        print(f"Pagamento via Boleto no valor de {amount:.2f}")


# Factory (Processor)

class PaymentProcessor(ABC):
    @abstractmethod
    def create_payment(self):
        ...
        
    def process_order(self, order: Order):
        payment = self.create_payment()
        payment.pay(amount=order.total())
        
class PixProcessor(PaymentProcessor):
    def create_payment(self):
        return PixPayment()
    
class CreditCardProcessor(PaymentProcessor):
    def create_payment(self):
        return CreditCardPayment()
    
class BoletoProcessor(PaymentProcessor):
    def create_payment(self):
        return BoletoPayment()
    

    
    