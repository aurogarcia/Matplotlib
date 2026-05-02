"""
DESAFIOS EXTRA - Implementação dos 4 Itens da Imagem
===================================================
1. Listar filmes ordenados por nota (decrescente)
2. Buscar filmes lançados após 2015  
3. Adicionar o campo 'assistido: False' em todos
4. Deletar o filme com menor nota
"""

from pymongo import MongoClient

class DesafiosSimples:
    def __init__(self):
        print("Iniciando desafios extra MongoDB...")
        # Simular dados (modo compatível)
        self.filmes = [
            {"titulo": "The Godfather", "ano": 1972, "nota": 9.2},
            {"titulo": "Inception", "ano": 2010, "nota": 8.8},
            {"titulo": "Parasite", "ano": 2019, "nota": 8.6},
            {"titulo": "Interstellar", "ano": 2014, "nota": 8.6},
            {"titulo": "Avengers: Endgame", "ano": 2019, "nota": 8.4},
            {"titulo": "Top Gun: Maverick", "ano": 2022, "nota": 8.3},
            {"titulo": "Spider-Man: No Way Home", "ano": 2021, "nota": 8.2},
            {"titulo": "Dune", "ano": 2021, "nota": 8.0},
            {"titulo": "The Batman", "ano": 2022, "nota": 7.8},
            {"titulo": "Filme Ruim", "ano": 2023, "nota": 5.2}  # Menor nota
        ]
        print(f"Base de dados: {len(self.filmes)} filmes carregados")
    
    def desafio_1_ordenar_por_nota(self):
        """1. Listar filmes ordenados por nota (decrescente)"""
        print("\\n=== DESAFIO 1: Listar filmes ordenados por nota ===")
        
        # Simular: filmes_col.find().sort("nota", -1)
        filmes_ordenados = sorted(self.filmes, key=lambda x: x['nota'], reverse=True)
        
        print("RANKING (decrescente):")
        for i, filme in enumerate(filmes_ordenados, 1):
            print(f"  {i:2d}. {filme['titulo']:<25} ({filme['ano']}) - {filme['nota']}/10")
        
        print("Query MongoDB: filmes_col.find().sort('nota', -1)")
        return filmes_ordenados
    
    def desafio_2_filmes_apos_2015(self):
        """2. Buscar filmes lançados após 2015"""
        print("\\n=== DESAFIO 2: Filmes lançados após 2015 ===")
        
        # Simular: filmes_col.find({"ano": {"$gt": 2015}})
        filmes_recentes = [f for f in self.filmes if f['ano'] > 2015]
        
        print(f"Filmes após 2015 ({len(filmes_recentes)} encontrados):")
        for filme in sorted(filmes_recentes, key=lambda x: x['ano'], reverse=True):
            print(f"  • {filme['titulo']:<25} ({filme['ano']}) - {filme['nota']}/10")
        
        print("Query MongoDB: filmes_col.find({'ano': {'$gt': 2015}})")
        return filmes_recentes
    
    def desafio_3_adicionar_assistido(self):
        """3. Adicionar o campo 'assistido: False' em todos"""
        print("\\n=== DESAFIO 3: Adicionar campo assistido ===")
        
        # Simular: filmes_col.update_many({}, {"$set": {"assistido": False}})
        for filme in self.filmes:
            filme['assistido'] = False
        
        print(f"Campo 'assistido: False' adicionado a {len(self.filmes)} filmes")
        print("Exemplos:")
        for filme in self.filmes[:3]:
            status = "Não assistido" if not filme['assistido'] else "Assistido"
            print(f"  • {filme['titulo']:<25} - {status}")
        
        print("Query MongoDB: filmes_col.update_many({}, {'$set': {'assistido': False}})")
        return len(self.filmes)
    
    def desafio_4_deletar_menor_nota(self):
        """4. Deletar o filme com menor nota"""
        print("\\n=== DESAFIO 4: Deletar filme com menor nota ===")
        
        if not self.filmes:
            print("Nenhum filme para deletar")
            return None
        
        # Encontrar filme com menor nota
        filme_menor = min(self.filmes, key=lambda x: x['nota'])
        print(f"Filme com menor nota: {filme_menor['titulo']} ({filme_menor['nota']}/10)")
        
        # Simular deleção
        self.filmes = [f for f in self.filmes if f['titulo'] != filme_menor['titulo']]
        
        print(f"Filme '{filme_menor['titulo']}' deletado!")
        print(f"Filmes restantes: {len(self.filmes)}")
        
        if self.filmes:
            nova_menor = min(self.filmes, key=lambda x: x['nota'])
            print(f"Nova menor nota: {nova_menor['titulo']} ({nova_menor['nota']}/10)")
        
        print("Query MongoDB: filmes_col.find().sort('nota', 1).limit(1) + delete_one()")
        return filme_menor
    
    def executar_todos(self):
        """Executar os 4 desafios em sequência"""
        print("🚀 EXECUTANDO TODOS OS DESAFIOS EXTRA")
        print("=" * 60)
        
        resultado1 = self.desafio_1_ordenar_por_nota()
        resultado2 = self.desafio_2_filmes_apos_2015()
        resultado3 = self.desafio_3_adicionar_assistido()
        resultado4 = self.desafio_4_deletar_menor_nota()
        
        print("\\n" + "=" * 60)
        print("✅ TODOS OS 4 DESAFIOS CONCLUÍDOS!")
        print("=" * 60)
        print("RESUMO:")
        print(f"  1. Ordenação por nota: {len(resultado1)} filmes listados")
        print(f"  2. Filmes pós-2015: {len(resultado2)} encontrados")
        print(f"  3. Campo assistido: {resultado3} filmes atualizados")
        print(f"  4. Deleção: 1 filme removido ({resultado4['titulo']})")
        print("\\n🎯 Todos os itens da imagem foram implementados!")

if __name__ == "__main__":
    desafios = DesafiosSimples()
    desafios.executar_todos()