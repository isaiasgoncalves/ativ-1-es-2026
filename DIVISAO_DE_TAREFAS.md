# Divisão de tarefas

**Atividade:** Design Patterns em Python - Sistema de pedidos

**Dupla:** Isaías Gouvêa Gonçalves e Mateus Mourão

**Prazo:** 23/09/2026, às 23h59

## Princípio da divisão

Cada arquivo possui um responsável principal. O outro integrante faz a revisão antes da integração. A divisão agrupa componentes relacionados para reduzir conflitos de Git e manter coerência entre código, testes e respostas escritas.

## Responsabilidades

| Questão | Escopo | Responsável principal | Revisão |
|---|---|---|---|
| 1 | Configuração e Singleton | Isaías | Mateus |
| 2 | Pedido e Builder | Isaías | Mateus |
| 3 | Pagamento e Factory Method | Isaías | Mateus |
| 4 | Famílias de canal e Abstract Factory | Mateus | Isaías |
| 5 | Registro de fábricas e canal KIOSK | Mateus | Isaías |
| 6 | Separação de responsabilidades e integração | Mateus | Isaías |
| 7 | Testes adicionais | Ambos | Revisão cruzada |
| 8 | Nova forma de pagamento | Isaías | Mateus |

## Propriedade dos arquivos

### Isaías

- `src/app_config.py`
- `src/orders.py`
- `src/payments.py`
- `tests/test_app_config.py`
- `tests/test_orders.py`
- `tests/test_payments.py`
- respostas escritas das questões 1, 2, 3 e 8
- teste adicional de Singleton
- teste adicional de Builder

### Mateus

- `src/channels.py`
- `src/channel_registry.py`
- `src/order_service.py`
- `src/event_logger.py`, caso a solução tenha registro de eventos
- `main.py`
- `tests/test_channels.py`
- `tests/test_channel_registry.py`
- `tests/test_integration.py`
- respostas escritas das questões 4, 5 e 6
- teste adicional de criação por Factory

### Compartilhado

- revisão da questão 7 e descrição dos três testes adicionais
- revisão cruzada do código e das respostas
- consolidação de `RESPOSTAS.md`
- execução completa da suíte de testes
- geração do PDF de respostas
- montagem e conferência do arquivo compactado para entrega

## Contratos compartilhados

Estes nomes e comportamentos devem permanecer estáveis durante o desenvolvimento para que os módulos possam ser implementados em paralelo:

```python
Order.total() -> float

Payment.pay(amount)
PaymentProcessor.create_payment()
PaymentProcessor.process_order(order)

Checkout.show(order)
Notification.send(order)

ChannelFactory.create_checkout()
ChannelFactory.create_notification()

get_channel_factory(channel)
```

Também devem ser combinados antes da integração:

- nomes dos atributos de `Order`;
- representação dos produtos;
- valores usados em `order.payment_method`;
- formato aceito pelo registro de fábricas;
- colaboradores recebidos por `OrderService`.

## Divisão dos testes adicionais da questão 7

Os testes abaixo devem verificar comportamentos diferentes dos exemplos obrigatórios do enunciado:

| Tipo | Responsável | Comportamento a definir |
|---|---|---|
| Singleton | Isaías | comportamento adicional de `AppConfig` |
| Builder | Isaías | comportamento adicional de `OrderBuilder` |
| Factory | Mateus | criação adicional por uma fábrica de canal ou pagamento |

Cada teste deve registrar no relatório:

1. o comportamento verificado;
2. o resultado esperado;
3. por que o comportamento é importante.

## Ordem de integração

1. Finalizar `AppConfig`, `Order` e os contratos compartilhados.
2. Implementar pagamentos e canais em paralelo.
3. Integrar um fluxo completo com canal WEB.
4. Confirmar um fluxo MOBILE com forma de pagamento independente do canal.
5. Adicionar KIOSK pelo registro de fábricas.
6. Adicionar a quarta forma de pagamento pelo Factory Method.
7. Executar os fluxos WEB e KIOSK pedidos no enunciado.
8. Executar todos os testes e conferir a coerência do relatório com o código final.

## Cronograma interno sugerido

### 20/09

- [ ] **Isaías:** finalizar questão 1 e iniciar questão 2.
- [ ] **Mateus:** implementar questão 4.
- [ ] Confirmar os contratos compartilhados.

### 21/09

- [ ] **Isaías:** finalizar questões 2 e 3.
- [ ] **Mateus:** finalizar questão 5.
- [ ] Integrar o primeiro fluxo WEB.

### 22/09

- [ ] Implementar questão 6.
- [ ] Adicionar KIOSK e a nova forma de pagamento.
- [ ] Finalizar os testes obrigatórios e adicionais.

### 23/09

- [ ] Revisar código e respostas de forma cruzada.
- [ ] Gerar e conferir o PDF de respostas.
- [ ] Executar a suíte completa em ambiente limpo.
- [ ] Montar e conferir o arquivo compactado antes do envio.

## Situação atual

- [x] Estrutura inicial do repositório criada.
- [x] `AppConfig` implementado.
- [x] Testes obrigatórios de `AppConfig` executados com sucesso.
- [ ] Respostas escritas da questão 1 registradas em `RESPOSTAS.md`.
- [ ] Questões 2 a 8 implementadas.

## Regra de colaboração

Antes de alterar um arquivo que pertence ao outro integrante, avisar a dupla. Fazer commits pequenos por questão e executar os testes relacionados antes de integrar. Mudanças nos contratos compartilhados devem ser combinadas antes de serem aplicadas.
