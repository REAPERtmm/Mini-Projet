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
        self.transform.position += self.velocity

        self.isGrounded = False
        for elt in self.game.ground:
            if self.transform.CollideRect(elt.transform):
                self.isGrounded = True
                break

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
