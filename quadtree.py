"""Quadtree — 2D spatial subdivision."""
class Quadtree:
    def __init__(self, x, y, w, h, cap=4):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cap = cap; self.points = []; self.divided = False
        self.nw = self.ne = self.sw = self.se = None
    def contains(self, p): return self.x<=p[0]<self.x+self.w and self.y<=p[1]<self.y+self.h
    def subdivide(self):
        hw, hh = self.w/2, self.h/2
        self.nw = Quadtree(self.x, self.y, hw, hh, self.cap)
        self.ne = Quadtree(self.x+hw, self.y, hw, hh, self.cap)
        self.sw = Quadtree(self.x, self.y+hh, hw, hh, self.cap)
        self.se = Quadtree(self.x+hw, self.y+hh, hw, hh, self.cap)
        self.divided = True
    def insert(self, p):
        if not self.contains(p): return False
        if len(self.points) < self.cap:
            self.points.append(p); return True
        if not self.divided: self.subdivide()
        return self.nw.insert(p) or self.ne.insert(p) or self.sw.insert(p) or self.se.insert(p)
    def query_range(self, x, y, w, h):
        result = []
        if not (self.x<x+w and self.x+self.w>x and self.y<y+h and self.y+self.h>y): return result
        for p in self.points:
            if x<=p[0]<x+w and y<=p[1]<y+h: result.append(p)
        if self.divided:
            result.extend(self.nw.query_range(x,y,w,h))
            result.extend(self.ne.query_range(x,y,w,h))
            result.extend(self.sw.query_range(x,y,w,h))
            result.extend(self.se.query_range(x,y,w,h))
        return result

if __name__ == "__main__":
    qt = Quadtree(0, 0, 100, 100)
    import random; random.seed(42)
    pts = [(random.uniform(0,100), random.uniform(0,100)) for _ in range(200)]
    for p in pts: qt.insert(p)
    hits = qt.query_range(25, 25, 50, 50)
    brute = [p for p in pts if 25<=p[0]<75 and 25<=p[1]<75]
    assert len(hits) == len(brute)
    print(f"Quadtree: {len(pts)} points, query found {len(hits)}")
    print("All tests passed!")
