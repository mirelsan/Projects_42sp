import os
import glob
from network import Network, MapParser, NetworkError

def run_batch_tests():
    # Busca todos os arquivos .txt no diretório atual
    map_files = sorted(glob.glob("*.txt"))
    
    if not map_files:
        print("Nenhum arquivo .txt encontrado na pasta.")
        return

    print(f"Iniciando testes em lote para {len(map_files)} mapas...\n")
    print("-" * 60)

    for file_path in map_files:
        print(f"Testando mapa: {file_path}")
        
        try:
            # Instancia o tabuleiro zerado para cada mapa
            parser = MapParser(file_path)
            rede = Network(parser)
            rede.load(file_path)
            
            # Validação do Pathfinding inicial (BFS)
            if rede.is_connected():
                status = "🟢 SUCESSO (Caminho Encontrado)"
            else:
                status = "🔴 FALHA (Labirinto sem saída)"
                
            print(f"Status: {status}")
            print(f"Drones: {parser.nb_drones} | Zonas: {len(rede.zones)} | Conexões: {len(rede.connections)}")
            
        except NetworkError as e:
            print(f"🟡 ERRO DE SINTAXE CAPTURADO: {e}")
        except Exception as e:
            print(f"💥 ERRO CRÍTICO (Crash): {e}")
            
        print("-" * 60)

if __name__ == "__main__":
    run_batch_tests()