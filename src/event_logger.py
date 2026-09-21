"""Registro de eventos do fluxo de pedidos.

Responsabilidade única extraída do antigo save_log() de OrderService:
apenas registra o que aconteceu, sem coordenar o fluxo nem decidir
pagamento/notificação.
"""

from datetime import datetime


class EventLogger:
    def __init__(self):
        self._events = []

    def log(self, message):
        entry = f"[{datetime.now().isoformat(timespec='seconds')}] {message}"
        self._events.append(entry)
        return entry

    @property
    def events(self):
        return list(self._events)
