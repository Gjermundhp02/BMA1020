from __future__ import annotations
from pyglet.math import Vec2
import pyglet.shapes as sh
from pyglet.graphics import Batch

class CompositeBody:
    def __init__(self, offset: Vec2 = Vec2(), vel: Vec2 = Vec2(), components: list[CompositeBody] = [], batch: Batch = Batch()) -> None:
        self.offset = offset
        self.vel = vel
        self.components = components
        self.batch = batch
        self.updateBatch(self.batch)

    def __name__(self) -> str:
        return "CompositeBody"

    def setPos(self, pos: Vec2) -> None:
        correctedPos = self.translate(pos)
        self.x = correctedPos.x
        self.y = correctedPos.y
    
    def translate(self, pos: Vec2) -> Vec2:
        raise NotImplementedError(f"translate is not implemented on ${self.__name__}")
    
    # def update(self, dt: float = 0, parentPos: Vec2 = Vec2()) -> None:
    #     self.setPos(Vec2(self.x, self.y)+self.offset)
    #     for i in self.components:
    #         i.setPos(self.translate(i.offset)+self.vel*dt)

    def updateComponents(self, dt: float = 0, parentPos: Vec2 = Vec2()) -> None:
        self.setPos(parentPos + (self.offset if not parentPos else Vec2(self.x+self.y)) + self.vel*dt)
        for i in self.components:
            i.updateComponents(dt, Vec2(self.x, self.y))
        print(self.x, self.y)
    
    def updateBatch(self, batch):
        self.batch=batch
        for i in self.components:
            i.updateBatch(batch)
    
    def addBody(self, body: CompositeBody):
        body.batch(self.batch)
        self.components.append(body)

class Circle(sh.Circle, CompositeBody):
    def __init__(self, offset: Vec2, radius: int, vel: Vec2 = Vec2(), components: list[CompositeBody]=[], segments=None, color=(0, 0, 0), group=None):
        self.offset = offset
        sh.Circle.__init__(self, 0, 0, radius, segments, color, group=group)
        CompositeBody.__init__(self, offset, vel, components=components)

    def translate(self, pos: Vec2 = Vec2()) -> Vec2:
        pos.x += self.radius
        pos.y += self.radius
        return pos