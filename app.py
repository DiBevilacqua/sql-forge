"""
╔══════════════════════════════════════════════════════════════╗
║         SQL FORGE — Sistema SaaS de Geração de Banco         ║
║         Desenvolvido com Python + Streamlit + IA             ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import re
from datetime import datetime

# ─────────────────────────────────────────────
#   CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Forge — Gerador de Banco de Dados",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#   CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

    :root {
        --bg: #0d0f14;
        --surface: #13161e;
        --border: #1e2230;
        --accent: #00e5ff;
        --accent2: #7c3aed;
        --green: #00ff88;
        --yellow: #ffd600;
        --text: #e2e8f0;
        --muted: #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1200px;
    }

    /* Header */
    .hero-header {
        text-align: center;
        padding: 3rem 0 2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2.5rem;
    }
    .hero-header h1 {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, var(--accent), var(--accent2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-header p {
        color: var(--muted);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* Cards de output */
    .sql-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .sql-card-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Textarea + input */
    .stTextArea textarea, .stTextInput input {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1rem !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
    }

    /* Botão principal */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #000 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        letter-spacing: 1px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,229,255,0.3) !important;
    }

    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px !important;
    }
    pre {
        background: #0a0c10 !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        border: 1px solid var(--border) !important;
        gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--border) !important;
        color: var(--accent) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        color: var(--accent) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    /* Info/success boxes */
    .insight-box {
        background: rgba(0,255,136,0.05);
        border: 1px solid rgba(0,255,136,0.2);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .insight-box p {
        margin: 0;
        color: var(--green);
        font-size: 0.92rem;
    }

    /* Tags de categoria */
    .tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .tag-fin { background: rgba(0,229,255,0.1); color: var(--accent); border: 1px solid rgba(0,229,255,0.3); }
    .tag-com { background: rgba(124,58,237,0.1); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
    .tag-op  { background: rgba(255,214,0,0.1); color: var(--yellow); border: 1px solid rgba(255,214,0,0.3); }
    .tag-adv { background: rgba(0,255,136,0.1); color: var(--green); border: 1px solid rgba(0,255,136,0.3); }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        flex: 1;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-card .num { font-size: 2rem; font-weight: 800; color: var(--accent); }
    .metric-card .lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#   BASE DE CONHECIMENTO DOS NEGÓCIOS
# ─────────────────────────────────────────────
NEGOCIOS_DB = {
    "funerária": {
        "nome": "Funerária",
        "icone": "🕊️",
        "entidades": ["Contratos", "Falecidos", "Clientes/Familiares", "Serviços", "Pagamentos", "Funcionários"],
        "banco": """-- ============================================
--  BANCO DE DADOS: FUNERÁRIA
--  Gerado por SQL Forge
-- ============================================

CREATE TABLE clientes (
    id_cliente     INT          PRIMARY KEY IDENTITY(1,1),
    nome           VARCHAR(150) NOT NULL,
    cpf            VARCHAR(14)  UNIQUE NOT NULL,
    telefone       VARCHAR(20),
    email          VARCHAR(100),
    endereco       VARCHAR(200),
    cidade         VARCHAR(80),
    estado         CHAR(2),
    created_at     DATETIME     DEFAULT GETDATE()
);

CREATE TABLE falecidos (
    id_falecido    INT          PRIMARY KEY IDENTITY(1,1),
    nome           VARCHAR(150) NOT NULL,
    data_nascimento DATE,
    data_falecimento DATE       NOT NULL,
    causa_morte    VARCHAR(200),
    id_cliente     INT          NOT NULL,  -- responsável
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE servicos (
    id_servico     INT          PRIMARY KEY IDENTITY(1,1),
    nome           VARCHAR(100) NOT NULL,
    descricao      TEXT,
    valor_padrao   DECIMAL(10,2) NOT NULL,
    ativo          BIT          DEFAULT 1
);

CREATE TABLE contratos (
    id_contrato    INT          PRIMARY KEY IDENTITY(1,1),
    numero         VARCHAR(20)  UNIQUE NOT NULL,
    id_cliente     INT          NOT NULL,
    id_falecido    INT          NOT NULL,
    data_contrato  DATETIME     DEFAULT GETDATE(),
    valor_total    DECIMAL(12,2) NOT NULL,
    status         VARCHAR(20)  DEFAULT 'ativo'  -- ativo, cancelado, encerrado
        CHECK (status IN ('ativo','cancelado','encerrado')),
    observacoes    TEXT,
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_falecido) REFERENCES falecidos(id_falecido)
);

CREATE TABLE contrato_servicos (
    id             INT          PRIMARY KEY IDENTITY(1,1),
    id_contrato    INT          NOT NULL,
    id_servico     INT          NOT NULL,
    quantidade     INT          DEFAULT 1,
    valor_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato),
    FOREIGN KEY (id_servico)  REFERENCES servicos(id_servico)
);

CREATE TABLE pagamentos (
    id_pagamento   INT          PRIMARY KEY IDENTITY(1,1),
    id_contrato    INT          NOT NULL,
    valor          DECIMAL(12,2) NOT NULL,
    data_vencimento DATE        NOT NULL,
    data_pagamento  DATE,
    forma_pagamento VARCHAR(30) DEFAULT 'boleto'
        CHECK (forma_pagamento IN ('boleto','pix','credito','debito','dinheiro')),
    status         VARCHAR(20)  DEFAULT 'pendente'
        CHECK (status IN ('pendente','pago','atrasado','cancelado')),
    FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato)
);

CREATE TABLE funcionarios (
    id_funcionario INT          PRIMARY KEY IDENTITY(1,1),
    nome           VARCHAR(150) NOT NULL,
    cargo          VARCHAR(80),
    salario        DECIMAL(10,2),
    ativo          BIT          DEFAULT 1
);""",
        "queries": {
            "💰 Faturamento Mensal": {
                "categoria": "fin",
                "sql": """-- Faturamento mensal com comparativo
SELECT
    FORMAT(data_pagamento, 'yyyy-MM')     AS mes,
    COUNT(*)                               AS total_pagamentos,
    SUM(valor)                             AS faturamento,
    AVG(valor)                             AS ticket_medio,
    LAG(SUM(valor)) OVER (ORDER BY FORMAT(data_pagamento,'yyyy-MM')) AS mes_anterior,
    SUM(valor) - LAG(SUM(valor)) OVER (ORDER BY FORMAT(data_pagamento,'yyyy-MM')) AS variacao
FROM pagamentos
WHERE status = 'pago'
  AND data_pagamento IS NOT NULL
