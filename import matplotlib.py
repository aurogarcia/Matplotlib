import matplotlib.pyplot as plt
import numpy as np

trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
vendas_2024 = [120, 145, 162, 198]
vendas_2023 = [100, 130, 140, 175]

fig, ax = plt.subplots(figsize=(8, 5))

x = np.arange(len(trimestres))
largura = 0.35

ax.bar(x - largura/2, vendas_2023, largura,
       label='2023', color='#0d9488', alpha=0.8)
ax.bar(x + largura/2, vendas_2024, largura,
       label='2024', color='#e05c2a', alpha=0.8)

ax.set_title('Vendas por Trimestre (mil R$)')
ax.set_xlabel('Trimestre')
ax.set_ylabel('Vendas (R$ mil)')
ax.set_xticks(x)
ax.set_xticklabels(trimestres)
ax.legend()
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.show()

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(df['total_bill'], kde=True,
             color='#0d9488', ax=axes[0])
axes[0].set_title('Distribuição das Contas')

sns.regplot(x='total_bill', y='tip',
            data=df, color='#e05c2a', ax=axes[1])
axes[1].set_title('Conta vs Gorjeta')

plt.tight_layout()
plt.show()

numeric = df.select_dtypes(include='number')
sns.heatmap(numeric.corr(), annot=True,
            cmap='coolwarm', center=0)
plt.title('Correlações')
plt.show()
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')

sns.pairplot(df, hue='sex',
             palette={'Male':'#0d9488','Female':'#e05c2a'})
plt.suptitle('Exploração Geral — Tips Dataset',
             y=1.02)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='day', y='total_bill',
            hue='sex', data=df,
            palette='Set2', ax=ax)
ax.set_title('Conta por Dia e Gênero')
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.show()

sns.violinplot(x='day', y='tip', data=df,
               palette='coolwarm', inner='box')
plt.title('Distribuição das Gorjetas por Dia')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dados = {
    'mes': ['Jan','Fev','Mar','Abr','Mai','Jun'],
    'receita': [80, 95, 70, 110, 130, 125],
    'clientes': [400, 450, 380, 520, 600, 570],
    'ticket_medio': [200, 211, 184, 212, 217, 219]
}
df = pd.DataFrame(dados)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
fig.suptitle('Análise de Performance — 1º Semestre 2024',
             fontsize=14, fontweight='bold')

# Receita por mês
axes[0].bar(df['mes'], df['receita'],
            color=['#e05c2a' if v==70 else '#0d9488'
                   for v in df['receita']])
axes[0].set_title('Receita (R$ mil)')
axes[0].set_ylim(0, 150)
axes[0].annotate('Queda em Março\n(-26%)',
                 xy=('Mar', 70), xytext=('Abr', 60),
                 fontsize=8, color='#e05c2a',
                 arrowprops=dict(arrowstyle='->', color='#e05c2a'))

# Clientes ativos
axes[1].plot(df['mes'], df['clientes'],
             marker='o', color='#0d9488', linewidth=2)
axes[1].set_title('Clientes Ativos')
axes[1].fill_between(range(6), df['clientes'],
                     alpha=0.1, color='#0d9488')

# Ticket médio
axes[2].bar(df['mes'], df['ticket_medio'],
            color='#2563eb', alpha=0.7)
axes[2].set_title('Ticket Médio (R$)')

for ax in axes:
    ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.show()

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
filmes_col = client["cinema"]["filmes"]

filmes_col.insert_many([
    {"titulo": "Inception",    "ano": 2010, "nota": 8.8,
     "generos": ["Ficção","Thriller"], "diretor": "Nolan"},
    {"titulo": "Parasite",     "ano": 2019, "nota": 8.6,
     "generos": ["Drama","Suspense"],  "diretor": "Bong"},
    {"titulo": "Interstellar", "ano": 2014, "nota": 8.6,
     "generos": ["Ficção","Drama"],    "diretor": "Nolan"},
    {"titulo": "The Godfather","ano": 1972, "nota": 9.2,
     "generos": ["Crime","Drama"],     "diretor": "Coppola"},
    {"titulo": "1917",         "ano": 2019, "nota": 8.3,
     "generos": ["Guerra","Drama"],    "diretor": "Mendes"},
])

bons = filmes_col.find({"nota": {"$gt": 8.5}},
                        {"titulo": 1, "nota": 1, "_id": 0})
print("Filmes bem avaliados:")
for f in bons:
    print(f" {f['titulo']} — {f['nota']}")

nolan = list(filmes_col.find({"diretor": "Nolan"},
                              {"titulo": 1, "ano": 1, "_id": 0}))
print(f"\nFilmes de Nolan ({len(nolan)} encontrados):")
for f in nolan:
    print(f"  {f['titulo']} ({f['ano']})")

filmes_col.update_one(
    {"titulo": "Parasite"},
    {"$set": {"nota": 8.7, "oscar": True}}
)

total_drama = filmes_col.count_documents(
    {"generos": "Drama"}
)
print(f"\nFilmes com gênero Drama: {total_drama}")
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
alunos = client["aula_ds"]["alunos"]

alunos.update_one(
    {"nome": "Carlos Lima"},          # filtro
    {"$set": {"media": 7.5}}          # operação
)

alunos.update_many(
    {"periodo": 2},
    {"$inc": {"periodo": 1}})
)


alunos.update_many(
    {},
    {"$set": {"turma": "2026-1"}}
)

alunos.delete_one({"nome": "Pedro Nunes"})

alunos.delete_many({"ativo": False})

# Deletar TODOS (cuidado!)
# alunos.delete_many({})

print("Total de alunos:", alunos.count_documents({}))
print("Alunos ativos:",   alunos.count_documents({"ativo": True}))
print("Coleções:", client["aula_ds"].list_collection_names())
filmes_col.find().sort("nota", -1)

filmes_col.find().sort(
    "nota", -1).limit(3)

filmes_col.find(
    {"ano": {"$gt": 2015}})
