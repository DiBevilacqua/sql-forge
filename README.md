# ⚡ SQL Builder

Sistema SaaS que gera automaticamente **bancos de dados e queries SQL** com base na descrição de um negócio.

🔗 **Acesse o app:** https://sqlbuilder.streamlit.app/

---

## 🚀 Sobre o projeto

O **SQL Builder** nasceu para resolver um problema comum:

> Empresas possuem dados desorganizados e não sabem como estruturar um banco eficiente para análise.

A solução permite que o usuário descreva seu negócio e receba automaticamente:

* 🏗️ Estrutura completa de banco de dados (DDL)
* 🔎 Queries SQL prontas para análise
* 📊 Modelagem pensada para BI
* 💡 Insights estratégicos

---

## 🧠 Diferencial

Este projeto não é apenas técnico — ele une:

* Modelagem de dados orientada a negócio
* SQL aplicado a cenários reais
* Pensamento analítico
* Automação de geração de estrutura de dados

---

## 🧩 Funcionalidades

* ⚡ Geração automática de banco de dados
* 🔎 Queries analíticas prontas
* 📊 Estrutura otimizada para dashboards (Power BI)
* 🎯 Suporte a múltiplos nichos:

  * Funerária
  * Loja de Motos
  * Clínica Médica
  * E-commerce
  * Restaurante

---

## 🛠️ Tecnologias utilizadas

* Python
* Streamlit
* SQL (SQL Server)
* Git & GitHub

---

## 📊 Exemplo de análise

### 🚨 Inadimplência de clientes

```sql
SELECT
    c.nome AS cliente,
    p.data_vencimento,
    DATEDIFF(DAY, p.data_vencimento, GETDATE()) AS dias_atraso,
    p.valor
FROM pagamentos p
JOIN contratos ct ON p.id_contrato = ct.id_contrato
JOIN clientes c ON ct.id_cliente = c.id_cliente
WHERE p.status = 'pendente'
```

📌 **Insight:** Clientes com maior tempo de atraso apresentam maior risco de churn, permitindo ações de cobrança segmentadas.

---

## 📸 Preview do sistema

> (Adicione prints do seu app na pasta /assets)

```md
![Tela inicial](assets/tela1.png)
![Queries](assets/tela2.png)
```

---

## 🎯 Objetivo do projeto

Este projeto demonstra na prática:

* Estruturação de dados para diferentes tipos de negócio
* Criação de queries analíticas (CTE, JOINs, Window Functions)
* Aplicação de SQL para geração de insights
* Construção de ferramenta interativa para usuários finais

---

## 🚀 Próximos passos

* 🤖 Integração com IA para geração dinâmica de bancos
* 🔐 Sistema de autenticação de usuários
* 📊 Exportação para dashboards (Power BI)
* 💰 Possível evolução para SaaS pago

---

## 👨‍💻 Autor

**Diego Bevilacqua**
Analista de Dados

* Experiência com SQL, Python e análise de dados
* Foco em transformar dados em decisões de negócio

---

## 📌 Observação

Este projeto foi desenvolvido como parte da minha evolução prática em análise de dados, com foco em resolver problemas reais de estruturação e análise.

---
