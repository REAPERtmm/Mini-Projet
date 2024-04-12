import time
from random import random, choice
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


class Projectile(StaticObject):
    def __init__(self, game, x: float, y: float, direction: Vector2, lifetime: float):
        super().__init__(game, x, y, 70, 80, "Projectile")
        self.direction = direction
        self.animator = Animator(
            idle=Animation(400_000_000, *load_all_images("Resources/Animation/ame/", (250, 250)))
        )
        self.lifetime = lifetime
        self.time_start = time.time()
        self.toDestroy = False

    def blit(self, screen: py.Surface):
        screen.blit(self.animator.get_current_image(), ((self.transform.position - Vector2(90, 75) - self.game.camera.position).tuple()))

    def update(self):
        self.animator.update()
        self.transform.position += self.direction * self.game.deltatime
        if time.time() > self.time_start + self.lifetime:
            self.toDestroy = True


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
            if self.isGrabbingRight or self.isGrabbingLeft:
                if self.velocity.y() > 0:
                    self.velocity -= Vector2(0, -GRAVITY * .1) * self.game.deltatime
                else:
                    self.velocity -= Vector2(0, -GRAVITY * 2.2) * self.game.deltatime
            else:
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


class Boss(Entity):
    def __init__(self, game, x: float, y: float, percent=.4):
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
            death=Animation(2_000_000_000, *load_all_images("Resources/Animation/Yack/death/", (YACK_WIDTH, YACK_HEIGHT)), StopAtEnd=True),
            r_death=Animation(2_000_000_000, *load_all_images("Resources/Animation/Yack/death/", (YACK_WIDTH, YACK_HEIGHT), reverseX=True), StopAtEnd=True),
        )

        self.animatorcloche = Animator(
            idle=Animation(0, py.transform.scale(py.image.load("Resources/Animation/Cloche/1.png"), (250, 250)).convert_alpha(),  StopAtEnd=True),
            ding=Animation(1_000_000_000, *load_all_images("Resources/Animation/Cloche/", (250, 250)), StopAtEnd=True),
        )

        self.platform = []

        self.cloche = StaticObject(self.game, 0, 0, 250, 250, "Cloche")
        self.halo = StaticObject(self.game, 0, 0, 0, 0, "Halo", HALO)

        self.offset = Vector2(self.transform.size.x() * .7, self.transform.size.y() * .87)
        self.is_Active = False
        self.cloche_enable = False
        self.phase = 0
        self.phase_duration = [
            1, 1
        ]
        self.map = None
        self.time_at_phase_start = time.time()
        self.attack_duration_range = {
            "Wait": (1, 2),
            "Pre-Charge": (.5, .8),
            "Charge": (0, 0),
            "Projectile": (0, 0),
            "turn": (0, 0)
        }
        self.attack = [
            ["Wait", "Pre-Charge"],
            ["Wait", "Pre-Charge", "Projectile"]
        ]

        self.projectiles = []
        self.status = "Wait"
        self.attack_duration = 5
        self.time_start_attack = time.time()
        self.goleft = True
        self.left = Vector2(0, 0)
        self.right = Vector2(0, 0)
        self.speed = 1
        self.left_and_right_border = []
        self.ended = False

    def get_physic(self, camera):
        return self.platform[self.phase] + self.map.get_physique_on_screen(camera) + self.left_and_right_border

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
        self.attack_duration = randfloat(self.attack_duration_range[self.status][0], self.attack_duration_range[self.status][0])
        self.time_start_attack = time.time()

    def EnterRoom(self):
        self.time_start_attack = time.time()
        self.time_at_phase_start = time.time()

    def Start(self, map):
        self.map = map
        self.platform.clear()
        self.left_and_right_border = [
            StaticObject(self.game, self.map.offset.x(), -TILETOTALSIZE * 2, TILETOTALSIZE + 3 * RESOLUTION, 3 * TILETOTALSIZE),
            StaticObject(self.game, self.map.offset.x() + 3 * TILETOTALSIZE - 3 * RESOLUTION, -TILETOTALSIZE * 2, TILETOTALSIZE + 3 * RESOLUTION, 3 * TILETOTALSIZE)
        ]
        self.left = self.map.offset + Vector2(TILETOTALSIZE + 3 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.right = self.map.offset + Vector2((self.map.width - 1) * TILETOTALSIZE - self.transform.size.x() - 3 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.goleft = True

        self.cloche.transform.position.x(TILETOTALSIZE + 3 * RESOLUTION + TILETOTALSIZE + self.map.offset.x() - 250)
        self.cloche.transform.position.y(TILETOTALSIZE - 3 * RESOLUTION - 230)

        self.halo.transform.position.x(self.cloche.transform.position.x() - self.halo.transform.size.x() / 2 + 250 / 2)
        self.halo.transform.position.y(TILETOTALSIZE - 3 * RESOLUTION - self.halo.transform.size.y())

        self.ended = False
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
        if self.phase == 1:
            self.die()
        self.phase = (self.phase + 1) % len(self.phase_duration)
        self.time_at_phase_start = time.time()
        self.cloche_enable = False
        self.animatorcloche.set_anim("ding")

    def die(self):
        self.status = "Death"

    def update(self):
        self.animator.update()
        if self.animatorcloche.is_ended():
            self.animatorcloche.set_anim("idle")
        self.animatorcloche.update()
        for elt in self.projectiles:
            elt.update()
            if elt.toDestroy:
                self.projectiles.remove(elt)
        if self.is_Active and self.ended:
            if self.cloche_enable and self.game.is_Interacting and self.cloche.transform.CollideRect(self.game.player.transform):
                self.game.restart()
        elif self.status == "Death":
            if self.goleft:
                self.animator.set_anim("death")
            else:
                self.animator.set_anim("r_death")
            if self.animator.is_ended():
                self.ended = True
                self.cloche_enable = True
        elif self.is_Active and not self.ended:
            if time.time() > self.time_at_phase_start + self.phase_duration[self.phase]:
                self.cloche_enable = True
            else:
                self.cloche_enable = False
            if self.cloche_enable and self.game.is_Interacting and self.cloche.transform.CollideRect(self.game.player.transform):
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
            if self.status == "Projectile":
                if len(self.projectiles) < 5:
                    Y = randfloat(300, TILETOTALSIZE - 3*RESOLUTION - 300)
                    Y2 = randfloat(300, TILETOTALSIZE - 3*RESOLUTION - 300)
                    X = self.map.offset.x() + TILETOTALSIZE + 3*RESOLUTION
                    X2 = self.map.offset.x() + TILETOTALSIZE - 3*RESOLUTION + 2 * TILETOTALSIZE
                    direction: Vector2 = (self.game.player.transform.position - Vector2(X, Y))
                    direction2: Vector2 = (self.game.player.transform.position - Vector2(X2, Y2))
                    direction /= direction.magnitude
                    direction *= 500
                    direction2 /= direction2.magnitude
                    direction2 *= 500
                    self.projectiles.append(Projectile(self.game, X, Y, direction, 8))
                    self.projectiles.append(Projectile(self.game, X2, Y2, direction2, 8))
                self.next_attack()

            if self.status == "Pre-Charge":
                if self.goleft:
                    self.animator.set_anim("precharge")
                else:
                    self.animator.set_anim("r_precharge")
                if time.time() > self.time_start_attack + self.attack_duration:
                    self.next_attack("Charge")
            if self.status == "Charge":
                if self.goleft:
                    self.animator.set_anim("charge")
                    self.transform.position = Lerp(self.transform.position, self.left, self.game.deltatime * self.speed)
                    if distance(self.transform.position, self.left) < 20:
                        self.goleft = False
                        self.next_attack("turn")
                else:
                    self.animator.set_anim("r_charge")
                    self.transform.position = Lerp(self.transform.position, self.right, self.game.deltatime * self.speed)
                    if distance(self.transform.position, self.right) < 20:
                        self.goleft = True
                        self.next_attack("turn")

    def blit(self, screen: py.Surface):
        for elt in self.platform[self.phase]:
            elt.blit(screen)
        for elt in self.projectiles:
            elt.blit(screen)
        screen.blit(self.animatorcloche.get_current_image(), (self.cloche.transform.position - self.game.camera.position).tuple())
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

        self.animatorVFX = Animator(
            idle=Animation(0, py.transform.scale(py.image.load("Resources/Animation/no.png"), (1, 1)).convert_alpha(),  StopAtEnd=True),
            doublejump=Animation(400_000_000, *load_all_images("Resources/Animation/VFX/doublejump/", (PLAYER_HEIGHT*3, PLAYER_HEIGHT*3)), StopAtEnd=True),
        )

    def blit(self, screen: py.Surface):
        screen.blit(self.animator.get_current_image(), (self.transform.position - self.game.camera.position - Vector2(self._decalX, 0)).tuple())
        if self.animatorVFX.current_anim == "doublejump":
            screen.blit(self.animatorVFX.get_current_image(), (self.transform.position - self.game.camera.position - Vector2(self._decalX + 1.25*PLAYER_HEIGHT, .25 * PLAYER_HEIGHT)).tuple())
            if self.animatorVFX.is_ended():
                self.animatorVFX.set_anim("idle")

    def update(self):
        super().update()
        if self.game.rightPressed:
            self.right = True
        elif self.game.leftPressed:
            self.right = False

        self.animator.update()
        self.animatorVFX.update()
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
            self.game.sounds.Jump()
            self.velocity = Vector2(self.velocity.x(), -13) * RESMULT
            self.CanJump = False
            self.CanDoubleJump = True
    
    def double_jump(self):
        if self.CanDoubleJump and self.ability_enable["Jump+"] and not (self.isGrabbingLeft or self.isGrabbingRight):
            self.game.sounds.Jump()
            self.animatorVFX.set_anim("doublejump")
            self.velocity = Vector2(self.velocity.x(), -13) * RESMULT
            self.CanDoubleJump = False

    def wall_jump(self):
        if self.ability_enable["WallJump"] and (self.isGrabbingLeft or self.isGrabbingRight) and self.CanDoubleJump:
            self.game.sounds.Jump()
            jump_direction = Vector2(self.velocity.x() + (-5 if self.isGrabbingRight else 5), -13)
            self.velocity = jump_direction * RESMULT
            self.CanDoubleJump = False

    def dash(self):
        if self.ability_enable["Dash"] and self.CanDash and self.isGrounded:
            self.game.sounds.dash()
            movementX = 100  # distance du dash
            if self.game.rightPressed:
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
                rightest = None
                mouvementbox = Box(self.transform.position - Vector2(movementX, 1), Vector2(movementX, self.transform.size.y() - 2))
                for elt in self.game.ground:
                    if mouvementbox.CollideRect(elt.transform):
                        if rightest is None:
                            rightest = elt.transform.position.x() + elt.transform.size.x()
                        elif elt.transform.position.x() + elt.transform.size.x() > rightest:
                            rightest = elt.transform.position.x() + elt.transform.size.x()
                if rightest is None:
                    self.transform.position += Vector2(-movementX, 0)
                else:
                    self.transform.position = Vector2(rightest, self.transform.position.y())
            self.CanDash = False


