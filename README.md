# ⚡ SQL Builder

Sistema SaaS que gera automaticamente bancos de dados e queries SQL com base na descrição de um negócio.

🔗 Acesse o app: https://sqlbuilder.streamlit.app/

---

## 🚀 Sobre o projeto

O SQL Builder foi criado para resolver um problema comum:

> Empresas não possuem estrutura de dados organizada e não sabem por onde começar.

A solução permite que qualquer pessoa descreva seu negócio e receba:

- Estrutura completa de banco de dados (DDL)
- Queries analíticas prontas
- Insights estratégicos

---

## 🧩 Funcionalidades

- 🏗️ Geração automática de banco de dados
- 🔎 Queries SQL para análise
- 📊 Estrutura pensada para BI
- ⚡ Interface interativa com Streamlit
- 🎯 Suporte a múltiplos nichos:
  - Funerária
  - Loja de Motos
  - Clínica Médica
  - E-commerce
  - Restaurante

---

## 🛠️ Tecnologias

- Python
- Streamlit
- SQL Server
- Git/GitHub

---

## 📊 Exemplo de análise

### Inadimplência

```sql
SELECT
    cliente,
    dias_atraso,
    valor_em_aberto
FROM pagamentos
WHERE status = 'pendente';
