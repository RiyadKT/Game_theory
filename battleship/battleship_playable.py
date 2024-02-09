import pygame as pg 
import numpy as np
import sys
#Constants
n,m=10,10
pg.init()
SURF=pg.display.set_mode((1450,1000))
font=pg.font.SysFont(None,30)

#colors in french
gris_clair=(220,220,220)
gris=(180,180,180)
gris_fonce=(150,150,150)

noir=(0,0,0)
rouge=(255,0,0)
bleuf=(0,0,139)

x0,y0=200,175
x1,y1=800,775

#Function that allows switching players (will be very useful)
#Joueur=player
def alt(joueur):
    if joueur=="j1":
        return "j2"
    else:
        return "j1"


class game():
    def __init__(self,tabj1,tabj2):
        #matrices associated to each player
        self.tabj1=tabj1
        self.tabj2=tabj2
    
    def joueur_to_tab(self,joueur):
        if joueur=="j1":
            return self.tabj1
        else:
            return self.tabj2
    #Tests if current player lost the game
    def lost(self,joueur):
        for i in range(n):
            for j in range(m):
                if self.joueur_to_tab(joueur)[i,j]=="C":
                    return False
        return True
    
    def draw(self,joueur):
        #displaying background, whoes turn is it to play...
        SURF.fill(gris_clair)
        if placement_phase:
            img2=font.render("Phase de placement",noir,True)
        else:
            img2=font.render("Phase d'attaque",noir,True)
        img3=font.render("Au tour de " + (joueur),noir,True)
        SURF.blit(img3,(1000,400))
        SURF.blit(img2,(1000,300))
        tab=self.joueur_to_tab(joueur)
        #displaying the color associated to each value of the current matrix
        for j in range(n):
            for i in range(m):
                if tab[i,j]=="C":
                    color=gris_fonce
                elif tab[i,j]=="X":
                    color=rouge
                elif tab[i,j]=="W":
                    color=gris
                else:
                    color=bleuf
                pg.draw.rect(SURF,color,[x0+i*(x1-x0)/(n-1),y0+j*(y1-y0)/(m-1),(x1-x0)/n,(y1-y0)/m])
                #Displaying coordinates to make gameplay easier
                number=font.render(str(i),noir,True)
                SURF.blit(number,(x0+10+i*(x1-x0)/(n-1),y0-50))
            letter=font.render(chr(j+65),noir,True)
            SURF.blit(letter,(x0-50,y0+10+j*(y1-y0)/(m-1)))
        pg.display.update()

#Returns matrix coordinates of where the mouse cursor is
def mouse_to_mat(x,y):
    xc,yc=x0,y0
    while (xc+(x1-x0)/(n-1)<x):
        xc+=(x1-x0)/(n-1)
    while (yc+(y1-y0)/(m-1)<y):
        yc+=(y1-y0)/(m-1)
    return round((xc-x0)*(n-1)/(x1-x0)),round((yc-y0)*(m-1)/(y1-y0))

#initialization of boat dictionnaries 
tab_bateaux1={2:3,3:2,4:1,5:1}
tab_bateaux2=tab_bateaux1.copy()
tab_bateaux={"j1":tab_bateaux1,"j2":tab_bateaux2}



placement_phase=True
current_joueur="j1"
current_ship=5
r=1,0

#empty game instance (will be filled in placement phase)
jeu=game(np.full((n,m)," "),np.full((n,m)," "))

while(placement_phase):
    x,y=pg.mouse.get_pos()
    x,y=mouse_to_mat(x,y)
    r0,r1=r
    tab=jeu.joueur_to_tab(current_joueur)
    #This value tests if you could fit a boat according to your mouse position and current boat orientation
    b=(x in list(range(min(n,n-r0*current_ship+1)))) and (y in list(range(min(m,m-r1*current_ship+1)))) and \
                all(v==" " or v=="W" for v in tab[x:x+r0*current_ship ,y]) and all(v==" " or v=="W" for v in tab[x,y:y+r1*current_ship])
    for event in pg.event.get():
        if event.type==pg.MOUSEBUTTONDOWN:
            #Switching orientation with right mouse button
            if event.button==3:
                r=1-r0,1-r1
            #If you can fit the current boat type, and click left mouse button, boat will be permanentely put in the temporary spot
            elif event.button==1 and b:
                for i in range(r0*current_ship):
                    tab[x+i,y]="C"
                for j in range(r1*current_ship):
                    tab[x,y+j]="C"
                if tab_bateaux[current_joueur][current_ship]==1:
                    if current_ship==2:
                        if current_joueur=="j2":
                            current_joueur="j1"
                            placement_phase=False
                        else:
                            current_ship=5
                            current_joueur="j2"
                    else:
                        current_ship-=1
                else:
                    tab_bateaux[current_joueur][current_ship]-=1
        #If you want to stop the game
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                sys.exit()
    #I redeclare b to take account for modifications possibly done in the loop above
    b=(x in list(range(min(n,n-r0*current_ship+1)))) and (y in list(range(min(m,m-r1*current_ship+1)))) and \
                all(v==" " or v=="W" for v in tab[x:x+r0*current_ship,y]) and all(v==" " or v=="W" for v in tab[x,y:y+r1*current_ship])
    #If you havent't clicked the left mouse button, but can fit a boat at your current mouse position and orientation
    #then the spots that can be filled will be displayed in a lighter shade of grey than a confirmed boat's
    if b:
        waiting_boat=[]
        for i in range(r0*current_ship):
            tab[x+i,y]="W"
            waiting_boat.append((x+i,y))
        for i in range(r1*current_ship):
            tab[x,i+y]="W"
            waiting_boat.append((x,i+y))
        #Making sure that "unconfirmed" matrix values that aren't in the possible boat (the one in light gray) positions
        #become empty again
        for i in range(n):
            for j in range(m):
                if ((i,j) not in waiting_boat) and tab[i,j]=="W":
                    tab[i,j]=" "
    jeu.draw(current_joueur)

run=True


play=False
pos=[-1,-1]
img=font.render("",noir,True)
adversaire=alt(current_joueur)
tab_adv=jeu.joueur_to_tab(adversaire)
#Playing phase
while(run):
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                sys.exit()
            #Confirming strike after giving position
            elif event.key==pg.K_SPACE:
                play=True
            #Registers the player's strike position and converts it into matrix coordinates
            else:
                if pos[0]==-1:
                    pos[0]=ord(pg.key.name(event.key))-97
                else:
                    pos[1]=int(pg.key.name(event.key))
    
    if play:
        play=False
        x,y=pos[1],pos[0]
        if tab_adv[x,y]=="C":
            res="touché"
            tab_adv[x,y]="X"
            if jeu.lost(adversaire):
                print(current_joueur +" a gagné")
                sys.exit()
        else:
            res="raté"
        tab_adv=jeu.joueur_to_tab(current_joueur)
        temp=current_joueur
        current_joueur=adversaire
        adversaire=temp
        img=font.render(res,noir,True)
        pos=[-1,-1]
    jeu.draw((current_joueur))
    SURF.blit(img,(1000,600))
    pg.display.update()



    

    
            

                

                

        