GROUP BY FORMAT(data_pagamento, 'yyyy-MM')
ORDER BY mes DESC;""",
                "explicacao": "Faturamento mensal com variação mês a mês usando Window Function LAG(). Identifica crescimento ou queda."
            },
            "🚨 Inadimplência": {
                "categoria": "fin",
                "sql": """-- Análise completa de inadimplência
SELECT
    c.nome                                 AS cliente,
    c.telefone,
    ct.numero                              AS contrato,
    p.data_vencimento,
    DATEDIFF(DAY, p.data_vencimento, GETDATE()) AS dias_atraso,
    p.valor                                AS valor_em_aberto,
    CASE
        WHEN DATEDIFF(DAY, p.data_vencimento, GETDATE()) BETWEEN 1  AND 30 THEN '🟡 Leve (1-30d)'
        WHEN DATEDIFF(DAY, p.data_vencimento, GETDATE()) BETWEEN 31 AND 90 THEN '🟠 Grave (31-90d)'
        ELSE '🔴 Crítico (90d+)'
    END AS classificacao
FROM pagamentos p
JOIN contratos ct ON p.id_contrato = ct.id_contrato
JOIN clientes c   ON ct.id_cliente = c.id_cliente
WHERE p.status = 'pendente'
  AND p.data_vencimento < GETDATE()
ORDER BY dias_atraso DESC;""",
                "explicacao": "Lista clientes inadimplentes com classificação por gravidade. Essencial para régua de cobrança."
            },
            "📋 Contratos Ativos": {
                "categoria": "op",
                "sql": """-- Dashboard de contratos com valor pago vs pendente
SELECT
    ct.numero,
    c.nome                                 AS cliente,
    f.nome                                 AS falecido,
    ct.data_contrato,
    ct.valor_total,
    ISNULL(SUM(CASE WHEN p.status = 'pago'     THEN p.valor END), 0) AS valor_pago,
    ISNULL(SUM(CASE WHEN p.status = 'pendente' THEN p.valor END), 0) AS valor_pendente,
    CAST(
        ISNULL(SUM(CASE WHEN p.status = 'pago' THEN p.valor END), 0)
        / ct.valor_total * 100
    AS DECIMAL(5,1))                       AS pct_quitado
FROM contratos ct
JOIN clientes c   ON ct.id_cliente  = c.id_cliente
JOIN falecidos f  ON ct.id_falecido = f.id_falecido
LEFT JOIN pagamentos p ON p.id_contrato = ct.id_contrato
WHERE ct.status = 'ativo'
GROUP BY ct.numero, c.nome, f.nome, ct.data_contrato, ct.valor_total
ORDER BY valor_pendente DESC;""",
                "explicacao": "Visão completa dos contratos ativos: quanto já foi pago e quanto ainda está em aberto."
            },
            "🏆 Serviços mais Vendidos": {
                "categoria": "com",
                "sql": """-- Ranking de serviços por receita gerada
WITH servicos_rank AS (
    SELECT
        s.nome                             AS servico,
        COUNT(cs.id)                       AS vezes_contratado,
        SUM(cs.valor_unitario * cs.quantidade) AS receita_total,
        RANK() OVER (ORDER BY SUM(cs.valor_unitario * cs.quantidade) DESC) AS ranking
    FROM contrato_servicos cs
    JOIN servicos s ON cs.id_servico = s.id_servico
    JOIN contratos ct ON cs.id_contrato = ct.id_contrato
    WHERE ct.status != 'cancelado'
    GROUP BY s.nome
)
SELECT ranking, servico, vezes_contratado, receita_total
FROM servicos_rank
ORDER BY ranking;""",
                "explicacao": "Ranking de serviços usando CTE + RANK(). Identifica quais serviços geram mais receita."
            }
        },
        "insights": [
            "📌 Monitor diário de inadimplência → crie alertas automáticos para pagamentos vencidos há +7 dias",
            "📌 Serviços mais vendidos → negocie volume com fornecedores dos top 3 serviços",
            "📌 Sazonalidade → cruze faturamento com meses para identificar picos e vales",
            "📌 Régua de cobrança → segmente clientes por faixa de atraso para abordagem personalizada"
        ]
    },

    "loja de motos": {
        "nome": "Loja de Motos",
        "icone": "🏍️",
        "entidades": ["Motos (Estoque)", "Clientes", "Vendas", "Financiamento", "Manutenções", "Vendedores"],
        "banco": """-- ============================================
--  BANCO DE DADOS: LOJA DE MOTOS
--  Gerado por SQL Forge
-- ============================================

CREATE TABLE marcas (
    id_marca   INT         PRIMARY KEY IDENTITY(1,1),
    nome       VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE motos (
    id_moto    INT         PRIMARY KEY IDENTITY(1,1),
    id_marca   INT         NOT NULL,
    modelo     VARCHAR(100) NOT NULL,
    ano        INT,
    cilindrada INT,
    cor        VARCHAR(40),
    chassi     VARCHAR(20) UNIQUE,
    preco_custo   DECIMAL(12,2),
    preco_venda   DECIMAL(12,2) NOT NULL,
    status     VARCHAR(20) DEFAULT 'disponivel'
        CHECK (status IN ('disponivel','reservada','vendida')),
    created_at DATETIME    DEFAULT GETDATE(),
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
);

CREATE TABLE clientes (
    id_cliente INT         PRIMARY KEY IDENTITY(1,1),
    nome       VARCHAR(150) NOT NULL,
    cpf        VARCHAR(14)  UNIQUE NOT NULL,
    telefone   VARCHAR(20),
    email      VARCHAR(100),
    cidade     VARCHAR(80),
    estado     CHAR(2),
    renda_mensal DECIMAL(10,2),
    score_credito INT,
    created_at DATETIME    DEFAULT GETDATE()
);

CREATE TABLE vendedores (
    id_vendedor INT        PRIMARY KEY IDENTITY(1,1),
    nome        VARCHAR(150) NOT NULL,
    cpf         VARCHAR(14) UNIQUE,
    meta_mensal DECIMAL(12,2),
    comissao_pct DECIMAL(5,2) DEFAULT 2.50,
    ativo       BIT        DEFAULT 1
);

CREATE TABLE vendas (
    id_venda    INT         PRIMARY KEY IDENTITY(1,1),
    id_moto     INT         NOT NULL,
    id_cliente  INT         NOT NULL,
    id_vendedor INT         NOT NULL,
    data_venda  DATETIME    DEFAULT GETDATE(),
    valor_venda DECIMAL(12,2) NOT NULL,
    desconto    DECIMAL(10,2) DEFAULT 0,
    forma_pagto VARCHAR(30) DEFAULT 'financiamento'
        CHECK (forma_pagto IN ('avista','financiamento','consorcio','troca')),
    FOREIGN KEY (id_moto)     REFERENCES motos(id_moto),
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor)
);

