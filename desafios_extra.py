"""
DESAFIOS EXTRA - MongoDB Queries
================================
Implementação dos 4 desafios específicos solicitados
"""

from pymongo import MongoClient
import pandas as pd

class DesafiosExtra:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
            self.db = self.client["desafios_cinema"]
            self.filmes = self.db["filmes"]
            print("Conexão MongoDB estabelecida")
            self.modo_simulado = False
        except Exception:
            print("MongoDB não disponível. Usando simulação em memória.")
            self.filmes = []
            self.modo_simulado = True
        
        self.preparar_dados()
    
    def preparar_dados(self):
        """Inserir dados de exemplo para os desafios"""
        print("Preparando dados para os desafios...")
        
        filmes_exemplo = [
            {"titulo": "Inception", "ano": 2010, "nota": 8.8, "genero": "Ficção"},
            {"titulo": "Parasite", "ano": 2019, "nota": 8.6, "genero": "Drama"}, 
            {"titulo": "Interstellar", "ano": 2014, "nota": 8.6, "genero": "Ficção"},
            {"titulo": "The Godfather", "ano": 1972, "nota": 9.2, "genero": "Crime"},
            {"titulo": "Avengers: Endgame", "ano": 2019, "nota": 8.4, "genero": "Ação"},
            {"titulo": "Spider-Man: No Way Home", "ano": 2021, "nota": 8.2, "genero": "Ação"},
            {"titulo": "Dune", "ano": 2021, "nota": 8.0, "genero": "Ficção"},
            {"titulo": "Top Gun: Maverick", "ano": 2022, "nota": 8.3, "genero": "Ação"},
            {"titulo": "The Batman", "ano": 2022, "nota": 7.8, "genero": "Ação"},
            {"titulo": "Filme Ruim", "ano": 2023, "nota": 5.2, "genero": "Terror"}  # Menor nota
        ]
        
        if self.modo_simulado:
            self.filmes = filmes_exemplo
        else:
            self.filmes.delete_many({})  # Limpar dados anteriores
            self.filmes.insert_many(filmes_exemplo)
        
        print(f"{len(filmes_exemplo)} filmes inseridos para teste")
    
    def desafio_1_listar_por_nota(self):
        """Desafio 1: Listar filmes ordenados por nota (decrescente)"""
        print("\n🎯 DESAFIO 1: Listar filmes ordenados por nota (decrescente)")
        print("-" * 60)
        
        if self.modo_simulado:
            resultados = sorted(self.filmes, key=lambda x: x['nota'], reverse=True)
        else:
            resultados = list(self.filmes.find({}, {"_id": 0}).sort("nota", -1))
        
        print("\ud83c\udf8b RANKING POR NOTA:")
        for i, filme in enumerate(resultados, 1):
            print(f"  {i:2d}º {filme['titulo']:25} ({filme['ano']}) - ⭐ {filme['nota']}/10")
        
        print(f"\n✅ Query MongoDB: filmes.find().sort('nota', -1)")
        return resultados
    
    def desafio_2_filmes_pos_2015(self):
        """Desafio 2: Buscar filmes lançados após 2015"""
        print("\n🎯 DESAFIO 2: Buscar filmes lançados após 2015")
        print("-" * 60)
        
        if self.modo_simulado:
            resultados = [f for f in self.filmes if f['ano'] > 2015]
        else:
            resultados = list(self.filmes.find(
                {"ano": {"$gt": 2015}}, 
                {"_id": 0}
            ).sort("ano", -1))
        
        print("🗓️ FILMES APÓS 2015:")
        for filme in resultados:
            print(f"  📅 {filme['titulo']:25} ({filme['ano']}) - ⭐ {filme['nota']}/10")
        
        print(f"\n📈 Total encontrado: {len(resultados)} filmes")
        print("✅ Query MongoDB: filmes.find({'ano': {'$gt': 2015}})")
        return resultados
    
    def desafio_3_adicionar_assistido(self):
        """Desafio 3: Adicionar o campo 'assistido: False' em todos"""
        print("\n🎯 DESAFIO 3: Adicionar campo 'assistido: False' em todos")
        print("-" * 60)
        
        if self.modo_simulado:
            for filme in self.filmes:
                filme['assistido'] = False
            count = len(self.filmes)
        else:
            result = self.filmes.update_many(
                {},  # Filtro vazio = todos os documentos
                {"$set": {"assistido": False}}
            )
            count = result.modified_count
        
        print(f"📝 Campo 'assistido: False' adicionado a {count} filmes")
        
        # Mostrar alguns exemplos
        if self.modo_simulado:
            exemplos = self.filmes[:3]
        else:
            exemplos = list(self.filmes.find({}, {"_id": 0}).limit(3))
        
        print("\n📋 EXEMPLOS DE FILMES ATUALIZADOS:")
        for filme in exemplos:
            assistido_status = "❌ Não assistido" if not filme.get('assistido', True) else "✅ Assistido"
            print(f"  🎬 {filme['titulo']:25} - {assistido_status}")
        
        print(f"\n✅ Query MongoDB: filmes.update_many({{}}, {{'$set': {{'assistido': False}}})")
        return count
    
    def desafio_4_deletar_menor_nota(self):
        """Desafio 4: Deletar o filme com menor nota"""
        print("\n🎯 DESAFIO 4: Deletar o filme com menor nota")
        print("-" * 60)
        
        # Primeiro, encontrar o filme com menor nota
        if self.modo_simulado:
            if not self.filmes:
                print("❌ Nenhum filme encontrado")
                return None
            filme_menor = min(self.filmes, key=lambda x: x['nota'])
            print(f"🔍 Filme com menor nota identificado:")
            print(f"  🎬 {filme_menor['titulo']} ({filme_menor['ano']}) - ⭐ {filme_menor['nota']}/10")
            
            # Remover da lista
            self.filmes = [f for f in self.filmes if f['titulo'] != filme_menor['titulo']]
        else:
            # Encontrar filme com menor nota
            filme_menor = list(self.filmes.find().sort("nota", 1).limit(1))
            if not filme_menor:
                print("❌ Nenhum filme encontrado")
                return None
            
            filme_menor = filme_menor[0]
            print(f"🔍 Filme com menor nota identificado:")
            print(f"  🎬 {filme_menor['titulo']} ({filme_menor['ano']}) - ⭐ {filme_menor['nota']}/10")
            
            # Deletar o filme
            result = self.filmes.delete_one({"_id": filme_menor["_id"]})
            if result.deleted_count == 0:
                print("❌ Erro ao deletar filme")
                return None
        
        print(f"🗑️ Filme '{filme_menor['titulo']}' deletado com sucesso!")
        
        # Mostrar estatísticas após deleção
        if self.modo_simulado:
            total_restante = len(self.filmes)
            if self.filmes:
                nota_minima_atual = min(f['nota'] for f in self.filmes)
                print(f"📊 Filmes restantes: {total_restante}")
                print(f"📊 Nova menor nota: {nota_minima_atual}/10")
        else:
            total_restante = self.filmes.count_documents({})
            print(f"📊 Filmes restantes: {total_restante}")
        
        print(f"\n✅ Query MongoDB: filmes.find().sort('nota', 1).limit(1) + delete_one()")
        return filme_menor
    
    def executar_todos_desafios(self):
        """Executar todos os 4 desafios em sequência"""
        print("🚀 EXECUTANDO TODOS OS DESAFIOS EXTRA")
        print("=" * 80)
        
        # Executar cada desafio
        resultado1 = self.desafio_1_listar_por_nota()
        resultado2 = self.desafio_2_filmes_pos_2015() 
        resultado3 = self.desafio_3_adicionar_assistido()
        resultado4 = self.desafio_4_deletar_menor_nota()
        
        # Resumo final
        print("\n" + "=" * 80)
        print("🎉 TODOS OS DESAFIOS CONCLUÍDOS COM SUCESSO!")
        print("=" * 80)
        print("📋 RESUMO:")
        print(f"  ✅ Desafio 1: {len(resultado1)} filmes ordenados por nota")
        print(f"  ✅ Desafio 2: {len(resultado2)} filmes após 2015 encontrados")
        print(f"  ✅ Desafio 3: {resultado3} filmes atualizados com campo 'assistido'")
        print(f"  ✅ Desafio 4: 1 filme deletado (menor nota)")
        print("\n💡 Todas as queries MongoDB foram implementadas e testadas!")

def main():
    """Função principal para executar os desafios"""
    desafios = DesafiosExtra()
    desafios.executar_todos_desafios()

if __name__ == "__main__":
    main()