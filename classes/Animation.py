from classes.AnimationFrame import AnimationFrame
from classes.Vector import Vector
import time
import pygame

class Animation:
    def __init__(self, _animation:list[AnimationFrame], _looped:bool, _fps = 12):
        self.animation = _animation
        self.looped = _looped
        self.start_time = time.time()
        self.fps = _fps
        self.frame = 0
        self.time_rem = 0

    def start(self):
        self.start_time = time.time()
        self.frame = 0
        self.time_rem = 0

    def draw(self, pos:Vector, screen:pygame.surface.Surface):
        now = time.time()
        time_rem = ((now - self.start_time)*self.fps + self.time_rem) % 1
        frames_number = int(((now - self.start_time)*self.fps + self.time_rem) // 1)
        offset = 0
        frame = self.frame
        for i in range(self.frame + 1, self.frame + frames_number + 1):
            frame = i - offset*len(self.animation)
            if frame == len(self.animation):
                if not self.looped:
                    break
                offset += 1
                frame = i - offset*len(self.animation)
            self.animation[frame].execute_code()
        self.animation[frame].draw(pos, screen)
        self.frame = frame
        self.start_time = time.time()
        self.time_rem = time_rem