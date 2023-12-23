import pygame #biblioteca de jogo do python
import os #para pegar caminhos
import random #gerar os canos de forma aleatória

widthScreen = 500 
heightScreen = 800

imagePipe = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imageFloor = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imageBackground = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagesBird = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]   #imagem para o pygame multiplicada por 2 (pasta, nome do arquivo)

pygame.font.init()
#inicializa a fonte
fontPoints = pygame.font.SysFont('arial', 50)
#define a fonte (família, tamanho)

class Bird:
    imgs = imagesBird
    # animações da rotação
    maximumRotation = 25 #parábola
    rotationSpeed = 20 #velocidade do angulo que ele faz
    timeAnimation = 5 #

    def __init__(self, x, y):
        self.x = x #posicao no eixo x
        self.y = y #posicao no eixo y
        self.angle = 0 #comeca reto
        self.speed = 0 #vai de cima para baixo, a cada tempo ele aumenta
        self.height = self.y #altura é a posicao no eixo
        self.time = 0 #tempo de animacao
        self.counterImage = 0 #se é a primeira, segunda ... imagem
        self.image = self.imgs[0] #a primeira

    #para ir para cima, ele diminui o eixo y, vai para a esquerda ele diminui o eixo x

    def jump(self):
        self.speed = -10.5 
        self.time = 0
        self.height = self.y

    def move(self):
        # calcular o deslocamento
        self.time += 1 #a cada frame
        deslocamento = 1.5 * (self.time**2) + self.speed * self.time #formula da aceleracao

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2 #quando jogar pra cima, dá um ganho extra

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50): 
            #onde ele tá, a ultima vez que ele pulou, se a posicao y tiver abaixo deixa
            if self.angulo < self.maximumRotation:
                self.angulo = self.maximumRotation
        else:
            if self.angulo > -90:
                self.angulo -= self.rotationSpeed

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.counterImage += 1

        #bater de asa do passaro
        if self.counterImage < self.timeAnimation:
            self.image = self.imgs[0] #a cada 5 frames eu mudo a imagem do passaro
        elif self.counterImage < self.timeAnimation*2:
            self.image = self.imgs[1]
        elif self.counterImage < self.timeAnimation*3:
            self.image = self.imgs[2]
        elif self.counterImage < self.timeAnimation*4:
            self.image = self.imgs[1]
        elif self.counterImage >= self.timeAnimation*4 + 1:
            self.image = self.imgs[0]
            self.counterImage = 0 #volta para o início


        # se o passaro tiver caindo eu não vou bater asa
        if self.angle <= -80:
            self.image = self.imgs[1]
            self.counterImage = self.timeAnimation*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.image, self.angle)
        pos_centro_imagem = self.image.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft) #a esquerda

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    #divide o quadrado criado em pixels
    #vai analizar se no mesmo pixel tem um cano e um passaro


class Pipe:
    distance = 200 #distancia entre os canos (cima e baixo)
    speed = 5 #movimenta fixo

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.afterTop = 0
        self.afterBase = 0
        self.pipeTop = pygame.transform.flip(imagePipe, False, True)
        self.pipeBase = imagePipe
        self.passe = False
        self.defineHeight()

    def defineHeight(self):
        self.height = random.randrange(50, 450) #o cano so pode ser criado daqui ate aqui
        self.afterTop = self.height - self.pipeTop.get_height() #altura do topo - altura do cano
        self.afterBase = self.height + self.distance #altura da base altura + a distancia entre os canos

    def move(self):
        self.x -= self.speed

    def desenhar(self, screen):
        screen.blit(self.pipeTop, (self.x, self.afterTop)) #uma tupla
        screen.blit(self.pipeBase, (self.x, self.afterBase))

    def colidir(self, bird):
        passaro_mask = bird.get_mask() 
        topo_mask = pygame.mask.from_surface(self.pipeTop) 
        base_mask = pygame.mask.from_surface(self.pipeBase)

        distancia_topo = (self.x - bird.x, self.pos_topo - round(bird.y))
        distancia_base = (self.x - bird.x, self.pos_base - round(bird.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Floor:
    speed = 5
    width = imageFloor.get_width()
    image = imageFloor

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def desenhar(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


def desenharScreen(screen, birds, pipes, floor, points):
    screen.blit(imageBackground, (0, 0))
    for bird in birds:
        bird.desenhar(screen)
    for pipe in pipes:
        pipe.desenhar(screen)

    texto = fontPoints.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(texto, (widthScreen - 10 - texto.get_width(), 10))
    floor.desenhar(screen)
    pygame.display.update()


def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((widthScreen, heightScreen))
    points = 0
    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        clock.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.pular()

        # mover as coisas
        for bird in birds:
            bird.move()
        floor.move()

        adicionar_cano = False
        remover_canos = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colidir(bird):
                    bird.pop(i)
                if not pipe.passou and bird.x > pipe.x:
                    pipe.passou = True
                    adicionar_cano = True
            pipe.move()
            if pipe.x + pipe.pipeTop.get_width() < 0:
                remover_canos.append(pipe)

        if adicionar_cano:
            points += 1
            pipes.append(Pipe(600))
        for pipe in remover_canos:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        desenharScreen(screen, birds, pipes, floor, points)


if __name__ == '__main__':
    main()