# Respostas da Atividade Avaliativa - Engenharia de Sofware

> Alunos:
>  - Isaías Gouvêa Gonçalves
>  - Mateus Mourão

---

## 1 - Config (Singleton)

### 1. Explique por que utilizar `__new__` não impede, por si só, novas execuções de `__init__`.

Sempre que `AppConfig()` é invocado, é executado `__new__` que irá retornar a instância, e logo em seguida será executado o `__init__` que inicializa o objeto independente se a instância retornada era a mesma que a anterior. Então se `__init__` define atributos do objeto, sempre que a classe for invocada, `__init__` será executado novamente e os atributos serão reiniciados.

### 2. Explique como um módulo Python poderia ser utilizado para compartilhar uma configuração sem implementar uma segunda versão do Singleton.

Uma possibilidade viável seria basicamente criar um arquivo (módulo) `config.py` que armazena variáveis com os valores de configuração:

```python
environment = "production"
currency = "BRL"
debug = False

# Constantes (configurações fixas costumam a ser nomeadas com Caps)

ENVIRONMENT = "production"
CURRENCY = "BRL"
DEBUG = False
```
Quando as configurações forem utilizadas, basta importar o módulo no arquivo:

```python
import config

print(f"Moeda utilizada: {config.CURRENCY}") # BRL
```

### 3. Identifique uma possível consequência de possuir um objeto de configuração global compartilhado.

Uma possível consequência é o acoplamento, que se dá quando diversos arquivos idependentes acessam uma mesma instância de um objeto na memória -- em que qualquer componente pode acabar editando e alterando uma configuração e gerando comportamentos inesperados no resto do código. Como exemplo disso, é necessário reiniciar a instância de `AppConfig` a cada teste com `AppConfig._instance = None`.

---

## 2 - Pedido e Builder

### 1. Identifique quais componentes da sua implementação correspondem ao Builder e ao objeto construído.

_Resposta:_

### 2. Explique por que seria possível construir o pedido diretamente pelo construtor de `Order` e qual seria a diferença em relação à solução adotada.

_Resposta:_

---

## 3 - Pagamento e Factory Method

### 1. Identifique os papéis de Creator, Concrete Creator, Product e Concrete Product na implementação desenvolvida.

_Resposta:_

### 2. Explique por que uma função contendo simplesmente uma sequência de `if/elif` escolhendo classes concretas não é, por si só, suficiente para caracterizar o padrão Factory Method.

_Resposta:_

### 3. Considere que uma nova forma de pagamento seja adicionada posteriormente. Explique quais partes da implementação precisariam ser alteradas.

_Resposta:_

---

## 4 - Famílias por canal e Abstract Factory

### 1. Explique por que checkout e notificação podem ser considerados uma família de produtos.

_Resposta:_

### 2. Explique qual problema a Abstract Factory resolve nessa situação.

_Resposta:_

### 3. Explique por que o pagamento não deve fazer parte da fábrica responsável pelo canal.

_Resposta:_

---

## 5 - Seleção de fábrica e canal KIOSK

### 1. Liste os arquivos criados ou alterados para adicionar KIOSK.

_Resposta:_

### 2. Explique por que as alterações realizadas são ou não compatíveis com o princípio OCP.

_Resposta:_

---

## 6 - Responsabilidades e integração

As respostas desta seção devem considerar a implementação efetivamente entregue pela dupla.

### 1. Qual é a responsabilidade principal de cada componente criado?

_Resposta:_

### 2. Escolha três componentes diferentes e indique uma mudança que deveria ficar restrita a cada um deles.

_Resposta:_

### 3. Identifique uma decisão de projeto da solução que poderia ser diferente. Explique qual seria a alternativa e qual seria a consequência dessa mudança.

_Resposta:_

---

## 7 - Testes adicionais

Para cada teste, informe o comportamento verificado, o resultado esperado e por que esse comportamento é importante para a solução. Os comportamentos não devem ser exatamente os exemplos apresentados no enunciado.

### Teste adicional de Singleton

#### Comportamento verificado

_Resposta:_

#### Resultado esperado

_Resposta:_

#### Por que esse comportamento é importante

_Resposta:_

### Teste adicional de Builder

#### Comportamento verificado

_Resposta:_

#### Resultado esperado

_Resposta:_

#### Por que esse comportamento é importante

_Resposta:_

### Teste adicional de criação por Factory

#### Comportamento verificado

_Resposta:_

#### Resultado esperado

_Resposta:_

#### Por que esse comportamento é importante

_Resposta:_

---

## 8 - Nova forma de pagamento

### 1. Quais arquivos foram criados ou modificados?

_Resposta:_

### 2. O fluxo principal de processamento precisou ser alterado?

_Resposta:_

### 3. Quais classes existentes precisaram ser modificadas?

_Resposta:_

### 4. Explique como o Factory Method contribuiu para essa extensão.

_Resposta:_

### 5. Compare essa alteração com a inclusão do canal KIOSK. Quais são as semelhanças e diferenças arquiteturais entre as duas extensões?

_Resposta:_

---
