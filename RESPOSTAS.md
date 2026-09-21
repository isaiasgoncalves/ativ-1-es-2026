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

A classe `OrderBuilder` corresponde ao Builder. Ela mantém temporariamente os dados usados na construção, como cliente, produtos, endereço, cupom, forma de pagamento e observação. Seus métodos `set_client()`, `add_product()`, `set_address()`, `set_coupon()`, `set_payment_method()` e `set_obs()` representam as etapas de configuração e retornam o próprio Builder para permitir encadeamento.
O método `build()` encerra o processo de construção. Ele verifica se o cliente obrigatório foi informado e cria uma instância de `Order`.
A classe `Order` corresponde ao objeto construído. Ela representa o pedido final e contém seus dados e comportamentos, como o método `total()`. A classe Product representa os produtos que compõem o pedido, mas não é o produto final do padrão Builder neste caso.

### 2. Explique por que seria possível construir o pedido diretamente pelo construtor de `Order` e qual seria a diferença em relação à solução adotada.

Seria possível construir o pedido diretamente porque o construtor de Order já recebe todas as informações necessárias:

```python
order = Order(
    client="Luis Bueno",
    products=[keyboard, mouse],
    address="Rua Exemplo, 42",
    coupon="DESCONTO10",
)
```

Em Python, os argumentos nomeados tornam essa construção relativamente clara, especialmente quando o objeto possui poucos campos e regras simples.
Na solução adotada, `OrderBuilder` permite que o pedido seja configurado em etapas, usando uma interface encadeada. O Builder mantém o estado intermediário da construção, permite adicionar produtos individualmente e centraliza a validação de que um cliente foi informado antes de criar o pedido.
Outra diferença é que o Builder copia a lista de produtos ao construir o Order. Dessa forma, reutilizar o mesmo Builder para criar outro pedido não modifica retroativamente um pedido já construído.
A construção direta seria mais curta, mas colocaria sobre o código cliente a responsabilidade de preparar todos os argumentos e poderia contornar a validação realizada em `build()`. O Builder se torna mais vantajoso caso o processo de criação ganhe novas etapas ou regras.

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

`Checkout` e `Notification` são duas variações que sempre aparecem juntas e precisam ser coerentes entre si: um pedido feito pelo canal WEB deve receber um `WebCheckout` e uma `WebNotification`; um pedido pelo MOBILE deve receber `MobileCheckout` e `MobileNotification`. Não faz sentido misturar, por exemplo, um checkout WEB com uma notificação MOBILE. Como esses objetos são criados aos pares, de forma consistente, e compartilham a mesma "variante" (o canal), eles formam uma família de produtos relacionados -- exatamente o que a Abstract Factory (`ChannelFactory`) foi feita para produzir.

### 2. Explique qual problema a Abstract Factory resolve nessa situação.

Sem a Abstract Factory, o código que monta o fluxo do pedido precisaria de lógica condicional (`if channel == "WEB": ... elif channel == "MOBILE": ...`) espalhada em vários pontos para escolher tanto o checkout quanto a notificação certos, correndo o risco de, em algum lugar, combinar classes de canais diferentes por engano. A `ChannelFactory` resolve isso concentrando em um único objeto (`WebFactory`, `MobileFactory`, ...) a responsabilidade de criar toda a família compatível de um canal. Quem usa a fábrica só chama `create_checkout()` e `create_notification()` sem saber qual canal está por trás, e a garantia de que os dois objetos pertencem ao mesmo canal fica embutida na própria fábrica.

### 3. Explique por que o pagamento não deve fazer parte da fábrica responsável pelo canal.

Canal de venda e forma de pagamento são escolhas independentes (WEB pode usar PIX, MOBILE pode usar cartão, e vice-versa). Se `ChannelFactory` também criasse o `Payment`, canal e forma de pagamento ficariam acoplados -- não seria possível combinar livremente um canal com qualquer forma de pagamento, e adicionar uma nova forma de pagamento exigiria mexer em todas as fábricas de canal. Ao manter o pagamento fora da `ChannelFactory` e resolvido por um `PaymentProcessor` separado (Factory Method da questão 3), as duas dimensões variam de forma independente, cada uma com sua própria responsabilidade (SRP).

