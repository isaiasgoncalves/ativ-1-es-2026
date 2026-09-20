"""Testes Unitários para a classe AppConfig -- Singleton"""

import unittest
from src.app_config import AppConfig

class TestAppConfig(unittest.TestCase):
    
    def setUp(self):
        """
        Reiniciando instância a cada execução
        """
        AppConfig._instance = None
        
    def test_valores_iniciais(self):
        """
        Testando se as configuações padrão são as mesmas estabelecidas no enunciado
        """
        
        config = AppConfig()
        
        self.assertEqual(config.environment, "production")
        self.assertEqual(config.currency, "BRL")
        self.assertFalse(config.debug)
        
    def test_duas_chamadas_retornam_mesmo_objeto(self):
        """
        Testa se o Singleton está implementado corretamente, verificando se
        dois objetos AppConfig apontam para a mesma instância (endereço de memória)
        """
        
        config1 = AppConfig()
        config2 = AppConfig()
        
        # config1 is config2
        self.assertIs(config1, config2)
        
    def test_alteracao_e_compartilhada_entre_referencias(self):
        """
        Verifica se alterar um dos parâmetros de um singleton altera
        todos os objetos da mesma instância
        """
        
        config1 = AppConfig()
        config2 = AppConfig()
        
        config1.currency = "USD"
        self.assertEqual(config2.currency, "USD")
        
    def test_nova_chamada_nao_restaura_os_valores(self):
        """
        Verifica se uma nova chamada da instância não restaura os parâmetros originais da clase
        """    
        
        config1 = AppConfig()
        config1.environment = "development"
        config1.debug = True
        
        config2 = AppConfig()
        
        self.assertEqual(config2.environment, "development")
        self.assertTrue(config2.debug)
        
        
if __name__ == "__main__":
    unittest.main()
    