import pygame, random, spritesheet, sys, os
from pygame import mixer
from button import Botao
from pygame.locals import *
import time #
from SaveLoadManager import SaveLoadSystem
pygame.init()

#inicializacao do módulo de som
pygame.mixer.pre_init(44100, -16, 2, 512)

#definir fontes e score, por preguiça está aqui
# valorscore = 0
valorscoreX = 5
valorscoreY = 5
global level
global iniciou
global terminou_contagem
terminou_contagem = False

contador_transicao = 0

pausado = False
#funcao para o main menu
def get_font(size):
    return pygame.font.Font("assets/font/font.ttf", size)

#background da fase msm, por enquanto aqui

background = pygame.image.load('assets/img/fundo1.png')
# background = pygame.image.load('assets/img/espacolindo.png')
background = pygame.transform.smoothscale(background, (635, 635))

#a ajeitar essa largura e altura da tela
LARGURA = background.get_width()
ALTURA = background.get_height()

pygame.display.set_caption('Spaceif')
click = pygame.mixer.Sound('assets/sound/click.wav')
click.set_volume(0.5)

somgameover = pygame.mixer.Sound('assets/sound/gameover.mp3')
somgameover.set_volume(0.8)

win = pygame.mixer.Sound('assets/sound/win.mp3')
win.set_volume(0.8)

musica_menu = pygame.mixer.Sound('assets/sound/musica_menu.mp3')
musica_menu.set_volume(0.6)
pygame.mixer.Channel(6).play(musica_menu, loops=-1)

saveloadmanager = SaveLoadSystem(".save", "save_data")

level, pontuacoes = saveloadmanager.load_game_data(["level", "pontuacoes"], [1, []])

def desenhar_texto(texto, font, text_color, x, y, tela):
    img = font.render(texto, True, text_color)
    rect = img.get_rect(center=(x,y))
    tela.blit(img, rect)
    
def desenhar_fundo(tela, imagem_de_fundo):
    tela.fill((0, 0, 0))
    global retangulo_imagem
    retangulo_imagem = imagem_de_fundo.get_rect(center=(tela.get_width()/2, tela.get_height()/2))
    tela.blit(imagem_de_fundo, retangulo_imagem)
    return retangulo_imagem

def main_menu():
  #background do menu
  bg = pygame.image.load('assets/img/menualt.png')

  screen = pygame.display.set_mode((635, 635), RESIZABLE)
  icon = pygame.image.load('assets/img/pythoniconpng.png')
  # a = pygame.transform.scale(icon, (32, 32))
  pygame.display.set_icon(icon)

  bp = pygame.font.Font('assets/font/BPimperialItalic.otf', 170)

  relogio = pygame.time.Clock()



  zoom = pygame.mixer.Sound('assets/sound/zoom.wav')
  zoom.set_volume(0.25)
  
  global musica
  musica = pygame.mixer.Sound('assets/sound/musicafases.mp3')
  musica.set_volume(1)    

  while True:
    # screen.fill((233, 165, 76))
    relogio.tick(60)
    bg_rect = desenhar_fundo(screen, bg)
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # spaceif = bp.render('SPACEIF', True, '#5e17fb')
    # spaceif_rect = spaceif.get_rect(center=(screen.get_width()/2, screen.get_height()/5))
    # screen.blit(spaceif, spaceif_rect)

    PLAY_BUTTON = Botao(bg_rect.centerx, bg_rect.centery, "PLAY", get_font(50), "White", "#8c52ff", image=None)
    AJUDA_BUTTON = Botao(bg_rect.centerx, bg_rect.centery + 100, "ajuda", get_font(50), "White", "#8c52ff", image=None)
    QUIT_BUTTON = Botao(bg_rect.centerx, bg_rect.centery + 200, "QUIT", get_font(50), "White", "#8c52ff", image=None)

    for button in [PLAY_BUTTON, AJUDA_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS, screen)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == VIDEORESIZE:
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            musica_menu.stop()
            click.play()
            time.sleep(0.7)
            play()
        if AJUDA_BUTTON.checkForInput(MENU_MOUSE_POS):           
            click.play()
            time.sleep(0.7)
            ajuda()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.7)
            saveloadmanager.save_game_data([level], ["level"])
            pygame.quit()

    pygame.display.update()
    pygame.display.flip()
  
