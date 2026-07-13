
from dataclasses import dataclass, field
from datetime import date


class LibroNoEncontradoError(Exception):
    """Se lanza cuando se busca un ISBN que no existe en el catálogo."""
    pass


class SinEjemplaresDisponiblesError(Exception):
    """Se lanza cuando no hay copias disponibles para prestar."""
    pass


class PrestamoNoEncontradoError(Exception):
    """Se lanza cuando se intenta devolver un libro que el usuario no tiene prestado."""
    pass


@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    cantidad_total: int
    cantidad_disponible: int = field(default=None)

    def __post_init__(self):
        if self.cantidad_disponible is None:
            self.cantidad_disponible = self.cantidad_total


class Biblioteca:
    """Administra el catálogo de libros y los préstamos activos."""

    VALOR_MULTA_POR_DIA = 500  # pesos colombianos, por día de retraso

    def __init__(self):
        self.catalogo = {}          # isbn -> Libro
        self.prestamos_activos = {}  # (isbn, usuario) -> fecha_prestamo

    def registrar_libro(self, isbn, titulo, autor, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if isbn in self.catalogo:
            self.catalogo[isbn].cantidad_total += cantidad
            self.catalogo[isbn].cantidad_disponible += cantidad
        else:
            self.catalogo[isbn] = Libro(isbn, titulo, autor, cantidad)
        return self.catalogo[isbn]

    def buscar_libro(self, isbn):
        if isbn not in self.catalogo:
            raise LibroNoEncontradoError(f"El ISBN {isbn} no existe en el catálogo")
        return self.catalogo[isbn]

    def prestar_libro(self, isbn, usuario, fecha_prestamo=None):
        libro = self.buscar_libro(isbn)
        if libro.cantidad_disponible <= 0:
            raise SinEjemplaresDisponiblesError(
                f"No hay ejemplares disponibles de '{libro.titulo}'"
            )
        libro.cantidad_disponible -= 1
        self.prestamos_activos[(isbn, usuario)] = fecha_prestamo or date.today()
        return True

    def devolver_libro(self, isbn, usuario):
        clave = (isbn, usuario)
        if clave not in self.prestamos_activos:
            raise PrestamoNoEncontradoError(
                f"El usuario {usuario} no tiene prestado el libro {isbn}"
            )
        libro = self.buscar_libro(isbn)
        libro.cantidad_disponible += 1
        del self.prestamos_activos[clave]
        return True

    def calcular_multa(self, dias_retraso):
        if dias_retraso <= 0:
            return 0
        return dias_retraso * self.VALOR_MULTA_POR_DIA
