import time
from random import random, choice

import pygame.draw

from Animation import *
import Events
from GeoMath import *


def randfloat(a, b):
    return a + random() * (b - a)


class Camera:
    def __init__(self, game, position: Vector2, speed: float, target):
        self.game = game
        self.position = position
        self.size = SCREEN.get_height()
        self.target = target
        self.speed = speed

    def update(self):
        self.position = Lerp(self.position, self.target.transform.position - self.Dimention()/2 + self.target.transform.size/2 - Vector2(0, 50), self.game.deltatime * self.speed)

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
    def __init__(self, game, x: float, y: float, w: float, h: float, name: str = "StaticObject", image: py.Surface = None):
        """
        :param game: class of the game
        :param x: x coordinate
        :param y: y coordinate
        :param w: width
        :param h: height
        :param name: nom (optional)
        :param image: (optional) image to blit (override the width and height)
        """
        super().__init__(game, x, y, w, h)
        self.image = image
        if self.image is not None:
            self.transform.size = Vector2(self.image.get_width(), self.image.get_height())
        self.name = name
        self.color = (100, 100, 100)
        self.isStatic = True

    def get_decal(self, position: Vector2):
        c = StaticObject(self.game, self.transform.position.x() + position.x(), self.transform.position.y() + position.y(), self.transform.size.x(), self.transform.size.y())
        return c

    def __str__(self):
        chaine = ""
        chaine += f"----{self.name}----\n"
        chaine += f"position = {self.transform.position}, size = {self.transform.size}"
        return chaine

    def blit(self, screen: py.Surface):
        if self.image is not None:
            screen.blit(self.image, (self.transform.position - self.game.camera.position).tuple())
        else:
            super().blit(screen)

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
        height = self.transform.size.y() / 10

        self.box_over = Box(self.transform.position + Vector2(width / 2, -5), Vector2(2 * width, 5))
        self.box_under = Box(self.transform.position + Vector2(width / 2, self.transform.size.y()), Vector2(2 * width, 5))
        self.box_left = Box(self.transform.position + Vector2(-5, int(height * 2.5)), Vector2(5, height * 5))
        self.box_right = Box(self.transform.position + Vector2(self.transform.size.x(), int(height * 2.5)), Vector2(5, height * 5))

        for elt in self.game.ground + self.game.interactible:
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
                    if self.velocity.y() < 0:
                        self.velocity.y(0)

                if check_right:
                    self.transform.position.x(elt.transform.position.x() - self.transform.size.x())
                    self.isGrabbingRight = True
                if check_left:
                    self.transform.position.x(elt.transform.position.x() + elt.transform.size.x())
                    self.isGrabbingLeft = True

        if not self.isGrounded:
            self.velocity -= Vector2(0, -GRAVITY * 2.2) * self.game.deltatime
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