CREATE TABLE financiamentos (
    id_financiamento INT    PRIMARY KEY IDENTITY(1,1),
    id_venda         INT    NOT NULL UNIQUE,
    banco            VARCHAR(80),
    valor_financiado DECIMAL(12,2) NOT NULL,
    entrada          DECIMAL(12,2) DEFAULT 0,
    parcelas         INT    NOT NULL,
    taxa_juros_mensal DECIMAL(6,4),
    valor_parcela    DECIMAL(10,2),
    status           VARCHAR(20) DEFAULT 'ativo'
        CHECK (status IN ('ativo','quitado','inadimplente')),
    FOREIGN KEY (id_venda) REFERENCES vendas(id_venda)
);

CREATE TABLE manutencoes (
    id_manutencao INT       PRIMARY KEY IDENTITY(1,1),
    id_moto       INT       NOT NULL,
    id_cliente    INT,
    data_entrada  DATETIME  DEFAULT GETDATE(),
    data_saida    DATETIME,
    descricao     TEXT,
    valor_mao_obra DECIMAL(10,2),
    valor_pecas   DECIMAL(10,2),
    status        VARCHAR(20) DEFAULT 'aberto'
        CHECK (status IN ('aberto','em_andamento','concluido')),
    FOREIGN KEY (id_moto)    REFERENCES motos(id_moto),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);""",
        "queries": {
            "💰 Faturamento por Mês": {
                "categoria": "fin",
                "sql": """-- Faturamento mensal com lucro bruto
SELECT
    FORMAT(v.data_venda, 'yyyy-MM')       AS mes,
    COUNT(v.id_venda)                      AS qtd_vendas,
    SUM(v.valor_venda - v.desconto)        AS faturamento_liquido,
    SUM((v.valor_venda - v.desconto) - m.preco_custo) AS lucro_bruto,
    AVG(v.valor_venda)                     AS ticket_medio,
    CAST(
        SUM((v.valor_venda - v.desconto) - m.preco_custo)
        / SUM(v.valor_venda - v.desconto) * 100
    AS DECIMAL(5,1))                       AS margem_pct
FROM vendas v
JOIN motos m ON v.id_moto = m.id_moto
GROUP BY FORMAT(v.data_venda, 'yyyy-MM')
ORDER BY mes DESC;""",
                "explicacao": "Faturamento líquido, lucro bruto e margem percentual por mês. Fundamental para DRE."
            },
            "🏆 Ranking de Vendedores": {
                "categoria": "com",
                "sql": """-- Performance de vendedores com meta
SELECT
    ve.nome                                AS vendedor,
    COUNT(v.id_venda)                      AS vendas_mes,
    SUM(v.valor_venda)                     AS faturamento,
    ve.meta_mensal,
    CAST(SUM(v.valor_venda) / ve.meta_mensal * 100 AS DECIMAL(5,1)) AS pct_meta,
    SUM(v.valor_venda) * (ve.comissao_pct / 100)   AS comissao_gerada,
    RANK() OVER (ORDER BY SUM(v.valor_venda) DESC)  AS ranking
FROM vendas v
JOIN vendedores ve ON v.id_vendedor = ve.id_vendedor
WHERE FORMAT(v.data_venda,'yyyy-MM') = FORMAT(GETDATE(),'yyyy-MM')
GROUP BY ve.nome, ve.meta_mensal, ve.comissao_pct
ORDER BY ranking;""",
                "explicacao": "Ranking do mês atual com % de meta atingida e comissão gerada. Use para gamificação do time."
            },
            "📦 Estoque por Marca": {
                "categoria": "op",
                "sql": """-- Análise de estoque com valor total
SELECT
    ma.nome                                AS marca,
    COUNT(mo.id_moto)                      AS unidades,
    SUM(mo.preco_venda)                    AS valor_total_estoque,
    MIN(mo.preco_venda)                    AS menor_preco,
    MAX(mo.preco_venda)                    AS maior_preco,
    AVG(mo.preco_venda)                    AS preco_medio
FROM motos mo
JOIN marcas ma ON mo.id_marca = ma.id_marca
WHERE mo.status = 'disponivel'
GROUP BY ma.nome
ORDER BY valor_total_estoque DESC;""",
                "explicacao": "Snapshot do estoque atual por marca. Identifica onde está concentrado o capital parado."
            },
            "🧠 Clientes com Maior Potencial": {
                "categoria": "adv",
                "sql": """-- Score de clientes por histórico + renda (análise avançada)
WITH historico AS (
    SELECT
        c.id_cliente, c.nome, c.renda_mensal, c.score_credito,
        COUNT(v.id_venda)  AS total_compras,
        SUM(v.valor_venda) AS valor_total_compras,
        MAX(v.data_venda)  AS ultima_compra
    FROM clientes c
    LEFT JOIN vendas v ON c.id_cliente = v.id_cliente
    GROUP BY c.id_cliente, c.nome, c.renda_mensal, c.score_credito
)
SELECT
    nome,
    renda_mensal,
    score_credito,
    total_compras,
    valor_total_compras,
    ultima_compra,
    DATEDIFF(DAY, ultima_compra, GETDATE()) AS dias_sem_comprar,
    NTILE(4) OVER (ORDER BY valor_total_compras DESC) AS quartil_valor,
    CASE
        WHEN score_credito >= 700 AND renda_mensal > 5000 THEN '⭐ VIP'
        WHEN score_credito >= 500                         THEN '🟢 Potencial'
        ELSE                                                   '🟡 Monitorar'
    END AS segmento
FROM historico
ORDER BY valor_total_compras DESC;""",
                "explicacao": "Segmentação avançada de clientes com CTE + NTILE(). Base para campanhas direcionadas."
            }
        },
        "insights": [
            "📌 Estoque parado há +90 dias → crie promoções direcionadas para girar o capital",
            "📌 Vendedores abaixo de 70% da meta → acione treinamentos ou redistribua carteira",
            "📌 Clientes VIP sem compra há +180 dias → campanha de reativação personalizada",
            "📌 Margem por modelo → identifique quais motos têm melhor ROI e priorize estoque"
        ]
    },

    "clínica médica": {
        "nome": "Clínica Médica",
        "icone": "🏥",
        "entidades": ["Pacientes", "Médicos", "Consultas", "Prontuários", "Faturamento", "Convênios"],
        "banco": """-- ============================================
--  BANCO DE DADOS: CLÍNICA MÉDICA
--  Gerado por SQL Forge
-- ============================================

