"""Ordenação painter's algorithm para sprites."""

from __future__ import annotations

from typing import Iterable, Protocol, TypeVar


class _HasPerp(Protocol):
    perp: float


T = TypeVar("T", bound=_HasPerp)


def sort_by_perp_desc(items: list[T]) -> list[T]:
    """Ordena in-place (mais longe primeiro) e devolve a mesma lista."""
    items.sort(key=lambda s: s.perp, reverse=True)
    return items


def sorted_by_perp_desc(items: Iterable[T]) -> list[T]:
    """Versão não-destrutiva. Útil quando a lista original precisa ser preservada."""
    return sorted(items, key=lambda s: s.perp, reverse=True)
