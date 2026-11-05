"""A small Dinic max-flow implementation used by the scheduler."""

from __future__ import annotations

from collections import deque
from typing import Optional

from .errors import SchedulingError


class FlowEdge:
    """One directed edge of the residual network."""

    __slots__ = ("to", "rev", "capacity", "original_capacity")

    def __init__(self, to: int, rev: int, capacity: int) -> None:
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.original_capacity = capacity

    @property
    def flow(self) -> int:
        """Return the amount of flow currently carried by this edge."""
        return self.original_capacity - self.capacity


class DinicNetwork:
    """Dinic's maximum-flow algorithm on an integer-capacity graph."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.graph: list[list[FlowEdge]] = [[] for _ in range(size)]
        self._level: list[int] = []
        self._iterator: list[int] = []

    def add_edge(
        self, source: int, target: int, capacity: int
    ) -> FlowEdge:
        """Add a directed edge and return its forward half."""
        forward = FlowEdge(
            target, len(self.graph[target]), capacity
        )
        backward = FlowEdge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(backward)
        return forward

    def max_flow(self, source: int, sink: int) -> int:
        """Return the value of a maximum source-to-sink flow."""
        total = 0
        while self._bfs(source, sink):
            self._iterator = [0] * self.size
            while True:
                pushed = self._dfs(source, sink, 10**18)
                if pushed == 0:
                    break
                total += pushed
        return total

    def _bfs(self, source: int, sink: int) -> bool:
        """Build the level graph of the residual network."""
        self._level = [-1] * self.size
        self._level[source] = 0
        queue: deque[int] = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge.capacity > 0 and self._level[edge.to] < 0:
                    self._level[edge.to] = self._level[node] + 1
                    queue.append(edge.to)
        return self._level[sink] >= 0

    def _dfs(self, node: int, sink: int, pushed: int) -> int:
        """Push flow along one augmenting path in the level graph."""
        if node == sink:
            return pushed
        while self._iterator[node] < len(self.graph[node]):
            edge = self.graph[node][self._iterator[node]]
            if (
                edge.capacity > 0
                and self._level[edge.to] == self._level[node] + 1
            ):
                delta = self._dfs(
                    edge.to, sink, min(pushed, edge.capacity)
                )
                if delta > 0:
                    edge.capacity -= delta
                    self.graph[edge.to][edge.rev].capacity += delta
                    return delta
            self._iterator[node] += 1
        return 0

    def extract_paths(
        self, source: int, sink: int, count: int
    ) -> list[list[FlowEdge]]:
        """Decompose the current flow into *count* source-sink paths."""
        paths: list[list[FlowEdge]] = []
        for _ in range(count):
            edges = self._find_path(source, sink, set())
            if edges is None:
                raise SchedulingError(
                    "internal error: could not decompose the flow"
                )
            for edge in edges:
                edge.capacity += 1
                reverse = self.graph[edge.to][edge.rev]
                reverse.capacity -= 1
            paths.append(edges)
        return paths

    def _find_path(
        self, node: int, sink: int, visited: set[int]
    ) -> Optional[list[FlowEdge]]:
        """Find a simple path that still carries positive flow."""
        if node == sink:
            return []
        visited.add(node)
        for edge in self.graph[node]:
            if edge.original_capacity <= 0 or edge.flow <= 0:
                continue
            if edge.to in visited:
                continue
            rest = self._find_path(edge.to, sink, visited)
            if rest is not None:
                return [edge] + rest
        return None
