""" Classe única de configuração da aplicação -- Implementar Singleton """


class AppConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.environment = "production"
            cls._instance.currency = "BRL"
            cls._instance.debug = False
            
            
        return cls._instance
    
