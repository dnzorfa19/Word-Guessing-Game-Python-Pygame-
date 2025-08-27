import pygame
import sys
import random
import string

# Pygame başlat
pygame.init()

# Ekran boyutu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kelime Tahmin Oyunu")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 149, 237)  # Hover rengi
BACKGROUND_COLOR = (240, 248, 255)  # Açık mavi arkaplan

# Fontlar
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 40)

# Kelime listesi
words = ["PYTHON", "KOD", "OYUN", "BILGISAYAR", "PROGRAM", "PIKACHU"]

# Oyun başlatma fonksiyonu
def new_game():
    global secret_word, guessed_letters, wrong_guesses, max_wrong, score, game_over
    secret_word = random.choice(words)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = 6
    score = 0
    game_over = False

# İlk oyun başlat
new_game()

# Harf butonları
letters = list(string.ascii_uppercase)
buttons = []
start_x, start_y = 50, 500
for i, letter in enumerate(letters):
    rect = pygame.Rect(start_x + (i % 13) * 50, start_y + (i // 13) * 50, 40, 40)
    buttons.append((letter, rect))

# Adam asma çizimleri
def draw_hangman(wrong):
    pygame.draw.line(screen, BLACK, (600, 500), (700, 500), 5)
    pygame.draw.line(screen, BLACK, (650, 500), (650, 100), 5)
    pygame.draw.line(screen, BLACK, (650, 100), (750, 100), 5)
    pygame.draw.line(screen, BLACK, (750, 100), (750, 150), 5)
    if wrong > 0:
        pygame.draw.circle(screen, BLACK, (750, 180), 30, 3)
    if wrong > 1:
        pygame.draw.line(screen, BLACK, (750, 210), (750, 320), 3)
    if wrong > 2:
        pygame.draw.line(screen, BLACK, (750, 230), (700, 270), 3)
    if wrong > 3:
        pygame.draw.line(screen, BLACK, (750, 230), (800, 270), 3)
    if wrong > 4:
        pygame.draw.line(screen, BLACK, (750, 320), (700, 380), 3)
    if wrong > 5:
        pygame.draw.line(screen, BLACK, (750, 320), (800, 380), 3)

# Yeniden Oyna buton alanı
replay_rect = pygame.Rect(50, 400, 200, 50)  # Kelimenin altında

# Oyun döngüsü
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    # Fare pozisyonu
    mx, my = pygame.mouse.get_pos()
    
    # Olaylar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Harf tıklamaları
            if not game_over:
                for letter, rect in buttons:
                    if rect.collidepoint((mx, my)) and letter not in guessed_letters:
                        guessed_letters.append(letter)
                        if letter not in secret_word:
                            wrong_guesses += 1
            
            # Yeniden Oyna tıklaması
            if replay_rect.collidepoint((mx, my)):
                new_game()
    
    # Kelimeyi ekranda göster
    display_word = ""
    for char in secret_word:
        display_word += char + " " if char in guessed_letters else "_ "
    text_surface = font.render(display_word, True, BLACK)
    screen.blit(text_surface, (50, 50))
    
    # Yanlış tahmin sayısı
    wrong_text = small_font.render(f"Yanlış Tahminler: {wrong_guesses}/{max_wrong}", True, RED)
    screen.blit(wrong_text, (50, 150))
    
    # Puan
    score_text = small_font.render(f"Puan: {wrong_guesses * -5 + len([c for c in guessed_letters if c in secret_word])*10}", True, BLACK)
    screen.blit(score_text, (50, 200))
    
    # Adam asma
    draw_hangman(wrong_guesses)
    
    # Harf butonları
    for letter, rect in buttons:
        # Hover efekti
        if rect.collidepoint((mx, my)) and not letter in guessed_letters:
            color = LIGHT_BLUE
        else:
            color = WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        letter_color = GRAY if letter in guessed_letters else BLACK
        letter_surface = small_font.render(letter, True, letter_color)
        screen.blit(letter_surface, (rect.x + 5, rect.y + 5))
    
    # Oyun bitiş kontrolü
    if wrong_guesses >= max_wrong:
        game_over_text = font.render(f"Kaybettiniz! Kelime: {secret_word}", True, RED)
        screen.blit(game_over_text, (50, 320))
        game_over = True
    elif all(char in guessed_letters for char in secret_word):
        game_over_text = font.render(f"Kazandınız!", True, GREEN)
        screen.blit(game_over_text, (50, 320))
        game_over = True
    
    # Yeniden Oyna butonu
    if replay_rect.collidepoint((mx, my)):
        pygame.draw.rect(screen, LIGHT_BLUE, replay_rect)
    else:
        pygame.draw.rect(screen, BLUE, replay_rect)
    replay_text = small_font.render("Yeniden Oyna", True, WHITE)
    screen.blit(replay_text, (replay_rect.x + 10, replay_rect.y + 10))
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
