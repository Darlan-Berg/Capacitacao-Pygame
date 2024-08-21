import pygame
import os

def carregar_sprites_jogador(caminho_listado, largura, altura, direcao=False):
    caminho = ''
    index_de_nomes = 0

    # juntar as partes do caminho passadas em caminho_listado
    for nome in caminho_listado:
        caminho = os.path.join(caminho, nome)

    nomes_spritesheets = os.listdir(caminho) # nomes_spritesheets contem os nomes dos arquivos que estao no diretorio sprites_jogador
    lista_spritesheets = []
    for spritesheet in nomes_spritesheets:
        lista_spritesheets.append(pygame.image.load(os.path.join(caminho, spritesheet)))
    
    todos_sprites = {}

    for spritesheet in lista_spritesheets:
        sprites = []
        for i in range(spritesheet.get_width() // largura):
            superficie_de_recorte = pygame.Surface((largura, altura), pygame.SRCALPHA, 32)
            rect = pygame.rect.Rect(i * largura, 0, largura, altura)
            superficie_de_recorte.blit(spritesheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(superficie_de_recorte, (64, 64)))
        
        if direcao == True:
            # criar chave no dicionario com os sprites da direita
            todos_sprites[nomes_spritesheets[index_de_nomes].replace('.png', '') + '_direita'] = sprites
            
            # criar chave no dicionario com os sprites da esquerda
            sprites_esquerda = []
            for sprite in sprites:
                sprites_esquerda.append(pygame.transform.flip(sprite, True, False))
            todos_sprites[nomes_spritesheets[index_de_nomes].replace('.png', '') + '_esquerda'] = sprites_esquerda
        
        else:
            todos_sprites[nomes_spritesheets[index_de_nomes].replace('.png', '')] = sprites

        index_de_nomes += 1
    
    return todos_sprites
