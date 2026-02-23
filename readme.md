# 🚗 Estacionar API

**Sistema de Gerenciamento Inteligente de Estacionamento**

O **Estacionar** é uma plataforma completa de gerenciamento de estacionamentos, construída em **Python 3.13** e **Flask 3.1.2**. O sistema oferece suporte a múltiplos clientes através de uma arquitetura **multi-tenant**, garantindo o isolamento total de dados entre diferentes estacionamentos.

---

## ✨ Características Principais

- ☁️ **Gravação em Nuvem:** Armazenamento seguro de todos os dados gerados.
- 🏢 **Multi-Tenant:** Cada cliente opera de forma independente, acessando apenas os seus próprios registros.
- 🚙 **Gestão de Carros:** Cadastro, monitoramento e checkout automatizado de veículos estacionados.
- ⏱️ **Cálculo de Tarifas:** Cálculo automático do valor total e tempo de permanência no checkout, incluindo suporte a horas extras e tolerância.
- 🛍️ **Produtos e Serviços:** Cadastro de serviços adicionais (ex: lavagem) ou produtos (ex: água) para os clientes finais.
- 🧾 **Histórico:** Logs detalhados de veículos que já deixaram o estacionamento.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13
- **Framework:** Flask 3.1.2
- **Banco de Dados:** MySQL (via conector direto)
- **Autenticação:** JWT (JSON Web Tokens)

---

## 🔒 Autenticação

A maioria dos endpoints requer autenticação via token JWT. O token deve ser incluído no header de todas as requisições autenticadas:

```http
Authorization: Bearer {seu_token_aqui}
```

> **Nota:** O token tem validade configurável (padrão 365 dias).

---

## 📡 Endpoints da API

Todas as requisições devem incluir obrigatoriamente os headers:

```http
Accept: application/json
Content-Type: application/json (para métodos POST e PUT)
```

### 🚙 Veículos (`/vehicles`)
Gerencia a entrada, permanência e saída de veículos.

| Método | Rota | Descrição |
|---|---|---|
| **POST** | `/vehicles` | Registra a entrada de um novo carro. <br>**Body:** `{ "license_plate": "ABC1234", "model": "Sedan", "locale": "Setor A" }` |
| **GET** | `/vehicles` | Lista carros estacionados. <br>**Params:** `page`, `limit`, `order` (ASC/DESC), `plate` (busca parcial). |
| **PUT** | `/vehicles/<plate>` | Atualiza dados de um carro (placa, modelo ou local). |
| **DELETE** | `/vehicles/<plate>` | Realiza o checkout, calcula o valor final e move para o histórico. |

### 📋 Histórico (`/vehicles-logs`)
Consulta de veículos que já finalizaram a estadia.

| Método | Rota | Descrição |
|---|---|---|
| **GET** | `/vehicles-logs` | Lista o histórico de veículos. <br>**Params:** `page`, `limit`, `order`, `plate`. |

### 💰 Configuração de Preços (`/price-parking`)
Gerencia a tabela de preços e regras de cobrança.

| Método | Rota | Descrição |
|---|---|---|
| **POST** | `/price-parking` | Cria a configuração de preços. <br>**Body:** `{ "parking_hours": 1, "quick_stop_price": 5, "until_time_price": 10, "extra_hour_price": 2, "quick_stop_limit_minutes": 15 }` |
| **GET** | `/price-parking` | Recupera a configuração de preços atual. |
| **PUT** | `/price-parking` | Atualiza a configuração existente. |
| **DELETE** | `/price-parking` | Deleta a configuração de preços. |

### 🛒 Produtos e Serviços (`/products`)
Gerencia a venda de itens e serviços extras.

| Método | Rota | Descrição |
|---|---|---|
| **POST** | `/products` | Cadastra um novo produto ou serviço. <br>**Body:** `{ "title": "Água", "description": "500ml", "amount": 100, "price": 5, "type": "produto" }` |
| **GET** | `/products` | Lista o catálogo disponível. |
| **PUT** | `/products/<id>` | Atualiza um produto/serviço específico. |
| **DELETE** | `/products/<id>` | Remove um item do catálogo. |

---

## 🚀 Como Rodar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/estacionar-software/estacionar-api.git
   cd estacionar-api
   ```

2. **Configure o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install flask flask-cors mysql-connector-python
   ```

4. **Execute a aplicação:**
   ```bash
   python app.py
   ```
   O servidor iniciará em `http://localhost:5001`.
