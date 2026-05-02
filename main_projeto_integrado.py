import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from banco_dados import CinemaDatabase
    from visualizacoes_basicas import criar_grafico_vendas, criar_grafico_performance_ecommerce
    from analises_avancadas import analisar_dataset_tips, criar_heatmap_correlacoes
except ImportError:
    print("Executando versão standalone (módulos integrados)")

plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

class ProjetoCienciaDados:
    
    def __init__(self):
        self.resultados = {}
        self.insights = []
        print("INICIANDO PROJETO DE CIÊNCIA DE DADOS")
        print("="*80)
        
    def fase1_coleta_dados(self):
        print("\nFASE 1: COLETA E PREPARAÇÃO DE DADOS")
        print("-"*50)
        
        # Simular dados de diferentes fontes
        self.dados_vendas = self._gerar_dados_vendas()
        self.dados_cinema = self._gerar_dados_cinema()
        self.dados_restaurante = self._carregar_dados_tips()
        
        print(f"Dados de vendas: {len(self.dados_vendas)} registros")
        print(f"Dados de cinema: {len(self.dados_cinema)} registros") 
        print(f"Dados de restaurante: {len(self.dados_restaurante)} registros")
        
        self.resultados['dados_coletados'] = {
            'vendas': len(self.dados_vendas),
            'cinema': len(self.dados_cinema),
            'restaurante': len(self.dados_restaurante)
        }
    
    def _gerar_dados_vendas(self):
        np.random.seed(42)
        meses = pd.date_range('2024-01-01', periods=12, freq='ME')
        
        vendas = []
        for i, mes in enumerate(meses):
            base = 100 + 10 * np.sin(i * np.pi / 6)
            ruido = np.random.normal(0, 15)
            tendencia = i * 2
            
            vendas.append({
                'mes': mes,
                'receita': max(50, base + ruido + tendencia),
                'clientes': np.random.randint(300, 800),
                'produtos_vendidos': np.random.randint(1000, 3000),
                'regiao': np.random.choice(['Norte', 'Sul', 'Sudeste', 'Centro'])
            })
        
        return pd.DataFrame(vendas)
    
    def _gerar_dados_cinema(self):
        filmes = [
            {"titulo": "Top Gun: Maverick", "ano": 2022, "nota": 8.3, "genero": "Ação", 
             "orcamento": 170, "bilheteria": 1488.7},
            {"titulo": "Avatar: The Way of Water", "ano": 2022, "nota": 7.6, "genero": "Ficção", 
             "orcamento": 350, "bilheteria": 2320.2},
            {"titulo": "Tudo em Todo Lugar ao Mesmo Tempo", "ano": 2022, "nota": 8.1, "genero": "Drama", 
             "orcamento": 14.3, "bilheteria": 139.4},
            {"titulo": "Oppenheimer", "ano": 2023, "nota": 8.4, "genero": "Drama", 
             "orcamento": 100, "bilheteria": 952.0},
            {"titulo": "Barbie", "ano": 2023, "nota": 6.9, "genero": "Comédia", 
             "orcamento": 145, "bilheteria": 1446.0},
        ]
        return pd.DataFrame(filmes)
    
    def _carregar_dados_tips(self):
        try:
            return sns.load_dataset('tips')
        except:
            np.random.seed(42)
            data = {
                'total_bill': np.random.exponential(20, 200) + 5,
                'tip': np.random.exponential(3, 200) + 0.5,
                'sex': np.random.choice(['Male', 'Female'], 200),
                'day': np.random.choice(['Thur', 'Fri', 'Sat', 'Sun'], 200),
                'time': np.random.choice(['Lunch', 'Dinner'], 200),
                'size': np.random.choice([1, 2, 3, 4, 5, 6], 200)
            }
            return pd.DataFrame(data)
    
    def fase2_analise_exploratoria(self):
        print("\nFASE 2: ANÁLISE EXPLORATÓRIA")
        print("-"*50)
        
        crescimento_vendas = ((self.dados_vendas['receita'].iloc[-1] / 
                              self.dados_vendas['receita'].iloc[0]) - 1) * 100
        
        print(f"Crescimento de receita anual: {crescimento_vendas:.1f}%")
        
        roi_cinema = ((self.dados_cinema['bilheteria'] / self.dados_cinema['orcamento']) - 1) * 100
        melhor_roi = self.dados_cinema.loc[roi_cinema.idxmax()]
        
        print(f"Melhor ROI cinema: {melhor_roi['titulo']} ({roi_cinema.max():.0f}%)")
        
        gorjeta_percent = (self.dados_restaurante['tip'] / self.dados_restaurante['total_bill'] * 100).mean()
        
        print(f"Gorjeta média: {gorjeta_percent:.1f}% da conta")
        
        self.insights.extend([
            f"Crescimento de receita: {crescimento_vendas:.1f}%",
            f"Melhor filme (ROI): {melhor_roi['titulo']}",
            f"Gorjeta média: {gorjeta_percent:.1f}%"
        ])
    
    def fase3_visualizacoes(self):
        print("\nFASE 3: VISUALIZAÇÕES AVANÇADAS")
        print("-"*50)
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(self.dados_vendas['mes'], self.dados_vendas['receita'], 
                marker='o', linewidth=3, markersize=8, color='#2E8B57')
        ax1.fill_between(self.dados_vendas.index, self.dados_vendas['receita'], 
                        alpha=0.3, color='#2E8B57')
        ax1.set_title('Evolução da Receita 2024', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Receita (R$ mil)')
        ax1.grid(True, alpha=0.3)
        ax1.spines[['top', 'right']].set_visible(False)
        
        ax2 = fig.add_subplot(gs[0, 2])
        roi_por_genero = ((self.dados_cinema['bilheteria'] / self.dados_cinema['orcamento']) - 1) * 100
        bars = ax2.bar(range(len(self.dados_cinema)), roi_por_genero, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'])
        ax2.set_title('ROI por Filme', fontweight='bold')
        ax2.set_ylabel('ROI (%)')
        ax2.tick_params(axis='x', rotation=45, labelsize=9)
        ax2.set_xticks(range(len(self.dados_cinema)))
        ax2.set_xticklabels([titulo[:10]+'...' if len(titulo) > 10 else titulo 
                            for titulo in self.dados_cinema['titulo']])
        
        ax3 = fig.add_subplot(gs[1, :2])
        numeric_tips = self.dados_restaurante.select_dtypes(include=[np.number])
        sns.heatmap(numeric_tips.corr(), annot=True, cmap='coolwarm', 
                   center=0, ax=ax3, square=True, fmt='.2f')
        ax3.set_title('Correlações - Dados Restaurante', fontweight='bold')
        
        ax4 = fig.add_subplot(gs[1, 2])
        self.dados_restaurante['tip_percent'] = (self.dados_restaurante['tip'] / 
                                                self.dados_restaurante['total_bill'] * 100)
        ax4.hist(self.dados_restaurante['tip_percent'], bins=20, 
                color='#FF6B6B', alpha=0.7, edgecolor='black')
        ax4.axvline(self.dados_restaurante['tip_percent'].mean(), 
                   color='red', linestyle='--', linewidth=2,
                   label=f'Média: {self.dados_restaurante["tip_percent"].mean():.1f}%')
        ax4.set_title('Distribuição % Gorjetas', fontweight='bold')
        ax4.set_xlabel('% da Conta')
        ax4.legend()
        
        ax5 = fig.add_subplot(gs[2, :2])
        vendas_regiao = self.dados_vendas.groupby('regiao')['receita'].sum().sort_values(ascending=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(vendas_regiao)))
        bars = ax5.barh(vendas_regiao.index, vendas_regiao.values, color=colors)
        ax5.set_title('Vendas Totais por Região', fontweight='bold')
        ax5.set_xlabel('Receita Total (R$ mil)')
        
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('off')
        
        metricas_text = f"""
        RESUMO EXECUTIVO
        ═══════════════════
        
        Receita Total 2024:
           R$ {self.dados_vendas['receita'].sum():.0f}k
        
        Bilheteria Cinema:
           ${self.dados_cinema['bilheteria'].sum():.1f}M
        
        Análise Restaurante:
           {len(self.dados_restaurante)} transações
        
        Taxa Crescimento:
           {((self.dados_vendas['receita'].iloc[-1]/self.dados_vendas['receita'].iloc[0])-1)*100:.1f}%
        
        Melhor Filme:
           {self.dados_cinema.loc[self.dados_cinema['bilheteria'].idxmax(), 'titulo']}
        """
        
        ax6.text(0.1, 0.9, metricas_text, transform=ax6.transAxes, 
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
        
        plt.suptitle('DASHBOARD INTEGRADO - CIÊNCIA DE DADOS', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.show()
        
        print("Dashboard integrado criado com sucesso!")
    
    def fase4_insights_recomendacoes(self):
        print("\nFASE 4: INSIGHTS E RECOMENDAÇÕES")
        print("-"*50)
        
        print("PRINCIPAIS DESCOBERTAS:")
        
        mes_maior_venda = self.dados_vendas.loc[self.dados_vendas['receita'].idxmax(), 'mes']
        print(f"Pico de vendas: {mes_maior_venda.strftime('%B')}")
        
        melhor_filme = self.dados_cinema.loc[
            ((self.dados_cinema['bilheteria'] / self.dados_cinema['orcamento']) - 1).idxmax()
        ]
        print(f"Filme mais eficiente: {melhor_filme['titulo']} (ROI: {((melhor_filme['bilheteria']/melhor_filme['orcamento'])-1)*100:.0f}%)")
        
        maior_gorjeta_dia = self.dados_restaurante.groupby('day')['tip'].mean().idxmax()
        print(f"Melhor dia para garçons: {maior_gorjeta_dia}")
        
        print("\nRECOMENDAÇÕES ESTRATÉGICAS:")
        print("  1. Foco em {}: período de maior conversão".format(mes_maior_venda.strftime('%B')))
        print("  2. Investir em filmes de baixo orçamento com potencial viral")
        print(f"  3. Otimizar operação de {maior_gorjeta_dia}: maior satisfação do cliente")
        print("  4. Expandir operações na região com melhor performance")
        print("  5. Implementar análise preditiva para próximos trimestres")
        
        self.gerar_relatorio_final()
    
    def gerar_relatorio_final(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        relatorio = f"""
RELATÓRIO DE CIÊNCIA DE DADOS - {datetime.now().strftime("%d/%m/%Y %H:%M")}
{'='*80}

RESUMO EXECUTIVO:
• Datasets processados: {len(self.resultados['dados_coletados'])}
• Total de registros analisados: {sum(self.resultados['dados_coletados'].values())}
• Período de análise: 2022-2024

PRINCIPAIS MÉTRICAS:
• Receita total 2024: R$ {self.dados_vendas['receita'].sum():.0f}k
• Crescimento anual: {((self.dados_vendas['receita'].iloc[-1]/self.dados_vendas['receita'].iloc[0])-1)*100:.1f}%
• ROI médio cinema: {((self.dados_cinema['bilheteria'].sum()/self.dados_cinema['orcamento'].sum())-1)*100:.1f}%

INSIGHTS PRINCIPAIS:
{chr(10).join(['• ' + insight for insight in self.insights])}

PRÓXIMOS PASSOS:
• Implementar modelo preditivo
• Automatizar coleta de dados
• Criar alertas de performance
• Desenvolver API de consultas

TECNOLOGIAS UTILIZADAS:
• Python 3.x
• Pandas, Matplotlib, Seaborn
• MongoDB (simulado)
• Jupyter Notebooks

Relatório gerado automaticamente pelo sistema de análise.
        """
        
        print("RELATÓRIO FINAL GERADO")
        print(relatorio)
    
    def executar_projeto_completo(self):
        try:
            self.fase1_coleta_dados()
            self.fase2_analise_exploratoria() 
            self.fase3_visualizacoes()
            self.fase4_insights_recomendacoes()
            
            print("\n" + "="*80)
            print("PROJETO CONCLUÍDO COM SUCESSO!")
            print("Todas as fases executadas")
            print("Dashboard criado")
            print("Relatório gerado")
            print("Insights documentados")
            print("="*80)
            
        except Exception as e:
            print(f"Erro durante execução: {e}")
            print("Verifique as dependências e dados")

if __name__ == "__main__":
    projeto = ProjetoCienciaDados()
    projeto.executar_projeto_completo()