def play():
  global valorscore
  valorscore = 0
  global contador_transicao
  contador_transicao = 0
  screen = pygame.display.set_mode((635, 635), pygame.RESIZABLE)
  
  global pausado
  screen.fill("black")

  #cores
  VERMELHO = (255, 0, 0)
  VERDE = (0, 255, 0)
  BRANCO = (255, 255, 255)

  #configs para a quantia de pyhtonaliens
  linha = 4
  coluna = 5
  # valorscore = 0

  ultimo_tiro_alien = pygame.time.get_ticks()
  
  ultima_contagem = pygame.time.get_ticks()
  global game_over
  game_over = 0 #0 é game over, 1 o player ganhou, -1 o player perdeu

  #configs de dificuldade
  #o quanto de x que os aliens descem a cada movimentação
  aliens_desce = 10
  cooldown = 700
  alien_cooldown = 1000
  len_tiro_alien = 5

  countdown = 3

  relogio = pygame.time.Clock()

  font = pygame.font.Font('freesansbold.ttf', 20)

  #carregar sons
  # woom = pygame.mixer.Sound('assets/sound/sweep.wav')
  # woom.set_volume(0.25)
 
  som_explosao = pygame.mixer.Sound('assets/sound/explosion.wav')
  som_explosao.set_volume(1)

  laser = pygame.mixer.Sound('assets/sound/laser.wav')
  laser.set_volume(1)  

  #definir criar texto
  def mostrarcoisas(tela):
    score = font.render("Score: " + str(valorscore),
                          True, (BRANCO))
    tela.blit(score, (screen.get_width() - (screen.get_width()-5), (screen.get_height() - (screen.get_height()-5))))

    nivel = font.render("Nivel " + str(level), True, (BRANCO))
    tela.blit(nivel, (screen.get_width() - 70, 5)) 

  #cria classe da nave
  class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/naveboa.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.vida_inicial = health
      self.vida_restante = health
      self.ultimo_tiro = pygame.time.get_ticks()
      

    def update(self):
      #definir velocidade de movimento
      velocidade = 8
      
      game_over = 0
      #procurar por teclas pressionadas
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT] and self.rect.left > 0:
        self.rect.x -= velocidade      
      if key[pygame.K_RIGHT] and self.rect.right < LARGURA:
        self.rect.x += velocidade
        

      #codigo para a nave atirar
      #gravar tempo atual
      tempo_agora = pygame.time.get_ticks()
      if key[pygame.K_SPACE] and tempo_agora - self.ultimo_tiro > cooldown:
        tiro = Tiro(self.rect.centerx, self.rect.top)
        pygame.mixer.Channel(1).play(laser)
        grupo_tiro.add(tiro)
        self.ultimo_tiro = tempo_agora

      #updeitar mascara
      self.mask = pygame.mask.from_surface(self.image)    

      #desenhar barra de vida
      pygame.draw.rect(screen, VERMELHO, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
      if self.vida_restante > 0:
        pygame.draw.rect(screen, VERDE, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 15))
      elif self.vida_restante <= 0:
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 3)
        grupo_explosao.add(explosao)
        self.kill()
        game_over = -1
      if pygame.sprite.spritecollide(self, grupo_alien, True, pygame.sprite.collide_mask):
        self.vida_restante = 0
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 3)
        grupo_explosao.add(explosao)
      return game_over

  #criar classe do tiro
  class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/bala.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]

    def update(self):
      self.rect.y -= 5
      if self.rect.bottom < 0:
        self.kill()
      if pygame.sprite.spritecollide(self, grupo_alien, True):
        global valorscore
        valorscore += 1
        self.kill()
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 1.9)
        grupo_explosao.add(explosao)        
      
  #criar classe dos python-aliens
  class Pythonaliens(pygame.sprite.Sprite):
    def __init__(self, x, y,):
      pygame.sprite .Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/pythonoficial.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.contador_de_movimentos = 0
      #comeca se movendo p direita
      self.direcao_movimento = 1
      
    def update(self):
      self.rect.x += self.direcao_movimento
      self.contador_de_movimentos += 1
      if abs(self.contador_de_movimentos) > 75:
        #faz os aliens descerem
        self.rect.y += aliens_desce
        self.direcao_movimento *= -1
        self.contador_de_movimentos *= self.direcao_movimento        
      
  class Tiroalien(pygame.sprite.Sprite):
    def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/tiroalien.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]

    def update(self):
      self.rect.y += 2
      if self.rect.top > ALTURA:
        self.kill()
      if pygame.sprite.spritecollide(self, grupo_nave, False, pygame.sprite.collide_mask):
        self.kill()
        #reduzir a vida da espaçonave
        nave.vida_restante -= 1
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 1.2)
        grupo_explosao.add(explosao)

  class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
      pygame.sprite.Sprite.__init__(self)
      self.escala = scale
      self.images = []
      explosion = pygame.image.load('assets/img/explosion.png')
      explo = spritesheet.Spritesheet(explosion)
      for a in range(10):
        self.images.append(explo.pegar_imagem(a, 34, 34, self.escala, (0,0,0)))
      self.index = 0
      self.image = self.images[self.index]
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.counter = 0

    def update(self):
      #valor n pode ser maior q 0
      velocidade_de_explosao = 3
      #updeitar anim. de explosao
      self.counter += 1

      if self.counter >= velocidade_de_explosao and self.index < len(self.images) - 1:
        self.counter = 0
        self.index += 1
        self.image = self.images[self.index]

      #se a animação acabar, deleta a explosão
      if self.index >= len(self.images) - 1 and self.counter >= velocidade_de_explosao:
        self.kill()
    
  #cria grupo de sprite
  grupo_nave = pygame.sprite.Group()
  grupo_tiro = pygame.sprite.Group()
  grupo_alien = pygame.sprite.Group()
  grupo_tiro_alien = pygame.sprite.Group()
  grupo_explosao = pygame.sprite.Group()

  
  #cria alien
  def criar_aliens():
    #gerar aliens
    for linha in range(4):
      for item in range(coluna): #5
        alien = Pythonaliens(100 + item * 100, 70 + linha * 70)
        grupo_alien.add(alien)  
  
  criar_aliens()

  #cria player
  nave = Nave(int(LARGURA/2), ALTURA - 75, 3)
  grupo_nave.add(nave)

  run = True
  while run:
    global terminou_contagem

    relogio.tick(60)
    desenhar_fundo(screen, background)    

    global bonus
    bonus = nave.vida_restante

    if level == 2:     
      
      aliens_desce = 13.5      
      alien_cooldown = 850
      len_tiro_alien = 6
    if level == 3:
     

      aliens_desce = 16      
      alien_cooldown = 650
      len_tiro_alien = 7
    if level == 4:   
      
      aliens_desce = 18.5      
      alien_cooldown = 450
      len_tiro_alien = 8

    if countdown == 0:
      
      musica.play(loops =-1)
      #criar tiro dos aliens de forma aleatória
      #gravar tempo atual
      tempo_atual = pygame.time.get_ticks()
      #atirar
      if tempo_atual - ultimo_tiro_alien > alien_cooldown and len(grupo_tiro_alien) < len_tiro_alien and len(grupo_alien) > 0:
        alien_atirador = random.choice(grupo_alien.sprites())
        tiro_alien = Tiroalien((alien_atirador.rect.centerx), (alien_atirador.rect.bottom))
        grupo_tiro_alien.add(tiro_alien)
        #som de laser alien
        ultimo_tiro_alien = tempo_atual
      
      #verifica se todos os aliens de uma fase morreram
      if len(grupo_alien) == 0:
        #vitoria
        pontuacoes.append((valorscore * nave.vida_restante))
        saveloadmanager.save_game_data([pontuacoes], ["pontuacoes"])
        game_over = 1
      
      if level == 4 and len(grupo_alien) == 0:
        time.sleep(0.7)
        terminou_contagem = True
        final()

        #se o jogo é para estar rodando
      if game_over == 0:
        
        #updeita a nave
        game_over = nave.update()

        #updeita grupos de sprite
        grupo_tiro.update()
        grupo_alien.update()
        grupo_tiro_alien.update()
      
      else:
        time.sleep(0.9)
        fim_de_fase()

    if countdown > 0:
      desenhar_texto('Prepare-se', get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 + 100), screen)
      desenhar_texto(str(countdown), get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 + 150), screen)
      count_timer = pygame.time.get_ticks()
      if count_timer - ultima_contagem > 1000:
        countdown -= 1
        ultima_contagem = count_timer


    #animacao explosao
    grupo_explosao.update()
          
    #desenha grupos de sprites
    grupo_nave.draw(screen)  
    grupo_tiro.draw(screen)
    grupo_alien.draw(screen)
    grupo_tiro_alien.draw(screen)
    grupo_explosao.draw(screen)

   
    
    #mostrar score
    mostrarcoisas(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            saveloadmanager.save_game_data([level], ["level"])
            sys.exit()
    
    key = pygame.key.get_pressed()
    if key[pygame.K_m]:
      grupo_alien = []
    if key[pygame.K_i]:
      minora()
    if key[pygame.K_l]:
      game_over = 1
    if key[pygame.K_f]:
      game_over = -1
    if key[pygame.K_p] or key[pygame.K_ESCAPE]:
      pausado = True
      time.sleep(0.4)
      pause()

    pygame.display.update()

def ajuda():
  screen = pygame.display.set_mode((635, 635))
  fundo = pygame.image.load('assets/img/menu2.png')

  run = True
  while run:
    bg_rect = desenhar_fundo(screen, fundo)

    BACKTO = Botao(bg_rect.centerx, bg_rect.bottom -70, 'BACK TO MAIN MENU', get_font(35), '#e9a44c', "#8c52ff", image=None)
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    desenhar_texto("AJUDA", get_font(65), "#a51f62", bg_rect.centerx, (bg_rect.top + 75), screen)

    desenhar_texto("PAUSAR/DESPAUSAR", get_font(30), "white", bg_rect.centerx, (bg_rect.centery - 150), screen)
    desenhar_texto("P, ESC", get_font(30), "#7ED957", bg_rect.centerx, (bg_rect.centery - 100), screen)

    desenhar_texto("ATIRAR", get_font(30), "white", bg_rect.centerx, (bg_rect.centery - 25), screen)
    desenhar_texto("BARRA DE ESPACO", get_font(30), "#7ED957", bg_rect.centerx, (bg_rect.centery + 25), screen)

    desenhar_texto("MOVER A NAVE", get_font(30), "white", bg_rect.centerx, (bg_rect.centery + 100), screen)
    desenhar_texto("SETA DIREITA, SETA ESQUERDA", get_font(30), "#7ED957", bg_rect.centerx, (bg_rect.centery + 150), screen)

    BACKTO.changeColor(MENU_MOUSE_POS, screen)
    BACKTO.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN: #especifico para o click
        if BACKTO.checkForInput(MENU_MOUSE_POS):
              click.play()
              time.sleep(1)
              main_menu()
    
    pygame.display.update()
    pygame.display.flip()
  
def unpause():
  global pausado
  pausado = False

def unlevel():
  global level
  level = 1
def pause():
  screen = pygame.display.set_mode((635, 635))
  musica.stop()

  pause = pygame.image.load('assets/img/quadradoroxo.png')

  
  while pausado:
    bg_rect = desenhar_fundo(screen, background)
    pause.set_alpha(209)
    screen.blit(pause, bg_rect)

    desenhar_texto("PAUSED", get_font(45), "#8c52ff", bg_rect.centerx, (bg_rect.centery - 125), screen)
    
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    PLAY_BUTTON = Botao(bg_rect.centerx, bg_rect.centery - 50, "PLAY", get_font(30), "White", "#8c52ff", image=None)
    RESTART_BUTTON = Botao(bg_rect.centerx, bg_rect.centery, "RESTART LEVEL", get_font(30), "White", "#8c52ff", image=None)
    RESTART_GAME = Botao(bg_rect.centerx, bg_rect.centery + 50, "RESTART GAME", get_font(30), "White", "#8c52ff", image=None)
    QUIT_BUTTON = Botao(bg_rect.centerx, bg_rect.centery + 100, "QUIT", get_font(30), "White", "#8c52ff", image=None)

    for button in [PLAY_BUTTON, RESTART_BUTTON, RESTART_GAME, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS, screen)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == VIDEORESIZE:
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            unpause()
        if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):           
            click.play()
            play()
        if RESTART_GAME.checkForInput(MENU_MOUSE_POS):
            click.play()
            unlevel()
            play()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            saveloadmanager.save_game_data([level], ["level"])
            pygame.mixer.Channel(6).play(musica_menu, loops=-1)
            main_menu()
    
    if pausado:
      key = pygame.key.get_pressed()
      if key[pygame.K_SPACE] or key[pygame.K_p] or key[pygame.K_ESCAPE]:
        time.sleep(0.3)
        unpause()

    pygame.display.update()
    pygame.display.flip()

