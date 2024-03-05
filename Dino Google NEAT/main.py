import pygame
import os
import random
import math
import sys
import neat

pygame.init()

# Constantes
TELA_ALTU = 600
TELA_LARG = 1100
TELA = pygame.display.set_mode((TELA_LARG, TELA_ALTU))
DINO_IMG_DIR = 'C:/Users/drake/vsCode/PythonProjects/Dino Google Neat/Dino Google NEAT/Assets/Dino'
CACTUS_IMG_DIR = 'C:/Users/drake/vsCode/PythonProjects/Dino Google Neat/Dino Google NEAT/Assets/Cactus'
OTHER_IMG_DIR = 'C:/Users/drake/vsCode/PythonProjects/Dino Google Neat/Dino Google NEAT/Assets/Other'

# Carrega as imagens e as modifica, se necessario
CORRENDO = [pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun1.png")).convert_alpha(),
            pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun2.png")).convert_alpha()]

PULANDO = pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoJump.png")).convert_alpha()

ABAIXANDO = [pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoDuck1.png")).convert_alpha(),
             pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoDuck2.png")).convert_alpha()]

CORRENDO_PLAYER = [pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun1Player.png")).convert_alpha(),
                   pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun2Player.png")).convert_alpha()]

PULANDO_PLAYER = pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoJumpPlayer.png")).convert_alpha()

ABAIXANDO_PLAYER = [pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoDuck1Player.png")).convert_alpha(),
                    pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoDuck2Player.png")).convert_alpha()]

DINO_MAU = [pygame.transform.flip((pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun1.png"))), True,
                                  False).convert_alpha(),
            pygame.transform.flip((pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun2.png"))), True,
                                  False).convert_alpha()]

DINO_MAU_FOGE = [pygame.transform.flip((pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun1.png"))), False,
                                       False).convert_alpha(),
                 pygame.transform.flip((pygame.image.load(os.path.join(DINO_IMG_DIR, "DinoRun2.png"))), False,
                                       False).convert_alpha()]

CACTUS_PEQUENO = [pygame.image.load(os.path.join(CACTUS_IMG_DIR, "SmallCactus1.png")),
                  pygame.image.load(os.path.join(CACTUS_IMG_DIR, "SmallCactus2.png")),
                  pygame.image.load(os.path.join(CACTUS_IMG_DIR, "SmallCactus3.png"))]
CACTUS_GRANDE = [pygame.image.load(os.path.join(CACTUS_IMG_DIR, "LargeCactus1.png")),
                 pygame.image.load(os.path.join(CACTUS_IMG_DIR, "LargeCactus2.png")),
                 pygame.image.load(os.path.join(CACTUS_IMG_DIR, "LargeCactus3.png"))]
PASSARO = [pygame.transform.scale(pygame.image.load(os.path.join(CACTUS_IMG_DIR, "Bird.png")), (150, 95)),
           pygame.transform.scale(pygame.image.load(os.path.join(CACTUS_IMG_DIR, "Bird2.png")), (150, 95))]

BG = pygame.image.load(os.path.join(OTHER_IMG_DIR, "Track.png"))

COIN = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_IMG_DIR, "coin.png")), (65, 65)).convert_alpha()

# fonte
FONT = pygame.font.SysFont('comicsansms', 20, True, False)

# variaveis globais
recorde = 0
recordeNivel = 0
dinoMortos = 0
ticks = 30
simVel = 1


# Classe dos Individuos
class Dino:
    X_POS = 80
    Y_POS = 310
    VEL_PULO = 8.5

    def __init__(self, img=CORRENDO[0]):
        self.imagem = img
        self.dino_corre = True
        self.dino_pula = False
        self.dino_abaixa = False
        self.vel_pulo = self.VEL_PULO
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.indiceDePassos = 0
        self.timer = 0

    def atualizar(self):
        if self.dino_corre:
            self.correr()
        if self.dino_pula:
            self.pular()
        if self.dino_abaixa:
            self.abaixar()
        if self.indiceDePassos >= 10:
            self.indiceDePassos = 0
        if self.timer >= 5:
            self.dino_abaixa = False
            self.dino_corre = True
            self.timer = 0

    def pular(self):
        self.imagem = PULANDO
        self.dino_abaixa = False
        if self.dino_pula:
            self.rect.y -= self.vel_pulo * 4
            self.vel_pulo -= .8
        if self.vel_pulo <= -self.VEL_PULO:
            self.dino_pula = False
            self.dino_corre = True
            self.vel_pulo = self.VEL_PULO

    def correr(self):
        self.imagem = CORRENDO[self.indiceDePassos // 5]
        self.rect.y = self.Y_POS
        self.rect.x = self.X_POS
        self.indiceDePassos += 1
        self.dino_abaixa = False
        self.dino_pula = False

    def abaixar(self):
        self.imagem = ABAIXANDO[self.indiceDePassos // 5]
        self.dino_pula = False
        if self.dino_abaixa:
            self.rect.y = self.Y_POS + 30
        self.indiceDePassos += 1
        self.timer += 1

    def desenhar(self, TELA):
        TELA.blit(self.imagem, (self.rect.x, self.rect.y))
        # pygame.draw.rect(TELA, self.cor, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        """for inimigo in inimigos:
            if self.dino_abaixa:
                pygame.draw.line(TELA, self.cor, (self.rect.x + 84, self.rect.y + 12), inimigo.rect.topleft, 2)
                pygame.draw.line(TELA, self.cor, (self.rect.x + 84, self.rect.y + 12), inimigo.rect.bottomleft, 2)
            else:
                pygame.draw.line(TELA, self.cor, (self.rect.x + 54, self.rect.y + 12), inimigo.rect.topleft, 2)
                pygame.draw.line(TELA, self.cor, (self.rect.x + 54, self.rect.y + 12), inimigo.rect.bottomleft, 2)"""


# Classe do Player manual
class Player(Dino):
    def __init__(self):
        super().__init__()

    def pular(self):
        self.imagem = PULANDO_PLAYER
        self.dino_abaixa = False
        if self.dino_pula:
            self.rect.y -= self.vel_pulo * 4
            self.vel_pulo -= 0.8
        if self.vel_pulo <= -self.VEL_PULO:
            self.dino_pula = False
            self.dino_corre = True
            self.vel_pulo = self.VEL_PULO

    def correr(self):
        self.imagem = CORRENDO_PLAYER[self.indiceDePassos // 5]
        self.rect.y = self.Y_POS
        self.rect.x = self.X_POS
        self.indiceDePassos += 1
        self.dino_abaixa = False
        self.dino_pula = False

    def abaixar(self):
        self.imagem = ABAIXANDO_PLAYER[self.indiceDePassos // 5]
        self.dino_pula = False
        if self.dino_abaixa:
            self.rect.y = self.Y_POS + 30
        self.indiceDePassos += 1


# Classe dos inimigos
class Inimigo:
    def __init__(self, imagem, numero_do_inimigo):
        self.image = imagem
        self.tipo = numero_do_inimigo
        self.rect = self.image[self.tipo].get_rect()
        self.rect.x = TELA_LARG + 5
        self.voando = False
        self.name = 'Nenhum'

    def atualizar(self):
        global nivelDoJogo
        self.rect.x -= nivelDoJogo
        if self.rect.x < -self.rect.width:
            inimigos.pop()

    def desenhar(self, TELA):
        TELA.blit(self.image[self.tipo], self.rect)


class CactoPequeno(Inimigo):
    def __init__(self, image, numero_do_inimigo):
        super().__init__(image, numero_do_inimigo)
        self.rect.y = 325
        self.voando = False
        self.name = 'CactoP'


class CactoGrande(Inimigo):
    def __init__(self, image, numero_do_inimigo):
        super().__init__(image, numero_do_inimigo)
        self.rect.y = 300
        self.voando = False
        self.name = 'CactoG'


class DinoMauFoge:
    def __init__(self):
        super().__init__()
        self.indiceDePassosInimigo = 0
        self.imagem = DINO_MAU_FOGE[self.indiceDePassosInimigo // 5]
        self.rect = self.imagem.get_rect()
        self.rect.y = 310
        self.rect.x = TELA_LARG + 5
        self.voando = False
        self.name = 'DinoFoge'

    def atualizar(self):
        global nivelDoJogo
        self.rect.x -= nivelDoJogo
        if self.rect.x < -self.rect.width:
            inimigos.pop()

    def move(self):
        self.rect.x += 5
        self.imagem = DINO_MAU_FOGE[self.indiceDePassosInimigo // 5]
        self.indiceDePassosInimigo += 1
        if self.indiceDePassosInimigo >= 10:
            self.indiceDePassosInimigo = 0

    def desenhar(self, TELA):
        TELA.blit(self.imagem, self.rect)


class DinoMau(DinoMauFoge):
    def __init__(self):
        super().__init__()
        self.imagem = DINO_MAU_FOGE[self.indiceDePassosInimigo // 5]
        self.name = 'DinoVem'

    def move(self):
        self.rect.x -= 5
        self.imagem = DINO_MAU[self.indiceDePassosInimigo // 5]
        self.indiceDePassosInimigo += 1
        if self.indiceDePassosInimigo >= 10:
            self.indiceDePassosInimigo = 0


class Passaro(DinoMauFoge):
    def __init__(self):
        super().__init__()
        self.imagem = PASSARO[self.indiceDePassosInimigo // 5]
        self.rect.y = 220
        self.voando = True
        self.name = 'Passaro'

    def move(self):
        self.rect.x -= 5
        self.imagem = PASSARO[self.indiceDePassosInimigo // 5]
        self.indiceDePassosInimigo += 1
        if self.indiceDePassosInimigo >= 10:
            self.indiceDePassosInimigo = 0


class Coin:
    def __init__(self):
        self.image = COIN
        self.rect = self.image.get_rect()
        self.rect.x = TELA_LARG + 5
        self.rect.y = 150
        self.name = 'Coin'
        self.passos = 0
        self.PASSO = random.randint(5, 15)
        self.mod = False

    def atualizar(self):
        global nivelDoJogo
        self.rect.x -= nivelDoJogo
        if self.rect.x < -self.rect.width:
            inimigos.pop()
        self.passos += self.PASSO
        self.rect.y += self.passos
        if self.passos > 20:
            self.PASSO = -self.PASSO
            self.mod = True
        if self.passos < -20:
            self.PASSO = -self.PASSO
            self.mod = False

    def desenhar(self, TELA):
        TELA.blit(self.image, self.rect)


# função de remoção
def remove(index):
    global dinoMortos
    dinossauros.pop(index)
    ge.pop(index)
    redes.pop(index)
    dinoMortos += 1


# Calcula distancia
def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


# Função principal
def eval_genomes(genomes, config):
    global nivelDoJogo, x_pos_bg, y_pos_bg, inimigos, dinossauros, ge, ge2, redes, redes2, pontos, recorde, rand_int, inimigo, dinoMortos, ticks, simVel
    clock = pygame.time.Clock()
    pontos = 0

    inimigos = []
    dinossauros = []
    ge = []
    redes = []

    player = Player()

    x_pos_bg = 0
    y_pos_bg = 380
    nivelDoJogo = 20

    for genome_id, genome in genomes:
        dinossauros.append(Dino())
        ge.append(genome)
        rede = neat.nn.FeedForwardNetwork.create(genome, config)
        redes.append(rede)
        genome.fitness = 0

    def score():
        global pontos, nivelDoJogo, recorde, text2, recordeNivel, text3
        pontos += 1
        if pontos % 100 == 0:
            nivelDoJogo += 1
        if nivelDoJogo >= 41:  # 41 é o maximo possivel
            nivelDoJogo = 41

        if pontos > recorde:
            recorde = pontos
            # print(recorde)

        if nivelDoJogo > recordeNivel:
            recordeNivel = nivelDoJogo
            # print(recordeNivel)

        text = FONT.render(f'Pontos: {str(pontos)}', True, (0, 0, 0))
        text2 = FONT.render(f'Recorde: {str(recorde)}', True, (0, 0, 0))
        if recordeNivel < 41:
            text3 = FONT.render(f'Nível Recorde: {str(recordeNivel - 19)}', True, (0, 0, 0))
        else:
            text3 = FONT.render(f'Nível Recorde: Max', True, (0, 0, 0))
        TELA.blit(text, (900, 50))
        TELA.blit(text2, (900, 480))
        TELA.blit(text3, (900, 510))

    def statistics():
        global dinossauros, nivelDoJogo, ge, ge2, dinoMortos
        text_1 = FONT.render(f'Dinossauros Vivos: {str(len(dinossauros))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Geração: {p.generation}', True, (0, 0, 0))
        if nivelDoJogo < 41:
            text_3 = FONT.render(f'Nível de Jogo: {str(nivelDoJogo - 19)}', True, (0, 0, 0))
        else:
            text_3 = FONT.render(f'Nível de Jogo: Max', True, (0, 0, 0))
        text_4 = FONT.render(f'Já Morreram: {str(dinoMortos)}', True, (0, 0, 0))
        text_5 = FONT.render(f'Velocidade da Simulação: x{str(simVel)}', True, (0, 0, 0))

        TELA.blit(text_1, (50, 450))
        TELA.blit(text_2, (50, 480))
        TELA.blit(text_3, (50, 510))
        TELA.blit(text_4, (50, 540))
        TELA.blit(text_5, (50, 50))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        TELA.blit(BG, (x_pos_bg, y_pos_bg))
        TELA.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= nivelDoJogo

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    player.dino_pula = True
                    player.dino_corre = False

                if event.key == pygame.K_DOWN:
                    player.dino_abaixa = True
                    player.dino_corre = False

                if event.key == pygame.K_1:
                    ticks = 30
                    simVel = 1

                if event.key == pygame.K_2:
                    ticks = 60
                    simVel = 2

                if event.key == pygame.K_3:
                    ticks = 90
                    simVel = 3

                if event.key == pygame.K_4:
                    ticks = 120
                    simVel = 4

                if event.key == pygame.K_5:
                    ticks = 150
                    simVel = 5

                if event.key == pygame.K_6:
                    ticks = 300
                    simVel = 10

                if event.key == pygame.K_7:
                    ticks = 600
                    simVel = 20

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.dino_corre = True
                    player.dino_abaixa = False

        TELA.fill((255, 255, 255))

        """player.atualizar()
        player.desenhar(TELA)"""

        for dinossauro in dinossauros:
            dinossauro.atualizar()
            dinossauro.desenhar(TELA)

        if len(dinossauros) == 0:
            break

        if len(inimigos) == 0:
            rand_int = random.randint(0, 5)
            if rand_int == 0:
                inimigos.append(CactoPequeno(CACTUS_PEQUENO, random.randint(0, 2)))
            elif rand_int == 1:
                inimigos.append(CactoGrande(CACTUS_GRANDE, random.randint(0, 2)))
            elif rand_int == 2:
                inimigos.append(DinoMau())
            elif rand_int == 3:
                inimigos.append(DinoMauFoge())
            elif rand_int == 4:
                inimigos.append(Coin())
            elif rand_int == 5:
                inimigos.append(Passaro())

        for inimigo in inimigos:
            inimigo.desenhar(TELA)
            inimigo.atualizar()
            if rand_int == 2 or rand_int == 3 or rand_int >= 5:
                inimigo.move()

            for i, dinossauro in enumerate(dinossauros):

                ge[i].fitness += 1

                """if inimigo.rect.x < -inimigo.rect.width:
                    ge[i].fitness += 0.5 # 0.5 funcionou
                    ge2[i].fitness += 0.5  # 0.5 funcionou

                if pontos % 100 == 0:
                    ge[i].fitness += 3  # 3 funcionou
                    ge2[i].fitness += 3  # 3 funcionou"""

                if dinossauro.rect.colliderect(inimigo.rect):
                    """ge[i].fitness -= 5  # 5 funcionou
                    ge2[i].fitness -= 5  # 5 funcionou
                    if pontos < 500:
                        ge[i].fitness -= 5  # 5 funcionou
                        ge2[i].fitness -= 5  # 5 funcionou"""
                    ge[i].fitness -= 1
                    remove(i)

        for i, dinossauro in enumerate(dinossauros):
            output = redes[i].activate(
                (dinossauro.rect.y, nivelDoJogo, distance(dinossauro.rect.topright,
                                                          inimigo.rect.topleft), distance(dinossauro.rect.topright,
                                                          inimigo.rect.bottomleft)))

            if output[0] > .7 and dinossauro.rect.y == dinossauro.Y_POS:
                dinossauro.dino_pula = True
                dinossauro.dino_corre = False
            elif output[1] > .7 and dinossauro.rect.y >= dinossauro.Y_POS:
                dinossauro.dino_abaixa = True
                dinossauro.dino_corre = False
            # elif output[1] <= .7 and output[0] <= .7:
            #     pass
            # elif output[1] > .7 and output[0] > .7:
            #     pass
            else:
                pass

            # print(output, output2)
            # print(decisao1, decisao2)

        statistics()
        score()
        background()
        clock.tick(ticks)
        pygame.display.update()


# Setup the NEAT Neural Network
def run(config_path):
    global p, winner
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 100)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '../../Dino Google NEAT/Dino Google NEAT/config.txt')
    run(config_path)
