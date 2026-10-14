from __future__ import annotations


# ---------------------------------------------------------------------------
# Erros
# ---------------------------------------------------------------------------

class NetworkError(Exception):
    """Base de todos os erros da rede."""


class MapSyntaxError(NetworkError):
    """Sintaxe inválida no arquivo do mapa."""


class DisconnectedNetworkError(NetworkError):
    """Mapa com zonas inalcançáveis."""


# ---------------------------------------------------------------------------
# Nó (zona)
# ---------------------------------------------------------------------------

class Zone:
    """Representa um nó do grafo."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.zone_type: str = "normal"
        self.max_drones: int = 1
        self.color = ""

    def __repr__(self) -> str:
        return f"Zone({self.name}, {self.zone_type})"


# ---------------------------------------------------------------------------
# Aresta (conexão)
# ---------------------------------------------------------------------------

class Connection:
    """Representa uma aresta entre duas zonas."""

    def __init__(self, zone_a: Zone, zone_b: Zone) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b 
        self.max_link_capacity: int = 1
        # guardar as pontas da conexão (e atributos extras, se houver)

    def __repr__(self) -> str:
        return f"Connection({self.zone_a.name} <-> {self.zone_b.name})"


# ---------------------------------------------------------------------------
# Parser do mapa
# ---------------------------------------------------------------------------

class MapParser:
    """Lê o arquivo do mapa e valida a sintaxe."""

    def __init__(self, path: str) -> None:
        self.path = path

    def parse(self) -> tuple[list[Zone], list[Connection]]:
        """Retorna as zonas e conexões lidas do arquivo."""
        zones_read = []
        connections_read = []

        with open(self.path, 'r') as file:
            for n_line, line in enumerate(file, 1):
                self._parse_line(line, n_line)
                result = self._parse_line(line, n_line)

                if isinstance(result, Zone):
                    zones_read.append(result)
                elif isinstance(result, Connection):
                    connections_read.append(result)

        return zones_read, connections_read

    def _parse_line(self, line: str, line_number: int) -> None:
        """Interpreta uma única linha (levanta MapSyntaxError se inválida)."""
        line = line.strip()

        if not line or line.startswith('#'):
            return None

        if line.startswith("nb_drones:"):
            quantity = int(line.split(":")[1].strip())
            self.nb_drones = quantity
            print(f"Total configured drones: {quantity}")
            return None

        parts = line.split('[')
        datas_base = parts[0].strip()
        blocks = datas_base.split()
        prefix = blocks[0].replace(":", "")

        metadatas = {}
        if len(parts) > 1:
            raw_meta = parts[1].replace(']', '').strip()
            tags = raw_meta.split()
            for tag in tags:
                if '-' in tag:
                    key, value = tag.split('-')
                    metadatas[key] = value

        if prefix in ["hub", "start_hub", "end_hub"]:
            if len(blocks) != 4:
                raise MapSyntaxError(f"Error: line {line_number}: Zone format invalid.")

            name = blocks[1]
            if '-' in name:
                raise MapSyntaxError(f"Error: line {line_number}: Zone names cannot contain dashes ({name}).")

            new_zone = Zone(name)

            if prefix == "start_hub":
                new_zone.zone_type = "start_hub"
            elif prefix == "end_hub":
                new_zone.zone_type = "end_hub"
            elif "zone" in metadatas:
                new_zone.zone_type = metadatas["zone"]

            if "max_drones" in metadatas:
                new_zone.max_drones = int(metadatas["max_drones"])
            if "color" in metadatas:
                new_zone.color = metadatas["color"]

            return new_zone

        elif prefix == "connection":
            if len(blocks) != 2:
                raise MapSyntaxError(f"Error: line {line_number}: connection format invalid.")

            zones_connected = blocks[1].split('-')
            zone_a_fake = Zone(zones_connected[0])
            zone_b_fake = Zone(zones_connected[1])
            new_connection = Connection(zone_a_fake, zone_b_fake)

            if "max_link_capacity" in metadatas:
                new_connection.max_link_capacity = int(metadatas["max_link_capacity"])

            return new_connection

        else:
            raise MapSyntaxError(f"Error: line {line_number}: Unknown prefix '{prefix}.")
# ---------------------------------------------------------------------------
# O Tabuleiro
# ---------------------------------------------------------------------------

class Network:
    """Armazena zonas e conexões e garante a consistência do mapa."""

    def __init__(self, parser: MapParser | None = None) -> None:
        # estrutura interna das zonas e conexões
        self._zones: dict[str, Zone] = {}
        self._adj_list: dict[str, list[Connection]] = {}
        self._parser = parser

    # --- acesso (somente leitura) ---

    @property
    def zones(self) -> list[Zone]:
        return list(self._zones.values())

    @property
    def connections(self) -> list[Connection]:
        connections_list = []

        unique_connections = set()
        for sublist in self._adj_list.values():
            for c in sublist:
                unique_connections.add(c)
        return list(unique_connections)

    # --- carregamento ---

    def load(self, path: str) -> None:
        """Usa o parser para popular a rede."""
        if not self._parser:
            self._parser = MapParser(path)

        zones, connections = self._parser.parse()

        for z in zones:
            self.add_zone(z)

        for c in connections:
            self.add_connection(c)

    # --- construção ---

    def add_zone(self, zone: Zone) -> None:
        #tratar zona duplicada
        if zone.name in self._zones:
            raise MapSyntaxError(f"Error: duplicated zone detected ({zone.name}).")

        self._zones[zone.name] = zone
        self._adj_list[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        #tratar zona inexistente / conexão duplicada
        name_a = connection.zone_a.name
        name_b = connection.zone_b.name

        if name_a not in self._zones or name_b not in self._zones:
            raise MapSyntaxError(f"Error: Trying to connect inexisted zones")

        for existing_conn in self._adj_list[name_a]:
            if existing_conn.zone_a.name == name_b or existing_conn.zone_b.name == name_b:
                raise MapSyntaxError(f"Error: duplicated connection between {name_a} and {name_b}.")

        self._adj_list[name_a].append(connection)
        self._adj_list[name_b].append(connection)
    # --- consulta ---

    def get_zone(self, name: str) -> Zone:
        # o que acontece se não existir?
        if name not in self._zones:
            raise KeyError(f"Error: trying to access a inexisted zone ({name}).")
        return self._zones[name]

    def neighbors(self, zone: Zone) -> list[Zone]:
        neighbors_list = []
        for c in self._adj_list[zone.name]:
            if c.zone_a.name == zone.name:
                neighbors_list.append(c.zone_b)
            else:
                neighbors_list.append(c.zone_a)
        return neighbors_list
        
    # --- validação ---

    def validate(self) -> None:
        """Roda todas as validações da rede."""
        if not self.is_connected():
            raise DisconnectedNetworkError("Error: the map is broken, there is no route to end_hub.")

    def is_connected(self) -> bool:
        start_zone = None
        end_zone_name = None

        for zone in self.zones:
            # Usando getattr para ser defensivo caso você não tenha inicializado o zone_type
            z_type = getattr(zone, 'zone_type', 'normal') 
            if z_type == "start_hub":
                start_zone = zone
            elif z_type == "end_hub":
                end_zone_name = zone.name

        # --- DEBUG 1: Descobrindo se o Start e o End existem ---
        print(f"  [DEBUG] START found: {start_zone.name if start_zone else 'NO'} | END found: {end_zone_name}")

        if not start_zone or not end_zone_name:
            return False

        visited = set()
        visited.add(start_zone.name)
        queue = [start_zone]

        while queue:
            current = queue.pop(0)
            # --- DEBUG 2: Verificando onde o drone virtual está pisando ---
            print(f"  [DEBUG] Visiting: {current.name}")

            if current.name == end_zone_name:
                print("  [DEBUG] -> Route connected with success!")
                return True

            vizinhos = self.neighbors(current)
            # --- DEBUG 3: Verificando se ele enxerga os caminhos ---
            print(f"  [DEBUG] -> Neighbors of {current.name}: {[v.name for v in vizinhos]}")
            
            for neighbor in vizinhos:
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append(neighbor)

        return False