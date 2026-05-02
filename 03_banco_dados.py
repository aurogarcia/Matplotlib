from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CinemaDatabase:
    
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
            self.db = self.client["cinema_analytics"]
            self.filmes = self.db["filmes"]
            self.avaliacoes = self.db["avaliacoes"]
            print("Conexão com MongoDB estabelecida")
        except Exception as e:
            print("MongoDB não disponível. Usando simulação em memória.")
            self.filmes = []
            self.avaliacoes = []
            self.modo_simulado = True
    
    def inserir_filmes_exemplo(self):
        print("Inserindo catálogo de filmes...")
        
        filmes_data = [
            {
                "titulo": "Inception",
                "ano": 2010,
                "nota": 8.8,
                "generos": ["Ficção Científica", "Thriller"],
                "diretor": "Christopher Nolan",
                "orcamento": 160,
                "bilheteria": 836.8,
                "oscar": False
            },
            {
                "titulo": "Parasite",
                "ano": 2019,
                "nota": 8.6,
                "generos": ["Drama", "Suspense", "Comédia"],
                "diretor": "Bong Joon-ho",
                "orcamento": 11.4,
                "bilheteria": 258.8,
                "oscar": True
            },
            {
                "titulo": "Interstellar",
                "ano": 2014,
                "nota": 8.6,
                "generos": ["Ficção Científica", "Drama"],
                "diretor": "Christopher Nolan",
                "orcamento": 165,
                "bilheteria": 677.5,
                "oscar": False
            },
            {
                "titulo": "The Godfather",
                "ano": 1972,
                "nota": 9.2,
                "generos": ["Crime", "Drama"],
                "diretor": "Francis Ford Coppola",
                "orcamento": 6.0,
                "bilheteria": 286.2,
                "oscar": True
            },
            {
                "titulo": "1917",
                "ano": 2019,
                "nota": 8.3,
                "generos": ["Guerra", "Drama"],
                "diretor": "Sam Mendes",
                "orcamento": 95,
                "bilheteria": 384.9,
                "oscar": True
            }
        ]
        
        if hasattr(self, 'modo_simulado'):
            self.filmes.extend(filmes_data)
        else:
            self.filmes.delete_many({})
            result = self.filmes.insert_many(filmes_data)
            print(f"{len(result.inserted_ids)} filmes inseridos")
    
    def buscar_filmes_bem_avaliados(self, nota_minima=8.5):
        print(f"Buscando filmes com nota > {nota_minima}...")
        
        if hasattr(self, 'modo_simulado'):
            resultados = [f for f in self.filmes if f['nota'] > nota_minima]
        else:
            resultados = list(self.filmes.find(
                {"nota": {"$gt": nota_minima}},
                {"titulo": 1, "nota": 1, "ano": 1, "_id": 0}
            ))
        
        print("Filmes bem avaliados:")
        for filme in resultados:
            print(f"   {filme['titulo']} ({filme['ano']}) — {filme['nota']}/10")
        
        return resultados
    
    def analisar_por_diretor(self, diretor):
        print(f"Analisando filmografia de {diretor}...")
        
        if hasattr(self, 'modo_simulado'):
            filmes_diretor = [f for f in self.filmes if f['diretor'] == diretor]
        else:
            filmes_diretor = list(self.filmes.find(
                {"diretor": diretor},
                {"titulo": 1, "ano": 1, "nota": 1, "bilheteria": 1, "_id": 0}
            ))
        
        if not filmes_diretor:
            print(f"Nenhum filme encontrado para {diretor}")
            return None
        
        print(f"{len(filmes_diretor)} filmes encontrados:")
        for filme in filmes_diretor:
            print(f"   {filme['titulo']} ({filme['ano']}) — {filme['nota']}/10")
        
        # Estatísticas
        notas = [f['nota'] for f in filmes_diretor]
        bilheteria = sum([f.get('bilheteria', 0) for f in filmes_diretor])
        
        print(f"\nEstatísticas de {diretor}:")
        print(f"   Nota média: {sum(notas)/len(notas):.1f}/10")
        print(f"   Bilheteria total: ${bilheteria:.1f}M")
        
        return filmes_diretor
    
    def atualizar_filme(self, titulo, **updates):
        print(f"Atualizando {titulo}...")
        
        if hasattr(self, 'modo_simulado'):
            for filme in self.filmes:
                if filme['titulo'] == titulo:
                    filme.update(updates)
                    break
        else:
            result = self.filmes.update_one(
                {"titulo": titulo},
                {"$set": updates}
            )
            print(f"{result.modified_count} documento(s) atualizados")
    
    def estatisticas_por_genero(self):
        print("Calculando estatísticas por gênero...")
        
        # Coletar todos os gêneros
        generos = {}
        filmes_data = self.filmes if hasattr(self, 'modo_simulado') else list(self.filmes.find())
        
        for filme in filmes_data:
            for genero in filme.get('generos', []):
                if genero not in generos:
                    generos[genero] = {'count': 0, 'notas': [], 'bilheteria': 0}
                
                generos[genero]['count'] += 1
                generos[genero]['notas'].append(filme['nota'])
                generos[genero]['bilheteria'] += filme.get('bilheteria', 0)
        
        print("Estatísticas por gênero:")
        for genero, stats in generos.items():
            nota_media = sum(stats['notas']) / len(stats['notas'])
            print(f"   {genero}: {stats['count']} filmes, nota média {nota_media:.1f}, ${stats['bilheteria']:.1f}M bilheteria")
    
    def export_para_pandas(self):
        print("Exportando para DataFrame pandas...")
        
        filmes_data = self.filmes if hasattr(self, 'modo_simulado') else list(self.filmes.find({}, {"_id": 0}))
        
        if not filmes_data:
            print("Nenhum dado encontrado")
            return None
        
        df = pd.DataFrame(filmes_data)
        
        print(f"DataFrame criado: {df.shape[0]} filmes, {df.shape[1]} colunas")
        print(f"Colunas: {list(df.columns)}")
        
        print("\nEstatísticas básicas:")
        print(f"   Nota média: {df['nota'].mean():.2f}")
        print(f"   Filme mais antigo: {df['ano'].min()}")
        print(f"   Filme mais recente: {df['ano'].max()}")
        
        return df

def executar_analise_completa():
    print("INICIANDO ANÁLISE COMPLETA DO CINEMA")
    print("="*60)
    
    db = CinemaDatabase()
    
    db.inserir_filmes_exemplo()
    print("\n" + "="*60)
    
    db.buscar_filmes_bem_avaliados(8.5)
    print("\n" + "="*60)
    
    db.analisar_por_diretor("Christopher Nolan")
    print("\n" + "="*60)
    
    db.atualizar_filme("Parasite", nota=8.7, oscar_melhor_filme=True)
    
    db.estatisticas_por_genero()
    print("\n" + "="*60)
    
    df = db.export_para_pandas()
    
    return df

if __name__ == "__main__":
    print("MÓDULO 3: Operações com Banco de Dados")
    print("="*60)
    
    df_cinema = executar_analise_completa()
    
    if df_cinema is not None:
        print("\nAnálise concluída! DataFrame disponível para visualizações.")