CREATE TABLE especialidades (
    id_especialidade INT        PRIMARY KEY IDENTITY(1,1),
    nome             VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE medicos (
    id_medico        INT        PRIMARY KEY IDENTITY(1,1),
    nome             VARCHAR(150) NOT NULL,
    crm              VARCHAR(20)  UNIQUE NOT NULL,
    id_especialidade INT        NOT NULL,
    valor_consulta   DECIMAL(10,2),
    ativo            BIT        DEFAULT 1,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade)
);

CREATE TABLE convenios (
    id_convenio INT          PRIMARY KEY IDENTITY(1,1),
    nome        VARCHAR(100) NOT NULL,
    cnpj        VARCHAR(18),
    desconto_pct DECIMAL(5,2) DEFAULT 0
);

CREATE TABLE pacientes (
    id_paciente  INT          PRIMARY KEY IDENTITY(1,1),
    nome         VARCHAR(150) NOT NULL,
    cpf          VARCHAR(14)  UNIQUE NOT NULL,
    data_nascimento DATE,
    sexo         CHAR(1)      CHECK (sexo IN ('M','F','O')),
    telefone     VARCHAR(20),
    email        VARCHAR(100),
    id_convenio  INT,
    created_at   DATETIME     DEFAULT GETDATE(),
    FOREIGN KEY (id_convenio) REFERENCES convenios(id_convenio)
);

CREATE TABLE agendamentos (
    id_agendamento INT        PRIMARY KEY IDENTITY(1,1),
    id_paciente    INT        NOT NULL,
    id_medico      INT        NOT NULL,
    data_hora      DATETIME   NOT NULL,
    tipo           VARCHAR(30) DEFAULT 'consulta'
        CHECK (tipo IN ('consulta','retorno','exame','cirurgia')),
    status         VARCHAR(20) DEFAULT 'agendado'
        CHECK (status IN ('agendado','confirmado','realizado','cancelado','faltou')),
    observacoes    TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico)   REFERENCES medicos(id_medico)
);

CREATE TABLE prontuarios (
    id_prontuario  INT        PRIMARY KEY IDENTITY(1,1),
    id_agendamento INT        NOT NULL UNIQUE,
    anamnese       TEXT,
    diagnostico    VARCHAR(300),
    cid10          VARCHAR(10),
    prescricao     TEXT,
    retorno_dias   INT,
    created_at     DATETIME   DEFAULT GETDATE(),
    FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento)
);

CREATE TABLE faturamentos (
    id_faturamento INT        PRIMARY KEY IDENTITY(1,1),
    id_agendamento INT        NOT NULL,
    valor_bruto    DECIMAL(10,2) NOT NULL,
    desconto       DECIMAL(10,2) DEFAULT 0,
    valor_liquido  AS (valor_bruto - desconto) PERSISTED,
    forma_pagto    VARCHAR(30) DEFAULT 'particular',
    status         VARCHAR(20) DEFAULT 'pendente'
        CHECK (status IN ('pendente','pago','glosado','cancelado')),
    data_pagamento DATE,
    FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento)
);""",
        "queries": {
            "💰 Receita por Médico": {
                "categoria": "fin",
                "sql": """-- Receita por médico no período
SELECT
    m.nome                                 AS medico,
    e.nome                                 AS especialidade,
    COUNT(a.id_agendamento)                AS consultas_realizadas,
    SUM(f.valor_liquido)                   AS receita_gerada,
    AVG(f.valor_liquido)                   AS ticket_medio,
    RANK() OVER (ORDER BY SUM(f.valor_liquido) DESC) AS ranking
FROM medicos m
JOIN especialidades e    ON m.id_especialidade   = e.id_especialidade
JOIN agendamentos a      ON a.id_medico          = m.id_medico
JOIN faturamentos f      ON f.id_agendamento     = a.id_agendamento
WHERE a.status      = 'realizado'
  AND f.status      = 'pago'
  AND YEAR(f.data_pagamento) = YEAR(GETDATE())
GROUP BY m.nome, e.nome
ORDER BY ranking;""",
                "explicacao": "Receita por médico no ano atual com ranking. Identifica os profissionais mais rentáveis."
            },
            "📅 Taxa de Absenteísmo": {
                "categoria": "op",
                "sql": """-- Taxa de falta dos pacientes por mês