def fim_de_fase():
  quadradoroxo = pygame.image.load('assets/img/quadradoroxo.png')
  
  if game_over == -1:
    pygame.mixer.Channel(3).play(somgameover)
  elif game_over == 1:
    pygame.mixer.Channel(3).play(win)
  screen = pygame.display.set_mode((635, 635))
  musica.stop()

  img_next_level = pygame.image.load('assets/img/botao_branco.png')
  img_next_level = pygame.transform.scale(img_next_level, (105, 40))

  backto = pygame.image.load('assets/img/back2.png')
  backto = pygame.transform.scale(backto, (96, 90))

  run = True
  while run:
    
    background_rect = desenhar_fundo(screen, background)
    #valor original 87
    quadradoroxo.set_alpha(157)
    screen.blit(quadradoroxo, (background_rect))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    RESTART = Botao(background_rect.centerx, background_rect.centery + 100, 'RESTART', get_font(35), 'white', "#8c52ff", image=None)
    BACKTO = Botao(background_rect.centerx, background_rect.bottom -70, '', get_font(35), 'white', "#8c52ff", backto)
    NEXT_LEVEL = Botao(background_rect.centerx + 130, background_rect.centery + 120, 'NEXT LEVEL', get_font(30), 'white', "#8c52ff", image=None)
    lista_botoes = []
    passou_de_fase = False

    #se perdeu
    if game_over == -1:
      global contador_transicao
           
      desenhar_texto('Game Over!', get_font(50), '#8c52ff', int(screen.get_width() / 2), int(screen.get_height() / 2 - 170), screen)
      if contador_transicao > 50:
        desenhar_texto('Score: ' + str(valorscore), get_font(27), 'white', background_rect.centerx, background_rect.centery - 100, screen)
      if contador_transicao > 125:
        desenhar_texto('Bonus: ' + str(bonus), get_font(27), 'white', background_rect.centerx, background_rect.centery - 65, screen)
      if contador_transicao > 200:
        pygame.draw.line(screen, 'white', (background_rect.centerx -90, background_rect.centery - 50), (background_rect.centerx + 90, background_rect.centery - 50), 4)
      if contador_transicao > 275:
        desenhar_texto('Total: ' + str(bonus * valorscore), get_font(27), '#e9a44c', background_rect.centerx, background_rect.centery - 20, screen)
      
      if contador_transicao > 350:
        lista_botoes.extend([RESTART])
      
      if contador_transicao > 400:
        lista_botoes.append(BACKTO)

      contador_transicao += 5

      

    #se venceu
    if game_over == 1:
      desenhar_texto('Voce venceu!', get_font(50), '#8c52ff', int(screen.get_width() / 2), int(screen.get_height() / 2 - 170), screen)
      if contador_transicao > 50:
        desenhar_texto('Score: ' + str(valorscore), get_font(27), 'white', background_rect.centerx, background_rect.centery - 80, screen)
      if contador_transicao > 125:
        desenhar_texto('Bonus: ' + str(bonus), get_font(27), 'white', background_rect.centerx, background_rect.centery - 45, screen)
      if contador_transicao > 200:
        pygame.draw.line(screen, 'white', (background_rect.centerx -90, background_rect.centery - 30), (background_rect.centerx + 90, background_rect.centery - 30), 4)
      if contador_transicao > 275:
        desenhar_texto('Total: ' + str(bonus * valorscore), get_font(27), '#e9a44c', background_rect.centerx, background_rect.centery, screen)

      RESTART = Botao(background_rect.centerx - 130, background_rect.centery + 120, 'RESTART', get_font(30), 'white', "#8c52ff", image=None)
      if contador_transicao > 350:
        lista_botoes.extend([RESTART, NEXT_LEVEL])
      if contador_transicao > 400:
        lista_botoes.append(BACKTO)
      contador_transicao += 5
      passou_de_fase = True

    for button in lista_botoes:
      button.changeColor(MENU_MOUSE_POS, screen)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if lista_botoes[0].checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            play()
        if lista_botoes[-1].checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            main_menu()
        if passou_de_fase:
          if lista_botoes[1].checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            global level
            level += 1
            play()

    pygame.display.update()
    pygame.display.flip()

