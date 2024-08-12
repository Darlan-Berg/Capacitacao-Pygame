import pygame
import os

class Bloco(pygame.sprite.Sprite):
    def __init__(self, dir_principal, x, y, nome_imagem, tamanho_bloco):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(dir_principal, 'imagens', 'blocos', nome_imagem)).convert()
        self.image = pygame.transform.scale(self.image, (tamanho_bloco, tamanho_bloco))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def desenhar(self, superficie):
        superficie.blit(self.image, (self.x, self.y))

class TileMap:
    def __init__(self, dir_principal, tamanho_bloco, informacoes_do_mapa):
        self.dir_principal = dir_principal
        self.tamanho_bloco = tamanho_bloco
        self.informacoes_do_mapa = informacoes_do_mapa
    
    def gerar(self):
        lista_blocos = []
        x, y = 0, 0
        for linha in self.informacoes_do_mapa:
            x = 0
            for item in linha:
                if item == 10:
                    bloco = Bloco(self.dir_principal, x * self.tamanho_bloco, y * self.tamanho_bloco, 'pedra.png', self.tamanho_bloco)
                    lista_blocos.append(bloco)
                if item == 962:
                    bloco = Bloco(self.dir_principal, x * self.tamanho_bloco, y * self.tamanho_bloco, 'terra.png', self.tamanho_bloco)
                    lista_blocos.append(bloco)
                if item == 930:
                    bloco = Bloco(self.dir_principal, x * self.tamanho_bloco, y * self.tamanho_bloco, 'grama.png', self.tamanho_bloco)
                    lista_blocos.append(bloco)
                x += 1
            y += 1
        return lista_blocos
    
    def desenhar(self, superficie, lista_blocos):
        for bloco in lista_blocos:
            superficie.blit(bloco.image, (bloco.rect.x, bloco.rect.y))