SELECT
    FORMAT(data_hora, 'yyyy-MM')           AS mes,
    COUNT(*)                               AS total_agendamentos,
    SUM(CASE WHEN status = 'faltou'   THEN 1 ELSE 0 END) AS faltas,
    SUM(CASE WHEN status = 'realizado' THEN 1 ELSE 0 END) AS realizados,
    CAST(
        SUM(CASE WHEN status = 'faltou' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100
    AS DECIMAL(5,1))                       AS taxa_falta_pct
FROM agendamentos
WHERE status NOT IN ('agendado','confirmado')
GROUP BY FORMAT(data_hora, 'yyyy-MM')
ORDER BY mes DESC;""",
                "explicacao": "Absenteísmo mensal. Taxas acima de 15% indicam necessidade de confirmação automática."
            },
            "🧠 Pacientes de Alto Risco de Churn": {
                "categoria": "adv",
                "sql": """-- Pacientes que não retornam conforme prescrito
WITH retornos AS (
    SELECT
        p.id_paciente, p.nome, p.telefone,
        MAX(a.data_hora)              AS ultima_consulta,
        MAX(pr.retorno_dias)          AS retorno_prescrito,
        DATEDIFF(DAY, MAX(a.data_hora), GETDATE()) AS dias_desde_ultima
    FROM pacientes p
    JOIN agendamentos a  ON a.id_paciente    = p.id_paciente
    JOIN prontuarios pr  ON pr.id_agendamento = a.id_agendamento
    WHERE a.status = 'realizado'
    GROUP BY p.id_paciente, p.nome, p.telefone
)
SELECT
    nome, telefone, ultima_consulta,
    retorno_prescrito,
    dias_desde_ultima,
    dias_desde_ultima - retorno_prescrito  AS dias_atraso_retorno,
    CASE
        WHEN dias_desde_ultima > retorno_prescrito * 2 THEN '🔴 Crítico'
        WHEN dias_desde_ultima > retorno_prescrito     THEN '🟡 Atenção'
        ELSE                                                '🟢 OK'
    END AS status_retorno
FROM retornos
WHERE retorno_prescrito IS NOT NULL
ORDER BY dias_atraso_retorno DESC;""",
                "explicacao": "Identifica pacientes que ultrapassaram o prazo de retorno prescrito. Reduz churn e aumenta LTV."
            }
        },
        "insights": [
            "📌 Taxa de falta acima de 20% → implemente confirmação automática via WhatsApp/SMS",
            "📌 Médico com agenda vazia → reequilibre horários ou intensifique marketing da especialidade",
            "📌 Pacientes sem retorno → campanha de reativação pode recuperar 15-30% da base",
            "📌 Glosas de convênio → audite os procedimentos mais glosados para correção de billing"
        ]
    },

    "e-commerce": {
        "nome": "E-commerce",
        "icone": "🛒",
        "entidades": ["Produtos", "Clientes", "Pedidos", "Pagamentos", "Estoque", "Entregas"],
        "banco": """-- ============================================
--  BANCO DE DADOS: E-COMMERCE
--  Gerado por SQL Forge
-- ============================================

CREATE TABLE categorias (
    id_categoria INT         PRIMARY KEY IDENTITY(1,1),
    nome         VARCHAR(80) NOT NULL,
    pai          INT,  -- hierarquia de categorias
    FOREIGN KEY (pai) REFERENCES categorias(id_categoria)
);

CREATE TABLE produtos (
    id_produto   INT          PRIMARY KEY IDENTITY(1,1),
    id_categoria INT          NOT NULL,
    nome         VARCHAR(200) NOT NULL,
    sku          VARCHAR(50)  UNIQUE NOT NULL,
    descricao    TEXT,
    preco        DECIMAL(12,2) NOT NULL,
    preco_custo  DECIMAL(12,2),
    estoque      INT          DEFAULT 0,
    peso_kg      DECIMAL(8,3),
    ativo        BIT          DEFAULT 1,
    created_at   DATETIME     DEFAULT GETDATE(),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
    id_cliente  INT           PRIMARY KEY IDENTITY(1,1),
    nome        VARCHAR(150)  NOT NULL,
    email       VARCHAR(100)  UNIQUE NOT NULL,
    cpf         VARCHAR(14)   UNIQUE,
    telefone    VARCHAR(20),
    created_at  DATETIME      DEFAULT GETDATE()
);

CREATE TABLE enderecos (
    id_endereco INT           PRIMARY KEY IDENTITY(1,1),
    id_cliente  INT           NOT NULL,
    cep         VARCHAR(10),
    logradouro  VARCHAR(200),
    numero      VARCHAR(10),
    complemento VARCHAR(80),
    bairro      VARCHAR(80),
    cidade      VARCHAR(80),
    estado      CHAR(2),
    principal   BIT           DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE pedidos (
    id_pedido   INT           PRIMARY KEY IDENTITY(1,1),
    id_cliente  INT           NOT NULL,
    id_endereco INT           NOT NULL,
    data_pedido DATETIME      DEFAULT GETDATE(),
    status      VARCHAR(30)   DEFAULT 'aguardando_pagamento'
        CHECK (status IN ('aguardando_pagamento','pago','em_separacao',
                          'enviado','entregue','cancelado','devolvido')),
    valor_produtos DECIMAL(12,2) NOT NULL,
    valor_frete    DECIMAL(10,2) DEFAULT 0,
    desconto       DECIMAL(10,2) DEFAULT 0,
    valor_total AS (valor_produtos + valor_frete - desconto) PERSISTED,
    cupom       VARCHAR(30),
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_endereco) REFERENCES enderecos(id_endereco)
);

CREATE TABLE pedido_itens (
    id_item     INT           PRIMARY KEY IDENTITY(1,1),
    id_pedido   INT           NOT NULL,
    id_produto  INT           NOT NULL,
    quantidade  INT           NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (id_pedido)  REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE pagamentos (
    id_pagamento INT          PRIMARY KEY IDENTITY(1,1),
    id_pedido    INT          NOT NULL UNIQUE,
    metodo       VARCHAR(30)  DEFAULT 'pix'
        CHECK (metodo IN ('pix','credito','debito','boleto')),
    parcelas     INT          DEFAULT 1,
    status       VARCHAR(20)  DEFAULT 'pendente'
        CHECK (status IN ('pendente','aprovado','reprovado','estornado')),
    gateway_id   VARCHAR(100),
    data_aprovacao DATETIME,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);""",
        "queries": {
            "💰 GMV e Receita Mensal": {
                "categoria": "fin",
                "sql": """-- GMV, receita líquida e ticket médio mensais
SELECT
    FORMAT(p.data_pedido, 'yyyy-MM')     AS mes,
    COUNT(DISTINCT p.id_pedido)           AS total_pedidos,
    COUNT(DISTINCT p.id_cliente)          AS clientes_unicos,
    SUM(p.valor_total)                    AS gmv,
    SUM(p.desconto)                       AS total_descontos,
    AVG(p.valor_total)                    AS ticket_medio,
    SUM(p.valor_total) - SUM(
        SELECT SUM(pi2.quantidade * prod.preco_custo)
        FROM pedido_itens pi2
        JOIN produtos prod ON pi2.id_produto = prod.id_produto
        WHERE pi2.id_pedido = p.id_pedido
    )                                     AS lucro_bruto_estimado
FROM pedidos p
WHERE p.status NOT IN ('cancelado','devolvido')
GROUP BY FORMAT(p.data_pedido, 'yyyy-MM')
ORDER BY mes DESC;""",
                "explicacao": "GMV mensal com clientes únicos, descontos e lucro bruto estimado. Base do dashboard financeiro."
            },
            "🔄 Taxa de Conversão por Funil": {
                "categoria": "com",
                "sql": """-- Conversão: pedidos criados vs pagos vs entregues
SELECT
    FORMAT(data_pedido, 'yyyy-MM')        AS mes,
    COUNT(*)                               AS pedidos_criados,
    SUM(CASE WHEN status != 'aguardando_pagamento' AND status != 'cancelado'
             THEN 1 ELSE 0 END)            AS pedidos_pagos,
    SUM(CASE WHEN status = 'entregue'     THEN 1 ELSE 0 END) AS pedidos_entregues,
    SUM(CASE WHEN status = 'cancelado'    THEN 1 ELSE 0 END) AS cancelamentos,
    CAST(SUM(CASE WHEN status != 'aguardando_pagamento'
                   AND status != 'cancelado' THEN 1.0 ELSE 0 END)
         / COUNT(*) * 100 AS DECIMAL(5,1)) AS taxa_conversao_pct
FROM pedidos
GROUP BY FORMAT(data_pedido, 'yyyy-MM')
ORDER BY mes DESC;""",
                "explicacao": "Funil de conversão de pedidos. Taxa abaixo de 60% indica problema no checkout ou pagamento."
            },
            "🏆 Produtos Mais Rentáveis": {
                "categoria": "com",
                "sql": """-- Top produtos por receita e margem
WITH prod_perf AS (
    SELECT
        pr.nome                            AS produto,
        pr.sku,
        SUM(pi.quantidade)                 AS unidades_vendidas,
        SUM(pi.quantidade * pi.preco_unitario) AS receita,
        SUM(pi.quantidade * pr.preco_custo)    AS custo_total,
        SUM(pi.quantidade * (pi.preco_unitario - pr.preco_custo)) AS lucro
    FROM pedido_itens pi
    JOIN produtos pr  ON pi.id_produto  = pr.id_produto
    JOIN pedidos p    ON pi.id_pedido   = p.id_pedido
    WHERE p.status NOT IN ('cancelado','devolvido')
    GROUP BY pr.nome, pr.sku
)
SELECT
    produto, sku,
    unidades_vendidas, receita,
    CAST(lucro / receita * 100 AS DECIMAL(5,1)) AS margem_pct,
    RANK() OVER (ORDER BY lucro DESC)            AS ranking_lucro
FROM prod_perf
ORDER BY ranking_lucro
OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;""",
                "explicacao": "Top 20 produtos por lucro real com margem percentual. Use para otimizar mix de produtos."
            },
            "🧠 Análise RFM (Clientes)": {
                "categoria": "adv",
                "sql": """-- Segmentação RFM: Recência, Frequência, Monetário
WITH rfm_base AS (
    SELECT
        c.id_cliente, c.nome, c.email,
        DATEDIFF(DAY, MAX(p.data_pedido), GETDATE())  AS recencia,
        COUNT(p.id_pedido)                             AS frequencia,
        SUM(p.valor_total)                             AS monetario
    FROM clientes c
    JOIN pedidos p ON c.id_cliente = p.id_cliente
    WHERE p.status NOT IN ('cancelado','devolvido')
    GROUP BY c.id_cliente, c.nome, c.email
),
rfm_score AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recencia  ASC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequencia DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetario  DESC) AS m_score
    FROM rfm_base
)
SELECT
    nome, email, recencia, frequencia, monetario,
    CAST((r_score + f_score + m_score) AS VARCHAR) AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN '💎 Campeão'
        WHEN r_score >= 3 AND f_score >= 3                  THEN '⭐ Leal'
        WHEN r_score >= 4 AND f_score <= 2                  THEN '🆕 Novo Promissor'
        WHEN r_score <= 2 AND f_score >= 3                  THEN '😴 Em Risco'
        WHEN r_score <= 2 AND m_score >= 4                  THEN '💤 Hibernando'
        ELSE                                                     '👻 Perdido'
    END AS segmento_rfm
