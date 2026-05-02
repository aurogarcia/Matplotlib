import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

def analisar_dataset_tips():
    print("Carregando dataset de restaurante...")
    
    df = sns.load_dataset('tips')
    print(f"Dataset carregado: {df.shape[0]} registros, {df.shape[1]} variáveis")
    print(f"Variáveis: {list(df.columns)}")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Análise Exploratória - Dataset Tips', fontsize=16, fontweight='bold')
    
    sns.histplot(df['total_bill'], kde=True, color='#0d9488', ax=axes[0,0])
    axes[0,0].set_title('Distribuição das Contas')
    axes[0,0].axvline(df['total_bill'].mean(), color='red', linestyle='--', 
                      label=f'Média: ${df["total_bill"].mean():.2f}')
    axes[0,0].legend()
    
    sns.regplot(x='total_bill', y='tip', data=df, color='#e05c2a', ax=axes[0,1])
    axes[0,1].set_title('Conta vs Gorjeta (com tendência)')
    
    sns.boxplot(x='day', y='tip', hue='time', data=df, 
                palette='Set2', ax=axes[1,0])
    axes[1,0].set_title('Gorjetas por Dia e Período')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    sns.violinplot(x='sex', y='total_bill', data=df, 
                   palette=['#0d9488', '#e05c2a'], ax=axes[1,1])
    axes[1,1].set_title('Distribuição das Contas por Gênero')
    
    plt.tight_layout()
    plt.show()
    
    return df

def criar_heatmap_correlacoes(df):
    print("Criando heatmap de correlações...")
    
    numeric_cols = df.select_dtypes(include=[np.number])
    
    plt.figure(figsize=(8, 6))
    mask = np.triu(np.ones_like(numeric_cols.corr(), dtype=bool))
    sns.heatmap(numeric_cols.corr(), 
                annot=True, 
                cmap='coolwarm', 
                center=0,
                mask=mask,
                square=True,
                fmt='.2f')
    plt.title('Matriz de Correlação - Variáveis Numéricas', fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    corr_matrix = numeric_cols.corr()
    print("Correlações mais fortes:")
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.5:
                print(f"   {corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}: {corr_value:.3f}")

def criar_pairplot_exploratório(df):
    print("Criando pairplot exploratório...")
    
    g = sns.pairplot(df, hue='sex', 
                     palette={'Male':'#0d9488', 'Female':'#e05c2a'},
                     diag_kind='kde', 
                     height=2.5)
    g.fig.suptitle('Exploração Completa - Dataset Tips', y=1.02, fontsize=14)
    plt.show()

def analise_segmentada(df):
    print("Realizando análise segmentada...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    tip_by_size = df.groupby('size')['tip'].agg(['mean', 'count']).reset_index()
    
    axes[0].bar(tip_by_size['size'], tip_by_size['mean'], 
                color='#0d9488', alpha=0.7)
    axes[0].set_title('Gorjeta Média por Tamanho do Grupo')
    axes[0].set_xlabel('Tamanho do Grupo')
    axes[0].set_ylabel('Gorjeta Média ($)')
    
    axes[1].bar(tip_by_size['size'], tip_by_size['count'], 
                color='#e05c2a', alpha=0.7)
    axes[1].set_title('Frequência por Tamanho do Grupo')
    axes[1].set_xlabel('Tamanho do Grupo')
    axes[1].set_ylabel('Número de Mesas')
    
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("Insights por tamanho:")
    for _, row in tip_by_size.iterrows():
        print(f"   Grupo de {int(row['size'])}: ${row['mean']:.2f} gorjeta média ({int(row['count'])} mesas)")

if __name__ == "__main__":
    print("MÓDULO 2: Análises Avançadas com Seaborn")
    print("="*60)
    
    df = analisar_dataset_tips()
    
    print("\n" + "="*60)
    criar_heatmap_correlacoes(df)
    
    print("\n" + "="*60)
    criar_pairplot_exploratório(df)
    
    print("\n" + "="*60)
    analise_segmentada(df)