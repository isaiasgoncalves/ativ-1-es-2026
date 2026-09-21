"""Testes do registro de fábricas de canal -- questão 5."""

import unittest

from src import channel_registry
from src.channels import MobileFactory, WebFactory
from src.kiosk_channel import KioskFactory


class TestChannelRegistry(unittest.TestCase):
    def setUp(self):
        channel_registry._factories.clear()

    def test_registra_e_recupera_fabrica(self):
        factory = WebFactory()
        channel_registry.register_factory("WEB", factory)

        self.assertIs(channel_registry.get_channel_factory("WEB"), factory)

    def test_busca_e_case_insensitive(self):
        factory = MobileFactory()
        channel_registry.register_factory("MOBILE", factory)

        self.assertIs(channel_registry.get_channel_factory("mobile"), factory)

    def test_canal_desconhecido_gera_erro_claro(self):
        channel_registry.register_factory("WEB", WebFactory())

        with self.assertRaises(ValueError) as ctx:
            channel_registry.get_channel_factory("FAX")

        self.assertIn("FAX", str(ctx.exception))

    def test_kiosk_e_registrado_sem_alterar_get_channel_factory(self):
        """KIOSK é adicionado só chamando register_factory com a nova
        fábrica -- get_channel_factory (importado sem alterações) já
        sabe encontrá-lo."""

        kiosk = KioskFactory()
        channel_registry.register_factory("KIOSK", kiosk)

        self.assertIs(channel_registry.get_channel_factory("KIOSK"), kiosk)


if __name__ == "__main__":
    unittest.main()
