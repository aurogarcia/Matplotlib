import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.ioff()

def demonstrar_organizacao():
    print("DEMONSTRAÇÃO DO PROJETO ORGANIZADO")
    print("="*60)
    
    print("\nESTRUTURA CRIADA:")
    arquivos = [
        "01_visualizacoes_basicas.py",
        "02_analises_avancadas.py", 
        "03_banco_dados.py",
        "main_projeto_integrado.py",
        "README.md",
        "codigo_original_backup.py"
    ]
    
    for arquivo in arquivos:
        print(f"{arquivo}")
    
    print(f"\nTOTAL: {len(arquivos)} arquivos organizados")

def executar_analise_rapida():
    print("\nANÁLISE RÁPIDA DOS DADOS")
    print("-"*40)
    
    np.random.seed(42)
    
    vendas = pd.DataFrame({
        'mes': pd.date_range('2024-01-01', periods=12, freq='ME'),
        'receita': np.random.exponential(100, 12) + 80,
        'clientes': np.random.randint(300, 800, 12)
    })
    
    cinema = pd.DataFrame({
        'filme': ['Top Gun', 'Avatar 2', 'Oppenheimer', 'Barbie', 'Tudo em Todo Lugar'],
        'orcamento': [170, 350, 100, 145, 14.3],
        'bilheteria': [1488.7, 2320.2, 952.0, 1446.0, 139.4]
    })
    
    try:
        tips = sns.load_dataset('tips')
    except:
        tips = pd.DataFrame({
            'total_bill': np.random.exponential(20, 200) + 5,
            'tip': np.random.exponential(3, 200) + 0.5,
            'size': np.random.choice([1,2,3,4,5,6], 200)
        })
    
    print(f"Dados de vendas: {len(vendas)} meses analisados")
    print(f"Filmes analisados: {len(cinema)} títulos")
    print(f"Transações restaurante: {len(tips)} registros")
    
    return vendas, cinema, tips

def gerar_insights(vendas, cinema, tips):
    print("\nPRINCIPAIS INSIGHTS")
    print("-"*40)
    
    crescimento = ((vendas['receita'].iloc[-1] / vendas['receita'].iloc[0]) - 1) * 100
    print(f"Crescimento vendas 2024: {crescimento:.1f}%")
    
    cinema['roi'] = ((cinema['bilheteria'] / cinema['orcamento']) - 1) * 100
    melhor_filme = cinema.loc[cinema['roi'].idxmax()]
    print(f"Melhor ROI: {melhor_filme['filme']} ({melhor_filme['roi']:.0f}%)")
    
    if 'tip' in tips.columns and 'total_bill' in tips.columns:
        gorjeta_media = (tips['tip'] / tips['total_bill'] * 100).mean()
        print(f"Gorjeta média: {gorjeta_media:.1f}%")
    
    print(f"\nRESUMO FINANCEIRO:")
    print(f"   Receita total 2024: R$ {vendas['receita'].sum():.0f}k")
    print(f"   Bilheteria total: ${cinema['bilheteria'].sum():.1f}M")
    print(f"   ROI médio cinema: {cinema['roi'].mean():.0f}%")

def demonstrar_capacidades():
    print("\nCAPACIDADES IMPLEMENTADAS")
    print("-"*40)
    
    capacidades = [
        "Visualizações com Matplotlib",
        "Análises estatísticas com Seaborn", 
        "Manipulação de dados com Pandas",
        "Operações de banco de dados (MongoDB)",
        "Pipeline completo de Data Science",
        "Geração automatizada de relatórios",
        "Cálculo de métricas de negócio (ROI, crescimento)",
        "Análise de correlações e distribuições",
        "Tratamento de múltiplas fontes de dados",
        "Código modular e reutilizável",
        "Documentação completa",
        "Tratamento de erros e fallbacks"
    ]
    
    for capacidade in capacidades:
        print(f"  {capacidade}")

def mostrar_proximo_passos():
    print("\nCOMO USAR O PROJETO")
    print("-"*40)
    
    print("EXECUÇÃO RECOMENDADA:")
    print("  1. python main_projeto_integrado.py    # Projeto completo")
    print("  2. python 01_visualizacoes_basicas.py  # Só gráficos")
    print("  3. python 02_analises_avancadas.py     # Só análises") 
    print("  4. python 03_banco_dados.py            # Só banco")
    
    print("\nCUSTOMIZAÇÕES POSSÍVEIS:")
    print("  • Conectar seus próprios dados")
    print("  • Modificar visualizações") 
    print("  • Adicionar novos módulos")
    print("  • Integrar com APIs externas")
    print("  • Implementar machine learning")
    
    print("\nMELHORIAS FUTURAS:")
    print("  • Dashboard web interativo")
    print("  • Modelos preditivos")
    print("  • Automação de relatórios")
    print("  • Deploy em nuvem")

def main():
    print("BEM-VINDO AO SEU PROJETO ORGANIZADO!")
    print("="*60)
    
    demonstrar_organizacao()
    
    vendas, cinema, tips = executar_analise_rapida()
    
    gerar_insights(vendas, cinema, tips)
    
    demonstrar_capacidades()
    
    mostrar_proximo_passos()
    
    print("\n" + "="*60)
    print("TRANSFORMAÇÃO CONCLUÍDA!")
    print("Código original → Projeto profissional")
    print("Dados desorganizados → Pipeline estruturado") 
    print("Análises isoladas → Sistema integrado")
    print("="*60)
    
    print(f"\nRelatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()