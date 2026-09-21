"""Coordenação do fluxo de um pedido (questão 6).

OrderService só chama colaboradores já prontos (PaymentProcessor e
ChannelFactory, recebidos por injeção). Ele não constrói pedidos (Builder),
não escolhe classes concretas de pagamento ou notificação (Factory Method /
Abstract Factory) e não guarda configuração global (Singleton) -- cada uma
dessas responsabilidades pertence ao seu próprio componente.
"""


class OrderService:
    def __init__(self, payment_processor, channel_factory, logger=None):
        self._payment_processor = payment_processor
        self._channel_factory = channel_factory
        self._logger = logger

    def process_order(self, order):
        checkout = self._channel_factory.create_checkout()
        checkout_message = checkout.show(order)
        self._log(f"Checkout apresentado: {checkout_message}")

        self._payment_processor.process_order(order)
        self._log(f"Pagamento processado. Total: {order.total()}")

        notification = self._channel_factory.create_notification()
        notification_message = notification.send(order)
        self._log(f"Notificação enviada: {notification_message}")

        return checkout_message, notification_message

    def _log(self, message):
        if self._logger is not None:
            self._logger.log(message)