---

## 5 - Seleção de fábrica e canal KIOSK

### 1. Liste os arquivos criados ou alterados para adicionar KIOSK.

**Criado:** `src/kiosk_channel.py` (com `KioskCheckout`, `KioskNotification` e `KioskFactory`, implementando as mesmas abstrações de `src/channels.py`).

**Alterado:** `main.py`, só na inicialização (`bootstrap()`), acrescentando o import de `KioskFactory` e a chamada `register_factory("KIOSK", KioskFactory())`.

**Não alterados:** `src/channel_registry.py` (o `get_channel_factory` e o mecanismo de registro continuam exatamente os mesmos), `src/channels.py` e `src/order_service.py` (o código que consome `Checkout`/`Notification` através das abstrações não precisou saber que KIOSK existe).

### 2. Explique por que as alterações realizadas são ou não compatíveis com o princípio OCP.

São compatíveis com o OCP. O módulo de registro (`channel_registry.py`) está fechado para modificação: `get_channel_factory` não teve nenhuma linha alterada e continua funcionando para qualquer canal que já esteja no dicionário `_factories`, seja WEB, MOBILE ou KIOSK. Ao mesmo tempo, o sistema está aberto para extensão: para suportar um canal novo bastou criar um arquivo novo que implementa as interfaces já existentes (`ChannelFactory`, `Checkout`, `Notification`) e registrá-lo. A única mudança em código já existente foi em `main.py`, que é a raiz de composição da aplicação (o lugar cuja função é justamente "ligar" os componentes); nenhuma classe que participa da lógica de negócio (`OrderService`, `channel_registry.py`, `channels.py`) precisou ser reaberta ou reescrita.

---

## 6 - Responsabilidades e integração

As respostas desta seção devem considerar a implementação efetivamente entregue pela dupla.

A primeira versão de `OrderService` misturava cinco responsabilidades (`create_order`, `calculate_total`, `create_payment`, `send_notification`, `save_log`). Elas foram redistribuídas assim:

* `create_order` -> `OrderBuilder` (constrói o pedido);
* `calculate_total` -> `Order.total()` (o próprio pedido sabe somar seus itens);
* `create_payment` -> `PaymentProcessor.create_payment()` de cada processador concreto (Factory Method, questão 3);
* `send_notification` -> `Notification.send(order)`, obtida de uma `ChannelFactory` (Abstract Factory, questão 4);
* `save_log` -> `EventLogger`, um componente próprio dedicado só a registrar o que aconteceu no fluxo.

O `OrderService` que sobrou só coordena: recebe por injeção um `PaymentProcessor` e uma `ChannelFactory` já prontos e chama, em sequência, `checkout.show(order)`, `payment_processor.process_order(order)`, `notification.send(order)` e (se houver) `logger.log(...)`. Ele não constrói o pedido, não decide qual classe concreta de pagamento ou notificação usar, e não guarda a configuração global -- essas decisões são tomadas antes, na inicialização da aplicação (`main.py`), que registra as fábricas de canal e escolhe o `PaymentProcessor` a usar.

### 1. Qual é a responsabilidade principal de cada componente criado?

