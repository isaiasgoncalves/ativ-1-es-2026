"""Canal KIOSK -- extensão da questão 5.

Adicionado sem alterar src/channels.py, src/channel_registry.py ou
src/order_service.py: só implementa as mesmas abstrações e é registrado
na inicialização da aplicação (ver main.py). Demonstra OCP: o sistema
está aberto a esta extensão e fechado para modificação dos módulos acima.
"""

from src.channels import ChannelFactory, Checkout, Notification


class KioskCheckout(Checkout):
    def show(self, order):
        return f"[KIOSK] Confirme o pedido de {order.customer} no totem -- total: {order.total()}"


class KioskNotification(Notification):
    def send(self, order):
        return f"[KIOSK] Comprovante impresso para {order.customer}."


class KioskFactory(ChannelFactory):
    def create_checkout(self):
        return KioskCheckout()

    def create_notification(self):
        return KioskNotification()
