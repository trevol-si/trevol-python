"""Paginación con iteradores (docs/api/43 §2.6.7): la API pagina por cursor (`starting_after`)."""

from __future__ import annotations

from typing import Any, Callable, Iterator, Optional


def paginar(pagina: Callable[[Optional[str]], Any]) -> Iterator[Any]:
    """Recorre todas las páginas de un listado, perezosamente.

    `pagina(cursor)` pide UNA página (`starting_after=cursor`; `None` la primera) y devuelve el sobre de lista. Sigue con `next_cursor`
    mientras `has_more`; si la página no lo trae, usa el `id` del último elemento (así lo arma la API). Se detiene si el cursor no avanza:
    una API que repitiera el mismo cursor no puede dejar el bucle girando para siempre.
    """
    cursor: Optional[str] = None
    while True:
        p = pagina(cursor)
        datos = list(getattr(p, "data", None) or [])
        yield from datos
        if not getattr(p, "has_more", False) or not datos:
            return
        siguiente = getattr(p, "next_cursor", None) or getattr(datos[-1], "id", None)
        if not siguiente or siguiente == cursor:
            return
        cursor = siguiente