* `AppConfig`: manter a configuração compartilhada da aplicação (Singleton).
* `Order` / `OrderBuilder`: representar e construir um pedido válido.
* `Payment` / `PixPayment` / `CreditCardPayment` / `BoletoPayment`: efetuar o pagamento de uma forma específica.
* `PaymentProcessor` (e subclasses `PixProcessor`, `CreditCardProcessor`, `BoletoProcessor`): definir o fluxo comum de processamento de pagamento e delegar a criação do `Payment` concreto ao Factory Method.
* `Checkout` / `Notification`: apresentar o checkout e enviar a notificação de um canal específico.
* `ChannelFactory` (`WebFactory`, `MobileFactory`, `KioskFactory`): criar a família coerente de `Checkout` e `Notification` de um canal (Abstract Factory).
* `channel_registry` (`register_factory` / `get_channel_factory`): saber, em tempo de execução, qual `ChannelFactory` corresponde a um canal, sem que quem consulta precise conhecer as classes concretas.
* `EventLogger`: registrar os eventos ocorridos durante o processamento de um pedido.
* `OrderService`: coordenar o fluxo completo chamando os colaboradores acima, na ordem certa, sem tomar decisões que pertencem a eles.
* `main.py`: raiz de composição -- registra as fábricas de canal, escolhe o `PaymentProcessor` e dispara o fluxo.

### 2. Escolha três componentes diferentes e indique uma mudança que deveria ficar restrita a cada um deles.

* `WebCheckout`/`WebNotification`: mudar o texto ou o layout apresentado ao cliente no canal WEB (ex.: incluir um novo campo no checkout) deveria alterar só essas duas classes, sem afetar MOBILE, KIOSK ou o `OrderService`.
* `channel_registry.py`: mudar a forma como as fábricas são armazenadas internamente (por exemplo, trocar o dicionário por outra estrutura, ou passar a validar duplicidade de registro) deveria ficar restrito a este arquivo -- quem chama `get_channel_factory(channel)` não percebe a diferença.
* `EventLogger`: mudar o destino dos logs (por exemplo, gravar em arquivo em vez de manter em memória, ou mudar o formato do timestamp) deveria ficar restrito a essa classe; `OrderService` continua só chamando `logger.log(mensagem)`.

### 3. Identifique uma decisão de projeto da solução que poderia ser diferente. Explique qual seria a alternativa e qual seria a consequência dessa mudança.

Optamos por registrar as fábricas de canal (`register_factory`) explicitamente em `main.py`, na inicialização da aplicação. Uma alternativa seria fazer cada módulo de canal se auto-registrar como efeito colateral da importação (por exemplo, `src/channels.py` chamar `register_factory("WEB", WebFactory())` no fim do próprio arquivo, e `src/kiosk_channel.py` fazer o mesmo para KIOSK). Nesse caso, adicionar KIOSK exigiria zero alterações em `main.py` -- bastaria importar o novo módulo em algum ponto de inicialização. A consequência seria um acoplamento mais implícito: o registro de um canal passaria a depender de "alguém importar aquele módulo em algum lugar", o que é mais fácil de esquecer e mais difícil de rastrear do que ler as poucas linhas de `bootstrap()` em `main.py`. Preferimos a explicitação em `main.py` por deixar visível, em um único lugar, quais canais a aplicação suporta.

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

`tests/test_channels.py::TestComportamentoAdicionalDeFactory.test_fabrica_cria_uma_nova_instancia_a_cada_chamada`

#### Comportamento verificado

Que duas chamadas sucessivas a `WebFactory.create_checkout()` devolvem duas instâncias distintas de `WebCheckout`, e não o mesmo objeto reaproveitado.

#### Resultado esperado

`checkout_1 is not checkout_2` -- os dois objetos criados são instâncias diferentes.

#### Por que esse comportamento é importante

O enunciado só pede para verificar que a fábrica cria o tipo certo de objeto para cada canal. Este teste cobre um comportamento diferente: garante que a fábrica realmente **fabrica** um objeto novo a cada chamada, em vez de cachear/reaproveitar uma instância (o que seria uma implementação de Factory incorreta, do tipo Singleton disfarçado). Isso importa porque pedidos processados em paralelo usam a mesma `ChannelFactory`; se ela devolvesse sempre o mesmo `Checkout`, um pedido poderia acabar enxergando ou até alterando estado de outro pedido através do mesmo objeto de checkout compartilhado.

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
