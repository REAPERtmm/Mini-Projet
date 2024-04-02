from math import sqrt, cos, sin
from Settings import *


class Vector2:
    def __init__(self, x: float, y: float):
        """
        Vecteur à deux dimention
        :param x: Coordonné X
        :param y: Coordonné y
        """
        self._x: float = x
        self._y: float = y
        self.magnitude: float = sqrt(self._x**2 + self._y**2)

    def _UpdateData(self):
        self.magnitude = sqrt(self._x ** 2 + self._y ** 2)

    def moveX(self, dx: float) -> None:
        self._x += dx
        self._UpdateData()

    def moveY(self, dy: float) -> None:
        self._y += dy
        self._UpdateData()

    def x(self, i_new: float = None) -> float:
        """
        Get / Set de X
        :param i_new: nouvelle valeur de X si renseigné
        :return: la valeur de x (après modification)
        """
        if i_new is not None:
            self._x = i_new
            self._UpdateData()  # Calcul de la longeur du vecteur
        return self._x

    def y(self, i_new: float = None) -> float:
        """
        Get / Set de Y
        :param i_new: nouvelle valeur de Y si renseigné
        :return: la valeur de Y (après modification)
        """
        if i_new is not None:
            self._y = i_new
            self._UpdateData()  # Calcul de la longeur du Vecteur
        return self._y

    def normalize(self):
        if self.magnitude == 0:
            print("vector zero normalize")
            return Vector2(0, 0)
        return Vector2(self._x, self._y) / self.magnitude

    def __add__(self, other):
        return Vector2(self._x + other.x(), self._y + other.y())

    def __sub__(self, other):
        return Vector2(self._x - other._x, self._y - other.y())

    def __mul__(self, scale: float):
        return Vector2(self._x * scale, self._y * scale)

    def __truediv__(self, scale: float):
        assert scale != 0, "Scale can't be equal to zero"
        return Vector2(self._x / scale, self._y / scale)

    def __str__(self):
        return f"(x: {self._x}, y: {self._y})"

    __radd__ = __add__
    __imul__ = __mul__


class Line:
    def __init__(self, start: Vector2, end: Vector2):
        self._Start: Vector2 = start
        self._End: Vector2 = end
        self.Direction = (self._End - self._Start).normalize()
    
    def end(self):
        return self._End
    
    def start(self):
        return self._Start
    
    def SetStart(self, start: Vector2):
        self._Start = start
        self.Direction = (self._End - self._Start).normalize()

    def SetEnd(self, end: Vector2):
        self._End = end
        self.Direction = (self._End - self._Start).normalize()

    def RayCastOnRect(self, rect) -> float:
        side = [
            Line(rect.position, rect.size + Vector2(0, rect.size.y())).CollideLine(self),
            Line(rect.position, rect.size + Vector2(rect.size.x(), 0)).CollideLine(self),
            Line(rect.position + rect.size, rect.size - Vector2(0, rect.size.y())).CollideLine(self),
            Line(rect.position + rect.size, rect.size - Vector2(rect.size.x(), 0)).CollideLine(self)
        ]

        minimum = None
        magnitude = 0
        for elt in side:
            if minimum is None:
                minimum = elt
                magnitude = (elt - self._Start).magnitude
            else:
                if (elt - self._Start).magnitude < magnitude:
                    minimum = elt
                    magnitude = (elt - self._Start).magnitude
        return magnitude

    def CollideLine(self, line) -> Vector2:
        """
        check la collision entre deux segement
        :param line: ligne par rapport à laquelle on check
        :return: le point de collision sinon None
        """

        uA = ((
                     (line.end().x() - line.start().x()) * (self.start().y() - line.start().y()) -
                     (line.end().y() - line.start().y()) * (self.start().x() - line.start().x())
             ) /
              (
                      (line.end().y() - line.start().y()) * (self.end().x() - self.start().x()) -
                      (line.end().x() - line.start().x()) * (self.end().y() - self.start().y())
              ));

        
        uB = ((
                      (self.end().x() - self.start().x()) * (self.start().y() - line.start().y()) -
                      (self.end().y() - self.start().y()) * (self.start().x() - line.start().x())
              ) /
              (
                      (line.end().y() - line.start().y()) * (self.end().x() - self.start().x()) -
                      (line.end().x() - line.start().x()) * (self.end().y() - self.start().y())
              ));

        if 0 <= uA <= 1 and 0 <= uB <= 1:
            return uA * self.Direction + self._Start
        return None


class Box:
    def __init__(self, position: Vector2, size: Vector2):
        self.position = position
        self.size = size

    def CollideRect(self, rect) -> bool:
        return (0 <= self.position.x() + self.size.x() - rect.position.x() and
                0 <= rect.position.x() + rect.size.x() - self.position.x() and
                0 <= self.position.y() + self.size.y() - rect.position.y() and
                0 <= rect.position.y() + rect.size.y() - self.position.y()
                )

    def CollideLine(self, line) -> Vector2:
        left = Line(self.position, self.size + Vector2(0, self.size.y())).CollideLine(line)
        top = Line(self.position, self.size + Vector2(self.size.x(), 0)).CollideLine(line)
        right = Line(self.position + self.size, self.size - Vector2(0, self.size.y())).CollideLine(line)
        down = Line(self.position + self.size, self.size - Vector2(self.size.x(), 0)).CollideLine(line)

        return left is not None or top is not None or right is not None or down is not None

    def CollidePoint(self, point: Vector2) -> bool:
        p = point - self.position
        return p.x() >= 0 or p.x() <= self.size.x() or p.y() >= 0 or p.y() <= self.size.y()

    def blit(self, screen, camera) -> None:
        py.draw.rect(
            screen,
            (255, 255, 255),
            (
                self.position.x() - camera.position.x(),
                self.position.y() - camera.position.y(),
                self.size.x(),
                self.size.y())
        )


def DotProduct(v1: Vector2, v2: Vector2) -> float:
    """
    :param v1: Vecteur 1
    :param v2: Vecteur 2
    :return: Produit Scalaire des Vecteurs 1 et 2
    """
    return v1.x() * v2.x() + v1.y() * v2.y()


def Rotation(vec: Vector2, angle: float) -> Vector2:
    """
    :param vec: Vecteur
    :param angle: Angle en radians
    :return: Le vecteur tourné de <angle> rad
    """
    return Vector2(vec.x() * cos(angle) - vec.y() * sin(angle), vec.x() * sin(angle) + vec.y() * cos(angle))


def Lerp(v1: Vector2, v2: Vector2, t: float) -> Vector2:
    return v1 * (1 - t) + v2 * t


if __name__ == '__main__':
    r1 = Box(Vector2(0, 0), Vector2(100, 100))
    r2 = Box(Vector2(-200, 400), Vector2(900, 50))
    print(r1.CollideRect(r2))
