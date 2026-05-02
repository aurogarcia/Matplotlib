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

    def listar_filmes_por_nota(self):
        """Desafio 1: Listar filmes ordenados por nota (decrescente)"""
        print("Listando filmes ordenados por nota (decrescente)...")
        
        if hasattr(self, 'modo_simulado'):
            filmes_ordenados = sorted(self.filmes, key=lambda x: x['nota'], reverse=True)
        else:
            filmes_ordenados = list(self.filmes.find({}, {"titulo": 1, "nota": 1, "ano": 1, "_id": 0}).sort("nota", -1))
        
        print("Ranking de filmes por nota:")
        for i, filme in enumerate(filmes_ordenados, 1):
            print(f"   {i}º {filme['titulo']} ({filme['ano']}) - {filme['nota']}/10")
        
        return filmes_ordenados
    
    def buscar_filmes_apos_2015(self):
        """Desafio 2: Buscar filmes lançados após 2015"""
        print("Buscando filmes lançados após 2015...")
        
        if hasattr(self, 'modo_simulado'):
            filmes_recentes = [f for f in self.filmes if f['ano'] > 2015]
        else:
            filmes_recentes = list(self.filmes.find(
                {"ano": {"$gt": 2015}},
                {"titulo": 1, "ano": 1, "nota": 1, "_id": 0}
            ))
        
        print(f"Encontrados {len(filmes_recentes)} filmes após 2015:")
        for filme in filmes_recentes:
            print(f"   {filme['titulo']} ({filme['ano']}) - {filme['nota']}/10")
        
        return filmes_recentes
    
    def adicionar_campo_assistido(self):
        """Desafio 3: Adicionar o campo 'assistido: False' em todos"""
        print("Adicionando campo 'assistido: False' em todos os filmes...")
        
        if hasattr(self, 'modo_simulado'):
            for filme in self.filmes:
                filme['assistido'] = False
            count = len(self.filmes)
        else:
            result = self.filmes.update_many(
                {},  # Todos os documentos
                {"$set": {"assistido": False}}
            )
            count = result.modified_count
        
        print(f"{count} filmes atualizados com campo 'assistido: False'")
        return count
    
    def deletar_filme_menor_nota(self):
        """Desafio 4: Deletar o filme com menor nota"""
        print("Identificando e deletando filme com menor nota...")
        
        if hasattr(self, 'modo_simulado'):
            if not self.filmes:
                print("Nenhum filme encontrado para deletar")
                return None
            
            filme_menor_nota = min(self.filmes, key=lambda x: x['nota'])
            self.filmes = [f for f in self.filmes if f['titulo'] != filme_menor_nota['titulo']]
        else:
            # Encontrar filme com menor nota
            filme_menor_nota = list(self.filmes.find().sort("nota", 1).limit(1))
            
            if not filme_menor_nota:
                print("Nenhum filme encontrado para deletar")
                return None
            
            filme_menor_nota = filme_menor_nota[0]
            
            # Deletar o filme
            result = self.filmes.delete_one({"_id": filme_menor_nota["_id"]})
            
            if result.deleted_count == 0:
                print("Erro ao deletar filme")
                return None
        
        print(f"Filme deletado: {filme_menor_nota['titulo']} (nota: {filme_menor_nota['nota']})")
        return filme_menor_nota
    
    def executar_desafios_extra(self):
        """Executar todos os desafios extra em sequência"""
        print("\n" + "="*60)
        print("EXECUTANDO DESAFIOS EXTRA")
        print("="*60)
        
        # Desafio 1
        print("\n[DESAFIO 1] Listar filmes por nota")
        self.listar_filmes_por_nota()
        
        # Desafio 2  
        print("\n" + "-"*40)
        print("[DESAFIO 2] Filmes após 2015")
        self.buscar_filmes_apos_2015()
        
        # Desafio 3
        print("\n" + "-"*40) 
        print("[DESAFIO 3] Adicionar campo assistido")
        self.adicionar_campo_assistido()
        
        # Desafio 4
        print("\n" + "-"*40)
        print("[DESAFIO 4] Deletar filme com menor nota")
        filme_deletado = self.deletar_filme_menor_nota()
        
        print("\n" + "="*60)
        print("TODOS OS DESAFIOS CONCLUÍDOS!")
        print("="*60)
        
        return filme_deletado

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
    
    db.export_para_pandas()
    
    # Executar desafios extra
    print("\n" + "="*60)
    db.executar_desafios_extra()
    
    return df

if __name__ == "__main__":
    print("MÓDULO 3: Operações com Banco de Dados")
    print("="*60)
    
    df_cinema = executar_analise_completa()
    
    if df_cinema is not None:
        print("\nAnálise concluída! DataFrame disponível para visualizações.")