FROM rfm_score
ORDER BY rfm_total DESC;""",
                "explicacao": "Segmentação RFM completa com NTILE(5). Base científica para campanhas de marketing segmentadas."
            }
        },
        "insights": [
            "📌 Análise RFM → clientes 'Campeão' custam 5x menos para reter do que adquirir novos",
            "📌 Taxa de cancelamento acima de 10% → revisite checkout, frete e meios de pagamento",
            "📌 Produtos com margem negativa → revise precificação urgente ou descontinue o item",
            "📌 Clientes 'Em Risco' → campanha de win-back com desconto exclusivo nos 30 dias seguintes"
        ]
    },

    "restaurante": {
        "nome": "Restaurante",
        "icone": "🍽️",
        "entidades": ["Cardápio", "Mesas", "Pedidos", "Funcionários", "Estoque", "Caixa"],
        "banco": """-- ============================================
--  BANCO DE DADOS: RESTAURANTE
--  Gerado por SQL Forge
-- ============================================

CREATE TABLE categorias_cardapio (
    id_categoria INT         PRIMARY KEY IDENTITY(1,1),
    nome         VARCHAR(60) NOT NULL,
    ordem        INT         DEFAULT 0
);

CREATE TABLE itens_cardapio (
    id_item      INT          PRIMARY KEY IDENTITY(1,1),
    id_categoria INT          NOT NULL,
    nome         VARCHAR(150) NOT NULL,
    descricao    TEXT,
    preco        DECIMAL(10,2) NOT NULL,
    custo        DECIMAL(10,2),
    disponivel   BIT          DEFAULT 1,
    FOREIGN KEY (id_categoria) REFERENCES categorias_cardapio(id_categoria)
);

CREATE TABLE mesas (
    id_mesa      INT          PRIMARY KEY IDENTITY(1,1),
    numero       INT          UNIQUE NOT NULL,
    capacidade   INT          DEFAULT 4,
    status       VARCHAR(20)  DEFAULT 'livre'
        CHECK (status IN ('livre','ocupada','reservada'))
);

CREATE TABLE funcionarios (
    id_funcionario INT        PRIMARY KEY IDENTITY(1,1),
    nome           VARCHAR(150) NOT NULL,
    cargo          VARCHAR(50),
    turno          VARCHAR(20) DEFAULT 'dia'
        CHECK (turno IN ('dia','noite','misto')),
    ativo          BIT        DEFAULT 1
);

CREATE TABLE comandas (
    id_comanda   INT          PRIMARY KEY IDENTITY(1,1),
    id_mesa      INT          NOT NULL,
    id_garcom    INT          NOT NULL,
    abertura     DATETIME     DEFAULT GETDATE(),
    fechamento   DATETIME,
    status       VARCHAR(20)  DEFAULT 'aberta'
        CHECK (status IN ('aberta','fechada','cancelada')),
    desconto     DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (id_mesa)   REFERENCES mesas(id_mesa),
    FOREIGN KEY (id_garcom) REFERENCES funcionarios(id_funcionario)
);

CREATE TABLE comanda_itens (
    id_item_cmd  INT          PRIMARY KEY IDENTITY(1,1),
    id_comanda   INT          NOT NULL,
    id_item      INT          NOT NULL,
    quantidade   INT          DEFAULT 1,
    preco_unit   DECIMAL(10,2) NOT NULL,
    observacao   VARCHAR(200),
    status       VARCHAR(20)  DEFAULT 'pendente'
        CHECK (status IN ('pendente','preparando','pronto','entregue')),
    FOREIGN KEY (id_comanda) REFERENCES comandas(id_comanda),
    FOREIGN KEY (id_item)    REFERENCES itens_cardapio(id_item)
);

CREATE TABLE pagamentos_comanda (
    id_pagamento INT          PRIMARY KEY IDENTITY(1,1),
    id_comanda   INT          NOT NULL,
    valor        DECIMAL(10,2) NOT NULL,
    forma        VARCHAR(20)   DEFAULT 'dinheiro'
        CHECK (forma IN ('dinheiro','pix','credito','debito','voucher')),
    data_pagto   DATETIME      DEFAULT GETDATE(),
    FOREIGN KEY (id_comanda) REFERENCES comandas(id_comanda)
);""",
        "queries": {
            "💰 Faturamento Diário": {
                "categoria": "fin",
                "sql": """-- Faturamento por dia com ticket médio e giro de mesas
