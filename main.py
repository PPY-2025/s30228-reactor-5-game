import pygame
from ui.game import run_game
from ui.menu import show_menu

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reactor 5")

def main():
    while True:
        username = show_menu(screen)
        result = run_game(username)

        while result == "restart":
            result = run_game(username)
        if result == "menu":
            continue

main()