import random
import sys
import pygame
import pygame.freetype
import math

pygame.init()

pygame.freetype.init()
myfont=pygame.freetype.SysFont(None, 20) #taille du texte 20

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")

clock=pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

RAYON_BALLE = 10
XMIN, YMIN = 0, 0
XMAX, YMAX = width, height

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8
        self.vitesse_par_angle(60)
        self.sur_raquette = True

    def afficher(self):
        pygame.draw.rect(screen, BLANC,(int(self.x-RAYON_BALLE), int(self.y-RAYON_BALLE), 2*RAYON_BALLE, 2*RAYON_BALLE), 0)

    def deplacer(self, raquette):
        if self.sur_raquette:
            self.y = raquette.y - 2*RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(raquette)
            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx
            if self.x - RAYON_BALLE <XMIN:
                self.vx = -self.vx
            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette = True
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur/2 + RAYON_BALLE
        angle = 90 + 80 * diff/longueur_totale
        self.vitesse_par_angle(angle)

class Jeu:
    def __init__(self):
        self.balle = Balle()
        self.raquette = Raquette()
        self.brique = Brique(400, 400)

    def gestion_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        if self.brique.en_vie():
            self.brique.collision_balle(self.balle)
        self.raquette.deplacer(x)       

    def affichage(self):
        screen.fill(NOIR)
        self.balle.afficher()
        self.raquette.afficher()
        if self.brique.en_vie():
            self.brique.afficher()

class Raquette:
    def __init__(self):
        self.x = (XMIN+XMAX)/2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10 * RAYON_BALLE

    def afficher(self):
        pygame.draw.rect(screen, BLANC,(int(self.x-self.longueur/2), int(self.y-RAYON_BALLE), self.longueur, 2 * RAYON_BALLE), 0)

    def deplacer(self, x):
        if x - self.longueur/2 < XMIN:
            self.x = XMIN + self.longueur/2
        elif x + self.longueur/2 >XMAX:
            self.x = XMAX - self.longueur/2
        else:
            self.x = x

    def collision_balle(self, balle):
        vertical = abs(self.y - balle.y) < 2 * RAYON_BALLE
        horizontal = abs(self.x - balle.x) < self.longueur/2 + RAYON_BALLE
        return vertical and horizontal

class Brique:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE
    
    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        pygame.draw.rect(screen, BLANC, (int(self.x-self.longueur/2),int(self.y-self.largeur/2), self.longueur, self.largeur), 0)

    def collision_balle(self, balle):
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x:
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge:
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx
        else:
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge:
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx
            if touche:
                self.vie -= 1
            return touche

jeu = Jeu()

while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()

    pygame.display.flip()
    clock.tick(60)