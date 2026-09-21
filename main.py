"""Ponto de entrada: inicialização da aplicação e execução do fluxo completo.

O registro das fábricas de canal acontece aqui, na inicialização -- é por
isso que adicionar KIOSK (questão 5) só exige criar src/kiosk_channel.py e
somar duas linhas neste arquivo, sem tocar em channel_registry.py,
channels.py nem order_service.py.

_DemoOrder e _DemoPaymentProcessor são substitutos mínimos para Order/
OrderBuilder e PaymentProcessor (parte do Isaías). Quando esses componentes
estiverem prontos, troque as duas classes abaixo pelos reais e o restante
do fluxo (OrderService, ChannelFactory, EventLogger) não muda.
"""

from src.app_config import AppConfig
from src.channel_registry import get_channel_factory, register_factory
from src.channels import MobileFactory, WebFactory
from src.event_logger import EventLogger
from src.kiosk_channel import KioskFactory
from src.order_service import OrderService


def bootstrap():
    register_factory("WEB", WebFactory())
    register_factory("MOBILE", MobileFactory())
    register_factory("KIOSK", KioskFactory())


class _DemoOrder:
    def __init__(self, customer, items):
        self.customer = customer
        self._items = items

    def total(self):
        return sum(price for _, price in self._items)


class _DemoPaymentProcessor:
    def process_order(self, order):
        print(f"Cobrando R$ {order.total():.2f} de {order.customer}.")


def run_flow(channel):
    config = AppConfig()
    print(f"-- Canal {channel} (ambiente: {config.environment}, moeda: {config.currency}) --")

    order = _DemoOrder("Cliente Demo", [("Produto A", 50.0), ("Produto B", 30.0)])
    channel_factory = get_channel_factory(channel)
    payment_processor = _DemoPaymentProcessor()
    logger = EventLogger()

    service = OrderService(payment_processor, channel_factory, logger)
    checkout_message, notification_message = service.process_order(order)

    print(checkout_message)
    print(notification_message)
    for event in logger.events:
        print(event)


if __name__ == "__main__":
    bootstrap()
    run_flow("WEB")
    print()
    run_flow("KIOSK")