def minora():
  screen = pygame.display.set_mode((635, 635))
  musica.stop()

  fundo = pygame.image.load('assets/img/menu2.png')

  minora = pygame.image.load('assets/img/imagemdeminora.png')
  minora = pygame.transform.smoothscale(minora, (255, 400))

  derrotou = pygame.image.load('assets/img/vocederrotou.png')
  derrotou = pygame.transform.smoothscale(derrotou, (441, 90))

  amigos = pygame.image.load('assets/img/amigos.png')
  amigos = pygame.transform.smoothscale(amigos, (426, 100))

  backto = pygame.image.load('assets/img/back2.png')
  backto = pygame.transform.scale(backto, (188, 175))


  run = True
  while run:
    MENU_MOUSE_POS = pygame.mouse.get_pos()
   
    background_rect = desenhar_fundo(screen, fundo)
    screen.blit(minora, (0, (screen.get_height() - minora.get_height())))
    desenhar_texto('FINAL BOM', get_font(50), '#8c52ff', background_rect.centerx, background_rect.top + 50, screen)
    
    screen.blit(derrotou, (background_rect.centerx - 220, background_rect.top + 100))

    screen.blit(amigos, (background_rect.centerx - 120, background_rect.centery - 100))

    BACKTOMAIN = Botao(background_rect.centerx + 120, background_rect.bottom - 135, '', get_font(30), '#a51f62', "#8c52ff", backto)
    BACKTOMAIN.changeColor(MENU_MOUSE_POS, screen)
    BACKTOMAIN.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if BACKTOMAIN.checkForInput(MENU_MOUSE_POS):
            click.play()
            # untermina_contagem()
            unlevel()
            time.sleep(0.5)
            pygame.mixer.Channel(6).play(musica_menu, loops=-1)
            main_menu()   
    
    pygame.display.update()
    pygame.display.flip()

