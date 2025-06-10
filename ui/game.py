import pygame
import sys
from game_engine.reactor import ReactorCore

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reactor 5")
font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()
reactor = ReactorCore()

def draw_text(text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def render():
    screen.fill((0, 0, 0))

    if not any(m.name == "Sensor Malfunction" for m in reactor.active_malfunctions):
        draw_text(f"Coolant: {reactor.coolant}", 20, 20)
        draw_text(f"Heat: {reactor.heat}", 20, 60)
        draw_text(f"Pressure: {reactor.pressure}", 20, 100)


    draw_text("Malfunctions:", 20, 160)
    for idx, mal in enumerate(reactor.active_malfunctions):
        draw_text(f"{idx + 1}. {mal.name} (Ticks Left: {mal.duration})", 40, 190 + 30 * idx)

    draw_text("1 - cool, 2 - valve, 3 - power, 4 - sensors, 5 - lockdown", 20, 530)
    draw_text("C - cool down, P - release pressure", 20, 560)

    pygame.display.flip()

def game_over():
    if reactor.coolant <= 0:
        return "You ran out of coolant! Sorry, it will hurt."
    if reactor.heat >= 100:
        return "Reactor meltdown! Heat exceeded safe limits."
    if reactor.pressure >= 120:
        return "Reactor exploded! Pressure too high."
    if reactor.red_button:
        return "Self-destructing protocol activated!"
    return None

def game_over_screen(message):
    screen.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont(None, 60)
    msg_surface = game_over_font.render("GAME OVER", True, (255, 0, 0))
    reason_surface = font.render(message, True, (255, 255, 255))
    instruction_surface = font.render("Press [R] to try again or [ESC] to quit", True, (180, 180, 180))

    screen.blit(msg_surface, (screen.get_width() // 2 - msg_surface.get_width() // 2, 200))
    screen.blit(reason_surface, (screen.get_width() // 2 - reason_surface.get_width() // 2, 300))
    screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, 350))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return
        clock.tick(10)

def run_game():
    global reactor
    reactor = ReactorCore()

    tick_rate = 3  # seconds per tick
    last_tick_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        if (current_time - last_tick_time) >= tick_rate * 1000:
            reactor.tick()
            last_tick_time = current_time

            reason = game_over()
            if reason:
                game_over_screen(reason)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    reactor.fix_coolant_leak()
                elif event.key == pygame.K_2:
                    reactor.unjam_valve()
                elif event.key == pygame.K_3:
                    reactor.reset_circuit()
                elif event.key == pygame.K_4:
                    reactor.calibrate_sensors()
                elif event.key == pygame.K_5:
                    reactor.override_lockdown()
                elif event.key == pygame.K_c:
                    if not any(m.name == "Control Lockout" for m in reactor.active_malfunctions):
                        reactor.cool_down()
                elif event.key == pygame.K_p:
                    if not any(m.name == "Control Lockout" for m in reactor.active_malfunctions):
                        reactor.release_pressure()
                elif event.key == pygame.K_z:
                    reactor.red_button = True
        render()
        clock.tick(30)

while True:
    run_game()