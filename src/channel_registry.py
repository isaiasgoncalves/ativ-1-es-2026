"""Registro de fábricas de canal.

Mantém get_channel_factory() e o mecanismo de registro estáveis para que um
canal novo (ex.: KIOSK) possa ser adicionado só com uma nova ChannelFactory
e uma chamada a register_factory() na inicialização da aplicação -- sem
alterar este arquivo nem o código que consome Checkout/Notification.
"""

_factories = {}


def register_factory(channel, factory):
    _factories[channel.upper()] = factory


def get_channel_factory(channel):
    try:
        return _factories[channel.upper()]
    except KeyError:
        raise ValueError(
            f"Canal desconhecido: '{channel}'. "
            f"Canais registrados: {sorted(_factories)}"
        ) from None
