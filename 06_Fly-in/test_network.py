"""
Testes da Network (etapa: grafo / validação do mapa).

A primeira parte testa Network isoladamente, montando zonas e conexões "na
mão" (sem passar pelo parser). A última parte é um teste de integração:
carrega o mapa de exemplo exatamente como está no subject (capítulo VI) e
confere o resultado final.

Rode com:  pytest -v test_network.py
"""
# flake8: noqa
from __future__ import annotations

from pathlib import Path

import pytest

from network import (
    Connection,
    DisconnectedNetworkError,
    MapSyntaxError,
    Network,
    Zone,
)


# ---------------------------------------------------------------------------
# add_zone / get_zone
# ---------------------------------------------------------------------------

def test_add_zone_can_be_retrieved_back() -> None:
    net = Network()
    zone = Zone("start")
    net.add_zone(zone)
    assert net.get_zone("start") is zone
    assert zone in net.zones


def test_duplicated_zone_name_is_rejected() -> None:
    net = Network()
    net.add_zone(Zone("start"))
    with pytest.raises(MapSyntaxError):
        net.add_zone(Zone("start"))


def test_get_zone_that_does_not_exist_raises_keyerror() -> None:
    net = Network()
    with pytest.raises(KeyError):
        net.get_zone("fantasma")


# ---------------------------------------------------------------------------
# add_connection
# ---------------------------------------------------------------------------

def test_add_connection_between_existing_zones() -> None:
    net = Network()
    net.add_zone(Zone("a"))
    net.add_zone(Zone("b"))
    net.add_connection(Connection(Zone("a"), Zone("b")))
    assert len(net.connections) == 1


def test_connection_to_unknown_zone_is_rejected() -> None:
    net = Network()
    net.add_zone(Zone("a"))
    with pytest.raises(MapSyntaxError):
        net.add_connection(Connection(Zone("a"), Zone("fantasma")))


def test_duplicated_connection_same_order_is_rejected() -> None:
    net = Network()
    net.add_zone(Zone("a"))
    net.add_zone(Zone("b"))
    net.add_connection(Connection(Zone("a"), Zone("b")))
    with pytest.raises(MapSyntaxError):
        net.add_connection(Connection(Zone("a"), Zone("b")))


def test_duplicated_connection_reversed_order_is_rejected() -> None:
    # o subject é explícito: "a-b and b-a are considered duplicates"
    net = Network()
    net.add_zone(Zone("a"))
    net.add_zone(Zone("b"))
    net.add_connection(Connection(Zone("a"), Zone("b")))
    with pytest.raises(MapSyntaxError):
        net.add_connection(Connection(Zone("b"), Zone("a")))


# ---------------------------------------------------------------------------
# neighbors()
# ---------------------------------------------------------------------------

def test_neighbors_returns_the_real_registered_zone() -> None:
    # neighbors() precisa devolver a MESMA zona que está cadastrada na rede
    # (com os atributos reais dela), e não um objeto novo e vazio criado só
    # para guardar o nome durante a leitura da conexão.
    net = Network()
    a = Zone("a")
    b = Zone("b")
    b.zone_type = "restricted"
    net.add_zone(a)
    net.add_zone(b)
    net.add_connection(Connection(Zone("a"), Zone("b")))

    neighbors_of_a = net.neighbors(a)

    assert len(neighbors_of_a) == 1
    assert neighbors_of_a[0] is b
    assert neighbors_of_a[0].zone_type == "restricted"


def test_neighbors_works_in_both_directions() -> None:
    net = Network()
    a, b = Zone("a"), Zone("b")
    net.add_zone(a)
    net.add_zone(b)
    net.add_connection(Connection(Zone("a"), Zone("b")))

    assert [z.name for z in net.neighbors(a)] == ["b"]
    assert [z.name for z in net.neighbors(b)] == ["a"]


# ---------------------------------------------------------------------------
# is_connected / validate
# ---------------------------------------------------------------------------

def test_is_connected_true_for_a_simple_path() -> None:
    net = Network()
    start, middle, end = Zone("start"), Zone("middle"), Zone("end")
    start.zone_type = "start_hub"
    end.zone_type = "end_hub"
    for z in (start, middle, end):
        net.add_zone(z)
    net.add_connection(Connection(Zone("start"), Zone("middle")))
    net.add_connection(Connection(Zone("middle"), Zone("end")))

    net.validate()  # não deve levantar nada


def test_disconnected_graph_is_detected() -> None:
    net = Network()
    start, end, isolated = Zone("start"), Zone("end"), Zone("isolated")
    start.zone_type = "start_hub"
    end.zone_type = "end_hub"
    for z in (start, end, isolated):
        net.add_zone(z)
    # start e isolated se conectam, mas end fica de fora
    net.add_connection(Connection(Zone("start"), Zone("isolated")))

    with pytest.raises(DisconnectedNetworkError):
        net.validate()


# ---------------------------------------------------------------------------
# Integração: mapa de exemplo do subject (capítulo VI)
# ---------------------------------------------------------------------------

SUBJECT_EXAMPLE_MAP = """\
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
"""


def write_map(tmp_path: Path, content: str) -> str:
    map_file = tmp_path / "map.txt"
    map_file.write_text(content)
    return str(map_file)


def test_subject_example_map_loads_with_the_right_zone_count(tmp_path: Path) -> None:
    path = write_map(tmp_path, SUBJECT_EXAMPLE_MAP)
    net = Network()
    net.load(path)

    assert len(net.zones) == 7
    assert len(net.connections) == 6


def test_subject_example_map_zone_types_are_correct(tmp_path: Path) -> None:
    path = write_map(tmp_path, SUBJECT_EXAMPLE_MAP)
    net = Network()
    net.load(path)

    assert net.get_zone("roof1").zone_type == "restricted"
    assert net.get_zone("obstacleX").zone_type == "blocked"
    assert net.get_zone("corridorA").zone_type == "priority"
    assert net.get_zone("corridorA").max_drones == 2


def test_subject_example_map_is_fully_connected(tmp_path: Path) -> None:
    path = write_map(tmp_path, SUBJECT_EXAMPLE_MAP)
    net = Network()
    net.load(path)

    net.validate()  # start ("hub") alcança end ("goal") — não deve levantar
