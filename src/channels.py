"""Abstract Factory de canal: famílias de Checkout e Notification.

Cada canal (WEB, MOBILE, ...) produz uma família coerente de objetos que
sabem apresentar o checkout e enviar a notificação daquele canal. A fábrica
de canal não conhece nem cria formas de pagamento -- isso é responsabilidade
de PaymentProcessor (questão 3), que é escolhido de forma independente.
"""

from abc import ABC, abstractmethod


class Checkout(ABC):
    @abstractmethod
    def show(self, order):
        raise NotImplementedError


class Notification(ABC):
    @abstractmethod
    def send(self, order):
        raise NotImplementedError


class ChannelFactory(ABC):
    @abstractmethod
    def create_checkout(self) -> Checkout:
        raise NotImplementedError

    @abstractmethod
    def create_notification(self) -> Notification:
        raise NotImplementedError


class WebCheckout(Checkout):
    def show(self, order):
        return f"[WEB] Checkout de {order.customer} -- total: {order.total()}"


class WebNotification(Notification):
    def send(self, order):
        return f"[WEB] E-mail enviado para {order.customer} confirmando o pedido."


class WebFactory(ChannelFactory):
    def create_checkout(self):
        return WebCheckout()

    def create_notification(self):
        return WebNotification()


class MobileCheckout(Checkout):
    def show(self, order):
        return f"[MOBILE] Tela de checkout de {order.customer} -- total: {order.total()}"


class MobileNotification(Notification):
    def send(self, order):
        return f"[MOBILE] Push enviado para {order.customer} confirmando o pedido."


class MobileFactory(ChannelFactory):
    def create_checkout(self):
        return MobileCheckout()

    def create_notification(self):
        return MobileNotification()
