import pygame
import mapa
import animacao
import os

# CONSTANTES
TAMANHO_BLOCO = 32
DIMENSOES_TELA = (30 * TAMANHO_BLOCO, 20 * TAMANHO_BLOCO)
DIR_PRINCIPAL = os.path.abspath(os.getcwd())
DIR_IMAGENS = os.path.join(DIR_PRINCIPAL, 'imagens')
AZUL = (66, 135, 245)
VERDE = (81, 166, 105)
FPS = 60
INFORMACOES_MAPA = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,930,930,930,930,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,930,930,962,962,962,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,930,930,930,930,930,930,-1,-1,-1,962,962,962,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,962,962,962,962,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,930,930,930,930,930,930,930,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,930,930,962,962,962,962,962,962,962,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,930,930,930],
    [930,930,930,962,962,962,962,962,962,962,962,962,930,930,930,-1,-1,-1,-1,-1,-1,-1,-1,930,930,930,930,962,962,962],
    [962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,930,-1,-1,-1,930,930,930,930,962,962,962,962,962,962,962],
    [962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,930,930,930,962,962,962,962,962,962,962,962,962,962,962],
    [962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962],
    [962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962,962],
    [962,962,962,10,10,10,962,962,962,962,10,962,962,962,962,962,10,10,10,962,962,962,962,962,962,962,962,962,962,962],
    [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,962,962,10,10],
    [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10],
    [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10],
    [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
]

# INICIALIZACAO
pygame.init()
tela = pygame.display.set_mode(DIMENSOES_TELA)
pygame.display.set_caption('Jogo Educativo')
relogio = pygame.time.Clock()
rodar = True

class Jogador:
    def __init__(self, x, y):
        self.SPRITES_JOGADOR = animacao.carregar_sprites_jogador([DIR_IMAGENS, 'jogador'], 32, 32, True)
        self.DELAY_ANIMACAO = 5
        self.x = x
        self.y = y
        self.imagem = self.SPRITES_JOGADOR['idle_direita'][0]
        self.rect = self.imagem.get_rect()
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.vel_y = 0 # e a velocidade com a qual o jogador e deslocado no eixo y
        self.tocando_chao = False
        self.direcao = 'direita'
        self.cont_animacao = 0
    
    def update(self):
        delta_x = 0
        delta_y = self.vel_y # e o deslocamento do jogador que e causado pela gravidade

        # aplicar gravidade ao jogador
        self.vel_y += 1
        if self.vel_y >= 10:
            self.vel_y = 10

        # coletar e tratar os inputs do teclado
        tecla_pressionada = pygame.key.get_pressed()
        if tecla_pressionada[pygame.K_LEFT] == True:
            delta_x -= 5
            self.direcao = 'esquerda'
        if tecla_pressionada[pygame.K_RIGHT] == True:
            delta_x += 5
            self.direcao = 'direita'
        
        # checar colisoes no eixo y
        for bloco in lista_blocos:
            if bloco.rect.colliderect(pygame.rect.Rect(self.rect.x, (self.rect.y + delta_y), self.largura, self.altura)):
                if self.vel_y > 0: # jogador esta caindo
                    self.vel_y = 0
                    delta_y = bloco.rect.top - self.rect.bottom
                    self.tocando_chao = True # jogador esta tocando no chao
                elif self.vel_y < 0: # jogador esta subindo
                    self.vel_y = 0
                    delta_y = bloco.rect.bottom - self.rect.top
                break
        
        # checar colisoes no eixo x
        for bloco in lista_blocos:
            if bloco.rect.colliderect(pygame.rect.Rect((self.rect.x + delta_x), self.rect.y, self.largura, self.altura)):
                if delta_x > 0: # jogador esta indo para direita
                    delta_x = bloco.rect.left - self.rect.right
                elif delta_x < 0: # jogador esta indo para esquerda
                    delta_x = bloco.rect.right - self.rect.left
                break
        
        # atualizar sprite do jogador
        self.update_sprite(delta_x, delta_y)
        
        # atualizar coordenadas do jogador
        self.x += delta_x
        self.y += delta_y
        self.rect.topleft = (self.x, self.y)
    
    def update_sprite(self, desl_x, desl_y):
        if desl_y > 0:
            spritesheet = 'fall'
        elif desl_y < 0:
            spritesheet = 'jump'
        elif desl_x != 0 and self.tocando_chao == True:
            spritesheet = 'run'
        else:
            spritesheet = 'idle'
        
        nome_da_spritesheet = spritesheet + '_' + self.direcao
        sprites  = self.SPRITES_JOGADOR[nome_da_spritesheet]
        sprite_index = (self.cont_animacao // self.DELAY_ANIMACAO) % len(sprites)
        self.imagem = sprites[sprite_index]
        self.cont_animacao += 1

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.rect.x, self.rect.y))

jogador = Jogador(400, 0)

tilemap = mapa.TileMap(DIR_PRINCIPAL, TAMANHO_BLOCO, INFORMACOES_MAPA)
lista_blocos = tilemap.gerar() # gerando  a lista de blocos que sera usada para as colisoes

while rodar:

    relogio.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jogador.tocando_chao == True:
                jogador.vel_y = -15
                jogador.tocando_chao = False # jogador nao esta mais no chao
    
    jogador.update()
    
    tela.fill(AZUL)

    tilemap.desenhar(tela,lista_blocos)

    jogador.desenhar(tela)

    pygame.display.update()
