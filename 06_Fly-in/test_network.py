import unittest

# Assumindo que seu arquivo original se chame network.py
# Descomente a linha abaixo quando for rodar de verdade:
from network import Network, Zone, Connection, MapSyntaxError, DisconnectedNetworkError, MapParser

class TestZoneAndConnection(unittest.TestCase):
    def test_zone_creation(self):
        """Garante que a zona inicializa e guarda o nome corretamente."""
        zone = Zone("start_hub")
        self.assertEqual(zone.name, "start_hub")
        
    def test_connection_creation(self):
        """Garante que a conexão liga as referências de duas instâncias de Zone."""
        z1 = Zone("A")
        z2 = Zone("B")
        conn = Connection(z1, z2)
        self.assertEqual(conn.zone_a.name, "A")
        self.assertEqual(conn.zone_b.name, "B")

class TestNetwork(unittest.TestCase):
    def setUp(self):
        """Roda antes de cada teste para criar um tabuleiro limpo e isolado."""
        self.net = Network()

    def test_add_and_get_zone(self):
        """Testa se uma zona adicionada ao dicionário pode ser recuperada."""
        z = Zone("roof1")
        self.net.add_zone(z)
        
        fetched_zone = self.net.get_zone("roof1")
        self.assertEqual(fetched_zone.name, "roof1")

    def test_get_nonexistent_zone(self):
        """Garante que buscar uma zona que não existe gera um erro claro, e não um crash silencioso."""
        with self.assertRaises(KeyError): # Substitua por uma NetworkError customizada se preferir
            self.net.get_zone("fantasma")

    def test_neighbors_mapping(self):
        """Verifica se a construção da lista de adjacência (vizinhos) funciona."""
        z1 = Zone("A")
        z2 = Zone("B")
        self.net.add_zone(z1)
        self.net.add_zone(z2)
        
        conn = Connection(z1, z2)
        self.net.add_connection(conn)
        
        # O subject exige que as conexões sejam bidirecionais
        neighbors_of_a = self.net.neighbors(z1)
        self.assertIn(z2, neighbors_of_a)

    def test_disconnected_network_raises_error(self):
        """Garante que a rede detecta quando não há caminho possível entre o início e o fim."""
        start = Zone("start")
        isolated = Zone("island")
        end = Zone("goal")
        
        self.net.add_zone(start)
        self.net.add_zone(isolated)
        self.net.add_zone(end)
        
        # Conecta o start apenas à zona isolada. O 'goal' fica inalcançável.
        conn = Connection(start, isolated)
        self.net.add_connection(conn)
        
        # O método validate() (ou is_connected()) deve varrer o grafo e perceber a falha
        with self.assertRaises(DisconnectedNetworkError):
            self.net.validate()

class TestMapParser(unittest.TestCase):
    def test_invalid_syntax_raises_error(self):
        """Garante que o parser interrompe a execução ao ler regras inválidas."""
        parser = MapParser("dummy_path")
        
        # Simulando uma zona com traço no nome (o subject proíbe traços em nomes de zonas)
        bad_line = "hub: roof-1 3 4"
        
        with self.assertRaises(MapSyntaxError):
            parser._parse_line(bad_line, line_number=1)

if __name__ == '__main__':
    unittest.main()