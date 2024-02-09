import pygame as pg
import random
import numpy as np
import sys
n,m=10,10

pg.init()
SURF = pg.display.set_mode((1450, 1000))
font = pg.font.SysFont(None, 30)


def next(x,y,d1,d2):
    xf=x
    yf=y
    if x+d1==n:
        xf=0
    elif x+d1==-1:
        xf=n-1
    if y+d2==m:
        yf=0
    elif y+d2==-1:
        yf=m-1
    if xf==x:
        xf+=d1
    if yf==y:
        yf+=d2
    return xf,yf

    

    

class game:
    def __init__(self,tab,dir,snake_list,score):
        self.tab=tab
        self.dir=dir
        self.snake_list=snake_list
        self.score=score

    def __str__(self):
        for i in range(n):
            for j in range(m):
                x=self.tab[i,j]
                if x=="S":
                    print("S ",end="")
                elif x=="F":
                    print("F ",end="")
                else:
                    print("X ",end="")
            print(" ")
        return ""
    
    def old_update(self):
        d1,d2=self.dir
        for i in range(len(self.snake_list)):
            x,y=self.snake_list[i]
            if self.tab[x,y].food=="F":
                a,b=self.snake_list[-1]
                nexta,nextb=next(a,b,d1,d2)
                self.snake_list.append((nexta,nextb))
                self.tab[nexta,nextb]="S"
                f1,f2=random.randint(0,n-1),random.randint(0,m-1)
                self.tab[f1,f2]="F"
                self.score+=10
            nextx,nexty=next(x,y,d1,d2)
            self.snake_list[i]=nextx,nexty
            self.tab[x, y] = "X"
            self.tab[nextx, nexty] = "S"
  
    def update(self):
        d1,d2=self.dir
        current=list.copy(self.snake_list)
        for i in range(len(self.snake_list)):
            x,y=self.snake_list[i]
            if i==0:
                xf,yf=next(x,y,d1,d2)
                if self.tab[xf,yf]=="S":
                    print("perdu! Score: "+str(self.score))
                    sys.exit()
                elif self.tab[xf,yf]=="F":
                    a,b=self.snake_list[-1]
                    self.snake_list.append(next(a,b,-d1,-d2))
                    f1,f2=random.randint(0,n-1),random.randint(0,m-1)
                    while((f1,f2) in self.snake_list):
                        f1,f2=random.randint(0,n-1),random.randint(0,m-1)
                    self.tab[f1,f2]="F"
                    self.score+=10
                xn,yn=next(x,y,d1,d2)
                self.snake_list[i]=xn,yn
                self.tab[xn,yn]="S"
                self.tab[x,y]="X"
            else:
                xprev,yprev=current[i-1]
                self.snake_list[i]=xprev,yprev
                self.tab[xprev,yprev]="S"
                self.tab[x,y]="X"

                
            
        

        
            

        


jeu=game(np.full((n,m),"X"),(1,0),[],0)
x,y=random.randint(0,n-1),random.randint(0,m-1)
jeu.tab[x,y]="S"
x2,y2=random.randint(0,n-1),random.randint(0,m-1)
jeu.tab[x2,y2]="F"
jeu.snake_list.append((x,y))
run=True 
gris_clair=(220,220,220)
gris_fonce=(150,150,150)

noir=(0,0,0)
rouge=(255,0,0)

x0,y0=200,150
x1,y1=800,750
def draw():
    SURF.fill(gris_clair)
    for j in range(m):
        for i in range(n):
            if jeu.tab[i,j]=="S":
                pg.draw.rect(SURF,noir,[x0+i*(x1-x0)/(n-1),y0+(m-1-j)*(y1-y0)/(m-1),(x1-x0)/n,(y1-y0)/m])
            elif jeu.tab[i,j]=="F":
                pg.draw.rect(SURF,rouge,[x0+i*(x1-x0)/(n-1),y0+(m-1-j)*(y1-y0)/(m-1),(x1-x0)/n,(y1-y0)/m])
            else:
                pg.draw.rect(SURF,gris_fonce,[x0+i*(x1-x0)/(n-1),y0+(m-1-j)*(y1-y0)/(m-1),(x1-x0)/n,(y1-y0)/m])
    img=font.render("Score "+str(jeu.score),True,noir)
    SURF.blit(img,(900,500))
    pg.display.update()
            



while(run):
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key==pg.K_w:
                jeu.dir=0,1
            elif event.key==pg.K_s:
                jeu.dir=0,-1
            elif event.key==pg.K_a:
                jeu.dir=-1,0
            elif event.key==pg.K_d:
                jeu.dir=1,0
    jeu.update()
    draw()
    pg.time.wait(100)
