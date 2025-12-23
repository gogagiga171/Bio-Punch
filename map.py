from classes import Obstacle, Vector, Player


def load_map():

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
    player1 = Player(350, 350, "r")
    player2 = Player(450, 350, "l")
    map = [floor, lramp, rramp, roof]
    return player1, player2, map