def final():
  quadradoroxo = pygame.image.load('assets/img/quadradoroxo.png')
  quadradoroxo.set_alpha(157)

  screen = pygame.display.set_mode((635, 635))
  musica.stop()

  backto = pygame.image.load('assets/img/back2.png')
  backto = pygame.transform.scale(backto, (96, 90))

  final = pygame.mixer.Sound('assets/sound/videoplayback.mp3')
  final.set_volume(1)

  final.play()

  run = True
  while run:
    global contador_transicao
    background_rect = desenhar_fundo(screen, background)
    screen.blit(quadradoroxo, (background_rect))

    MENU_MOUSE_POS = pygame.mouse.get_pos()


    desenhar_texto('FIM DE JOGO!', get_font(50), '#8c52ff', int(screen.get_width() / 2), int(screen.get_height() / 2 - 170), screen)
    
    if terminou_contagem:
      if contador_transicao > 50:
        desenhar_texto('Level 1: ' + str(pontuacoes[-4]), get_font(27), 'white', background_rect.centerx, background_rect.centery - 100, screen)
      if contador_transicao > 125:
        desenhar_texto('Level 2: ' + str(pontuacoes[-3]), get_font(27), 'white', background_rect.centerx, background_rect.centery - 65, screen)
      if contador_transicao > 200:
        desenhar_texto('Level 3: ' + str(pontuacoes[-2]), get_font(27), 'white', background_rect.centerx, background_rect.centery - 30, screen)
      if contador_transicao > 275:
        desenhar_texto('Level 4: ' + str(pontuacoes[-1]), get_font(27), 'white', background_rect.centerx, background_rect.centery + 5, screen)
      if contador_transicao > 350:
        pygame.draw.line(screen, 'white', (background_rect.centerx -100, background_rect.centery + 35), (background_rect.centerx + 100, background_rect.centery + 35), 4)
      if contador_transicao > 425:
        desenhar_texto('Final: ' + str(pontuacoes[-4] + pontuacoes[-3] + pontuacoes[-2] + pontuacoes[-1]), get_font(30), '#7ed957', background_rect.centerx, background_rect.centery + 70, screen)

    
    BACKTO = Botao(background_rect.centerx, background_rect.bottom -70, '', get_font(35), 'white', "#8c52ff", backto)

    if contador_transicao > 500:
      BACKTO.changeColor(MENU_MOUSE_POS, screen)
      BACKTO.update(screen)

    contador_transicao += 5

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if BACKTO.checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            minora()
    
    pygame.display.update()
    pygame.display.flip()

main_menu()
