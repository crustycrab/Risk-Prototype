import pygame
from pygame.locals import *
import res
import sys
import numpy as np
pygame.init()
myfont = pygame.font.SysFont(None, 15)

class planet:
    def __init__(self,x,y,R,side=0):
        self.x=x
        self.y=y
        self.R=R
        self.side=side #0 - neutral, 1-player1 2-player2 3-warzone
        self.forces=[0.0,0.0]

    def draw(self,screen):
        label=None
        if self.side==0:
            colour=[100,100,100,0]
        if self.side==1:
            colour=[0,255,0,0]
            label = myfont.render("%.1f"%self.forces[0], 1, (0,0,0))
        if self.side==2:
            colour=[0,0,255,0]
            label = myfont.render("%.1f"%self.forces[1], 1, (255,255,255))
        if self.side==3:
            colour=[255,0,0,0]
            label = myfont.render("%.1f:%.1f"%(self.forces[0],self.forces[1]), 1, (255,255,255))
        pygame.draw.circle(screen, colour, (int(self.x),int(self.y)), int(int(self.R)))
        if label:
            screen.blit(label, (self.x, self.y))


    def ifcollide(self,x,y):
        if (x-self.x)**2 + (y-self.y)**2 < self.R*self.R:
            return True
        return False

    def update(self,dt):
        if self.forces[0]==0.0 and self.forces[1]==0.0:
            self.side=0

        if self.forces[0]>0.0 and self.forces[1]==0.0:
            self.side=1
            self.forces[0]=np.min([self.forces[0]+0.02*dt,self.R/10.])

        if self.forces[0]==0.0 and self.forces[1]>0.0:
            self.side=2
            self.forces[1]=np.min([self.forces[1]+0.02*dt,self.R/10.])

        if self.forces[0]>0.0 and self.forces[1]>0.0:
            self.side=3
            self.forces[0]=np.max([0.0,self.forces[0]-0.1*dt])
            self.forces[1]=np.max([0.0,self.forces[1]-0.1*dt])



class rocket:
    def __init__(self,x,y,side):
        self.x=x
        self.y=y
        self.side=side
        self.vx=0.0
        self.vy=0.0 

    def update(self,dt):
        self.x+=self.vx*dt
        self.y+=self.vy*dt

    def launch(self,vx,vy):
        self.vx=vx
        self.vy=vy

    def draw(self,screen):
        if self.side==1:
            colour=[100,255,100,0]
        if self.side==2:
            colour=[100,100,255,0]
        pygame.draw.circle(screen, colour, (int(self.x),int(self.y)), 5)

class game:
    def __init__(self,nPlanets,(width,height)):
         self.planets = []
         for i in range(nPlanets):
              collision=True
              x=0
              y=0
              R=0
              while collision==True:
                  R= np.max([20.0,20.0*np.random.randn()+np.min([height,width])/100.0])
                  x= np.max([np.min([width*np.random.rand(),width-R]),R])
                  y= np.max([np.min([height*np.random.rand(),height-R]),R])
                  print x,y,R
                  collision=False
                  for p in self.planets:
                       if (p.x-x)*(p.x-x)+(p.y-y)*(p.y-y)<(p.R+R)*(p.R+R):
                          collision=True
                          break
              self.planets.append(planet(x,y,R))
         p1 = np.random.random_integers(1,nPlanets-1)
         p2 = 0
         self.planets[p1].forces[0]=1.0
         self.planets[p2].forces[1]=1.0
         print self.planets[p1].x,self.planets[p1].y
         
         self.rockets=[]

         self.G=3000.0
         self.coefV=80.0

#player
         self.selection=p1
   
    def update(self,screen,dt):

        for num,i in enumerate(self.planets):
            #pygame.draw.circle(screen, [0,0,0], (int(i.x),int(i.y)), int(i.R+5))
            if self.selection==num:
                pygame.draw.circle(screen, [255,255,255], (int(i.x),int(i.y)), int(i.R+5))
            i.draw(screen)
            i.update(dt)
            #gravity
            for r in self.rockets:
                dir=np.array([r.x-i.x,r.y-i.y])
                ra=np.sqrt(dir[0]*dir[0]+dir[1]*dir[1])
                f=self.G*i.R*dir/(ra**3)
                r.vx-=f[0]*dt
                r.vy-=f[1]*dt
                
        toRemove=[]
        for r in self.rockets:
            #print r.x,r.y,r.vx,r.vy
            r.draw(screen)             
            r.update(dt)
            #landing of rockets
            collided=False
            for p in self.planets:
                if p.ifcollide(r.x,r.y):
                    p.forces[r.side-1]+=0.8
                    collided=True
            toRemove.append(collided)

        new_rockets = []
        for n,r in enumerate(self.rockets):
            if not toRemove[n]:
                new_rockets.append(r)
        self.rockets=new_rockets



    def selectPlanet(self,x,y):
        for nSel,p in enumerate(self.planets):
            if p.ifcollide(x,y):
                self.selection=nSel

    def launchRocket(self,x,y):
        x0=self.planets[self.selection].x
        y0=self.planets[self.selection].y
        pr0=np.array([x0,y0])
        R = self.planets[self.selection].R
        dir=np.array([x-x0,y-y0])
        moddir=np.sqrt(dir[0]*dir[0]+dir[1]*dir[1])
        r0= pr0 + dir*(R+0.1)/moddir
        new_rocket=rocket(r0[0],r0[1],1)
        v0=self.coefV*dir/moddir

        if v0[0]*dir[0]+v0[1]*dir[1]>0 and self.planets[self.selection].forces[0]>1.0:
            new_rocket.launch(v0[0],v0[1])
            self.rockets.append(new_rocket)
            self.planets[self.selection].forces[0]-=1



LEFT=1
RIGHT=3
def main():

    window = pygame.display.set_mode(res.WIN_SIZE)
    pygame.display.set_caption('Risk')
    clock = pygame.time.Clock()

    G = game(10,res.WIN_SIZE)
    while True:
    	delta = clock.tick(res.FPS) / 1000.0

        for event in pygame.event.get():
            if (event.type == QUIT):
                sys.exit(0)
            if  event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos=pygame.mouse.get_pos()
                G.selectPlanet(pos[0],pos[1])
                print pos,"left"
            if  event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                pos=pygame.mouse.get_pos()
                G.launchRocket(pos[0],pos[1])
                print pos, "right"
        window.fill((0,0,0))
        G.update(window,delta)

        pygame.display.flip()

if __name__ == '__main__':
    main()
