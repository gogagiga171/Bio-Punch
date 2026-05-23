from classes.Player import Player
from pygame import Surface
import pygame

# Игрок нажимает -> на сервер отправляется информация о нажатии -> на сервере происходит логика -> при создании нового проджектайла об этом возвращается информация -> логика проджектайла на клиенте работает без постоянной синхронизацией с сервером -> при попадании проджектайла информация об этом возвращается на клиент
# для всего этого нужно чтобы в классах игроков хранился сокет, у проджектайлы должны разделятся на серверные и обычные, для синхронизации у проджектайлов должны быть id, при удалении, отправляется id проджектайла который нужно удалить

class ServerUpgrade:
    triggerable = False

    def __init__(self):
        pass

    def when_applied(self, player: Player):
        pass

    def logic(self, player: Player):
        pass

    def trigger(self, player: Player, projectiles):
        pass

class Upgrade (ServerUpgrade):
    image: Surface
    image_path = "resources/upgrades/"
    image_name: str

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(self.image_path + self.image_name).convert_alpha()
        w, h = self.image.get_size()
        size = 1/2
        self.image = pygame.transform.scale(self.image, (int(w * size), int(h * size)))