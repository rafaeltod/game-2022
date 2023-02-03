import pygame
pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)

run_once = False

class Botao():
    def __init__(self, x, y, text_input, fonte, cor_base, cor_de_mudanca, image):
        self.image = image
        self.x = x
        self.y = y
        self.text_input = text_input
        self.fonte = fonte
        self.cor_base, self.cor_de_mudanca = cor_base, cor_de_mudanca
        self.text = self.fonte.render(self.text_input, True, self.cor_base)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.zoom = pygame.mixer.Sound('assets/sound/zoom.wav')
        self.zoom.set_volume(0.25)
        
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position, screen):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            # self.text = self.fonte.render(self.text_input, True, self.cor_de_mudanca)       	
            pygame.draw.rect(screen, '#8c52ff', ((self.rect.x -15, self.rect.y - 5), (self.rect.width + 30, self.rect.height + 5)), 3)
            
            
        else:
            self.text = self.fonte.render(self.text_input, True, self.cor_base)
            # pygame.draw.rect(screen, 'white', ((self.rect.x -15, self.rect.y - 5), (self.rect.width + 30, self.rect.height + 5)), 3)


    
    