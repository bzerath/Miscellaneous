import pygame
import sys

# Dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Classe représentant un talent
class Talent:
    def __init__(self, name, prerequisites):
        self.name = name
        self.prerequisites = prerequisites
        self.rect = pygame.Rect(0, 0, 100, 50)  # Rectangle représentant le talent

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        text = font.render(self.name, True, BLACK)
        surface.blit(text, self.rect.center)

# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arbre de Talent")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Liste des talents
talents = [
    Talent("Talent 1", []),
    Talent("Talent 2", ["Talent 1"]),
    Talent("Talent 3", ["Talent 1"]),
    Talent("Talent 4", ["Talent 2", "Talent 3"]),
    Talent("Talent 5", ["Talent 4"]),
    Talent("Talent 6", ["Talent 2"])
]

# Fonction récursive pour trouver tous les talents requis
def find_required_talents(talent, required_talents):
    required_talents.append(talent)
    for prerequisite in talent.prerequisites:
        prerequisite_talent = next((t for t in talents if t.name == prerequisite), None)
        if prerequisite_talent:
            find_required_talents(prerequisite_talent, required_talents)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill(BLACK)

    # Récupération de la position de la souris
    mouse_pos = pygame.mouse.get_pos()

    # Vérification des talents survolés
    highlighted_talents = []
    for talent in talents:
        if talent.rect.collidepoint(mouse_pos):
            find_required_talents(talent, highlighted_talents)

    # Affichage des talents
    for talent in talents:
        if talent in highlighted_talents:
            talent_color = YELLOW
        else:
            talent_color = GREEN
        pygame.draw.rect(window, talent_color, talent.rect)
        talent.draw(window)

    pygame.display.flip()
    clock.tick(60)
