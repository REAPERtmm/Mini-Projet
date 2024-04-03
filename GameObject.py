from GeoMath import *


class Camera:
    def __init__(self, game, position: Vector2, speed: float, target):
        self.game = game
        self.position = position
        self.size = SCREEN.get_height()
        self.target = target
        self.speed = speed

    def update(self):
        self.position = Lerp(self.position, self.target.transform.position - self.Dimention()/2 + self.target.transform.size/2, self.game.deltatime * self.speed)

    def Dimention(self) -> Vector2:
        return Vector2(self.size * SCREEN.get_width() / SCREEN.get_height(), self.size)


class GameObject:
    def __init__(self, game, x: float, y: float, w: float, h: float):
        self.game = game
        self.transform = Box(Vector2(x, y), Vector2(w, h))

    def update(self):
        pass

    def blit(self, screen: py.Surface):
        self.transform.blit(screen, self.game.camera)


class StaticObject(GameObject):
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)
        self.isStatic = True

    def update(self):
        super().update()


class PhysicalObject(GameObject):
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)
        self.isStatic = False
        self.velocity = Vector2(0, 0)
        self.isGrounded = False

    def update(self):
        super().update()

        #print(f"id : {id(self)}, x: {self.transform.position.x()}, y: {self.transform.position.x()}, velocity: {self.velocity}")

        self.transform.position += self.velocity
        self.isGrounded = False

        box_over = Box(self.transform.position + Vector2(1, -1), Vector2(self.transform.size.x() - 2, 1))
        box_under = Box(self.transform.position + Vector2(1, self.transform.size.y()), Vector2(self.transform.size.x() - 2, 1))

        box_left = Box(self.transform.position + Vector2(-1, 1), Vector2(1, self.transform.size.x() - 2))
        box_right = Box(self.transform.position + Vector2(self.transform.size.x(), 1), Vector2(1, self.transform.size.x() - 2))

        for elt in self.game.ground:
            if id(self) != id(elt) and self.transform.CollideRect(elt.transform):

                check_over = box_over.CollideRect(elt.transform)
                check_under = box_under.CollideRect(elt.transform)
                check_left = box_left.CollideRect(elt.transform)
                check_right = box_right.CollideRect(elt.transform)

                if check_under:
                    self.transform.position.y(elt.transform.position.y() - self.transform.size.y())
                    self.isGrounded = True
                    print("Somthing under")
                if check_over and not check_left and not check_right:
                    self.transform.position.y(elt.transform.position.y() + elt.transform.size.y())
                    print("Somthing over")

                if check_left and not check_under and not check_right:
                    self.transform.position.x(elt.transform.position.x() - self.transform.size.x())
                    print("Somthing left")
                if check_right and not check_under and not check_right:
                    self.transform.position.x(elt.transform.position.x() + elt.transform.size.x())
                    print("Somthing right")

        if not self.isGrounded:
            self.velocity -= Vector2(0, -GRAVITY) * self.game.deltatime
        else:
            self.velocity = Vector2(0, 0)


class Entity(PhysicalObject):
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)

    def update(self):
        super().update()
        """
        print("DEBUG PLAYER =======")

        print("position : ", self.transform.position)
        print("size : ", self.transform.size)
        print("Grounded = ", self.isGrounded)
        print("Velocity = ", self.velocity)
        print("Ground :")
        for elt in self.game.ground:
            print("position : ", elt.transform.position)
            print("size : ", elt.transform.size)
            print("Collide : ", self.transform.CollideRect(elt.transform))"""


class Player(Entity):
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)

    def update(self):
        super().update()

    def jump(self):
        self.velocity -= Vector2(0, 10)


if __name__ == '__main__':
    r1 = Box(Vector2(0, 0), Vector2(10, 10))
    r2 = Box(Vector2(11, 0), Vector2(10, 10))
    movement = Vector2(40, 40)

    print(r1.position)
    print(r2.position)

    mire = Line(r1.position + r1.size / 2, r2.position + r2.size / 2)
    print(mire.start(), " to ", mire.end())

    print("hit on r2 :", r2.CollideLine(mire))
    print("hit on r1 :", r1.CollideLine(mire))
