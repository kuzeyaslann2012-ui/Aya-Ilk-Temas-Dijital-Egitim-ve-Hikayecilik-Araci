
import pygame
import sys
import random

# --- AYARLAR VE RENKLER ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 255)
GOLD = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AYA YOLCULUK - İnteraktif Piksel Macera")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Courier", 24, bold=True)
large_font = pygame.font.SysFont("Courier", 48, bold=True)

# --- OYUN DEĞİŞKENLERİ ---
stage = "START"  # START, PICK_PARTS, JOURNEY, CHOICE_1, CHOICE_2, FLAG_MISSION, ENDING, CREDITS
selected_items = []
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]
rocket_y = HEIGHT - 150
alive = True
flag_placed = False

# --- GÖRSEL ÇİZİM FONKSİYONLARI ---
def draw_pixel_human(x, y, color):
    pygame.draw.rect(screen, (240, 200, 150), (x+5, y, 10, 10)) # Kafa
    pygame.draw.rect(screen, (100, 200, 255), (x+7, y+2, 6, 4)) # Kask
    pygame.draw.rect(screen, color, (x, y+10, 20, 20))           # Gövde
    pygame.draw.rect(screen, color, (x+2, y+30, 6, 10))         # Bacak 1
    pygame.draw.rect(screen, color, (x+12, y+30, 6, 10))        # Bacak 2

def draw_rocket(x, y):
    pygame.draw.polygon(screen, GRAY, [(x, y), (x-20, y+40), (x+20, y+40)]) # Burun
    pygame.draw.rect(screen, WHITE, (x-20, y+40, 40, 80)) # Gövde
    pygame.draw.rect(screen, BLUE, (x-5, y+55, 10, 10)) # Pencere
    pygame.draw.polygon(screen, RED, [(x-20, y+100), (x-40, y+120), (x-20, y+120)]) # Sol kanat
    pygame.draw.polygon(screen, RED, [(x+20, y+100), (x+40, y+120), (x+20, y+120)]) # Sağ kanat
    if stage == "JOURNEY":
        pygame.draw.circle(screen, (255, 165, 0), (x, y+130 + random.randint(0,10)), 10)

def draw_moon_ground():
    # Ay zemini (Piksel kraterli)
    pygame.draw.rect(screen, DARK_GRAY, (0, HEIGHT - 150, WIDTH, 150))
    pygame.draw.ellipse(screen, GRAY, (100, HEIGHT - 120, 80, 40))
    pygame.draw.ellipse(screen, GRAY, (350, HEIGHT - 140, 120, 50))
    pygame.draw.ellipse(screen, GRAY, (600, HEIGHT - 100, 90, 30))

def draw_turkish_flag(x, y):
    # Direk
    pygame.draw.rect(screen, WHITE, (x, y, 4, 80))
    # Kırmızı Zemin
    pygame.draw.rect(screen, RED, (x+4, y, 60, 40))
    # Ay
    pygame.draw.circle(screen, WHITE, (x+25, y+20), 12)
    pygame.draw.circle(screen, RED, (x+29, y+20), 10) # Ayı kesmek için
    # Yıldız (Piksel yaklaşımı)
    pygame.draw.circle(screen, WHITE, (x+45, y+20), 4)

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), 1)
        if stage == "JOURNEY":
            star[1] += 5 
            if star[1] > HEIGHT: star[1] = 0

def show_text(text, x, y, color=WHITE, font_type=font):
    img = font_type.render(text, True, color)
    screen.blit(img, (x, y))

