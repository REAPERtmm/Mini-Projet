import Events
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
        self.color = (255, 255, 255)
        self.transform = Box(Vector2(x, y), Vector2(w, h))

    def update(self):
        pass

    def blit(self, screen: py.Surface):
        self.transform.blit(screen, self.game.camera, self.color)


class StaticObject(GameObject):
    def __init__(self, game, x: float, y: float, w: float, h: float, name: str="StaticObject"):
        super().__init__(game, x, y, w, h)
        self.name = name
        self.color = (100, 100, 100)
        self.isStatic = True

    def __str__(self):
        chaine = ""
        chaine += f"----{self.name}----\n"
        chaine += f"position = {self.transform.position}, size = {self.transform.size}"
        return chaine

    def update(self):
        super().update()


class PhysicalObject(GameObject):
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)
        self.isStatic = False
        self.velocity = Vector2(0, 0)
        self.isGrounded = False
        self.isGrabbingFloor = False
        self.isGrabbingLeft = False
        self.isGrabbingRight = False

        width = self.transform.size.x() / 3
        height = self.transform.size.y() / 3
        self.box_over = Box(self.transform.position + Vector2(width / 2, 0), Vector2(2 * width, 1))
        self.box_under = Box(self.transform.position + Vector2(width / 2, self.transform.size.y()), Vector2(2 * width, 1))
        self.box_left = Box(self.transform.position + Vector2(0, height / 2), Vector2(1, height * 2))
        self.box_right = Box(self.transform.position + Vector2(self.transform.size.x(), height / 2), Vector2(1, height * 2))

    def update(self):
        super().update()

        self.transform.position += self.velocity
        self.isGrounded = False
        self.isGrabbingFloor = False
        self.isGrabbingLeft = False
        self.isGrabbingRight = False

        width = self.transform.size.x() / 3
        height = self.transform.size.y() / 3

        self.box_over = Box(self.transform.position + Vector2(width / 2, -5), Vector2(2 * width, 5))
        self.box_under = Box(self.transform.position + Vector2(width / 2, self.transform.size.y()), Vector2(2 * width, 5))
        self.box_left = Box(self.transform.position + Vector2(-5, height / 2), Vector2(5, height * 2))
        self.box_right = Box(self.transform.position + Vector2(self.transform.size.x(), height / 2), Vector2(5, height * 2))

        for elt in self.game.ground:
            if id(self) != id(elt) and self.transform.CollideRect(elt.transform):
                if type(elt) is ReactiveObject and elt.triggerOnColision:
                    elt.Trigger()

                check_over = self.box_over.CollideRect(elt.transform)
                check_under = self.box_under.CollideRect(elt.transform)
                check_left = self.box_left.CollideRect(elt.transform)
                check_right = self.box_right.CollideRect(elt.transform)

                Box(self.transform.position + Vector2(1, -1),
                    self.transform.position + Vector2(self.transform.size.x() + 1, -1))
                if check_under and not check_left and not check_right:
                    self.transform.position.y(elt.transform.position.y() - self.transform.size.y())
                    self.isGrounded = True
                if check_over and not check_left and not check_right:
                    self.transform.position.y(elt.transform.position.y() + elt.transform.size.y())
                    self.isGrabbingFloor = True
                if check_right:
                    self.transform.position.x(elt.transform.position.x() - self.transform.size.x())
                    self.isGrabbingRight = True
                if check_left:
                    self.transform.position.x(elt.transform.position.x() + elt.transform.size.x())
                    self.isGrabbingLeft = True

        if not self.isGrounded:
            self.velocity -= Vector2(0, -GRAVITY) * self.game.deltatime
        else:
            self.velocity = Vector2(0, 0)

    def blit(self, screen: py.Surface):
        super().blit(screen)
        self.box_over.blit(screen, self.game.camera, (0, 255, 0))
        self.box_under.blit(screen, self.game.camera, (0, 255, 0))
        self.box_left.blit(screen, self.game.camera, (0, 0, 255))
        self.box_right.blit(screen, self.game.camera, (0, 0, 255))


class ReactiveObject(StaticObject):
    def __init__(self, game, x: float, y: float, w: float, h: float, triggerOnColision=True, *events: Events.Event):
        super().__init__(game, x, y, w, h, "Reactive Object")
        self.triggerOnColision = triggerOnColision
        self._CallBack = list(events)
        self._OnetimeCallBack = []

    def addCallBack(self, callback):
        self._CallBack.append(callback)

    def addOneTimeCallBack(self, callback):
        self._OnetimeCallBack.append(callback)

    def Trigger(self):
        for elt in self._CallBack:
            elt.trigger()
        for i in range(0, len(self._OnetimeCallBack), -1):
            self._OnetimeCallBack[i].trigger()
            self._OnetimeCallBack.pop()


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
        self.CanJump = True

    def update(self):
        super().update()
        if self.isGrounded:
            self.CanJump = True

    def jump(self):
        if self.CanJump:
            self.velocity -= Vector2(0, 10)
            self.CanJump = False


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
