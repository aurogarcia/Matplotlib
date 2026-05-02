import matplotlib.pyplot as plt
import numpy as np

def criar_grafico_vendas():
    print("Criando gráfico de vendas por trimestre...")
    
    trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
    vendas_2024 = [120, 145, 162, 198]
    vendas_2023 = [100, 130, 140, 175]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(trimestres))
    largura = 0.35

    ax.bar(x - largura/2, vendas_2023, largura,
           label='2023', color='#0d9488', alpha=0.8)
    ax.bar(x + largura/2, vendas_2024, largura,
           label='2024', color='#e05c2a', alpha=0.8)

    ax.set_title('Vendas por Trimestre (mil R$)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Vendas (R$ mil)')
    ax.set_xticks(x)
    ax.set_xticklabels(trimestres)
    ax.legend()
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()
    
    crescimento = [(v2024/v2023 - 1)*100 for v2023, v2024 in zip(vendas_2023, vendas_2024)]
    print(f"Crescimento médio: {np.mean(crescimento):.1f}%")

def criar_grafico_performance_ecommerce():
    print("Criando dashboard de e-commerce...")
    
    import pandas as pd
    
    dados = {
        'mes': ['Jan','Fev','Mar','Abr','Mai','Jun'],
        'receita': [80, 95, 70, 110, 130, 125],
        'clientes': [400, 450, 380, 520, 600, 570],
        'ticket_medio': [200, 211, 184, 212, 217, 219]
    }
    df = pd.DataFrame(dados)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Análise de Performance — 1º Semestre 2024',
                 fontsize=16, fontweight='bold')
    cores = ['#e05c2a' if v == 70 else '#0d9488' for v in df['receita']]
    axes[0].bar(df['mes'], df['receita'], color=cores, alpha=0.8)
    axes[0].set_title('Receita (R$ mil)')
    axes[0].set_ylim(0, 150)
    axes[0].annotate('Queda em Março\n(-26%)',
                     xy=('Mar', 70), xytext=('Abr', 60),
                     fontsize=10, color='#e05c2a',
                     arrowprops=dict(arrowstyle='->', color='#e05c2a'))

    axes[1].plot(df['mes'], df['clientes'],
                 marker='o', color='#0d9488', linewidth=3, markersize=8)
    axes[1].set_title('Clientes Ativos')
    axes[1].fill_between(range(6), df['clientes'],
                         alpha=0.2, color='#0d9488')

    axes[2].bar(df['mes'], df['ticket_medio'],
                color='#2563eb', alpha=0.7)
    axes[2].set_title('Ticket Médio (R$)')
    axes[2].set_ylim(180, 225)

    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()
    
    print(f"Receita total do semestre: R$ {df['receita'].sum()}k")
    print(f"Crescimento de clientes: {((df['clientes'].iloc[-1]/df['clientes'].iloc[0])-1)*100:.1f}%")

if __name__ == "__main__":
    print("MÓDULO 1: Visualizações Básicas")
    print("="*50)
    
    criar_grafico_vendas()
    print("\n" + "="*50)
    criar_grafico_performance_ecommerce()