# --- ANA DÖNGÜ ---
running = True
while running:
    screen.fill(BLACK)
    draw_stars()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if stage == "START":
                stage = "PICK_PARTS"
            
            elif stage == "PICK_PARTS":
                if event.key == pygame.K_1 and "Kalkan" not in selected_items: selected_items.append("Kalkan")
                if event.key == pygame.K_2 and "Bant" not in selected_items: selected_items.append("Bant")
                if event.key == pygame.K_3 and "Yemek" not in selected_items: selected_items.append("Yemek")
                if event.key == pygame.K_4 and "Oksijen" not in selected_items: selected_items.append("Oksijen")
                if len(selected_items) >= 2: 
                    stage = "JOURNEY"
            
            elif stage == "CHOICE_1":
                if event.key == pygame.K_a: 
                    if "Kalkan" in selected_items: stage = "CHOICE_2"
                    else: 
                        alive = False
                        stage = "ENDING"
                if event.key == pygame.K_b: stage = "CHOICE_2"

            elif stage == "CHOICE_2":
                if event.key == pygame.K_a:
                    if "Bant" not in selected_items: alive = False
                    if alive: stage = "FLAG_MISSION"
                    else: stage = "ENDING"
                if event.key == pygame.K_b: 
                    stage = "FLAG_MISSION"
            
            elif stage == "FLAG_MISSION":
                if event.key == pygame.K_f:
                    flag_placed = True
                    stage = "ENDING"

            elif stage == "ENDING":
                stage = "CREDITS"

    # --- SAHNE YÖNETİMİ ---
    if stage == "START":
        draw_moon_ground()
        draw_turkish_flag(WIDTH//2 + 100, HEIGHT - 230)
        draw_rocket(WIDTH//2 - 150, HEIGHT - 270)
        for i in range(3):
            draw_pixel_human(WIDTH//2 - 100 + (i*50), HEIGHT - 180, WHITE)
            
        show_text("AYA YOLCULUK", WIDTH//2 - 180, 50, GOLD, large_font)
        show_text("TÜRKİYE UZAY GÖREVİ", WIDTH//2 - 150, 120, WHITE)
        show_text("BAŞLAMAK İÇİN BİR TUŞA BAS", WIDTH//2 - 180, 250, GREEN)

    elif stage == "PICK_PARTS":
        show_text("ROKET İÇİN 2 PARÇA SEÇİN:", 50, 50, GOLD)
        show_text("1- KALKAN (Meteorlar için)", 50, 150, BLUE)
        show_text("2- BANT (Tamirat için)", 50, 200, BLUE)
        show_text("3- YEMEK VE SU (Yol uzarsa)", 50, 250, BLUE)
        show_text("4- YEDEK OKSİJEN", 50, 300, BLUE)
        show_text(f"Seçilenler: {', '.join(selected_items)}", 50, 450, GREEN)

    elif stage == "JOURNEY":
        draw_rocket(WIDTH//2, rocket_y)
        rocket_y -= 3
        if rocket_y < 100:
            stage = "CHOICE_1"

    elif stage == "CHOICE_1":
        draw_rocket(WIDTH//2, 150)
        show_text("UYARI: METEOR GELİYOR!", WIDTH//2 - 150, 50, RED)
        show_text("A) SAĞA MANEVRA (Riskli ama hızlı)", 100, 450)
        show_text("B) SOLA MANEVRA (Uzun ama güvenli)", 100, 500)

    elif stage == "CHOICE_2":
        draw_rocket(WIDTH//2, 150)
        draw_moon_ground()
        show_text("AY YÜZEYİNE GELİNDİ. İNİŞ TARZI?", WIDTH//2 - 220, 50, BLUE)
        show_text("A) SERT VE HIZLI İNİŞ", 100, 450)
        show_text("B) YAVAŞ VE GÜVENLİ İNİŞ", 100, 500)
        
    elif stage == "FLAG_MISSION":
        draw_moon_ground()
        draw_rocket(WIDTH//2 - 150, HEIGHT - 270)
        draw_pixel_human(WIDTH//2, HEIGHT - 180, WHITE)
        show_text("AY'A BAŞARIYLA İNDİNİZ!", WIDTH//2 - 160, 50, GREEN)
        show_text("TÜRK BAYRAĞINI DİKMEK İÇİN 'F' TUŞUNA BAS!", WIDTH//2 - 280, 100, GOLD)

    elif stage == "ENDING":
        if alive:
            draw_moon_ground()
            draw_rocket(WIDTH//2 - 150, HEIGHT - 270)
            if flag_placed:
                draw_turkish_flag(WIDTH//2 + 50, HEIGHT - 230)
                show_text("GÖREV TAMAMLANDI: BAYRAK AY'DA DALGALANIYOR!", 50, 50, GREEN)
            else:
                show_text("AY'A İNDİN AMA BAYRAK DİKMEDİN...", 50, 50, GOLD)
            
            for i in range(3): 
                draw_pixel_human(WIDTH//2 - 50 + (i*60), HEIGHT - 180, WHITE)
        else:
            show_text("ROKET PARÇALANDI... GÖREV BAŞARISIZ.", 150, 250, RED)
            
        show_text("DEVAM ETMEK İÇİN BİR TUŞA BASIN", 150, 500, GRAY)

    elif stage == "CREDITS":
        show_text("KOD YAZAN:", WIDTH//2 - 100, 100, GOLD)
        show_text("Kuzey Aslan", WIDTH//2 - 80, 140)
        show_text("TASARIMCILAR:", WIDTH//2 - 100, 220, GOLD)
        show_text("Zeynep Azra - Elif Saracoğlu", WIDTH//2 - 180, 260)
        show_text("PROJE YARDIMCISI:", WIDTH//2 - 100, 340, GOLD)
        show_text("Salih Dalkılıç", WIDTH//2 - 80, 380)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()