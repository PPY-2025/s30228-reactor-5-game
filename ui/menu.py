import pygame
import sys
from database.db import get_leaderboard

pygame.init()
font = pygame.font.SysFont("Courier", 28)

def draw_text(surface, text, x, y, color=(0, 255, 0)):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))

def show_menu(screen):
    username = ""
    input_active = True
    menu_state = "menu"

    while True:
        screen.fill((0, 0, 0))

        if menu_state == "menu":
            draw_text(screen, "ENTER USERNAME:", 50, 100)
            draw_text(screen, username + ("_" if input_active else ""), 300, 100)
            draw_text(screen, "[ENTER] Start", 50, 200)
            draw_text(screen, "[L] Leaderboard", 50, 240)
            draw_text(screen, "[ESC] Quit", 50, 280)

        elif menu_state == "leaderboard":
            draw_text(screen, "--- LEADERBOARD ---", 50, 60)
            leaderboard = get_leaderboard()
            for i, entry in enumerate(leaderboard):
                draw_text(screen, f"{i+1}. {entry['username']} - {entry['survival_time']}s", 50, 100 + i*30)
            draw_text(screen, "[B] Back", 50, 500)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if menu_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            if username:
                                return username
                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif event.unicode.isalnum() and len(username) < 20:
                            username += event.unicode
                    if event.key == pygame.K_l:
                        menu_state = "leaderboard"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            elif menu_state == "leaderboard":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    menu_state = "menu"