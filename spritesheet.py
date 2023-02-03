import pygame

class Spritesheet():
  def __init__(self, image):
    self.sheet = image

  def pegar_imagem(self, frame, largura, altura, scale, cor):
    #cria um surface quadrado
    image = pygame.Surface((largura, altura)).convert_alpha()
    
    #blita apenas a parte do sprite que a gnt quer nessa surface
    image.blit(self.sheet, (0,0), (0, (frame * altura), largura, altura))

    #aumenta ou diminui o sprite q a gnt quer
    image = pygame.transform.scale(image, (largura * scale, altura * scale))

    #deixa o fundo do sprite q a gnt quer transparente
    image.set_colorkey(cor)

    return image