class Boss(Entity):
    def __init__(self, game, x: float, y: float, percent=.5):
        super().__init__(game, x, y, int(YACK_WIDTH * percent), int(YACK_HEIGHT * percent))
        self.spawn = Vector2(x, y)
        self.animator = Animator(
            idle=Animation(400_000_000, *load_all_images("Resources/Animation/Yack/idle/", (YACK_WIDTH, YACK_HEIGHT))),
            r_idle=Animation(400_000_000, *load_all_images("Resources/Animation/Yack/idle/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True)),
            charge=Animation(1_000_000_000, *load_all_images("Resources/Animation/Yack/charge/", (YACK_WIDTH, YACK_HEIGHT))),
            r_charge=Animation(1_000_000_000, *load_all_images("Resources/Animation/Yack/charge/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True)),
            precharge=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/precharge/", (YACK_WIDTH, YACK_HEIGHT)), StopAtEnd=True),
            r_precharge=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/precharge/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True), StopAtEnd=True),
            turn=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/turn/", (YACK_WIDTH, YACK_HEIGHT)), StopAtEnd=True),
            r_turn=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/turn/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True), StopAtEnd=True),
            death=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/death/", (YACK_WIDTH, YACK_HEIGHT)), StopAtEnd=True),
            r_death=Animation(800_000_000, *load_all_images("Resources/Animation/Yack/death/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True), StopAtEnd=True),
        )

        self.platform = []

        self.cloche = StaticObject(self.game, 0, 0, 0, 0, "Cloche", CLOCHE)
        self.halo = StaticObject(self.game, 0, 0, 0, 0, "Halo", HALO)

        self.offset = self.transform.size / 2 - Vector2(0, 10)
        self.is_Active = False
        self.cloche_enable = False
        self.phase = 0
        self.phase_duration = [
            5, 10
        ]
        self.map = None
        self.time_at_phase_start = time.time()
        self.attack_duration_range = {
            "Wait": [1, 2],
            "Pre-Charge": [-1],
            "Charge": [-1],
            "Projectile": [-1],
            "turn": [-1]
        }
        self.attack = [
            ["Wait", "Pre-Charge"],
            ["Wait", "Pre-Charge", "Projectile"]
        ]
        self.status = "Wait"
        self.attack_duration = 5
        self.time_start_attack = time.time()
        self.goleft = True
        self.left = Vector2(0, 0)
        self.right = Vector2(0, 0)
        self.speed = 1

    def get_physic(self, camera):
        return self.platform[self.phase] + self.map.get_physique_on_screen(camera)

    def next_attack(self, status=None, different=False):
        if status is None:
            if different:
                prec = self.status
                while prec == self.status:
                    self.status = choice(self.attack[self.phase])
            else:
                self.status = choice(self.attack[self.phase])
        else:
            self.status = status
        self.attack_duration = choice(self.attack_duration_range[self.status])
        self.time_start_attack = time.time()

    def EnterRoom(self):
        self.time_start_attack = time.time()
        self.time_at_phase_start = time.time()

    def Start(self, map):
        self.map = map
        self.platform.clear()
        self.left = self.map.offset + Vector2(TILETOTALSIZE + 3 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.right = self.map.offset + Vector2((self.map.width - 1) * TILETOTALSIZE - self.transform.size.x() - 3 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.goleft = True

        self.cloche.transform.position.x(TILETOTALSIZE + 3 * RESOLUTION + TILETOTALSIZE - 200 + self.map.offset.x())
        self.cloche.transform.position.y(TILETOTALSIZE - 3 * RESOLUTION - self.cloche.transform.size.y())

        self.halo.transform.position.x(self.cloche.transform.position.x() - self.halo.transform.size.x() / 2 + self.cloche.transform.size.x() / 2)
        self.halo.transform.position.y(TILETOTALSIZE - 3 * RESOLUTION - self.halo.transform.size.y())

        # Phase 0
        self.platform.append([])
        # Phase 1
        Y = 2 * TILETOTALSIZE / 3
        self.platform.append([
                StaticObject(self.game, TILETOTALSIZE + 3 * RESOLUTION + self.map.offset.x(), Y, 200, 50),
                StaticObject(self.game, TILETOTALSIZE + 3 * RESOLUTION + TILETOTALSIZE - 200 + self.map.offset.x(), Y, 200, 50),
                StaticObject(self.game, TILETOTALSIZE + 3 * RESOLUTION + TILETOTALSIZE + self.map.offset.x(), Y, 200, 50),
                StaticObject(self.game, TILETOTALSIZE + TILETOTALSIZE * 2 + self.map.offset.x(), Y, 200, 50),
            ])

        self.transform.position = (self.right + self.left)/2
        self.phase = 0
        self.status = "Wait"
        self.attack_duration = 5
        self.time_start_attack = time.time()
    
    def next_phase(self):
        self.phase = (self.phase + 1) % len(self.phase_duration)
        self.time_at_phase_start = time.time()
        self.cloche_enable = False
    
    def update(self):
        self.animator.update()
        if self.is_Active:
            print(self.animator.current_anim)
            if time.time() > self.time_at_phase_start + self.phase_duration[self.phase]:
                self.cloche_enable = True
            else:
                self.cloche_enable = False
            if self.cloche_enable and self.game.is_Interacting and self.halo.transform.CollideRect(self.game.player.transform):
                self.next_phase()

            if self.status == "Wait":
                if self.goleft:
                    self.animator.set_anim("idle")
                else:
                    self.animator.set_anim("r_idle")
                if time.time() > self.time_start_attack + self.attack_duration:
                    self.next_attack(different=True)
            if self.status == "turn":
                if self.goleft:
                    self.animator.set_anim("r_turn")
                else:
                    self.animator.set_anim("turn")
                if self.animator.is_ended():
                    self.next_attack()
            if self.status == "Pre-Charge":
                if self.goleft:
                    self.animator.set_anim("precharge")
                else:
                    self.animator.set_anim("r_precharge")
                if self.animator.is_ended():
                    self.next_attack("Charge")
            if self.status == "Charge":
                if self.goleft:
                    self.animator.set_anim("charge")
                    self.transform.position = Lerp(self.transform.position, self.left, self.game.deltatime * self.speed)
                    if distance(self.transform.position, self.left) < 100:
                        self.goleft = False
                        self.next_attack("turn")
                else:
                    self.animator.set_anim("r_charge")
                    self.transform.position = Lerp(self.transform.position, self.right, self.game.deltatime * self.speed)
                    if distance(self.transform.position, self.right) < 100:
                        self.goleft = True
                        self.next_attack("turn")

    def blit(self, screen: py.Surface):
        for elt in self.platform[self.phase]:
            elt.blit(screen)
        self.cloche.blit(screen)
        if self.cloche_enable:
            self.halo.blit(screen)
        self.map.blit(screen, self.game.camera)
        screen.blit(self.animator.get_current_image(), (self.transform.position - self.game.camera.position - self.offset).tuple())


class Player(Entity):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.CanJump = True
        self.CanDoubleJump = False
        self.CanDash = True
        self.right = True

        self.ability_enable = {
            "Jump+": False,
            "Dash": False,
            "WallJump": False
        }

        self.wall_jump_count = 0
        self.wall_jump_max_count = 1
        self._decalX = int(PLAYER_HEIGHT/2 - PLAYER_WIDTH/2)
        self.last = py.time.get_ticks()
        self.cooldown = 500
        self.animator = Animator(
            idle=Animation(400_000_000, *load_all_images("Resources/Animation/Player/idle/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_idle=Animation(400_000_000, *load_all_images("Resources/Animation/Player/idle/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            run=Animation(800_000_000, *load_all_images("Resources/Animation/Player/run/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_run=Animation(400_000_000, *load_all_images("Resources/Animation/Player/run/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            fall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/fall/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_fall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/fall/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            jump=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/jump/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_jump=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/jump/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            wallfall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/wallfall/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            r_wallfall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/wallfall/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
        )

    def blit(self, screen: py.Surface):
        screen.blit(self.animator.get_current_image(), (self.transform.position - self.game.camera.position - Vector2(self._decalX, 0)).tuple())

    def update(self):
        super().update()
        if self.game.rightPressed:
            self.right = True
        elif self.game.leftPressed:
            self.right = False

        self.animator.update()
        if self.isGrounded:
            if self.game.leftPressed or self.game.rightPressed:
                if self.right:
                    self.animator.set_anim("run")
                else:
                    self.animator.set_anim("r_run")
            else:
                if self.right:
                    self.animator.set_anim("idle")
                else:
                    self.animator.set_anim("r_idle")
            self.CanJump = True
            self.CanDash = True
            self.wall_jump_count = 0  
            self.CanDoubleJump = False
        else:
            if self.velocity.y() > 0:
                if self.right:
                    self.animator.set_anim("fall")
                else:
                    self.animator.set_anim("r_fall")
            else:
                if self.right:
                    self.animator.set_anim("jump")
                else:
                    self.animator.set_anim("r_jump")
        if self.isGrabbingLeft and not self.isGrounded:
            self.animator.set_anim("wallfall")
        if self.isGrabbingRight and not self.isGrounded:
            self.animator.set_anim("r_wallfall")

    def jump(self):
        if self.CanJump:
            self.velocity = Vector2(0, -13) * RESMULT
            self.CanJump = False
            self.wall_jump_count = 0
            self.CanDoubleJump = True
    
    def double_jump(self):
        if self.CanDoubleJump and self.ability_enable["Jump+"]:
            self.velocity = Vector2(0, -13) * RESMULT
            self.wall_jump_count = 0
            self.CanDoubleJump = False

    def wall_jump(self):
        isgrabbing = False
        if self.isGrabbingLeft:
            self.transform.position.moveX(10)
            isgrabbing = True
        elif self.isGrabbingRight:
            self.transform.position.moveX(-10)
            isgrabbing = True
        if self.ability_enable["WallJump"] and isgrabbing and self.wall_jump_count < self.wall_jump_max_count and (self.CanDoubleJump or self.CanJump):
            jump_direction = Vector2(0, -13)
            self.velocity = jump_direction * RESMULT
            self.wall_jump_count += 1  

    def dash(self):
        if self.ability_enable["Dash"] and self.CanDash and self.isGrounded:
            if self.game.rightPressed:
                movementX = 100
                leftest = None
                mouvementbox = Box(self.transform.position + Vector2(self.transform.size.x(), 1), Vector2(movementX, self.transform.size.y() - 2))
                for elt in self.game.ground:
                    if mouvementbox.CollideRect(elt.transform):
                        if leftest is None:
                            leftest = elt.transform.position.x()
                        elif elt.transform.position.x() < leftest:
                            leftest = elt.transform.position.x()
                if leftest is None:
                    self.transform.position += Vector2(movementX, 0)
                else:
                    self.transform.position = Vector2(leftest - self.transform.size.x(), self.transform.position.y())
            elif self.game.leftPressed:
                movementX = -100
                rightest = None
                mouvementbox = Box(self.transform.position - Vector2(movementX, 1), Vector2(-movementX, self.transform.size.y() - 2))
                for elt in self.game.ground:
                    if mouvementbox.CollideRect(elt.transform):
                        if rightest is None:
                            rightest = elt.transform.position.x() - elt.transform.size.x()
                        elif elt.transform.position.x() - elt.transform.size.x() > rightest:
                            rightest = elt.transform.position.x() - elt.transform.size.x()
                if rightest is None:
                    self.transform.position += Vector2(movementX, 0)
                else:
                    self.transform.position = Vector2(rightest, self.transform.position.y())
            self.CanDash = False


