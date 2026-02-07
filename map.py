from classes.Obstacle import Obstacle
from classes.Vector import Vector
from classes.Player import Player


def load_map(player1, player2):

    floor = Obstacle([
        Vector((100, 400)), Vector((700, 400)), Vector((700, 500)), Vector((100, 500))
    ])
    lramp = Obstacle([
        Vector((200, 400)), Vector((200, 200)), Vector((300, 400))
    ])
    rramp = Obstacle([
        Vector((500, 400)), Vector((600, 200)), Vector((600, 400))
    ])
    roof = Obstacle([
        Vector((250, 250)), Vector((350, 250)), Vector((350, 300))
    ])
    player1.orientation = "r"
    player2.orientation = "l"
    player1.health = player1.maxHealth
    player2.health = player2.maxHealth
    player1.pos = Vector([350, 350])
    player2.pos = Vector([450, 350])
    player1.set_animation("idle")
    player2.set_animation("idle")
    map = [floor, lramp, rramp, roof]
    return player1, player2, map