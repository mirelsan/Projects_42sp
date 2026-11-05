"""
Testes do MapParser (etapa: parser).

Cada teste escreve um "mapa" minúsculo num arquivo temporário (tmp_path é um
recurso pronto do pytest: cria uma pasta temporária só para o teste) e chama
MapParser(path).parse() em cima dele, exatamente como o programa real faria.

Rode com:  pytest -v test_parser.py
"""
from __future__ import annotations

# flake8: noqa
from pathlib import Path

import pytest

from network import MapParser, MapSyntaxError


def write_map(tmp_path: Path, content: str) -> str:
    """Escreve `content` num arquivo temporário e devolve o caminho dele."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(content)
    return str(map_file)


# ---------------------------------------------------------------------------
# nb_drones, comentários e linhas vazias
# ---------------------------------------------------------------------------

def test_nb_drones_is_stored_on_the_parser(tmp_path: Path) -> None:
    path = write_map(tmp_path, "nb_drones: 5\n")
    parser = MapParser(path)
    parser.parse()
    assert parser.nb_drones == 5


def test_comments_and_blank_lines_are_ignored(tmp_path: Path) -> None:
    content = (
        "# isso é um comentário, deve ser ignorado\n"
        "\n"
        "nb_drones: 2\n"
        "\n"
        "# outro comentário\n"
        "hub: meio 1 1\n"
    )
    path = write_map(tmp_path, content)
    zones, connections = MapParser(path).parse()
    assert len(zones) == 1
    assert zones[0].name == "meio"


# ---------------------------------------------------------------------------
# Zonas básicas
# ---------------------------------------------------------------------------

def test_basic_zone_is_parsed_with_default_type(tmp_path: Path) -> None:
    path = write_map(tmp_path, "hub: roof1 3 4\n")
    zones, _ = MapParser(path).parse()
    assert len(zones) == 1
    assert zones[0].name == "roof1"
    assert zones[0].zone_type == "normal"  # default quando não há metadata


def test_start_hub_and_end_hub_get_their_own_type(tmp_path: Path) -> None:
    content = "start_hub: hub 0 0\nend_hub: goal 10 10\n"
    path = write_map(tmp_path, content)
    zones, _ = MapParser(path).parse()
    by_name = {z.name: z for z in zones}
    assert by_name["hub"].zone_type == "start_hub"
    assert by_name["goal"].zone_type == "end_hub"


def test_zone_name_with_dash_is_rejected(tmp_path: Path) -> None:
    path = write_map(tmp_path, "hub: roof-1 3 4\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


def test_zone_line_with_missing_field_is_rejected(tmp_path: Path) -> None:
    # falta a coordenada y
    path = write_map(tmp_path, "hub: roof1 3\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


def test_unknown_line_prefix_is_rejected(tmp_path: Path) -> None:
    path = write_map(tmp_path, "foo: bar 1 1\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


# ---------------------------------------------------------------------------
# Metadata das zonas: [zone=... color=... max_drones=...]
# ---------------------------------------------------------------------------

def test_zone_metadata_sets_type_and_color(tmp_path: Path) -> None:
    path = write_map(tmp_path, "hub: roof1 3 4 [zone=restricted color=red]\n")
    zones, _ = MapParser(path).parse()
    zone = zones[0]
    assert zone.zone_type == "restricted"
    assert zone.color == "red"


def test_zone_metadata_sets_max_drones(tmp_path: Path) -> None:
    path = write_map(tmp_path, "hub: corridorA 4 3 [zone=priority max_drones=2]\n")
    zones, _ = MapParser(path).parse()
    assert zones[0].max_drones == 2


def test_invalid_zone_type_is_rejected(tmp_path: Path) -> None:
    # o subject diz: "Zone types must be one of: normal, blocked, restricted,
    # priority. Any invalid type must raise a parsing error."
    path = write_map(tmp_path, "hub: roof1 3 4 [zone=lava]\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


def test_non_integer_max_drones_is_rejected(tmp_path: Path) -> None:
    path = write_map(tmp_path, "hub: corridorA 4 3 [max_drones=abc]\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


# ---------------------------------------------------------------------------
# Coordenadas
# ---------------------------------------------------------------------------

def test_non_integer_coordinates_are_rejected(tmp_path: Path) -> None:
    # "The zones coordinates will always be integers" — uma coordenada que
    # não é inteiro deve dar erro de parsing, não passar batido.
    path = write_map(tmp_path, "hub: roof1 three four\n")
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()


# ---------------------------------------------------------------------------
# Conexões
# ---------------------------------------------------------------------------

def test_basic_connection_is_parsed(tmp_path: Path) -> None:
    content = "hub: a 0 0\nhub: b 1 1\nconnection: a-b\n"
    path = write_map(tmp_path, content)
    _, connections = MapParser(path).parse()
    assert len(connections) == 1
    names = {connections[0].zone_a.name, connections[0].zone_b.name}
    assert names == {"a", "b"}


def test_connection_metadata_sets_max_link_capacity(tmp_path: Path) -> None:
    content = "hub: a 0 0\nhub: b 1 1\nconnection: a-b [max_link_capacity=3]\n"
    path = write_map(tmp_path, content)
    _, connections = MapParser(path).parse()
    assert connections[0].max_link_capacity == 3


def test_malformed_connection_line_is_rejected(tmp_path: Path) -> None:
    content = "hub: a 0 0\nhub: b 1 1\nconnection: a b\n"  # falta o '-'
    path = write_map(tmp_path, content)
    with pytest.raises(MapSyntaxError):
        MapParser(path).parse()
