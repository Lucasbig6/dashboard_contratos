import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker("pt_BR")
random.seed(42)

# Lista de cidades do Piauí (pode expandir se quiser todas)
cidades_piaui = [
    "Teresina", "Parnaíba", "Picos", "Floriano", "Piripiri",
    "Campo Maior", "Barras", "Oeiras", "São Raimundo Nonato",
    "Esperantina", "Altos", "José de Freitas", "Pedro II",
    "Union", "Cocal", "Luís Correia"
]

# ---------- Clientes ----------
n_clientes = 200
clientes = []
for i in range(1, n_clientes+1):
    clientes.append({
        "cliente_id": i,
        "nome": fake.name(),
        "email": fake.email(),
        "cidade": random.choice(cidades_piaui),
        "estado": "Piauí",
        "setor": random.choice(["Tecnologia", "Saúde", "Educação", "Comércio", "Serviços"])
    })

df_clientes = pd.DataFrame(clientes)

# ---------- Contratos ----------
n_contratos = 300
contratos = []
for i in range(1, n_contratos+1):
    cliente_id = random.randint(1, n_clientes)
    data_inicio = fake.date_between(start_date="-3y", end_date="today")
    meses = random.randint(6, 36)
    data_fim = data_inicio + timedelta(days=30*meses)
    valor_mensal = random.randint(500, 10000)
    status = random.choice(["Ativo", "Encerrado", "Inadimplente"])
    data_cancelamento = None
    if status != "Ativo":
        data_cancelamento = fake.date_between(start_date=data_inicio, end_date=data_fim)

    contratos.append({
        "id_contrato": i,
        "cliente_id": cliente_id,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "valor_mensal": valor_mensal,
        "status": status,
        "data_cancelamento": data_cancelamento
    })

df_contratos = pd.DataFrame(contratos)

# ---------- Pagamentos ----------
n_pagamentos = 2000
pagamentos = []
for i in range(1, n_pagamentos+1):
    contrato = random.choice(contratos)
    data_pagamento = fake.date_between(start_date=contrato["data_inicio"], end_date="today")
    valor_pago = contrato["valor_mensal"]
    status_pagamento = random.choice(["Pago", "Atrasado", "Em aberto"])
    if status_pagamento == "Atrasado":
        valor_pago *= random.uniform(0.5, 0.9)  # simula pagamento parcial

    pagamentos.append({
        "id_pagamento": i,
        "id_contrato": contrato["id_contrato"],
        "data_pagamento": data_pagamento,
        "valor_pago": round(valor_pago, 2),
        "forma_pagamento": random.choice(["Cartão", "Boleto", "PIX", "Transferência"]),
        "status_pagamento": status_pagamento
    })

df_pagamentos = pd.DataFrame(pagamentos)

# ---------- Exportar ----------
df_clientes.to_csv("data/clientes.csv", index=False, encoding="utf-8")
df_contratos.to_csv("data/contratos.csv", index=False, encoding="utf-8")
df_pagamentos.to_csv("data/pagamentos.csv", index=False, encoding="utf-8")

print("✅ Dados com cidades do Piauí gerados: clientes.csv, contratos.csv, pagamentos.csv")
