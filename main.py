import pygame
import sys
import os
import random
import time
import math

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 1000, 700
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (40,40,40)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Moon Mission PRO")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 20)

# ---------------- ASSET SYSTEM ----------------
def load_image(path, size=(80,80)):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    else:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf,(random.randint(100,255),random.randint(100,255),random.randint(100,255)),(0,0,*size))
        return surf

def load_bg(path):
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    else:
        surf = pygame.Surface((WIDTH,HEIGHT))
        surf.fill((10,10,30))
        # yıldız ekle
        for _ in range(200):
            pygame.draw.circle(surf, WHITE, (random.randint(0,WIDTH), random.randint(0,HEIGHT)), 1)
        return surf

# ---------------- CHARACTER ----------------
class Player:
    def __init__(self, name, role, stats):
        self.name = name
        self.role = role
        self.stats = stats
        self.image = load_image(f"assets/characters/{name}.png", (60,60))
        self.angle = 0  # bakış yönü

class AIPlayer(Player):
    def comment(self):
        if self.stats["intelligence"] > 7:
            return random.choice([
                "Bu parça mantıklı.",
                "Yakıt önemli!",
                "Bu güvenli görünüyor."
            ])
        else:
            return random.choice([
                "Riskli olabilir!",
                "Deneyelim bakalım.",
                "Hızlı seç!"
            ])

# ---------------- ROCKET ----------------
class Rocket:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        if len(self.parts) < 5 and part not in self.parts:
            self.parts.append(part)

    def score(self):
        return sum([p["power"] for p in self.parts])

# ---------------- GAME ----------------
class Game:
    def __init__(self):
        self.scene = "menu"
        self.start_time = None

        self.characters = [
            Player("Elif","Scientist",{"intelligence":9,"speed":5}),
            Player("Zeynep","Engineer",{"intelligence":8,"speed":6}),
            Player("Rüzgar","Explorer",{"intelligence":6,"speed":9}),
            Player("Salih","Pilot",{"intelligence":7,"speed":7}),
            Player("Kuzey","Leader",{"intelligence":8,"speed":6}),
        ]

        self.selected = None
        self.ai_team = []

        self.rocket = Rocket()

        self.parts = [{"name":f"Part{i}","power":random.randint(1,10)} for i in range(25)]

        self.bg_space = load_bg("assets/backgrounds/space.png")
        self.bg_moon = load_bg("assets/backgrounds/moon.png")

        self.dialog = ""

        # roket y konumu
        self.rocket_y = HEIGHT

    # -------- MENU --------
    def draw_menu(self):
        screen.fill(BLACK)
        text = FONT.render("Karakter Seç", True, WHITE)
        screen.blit(text,(400,50))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for i,char in enumerate(self.characters):
            x = 100 + i*150
            rect = pygame.Rect(x,200,80,80)

            screen.blit(char.image,(x,200))
            screen.blit(FONT.render(char.name,True,WHITE),(x,300))

            if rect.collidepoint(mouse_pos) and click:
                self.selected = char
                self.ai_team = [AIPlayer(c.name,c.role,c.stats) for c in self.characters if c != char]
                pygame.time.delay(200)
                self.scene = "build"

    # -------- BUILD --------
    def draw_build(self):
        screen.fill(GRAY)
        screen.blit(FONT.render("Roket Parçalarını Seç (5 tane)",True,WHITE),(300,20))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for i,part in enumerate(self.parts):
            x = 50 + (i%10)*90
            y = 100 + (i//10)*100
            rect = pygame.Rect(x,y,70,70)
            pygame.draw.rect(screen,YELLOW,rect)
            screen.blit(FONT.render(str(part["power"]),True,BLACK),(x+20,y+20))

            if rect.collidepoint(mouse_pos) and click:
                self.rocket.add_part(part)
                self.dialog = random.choice([ai.comment() for ai in self.ai_team])
                pygame.time.delay(100)

        # slotlar
        for i in range(5):
            x = 300 + i*100
            y = 500
            rect = pygame.Rect(x,y,70,70)
            pygame.draw.rect(screen,WHITE,rect,2)
            if len(self.rocket.parts) > i:
                p = self.rocket.parts[i]
                screen.blit(FONT.render(str(p["power"]),True,WHITE),(x+20,y+20))

        screen.blit(FONT.render(self.dialog,True,GREEN),(50,650))
        if len(self.rocket.parts) == 5:
            screen.blit(FONT.render("SPACE tuşuna bas →",True,WHITE),(700,650))

    # -------- SPACE --------
    def draw_space(self):
        screen.blit(self.bg_space,(0,0))

        # ease-out yavaşlama
        if self.start_time:
            t = time.time() - self.start_time
            duration = 30  # toplam uçuş süresi saniye
            progress = min(1, t/duration)
            ease_progress = 1 - (1-progress)**2  # ease-out quadratic
            self.rocket_y = HEIGHT - ease_progress * (HEIGHT - 100)

        # roket çiz
        rocket_rect = pygame.Rect(WIDTH//2-40, self.rocket_y, 80, 120)
        pygame.draw.rect(screen, RED, rocket_rect)

        # karakterler roketin üstüne dönsün
        for i,ai in enumerate([self.selected]+self.ai_team):
            angle = 0 if i==0 else 180  # basit: arka karakterler 180° dönsün
            img = pygame.transform.rotate(ai.image, angle)
            x = WIDTH//2 - img.get_width()//2
            y = self.rocket_y - 60 - i*40
            screen.blit(img,(x,y))

        remaining = max(0, int(duration - (time.time() - self.start_time)))
        screen.blit(FONT.render(f"Aya varış: {remaining}s",True,WHITE),(20,20))

        if random.random() < 0.02:
            self.dialog = random.choice(["Meteor geliyor!","Oksijen düşüyor!","Sistem hatası!"])
        screen.blit(FONT.render(self.dialog,True,YELLOW),(20,60))

        if self.rocket_y <= 100:
            self.scene = "moon"

    # -------- MOON --------
    def draw_moon(self):
        screen.blit(self.bg_moon,(0,0))
        screen.blit(FONT.render("AYA HOŞGELDİN 🌕",True,WHITE),(400,50))
        for i,ai in enumerate([self.selected]+self.ai_team):
            screen.blit(FONT.render(ai.name,True,WHITE),(100,200+i*40))

    # -------- RUN --------
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.scene == "build" and event.key == pygame.K_SPACE:
                        if len(self.rocket.parts) == 5:
                            self.start_time = time.time()
                            self.rocket_y = HEIGHT
                            self.scene = "space"

            if self.scene == "menu":
                self.draw_menu()
            elif self.scene == "build":
                self.draw_build()
            elif self.scene == "space":
                self.draw_space()
            elif self.scene == "moon":
                self.draw_moon()

            pygame.display.update()
            clock.tick(FPS)

# ---------------- START ----------------
game = Game()
game.run()