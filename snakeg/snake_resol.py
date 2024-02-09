from snake_functions import *
import math

def find_food(gamestate):
    mat=gamestate.tab
    for i in range(n):
        for j in range(m):
            if mat[i,j]=="F":
                return i,j
    return "pas trouvé"



def dist(x,y):
    a,b=x
    c,d=y
    return np.sqrt((c-a)**2+(d-b)**2)

mov_list=[(-1,0),(1,0),(0,1),(0,-1)]

def find_shortest_path(gamestate):
    x0,y0=gamestate.snake_list[0]
    tab_dist={(x0,y0):0}
    prev={}
    f=find_food(gamestate)
    if f=="pas trouvé":
        print(gamestate.tab)
    xf,yf=f
    for i in range(n):
        for j in range(m):
            if i!=x0 or j!=y0:
                tab_dist[(i,j)]=math.inf
    def sort_fun(x):
        a,b=x
        return tab_dist[(a,b)]+dist((a,b),(xf,yf))
    traites=[]
    atraiter=[(x0,y0)]
    run=True
    while(run):
        atraiter.sort(key=sort_fun)
        #print(atraiter)
        if atraiter==[]:
            print(gamestate.tab)
        current=atraiter.pop(0)
        xc,yc=current
        for (x,y) in mov_list:
            a,b=next(xc,yc,x,y)
            if a==xf and b==yf:
                run=False
                prev[(a,b)]= current
                tab_dist[(a,b)]=tab_dist[current]+1
            elif ((a,b) not in traites) and gamestate.tab[a,b]!="S":
                atraiter.append((a,b))
                if tab_dist[(xc,yc)]+1<tab_dist[(a,b)]:
                    prev[(a,b)]=(xc,yc)
                    tab_dist[(a,b)]=tab_dist[(xc,yc)]+1
        traites.append(current)
    tab_dir=[]
    xc,yc=xf,yf
    while(xc!=x0 or yc!=y0):
        xn,yn=prev[(xc,yc)]
        d1,d2=xc-xn,yc-yn
        xc,yc=xn,yn
        tab_dir.append((d1,d2))
    tab_dir.reverse()
    return tab_dir

def next_move(gamestate,path):
    if path==[]:
        path=find_shortest_path(gamestate)
    gamestate.dir=path.pop(0)

        
            
                    

run=True
jeu=game(np.full((n,m),"X"),(1,0),[],0)
x,y=random.randint(0,n-1),random.randint(0,m-1)
jeu.tab[x,y]="S"
x2,y2=random.randint(0,n-1),random.randint(0,m-1)
jeu.tab[x2,y2]="F"
jeu.snake_list.append((x,y))
path=find_shortest_path(jeu)



while(run):
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                pg.quit()
                sys.exit()
    next_move(jeu,path)
    pg.time.wait(5)
    jeu.update()
    pg.time.wait(5)
    draw(jeu)