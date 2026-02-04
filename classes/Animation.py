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

    def draw(self, pos:Vector, screen:pygame.surface.Surface):
        now = time.time()
        frames_number = int((now - self.start_time)*self.fps)
        offset = 0
        frame = 0
        for i in range(self.frame, self.frame + frames_number):
            frame = i - offset
            if frame == len(self.animation):
                if not self.looped:
                    break
                offset += 1
                frame = i - offset
            self.animation[frame].execute_code()
        self.animation[frame].draw(pos, screen)
        self.frame = frame