SELECT
    CAST(c.abertura AS DATE)              AS data,
    COUNT(DISTINCT c.id_comanda)           AS comandas_fechadas,
    COUNT(DISTINCT c.id_mesa)              AS mesas_utilizadas,
    SUM(p.valor)                           AS faturamento,
    SUM(p.valor) / COUNT(DISTINCT c.id_comanda) AS ticket_medio,
    AVG(DATEDIFF(MINUTE, c.abertura, c.fechamento)) AS tempo_medio_minutos
FROM comandas c
JOIN pagamentos_comanda p ON c.id_comanda = p.id_comanda
WHERE c.status = 'fechada'
GROUP BY CAST(c.abertura AS DATE)
ORDER BY data DESC;""",
                "explicacao": "Faturamento diário com tempo médio de mesa ocupada. Otimiza o giro e capacidade do salão."
            },
            "🏆 Itens Mais Pedidos": {
                "categoria": "com",
                "sql": """-- Ranking de itens com receita e margem
SELECT
    ic.nome                                AS item,
    cat.nome                               AS categoria,
    SUM(ci.quantidade)                     AS qtd_pedida,
    SUM(ci.quantidade * ci.preco_unit)     AS receita,
    SUM(ci.quantidade * ic.custo)          AS custo_total,
    CAST(
        (SUM(ci.quantidade * ci.preco_unit) - SUM(ci.quantidade * ic.custo))
        / SUM(ci.quantidade * ci.preco_unit) * 100
    AS DECIMAL(5,1))                       AS margem_pct,
    RANK() OVER (ORDER BY SUM(ci.quantidade) DESC) AS ranking
FROM comanda_itens ci
JOIN itens_cardapio ic ON ci.id_item    = ic.id_item
JOIN categorias_cardapio cat ON ic.id_categoria = cat.id_categoria
JOIN comandas c ON ci.id_comanda = c.id_comanda
WHERE c.status = 'fechada'
GROUP BY ic.nome, cat.nome
ORDER BY ranking;""",
                "explicacao": "Engineering de cardápio: combina popularidade com margem para decisões de menu e promoções."
            }
        },
        "insights": [
            "📌 Itens populares com margem baixa → reposicione no cardápio ou ajuste preço/fornecedor",
            "📌 Tempo de mesa acima de 90 min → gargalo na cozinha ou atendimento; revise processos",
            "📌 Garçons com menor ticket → oportunidade de treinamento em upsell e cross-sell",
            "📌 Análise por dia da semana → dimensione equipe e estoque com base nos picos reais"
        ]
    }
}


def detectar_negocio(descricao: str) -> str:
    """Detecta o tipo de negócio baseado em palavras-chave."""
    descricao_lower = descricao.lower()
    mapeamento = {
        "funerária": ["funerária", "funeral", "velório", "sepultamento", "óbito", "falecido", "cemitério"],
        "loja de motos": ["moto", "motocicleta", "bike", "honda", "yamaha", "financiamento moto", "concessionária"],
        "clínica médica": ["clínica", "médico", "hospital", "paciente", "consulta", "saúde", "prontuário", "médica"],
        "e-commerce": ["e-commerce", "loja online", "ecommerce", "marketplace", "loja virtual", "pedido online"],
        "restaurante": ["restaurante", "lanchonete", "bar", "café", "comida", "cardápio", "garçom", "mesa", "delivery"]
    }
    for negocio, palavras in mapeamento.items():
        if any(p in descricao_lower for p in palavras):
            return negocio
    return None


def gerar_indices(tipo_negocio: str) -> str:
    """Gera sugestões de índices para o tipo de negócio."""
    indices = {
        "funerária": """-- ⚡ ÍNDICES RECOMENDADOS
CREATE INDEX IX_pagamentos_status       ON pagamentos(status);
CREATE INDEX IX_pagamentos_vencimento   ON pagamentos(data_vencimento);
CREATE INDEX IX_contratos_status        ON contratos(status);
CREATE INDEX IX_contratos_cliente       ON contratos(id_cliente);
CREATE INDEX IX_clientes_cpf            ON clientes(cpf);""",
        "loja de motos": """-- ⚡ ÍNDICES RECOMENDADOS
CREATE INDEX IX_motos_status            ON motos(status);
CREATE INDEX IX_vendas_data             ON vendas(data_venda);
CREATE INDEX IX_vendas_vendedor         ON vendas(id_vendedor);
CREATE INDEX IX_financiamentos_status   ON financiamentos(status);
CREATE INDEX IX_clientes_cpf            ON clientes(cpf);""",
        "clínica médica": """-- ⚡ ÍNDICES RECOMENDADOS
CREATE INDEX IX_agendamentos_data       ON agendamentos(data_hora);
CREATE INDEX IX_agendamentos_status     ON agendamentos(status);
CREATE INDEX IX_agendamentos_medico     ON agendamentos(id_medico);
CREATE INDEX IX_faturamentos_status     ON faturamentos(status);
CREATE INDEX IX_pacientes_cpf           ON pacientes(cpf);""",
        "e-commerce": """-- ⚡ ÍNDICES RECOMENDADOS
CREATE INDEX IX_pedidos_status          ON pedidos(status);
CREATE INDEX IX_pedidos_data            ON pedidos(data_pedido);
CREATE INDEX IX_pedidos_cliente         ON pedidos(id_cliente);
CREATE INDEX IX_produtos_sku            ON produtos(sku);
CREATE INDEX IX_produtos_estoque        ON produtos(estoque);""",
        "restaurante": """-- ⚡ ÍNDICES RECOMENDADOS
