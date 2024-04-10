from Animation import *
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
            self.velocity -= Vector2(0, -GRAVITY * 2) * self.game.deltatime
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
    def __init__(self, game, x: float, y: float, w: float, h: float):
        super().__init__(game, x, y, w, h)
        self.animator = Animator(
            Animation(1, *load_all_images("Resources/Animation/Yack/idle/", ()))
        )
        self.is_Active = False
        self.phase = 0
        self.map = None
        self.goleft = True
        self.left = Vector2(0, 0)
        self.right = Vector2(0, 0)
        self.speed = 1

    def Start(self, map):
        self.map = map
        self.left = self.map.offset + Vector2(3 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.right = self.map.offset + Vector2(self.map.width * TILETOTALSIZE - 6 * RESOLUTION, TILETOTALSIZE - self.transform.size.y() - 3 * RESOLUTION)
        self.transform.position = self.right.copy()

    def update(self):
        if self.is_Active:
            if self.phase == 0:
                if self.goleft:
                    self.transform.position = Lerp(self.transform.position, self.left, self.game.deltatime)
                    if distance(self.transform.position, self.left) < 10:
                        self.goleft = False
                else:
                    self.transform.position = Lerp(self.transform.position, self.right, self.game.deltatime)
                    if distance(self.transform.position, self.right) < 10:
                        self.goleft = True

    def blit(self, screen: py.Surface):
        super().blit(screen)
        self.map.blit(screen, self.game.camera)


class Player(Entity):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.CanJump = True
        self.CanDash = True
        self.right = True
        self.CountDash = 0
        self.wall_jump_count = 0  
        self.wall_jump_max_count = 1  
        self._decalX = int(PLAYER_HEIGHT/2 - PLAYER_WIDTH/2)
        self.last = py.time.get_ticks()
        self.cooldown = 500
        self.CountDash = 0
        self.animator = Animator(
            idle=Animation(400_000_000, *load_all_images("Resources/Animation/Player/idle/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_idle=Animation(400_000_000, *load_all_images("Resources/Animation/Player/idle/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            run=Animation(800_000_000, *load_all_images("Resources/Animation/Player/run/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_run=Animation(400_000_000, *load_all_images("Resources/Animation/Player/run/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            fall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/fall/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_fall=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/fall/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),
            jump=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/jump/", (PLAYER_HEIGHT, PLAYER_HEIGHT))),
            r_jump=Animation(1_000_000_000, *load_all_images("Resources/Animation/Player/jump/", (PLAYER_HEIGHT, PLAYER_HEIGHT), reverseX=True)),

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
            self.CanJump = False
            self.CanDoubleJump = True
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

    def jump(self):
        if self.CanJump:
            self.velocity = Vector2(0, -1000) * self.game.deltatime * RESMULT
            self.CanJump = False
            self.wall_jump_count = 0  
    
    def double_jump(self):
        if self.CandoubleJump == False :
            if self.CountJump !=0 :
                self.velocity = Vector2(0, -1000) * self.game.deltatime
                self.wall_jump_count = 0
                self.CountJump = 0
                
    def wall_jump(self):
        wall_side = self.check_wall_contact()
        if wall_side and self.wall_jump_count < self.wall_jump_max_count:
            
            jump_direction = Vector2(0, -1) 
            if wall_side == 'left':
                jump_direction.x = 1 
            elif wall_side == 'right':
                jump_direction.x = -1  
            
            self.velocity = jump_direction * 1000 * self.game.deltatime
            self.wall_jump_count += 1  

    def dash(self):
        right = self.game.rightPressed
        left = self.game.leftPressed
        self.CountDash = 0
        if self.isGrounded:
            self.CountDash += 1
        if self.CanDash and self.CountDash > 0:
            if right:
                self.velocity += Vector2(100, 0)
                self.CountDash -= 1
            if left:
                self.velocity += Vector2(-100, 0)
                self.CountDash -= 1

    def check_wall_contact(self):
        
        for elt in self.game.ground + self.game.interactible:
            if id(self) != id(elt) and self.transform.CollideRect(elt.transform):
                check_left = self.box_left.CollideRect(elt.transform)
                check_right = self.box_right.CollideRect(elt.transform)

                if check_left:
                    return 'left'
                elif check_right:
                    return 'right'

        return None  

