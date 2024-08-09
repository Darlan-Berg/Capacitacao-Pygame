import pygame
import os

# CONSTANTES
DIMENSOES_TELA = (800, 400)
DIR_PRINCIPAL = os.path.abspath(os.getcwd())
DIR_IMAGENS = os.path.join(DIR_PRINCIPAL, 'imagens')
AZUL = (66, 135, 245)
VERDE = (81, 166, 105)
FPS = 60

# CARREGAMENTO DE IMAGENS
imagem_jogador = pygame.image.load(os.path.join(DIR_IMAGENS, 'quadrado.png'))
imagem_jogador = pygame.transform.scale(imagem_jogador, (50, 50))

# INICIALIZACAO
pygame.init()
tela = pygame.display.set_mode(DIMENSOES_TELA)
pygame.display.set_caption('Jogo Educativo')
relogio = pygame.time.Clock()
rodar = True

class Jogador:
    def __init__(self, x, y, imagem):
        self.x = x
        self.y = y
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.vel_y = 0 # e a velocidade com a qual o jogador e deslocado no eixo y
    
    def update(self):
        delta_x = 0
        delta_y = self.vel_y # e o deslocamento do jogador que e causado pela gravidade

        # aplicar gravidade ao jogador
        self.vel_y += 1
        if self.vel_y >= 5:
            self.vel_y = 5

        # coletar e tratar os inputs do teclado
        tecla_pressionada = pygame.key.get_pressed()
        if tecla_pressionada[pygame.K_LEFT] == True:
            delta_x -= 5
        elif tecla_pressionada[pygame.K_RIGHT] == True:
            delta_x += 5
        
        # checar colisoes no eixo y
        for plataforma in lista_plataformas:
            if plataforma.colliderect(pygame.rect.Rect(self.rect.x, (self.rect.y + delta_y), self.largura, self.altura)):
                if self.vel_y > 0: # jogador esta caindo
                    delta_y = plataforma.top - self.rect.bottom
                break
        
        # checar colisoes no eixo x
        for plataforma in lista_plataformas:
            if plataforma.colliderect(pygame.rect.Rect((self.rect.x + delta_x), self.rect.y, self.largura, self.altura)):
                if delta_x > 0: # jogador esta indo para direita
                    delta_x = plataforma.left - self.rect.right
                elif delta_x < 0: # jogador esta indo para esquerda
                    delta_x = plataforma.right - self.rect.left
                break
        
        # atualizar coordenadas do jogador
        self.x += delta_x
        self.y += delta_y
        self.rect.topleft = (self.x, self.y)
    
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.rect.x, self.rect.y))

lista_plataformas = [
    pygame.rect.Rect(0, 350, DIMENSOES_TELA[0], 50),
    pygame.rect.Rect(100, 50, 100, 300)
]

jogador = Jogador(400, 0, imagem_jogador)

while rodar:

    relogio.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False
    
    jogador.update()
    
    tela.fill(AZUL)

    # desenhar plataformas
    for plataforma in lista_plataformas:
        pygame.draw.rect(tela, VERDE, plataforma)

    jogador.desenhar(tela)

    pygame.display.update()
