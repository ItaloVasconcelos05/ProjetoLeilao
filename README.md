# 🏠 Projeto Leilão Online

Um sistema de leilão em tempo real desenvolvido em Python que permite múltiplos clientes participarem simultaneamente de um leilão de uma casa.

## 📋 Descrição

Este projeto implementa um sistema de leilão distribuído onde:
- Um servidor gerencia o leilão de uma casa
- Múltiplos clientes podem se conectar simultaneamente
- Os lances são processados em tempo real
- Todos os participantes recebem notificações de novos lances
- Thread-safe com controle de concorrência

## 🚀 Funcionalidades

- **Conexão Multi-cliente**: Suporte para múltiplos participantes simultâneos
- **Leilão em Tempo Real**: Lances são processados instantaneamente
- **Broadcast de Mensagens**: Todos os clientes recebem notificações de novos lances
- **Thread-Safe**: Controle de concorrência com locks para evitar condições de corrida
- **Validação de Lances**: Apenas lances maiores que o atual são aceitos
- **Gerenciamento de Conexões**: Tratamento automático de desconexões

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Socket Programming**: Para comunicação cliente-servidor
- **Threading**: Para gerenciar múltiplas conexões simultâneas
- **Thread Locks**: Para sincronização e controle de concorrência

## 📦 Instalação

### Pré-requisitos
- Python 3.6 ou superior

### Passos para instalação

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd ProjetoLeilao
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
   
   *Nota: O projeto utiliza apenas bibliotecas padrão do Python, não sendo necessárias dependências externas.*

## 🎮 Como Usar

### 1. Iniciar o Servidor

Abra um terminal e execute:
```bash
python server.py
```

Você verá a mensagem:
```
--- Servidor escutando em 127.0.0.1:55555 ---
```

### 2. Conectar Clientes

Em terminais separados, execute:
```bash
python client.py
```

Para cada cliente, você verá:
```
[*] Conectando ao servidor em 127.0.0.1:55555

[LEILÃO ABERTO] 
Item: Casa
Lance Atual: R$100.00
Arrematante: Ninguém

 [#] Escreva sua mensagem: 
```

### 3. Participar do Leilão

- Digite um valor numérico para dar um lance
- Apenas lances maiores que o atual serão aceitos
- Todos os participantes receberão notificações de novos lances
- O leilão continua até que o servidor seja encerrado

### Exemplo de Uso:

**Cliente 1**:
```
 [#] Escreva sua mensagem: 150
```

**Todos os clientes recebem**:
```
[NOVO LANCE] R$150.00 por ('127.0.0.1', 54321)
```

**Cliente 2**:
```
 [#] Escreva sua mensagem: 200
```

**Todos os clientes recebem**:
```
[NOVO LANCE] R$200.00 por ('127.0.0.1', 54322)
```

## 🏗️ Arquitetura

### Servidor (`server.py`)

- **Classe `Auction`**: Gerencia o estado do leilão com thread locks
- **Função `broadcast`**: Envia mensagens para todos os clientes conectados
- **Função `client_management`**: Gerencia cada conexão de cliente
- **Threading**: Cada cliente é gerenciado em uma thread separada

### Cliente (`client.py`)

- **Thread de Recebimento**: Escuta mensagens do servidor continuamente
- **Thread de Envio**: Permite ao usuário enviar lances
- **Conexão TCP**: Comunicação com o servidor via sockets

## 🔧 Configuração

### Parâmetros Configuráveis

No arquivo `server.py`:
```python
HOST = '127.0.0.1'  # Endereço do servidor
PORTA = 55555       # Porta do servidor
house_auction = Auction("Casa", 100)  # Item e lance inicial
```

No arquivo `client.py`:
```python
HOST = '127.0.0.1'  # Deve coincidir com o servidor
PORTA = 55555       # Deve coincidir com o servidor
```

## 📁 Estrutura do Projeto

```
ProjetoLeilao/
├── server.py          # Servidor do leilão
├── client.py          # Cliente para participação
├── requirements.txt   # Dependências (vazio - usa bibliotecas padrão)
└── README.md          # Este arquivo
```

## 🚨 Tratamento de Erros

O sistema trata os seguintes cenários:
- **Conexão recusada**: Cliente não consegue conectar ao servidor
- **Cliente desconectado**: Servidor remove automaticamente clientes offline
- **Lances inválidos**: Apenas números são aceitos como lances
- **Lances insuficientes**: Lances menores que o atual são rejeitados

## 🔒 Segurança e Concorrência

- **Thread Locks**: Evitam condições de corrida no acesso ao estado do leilão
- **Validação de Entrada**: Lances são validados antes de serem processados
- **Gerenciamento de Conexões**: Conexões são limpas automaticamente

## 🎯 Melhorias Futuras

- Interface gráfica para os clientes
- Sistema de autenticação de usuários
- Múltiplos leilões simultâneos
- Histórico de lances
- Sistema de tempo limite para lances
- Persistência de dados em banco

## 👥 Contribuição

Sinta-se à vontade para contribuir com melhorias:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request


