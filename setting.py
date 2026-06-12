class Screen:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        return  getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Высота должна быть целым числом")

        if value < 0:
            raise ValueError("Высота должна быть больше 0")

        setattr(instance, self.name, value)

class Game:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Значение должно быть целым числом")

        if value < 0:
            raise ValueError("Значение должно быть положительным")

        setattr(instance, self.name, value)

class Setting:
    height = Screen()
    width = Screen()

    fps = Game()
    ship_speed = Game()
    bullets_speed = Game()

    def __init__(
            self,
            width: int,
            height: int,
            fps: int,
            bg_color: tuple,
            ship_speed: int,
            bullets_speed: int
    ):
        self.height = height
        self.width = width
        self.fps = fps
        self.bg_color = bg_color
        self.ship_speed = ship_speed
        self.bullets_speed = bullets_speed

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color: tuple):
        if not isinstance(color, tuple):
            raise TypeError("Цвет должен быть кортежом (R, G, B)")

        if len(color) != 3:
            raise ValueError("Цвет должен состоять из трех значений")

        for el in color:
            if not 0 < el < 255:
                raise ValueError("Значние передаются от 0 до 255")

        self._bg_color = color

    def get_screen_setting(self):
        return self.width, self.height