CREATE INDEX IX_comandas_status         ON comandas(status);
CREATE INDEX IX_comandas_abertura       ON comandas(abertura);
CREATE INDEX IX_comanda_itens_status    ON comanda_itens(status);
CREATE INDEX IX_mesas_status            ON mesas(status);"""
    }
    return indices.get(tipo_negocio, "-- Índices serão sugeridos conforme análise do schema.")


# ─────────────────────────────────────────────
#   INTERFACE PRINCIPAL
# ─────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="hero-header">
        <h1>⚡ SQL FORGE</h1>
        <p>Sistema inteligente de geração automática de bancos de dados e queries SQL</p>
    </div>
    """, unsafe_allow_html=True)

    # Área de input
    col1, col2 = st.columns([3, 1])
    with col1:
        descricao = st.text_area(
            "Descreva seu negócio:",
            placeholder="Ex: Preciso de um banco de dados para minha funerária com controle de contratos e pagamentos...",
            height=120,
            label_visibility="visible"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        tipo_selecionado = st.selectbox(
            "Ou escolha direto:",
            ["— Detectar automaticamente —"] + list(NEGOCIOS_DB.keys()),
            label_visibility="visible"
        )

    # Botão
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        gerar = st.button("⚡ Gerar Banco e Queries", use_container_width=True)

    st.markdown("---")

    # Processamento
    if gerar:
        tipo = None

        if tipo_selecionado != "— Detectar automaticamente —":
            tipo = tipo_selecionado
        elif descricao.strip():
            tipo = detectar_negocio(descricao)

        if not tipo:
            st.warning("⚠️ Não consegui identificar o tipo de negócio. Tente ser mais específico ou selecione diretamente.")
            st.stop()

        dados = NEGOCIOS_DB[tipo]

        # Métricas rápidas
        n_tabelas = dados["banco"].count("CREATE TABLE")
        n_queries = len(dados["queries"])
        n_entidades = len(dados["entidades"])

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="num">{n_tabelas}</div>
                <div class="lbl">Tabelas Criadas</div>
            </div>
            <div class="metric-card">
                <div class="num">{n_queries}</div>
                <div class="lbl">Queries Prontas</div>
            </div>
            <div class="metric-card">
                <div class="num">{n_entidades}</div>
                <div class="lbl">Entidades Mapeadas</div>
            </div>
            <div class="metric-card">
                <div class="num">SQL</div>
                <div class="lbl">Compatível SQL Server</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"{dados['icone']} Negócio identificado: **{dados['nome']}** — Gerando estrutura completa...")

        # Tabs principais
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏗️ Banco de Dados",
            "🔎 Queries SQL",
            "⚡ Otimizações",
            "💡 Insights"
        ])

        # ── TAB 1: BANCO
        with tab1:
            st.markdown("#### 📊 Entidades Mapeadas")
            cols = st.columns(len(dados["entidades"]))
            for i, ent in enumerate(dados["entidades"]):
                cols[i].info(ent)

            st.markdown("#### 🏗️ DDL — Estrutura Completa")
            st.code(dados["banco"], language="sql")

            # Botão de cópia via download
            st.download_button(
                label="💾 Baixar SQL do Banco",
                data=dados["banco"],
                file_name=f"banco_{tipo.replace(' ', '_')}.sql",
                mime="text/plain"
            )

        # ── TAB 2: QUERIES
        with tab2:
            tag_map = {"fin": "tag-fin", "com": "tag-com", "op": "tag-op", "adv": "tag-adv"}
            tag_nome = {"fin": "Financeiro", "com": "Comercial", "op": "Operacional", "adv": "Avançado"}

            sql_completo = ""
            for titulo, info in dados["queries"].items():
                cat = info["categoria"]
                tag_class = tag_map.get(cat, "tag-fin")
                tag_label = tag_nome.get(cat, cat)

                st.markdown(f"""
                <span class="tag {tag_class}">{tag_label}</span>
                <strong>{titulo}</strong>
                """, unsafe_allow_html=True)

                st.code(info["sql"], language="sql")
                st.caption(f"ℹ️ {info['explicacao']}")
                st.markdown("---")
                sql_completo += f"-- {titulo}\n{info['sql']}\n\n"

            st.download_button(
                label="💾 Baixar Todas as Queries",
                data=sql_completo,
                file_name=f"queries_{tipo.replace(' ', '_')}.sql",
                mime="text/plain"
            )

        # ── TAB 3: OTIMIZAÇÕES
        with tab3:
            st.markdown("#### ⚡ Índices Recomendados")
            st.code(gerar_indices(tipo), language="sql")

            st.markdown("#### 🔧 Boas Práticas")
            boas_praticas = [
                ("Paginação", "Use `OFFSET / FETCH` para consultas com grandes volumes de dados. Evite `SELECT *` em produção."),
                ("Transactions", "Envolva operações críticas (INSERT + UPDATE em cascata) em `BEGIN TRAN / COMMIT / ROLLBACK`."),
                ("Soft Delete", "Prefira `ativo = 0` a `DELETE` físico. Mantém histórico e evita problemas de integridade referencial."),
                ("Auditoria", "Adicione `created_at`, `updated_at` e `updated_by` em todas as tabelas críticas."),
                ("Backup", "Configure backup automático diário (FULL) + log backup a cada hora para zero perda de dados."),
                ("Views", "Crie views para as queries mais usadas: `CREATE VIEW vw_inadimplencia AS SELECT...`"),
            ]
            for titulo_bp, desc in boas_praticas:
                with st.expander(f"✅ {titulo_bp}"):
                    st.write(desc)

        # ── TAB 4: INSIGHTS
        with tab4:
            st.markdown("#### 💡 O que você pode analisar com este banco")
            for insight in dados["insights"]:
                st.markdown(f"""
                <div class="insight-box"><p>{insight}</p></div>
                """, unsafe_allow_html=True)

            st.markdown("#### 🚀 Próximos Passos Sugeridos")
            proximos = [
                "1️⃣ Execute o DDL no seu SQL Server para criar o banco",
                "2️⃣ Popule as tabelas mestres (categorias, funcionários, serviços)",
                "3️⃣ Rode as queries de análise após 30 dias de dados reais",
                "4️⃣ Crie um dashboard no Power BI conectando diretamente às views",
                "5️⃣ Configure alertas automáticos para as queries de inadimplência/risco"
            ]
            for p in proximos:
                st.markdown(p)

    else:
        # Estado inicial — exemplos
        st.markdown("#### 💬 Exemplos de uso")
        exemplos = [
            ("🕊️", "Funerária", "Banco com contratos, pagamentos e inadimplência"),
            ("🏍️", "Loja de Motos", "Estoque, financiamento e ranking de vendedores"),
            ("🏥", "Clínica Médica", "Agendamentos, prontuários e análise de churn"),
            ("🛒", "E-commerce", "Pedidos, estoque e análise RFM de clientes"),
            ("🍽️", "Restaurante", "Comandas, cardápio e giro de mesas"),
        ]
        cols = st.columns(len(exemplos))
        for i, (icone, nome, desc) in enumerate(exemplos):
            with cols[i]:
                st.markdown(f"""
                <div class="sql-card" style="text-align:center;cursor:pointer;">
                    <div style="font-size:2rem;">{icone}</div>
                    <div style="font-weight:700;margin:0.5rem 0;">{nome}</div>
                    <div style="font-size:0.8rem;color:#64748b;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()