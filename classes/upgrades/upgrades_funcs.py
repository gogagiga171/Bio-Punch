from classes.upgrades.ShotgunUpgrade import SUShotgun

def load_upgrade(name, _dict):
    names = {
        "Shotgun": SUShotgun
    }
    upgrade = names[name]()
    upgrade.load_from_dict(_dict)
    return upgrade