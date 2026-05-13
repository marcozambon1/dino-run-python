import pygame
import random

#inicializacao
pygame.init()
tela = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run")

pygame.mixer.init()
som_pulo = pygame.mixer.Sound("assets/sons/gta-menu.mp3")
som_colisao = pygame.mixer.Sound("assets/sons/faustao-errou.mp3")


#variavel de estado: 'menu', 'jogando', 'game_over'
estado_jogo = 'menu'

#dpersonagem dino
dino_index = 0 #frame atual, qual parte da animação esta sendo usada
dino_timer = 0 #contador de frames para trocar a animacao
velocidade_animacao = 0.2 
dino_x = 50
dino_y = 310
dino_vel_y = 0
gravidade = 1
pulando = False

#cacto
cacto_x = 800
cacto_y = 310
cacto_largura = 30
cacto_altura = 50
velocidade_jogo = 10

#animacao dinossauro
#carrega a sequência completa
sprite_sheet = pygame.image.load("assets/imagens/newdino/dino_walk_carry.bmp").convert()
sprite_sheet.set_colorkey((255, 0, 255))

dino_frames = []
#pega a largura total da imagem e dividimos por 8 que são a quantidade de animacoes
largura_total = sprite_sheet.get_width()
altura_total = sprite_sheet.get_height()
largura_frame = largura_total // 8 

# Carrega a imagem do cacto
cacto_img = pygame.image.load("assets/imagens/wild_cactus/wild_cactus_14.png").convert_alpha()

#ajuste de tamanho para bater com a largura e alturadefinida  nas variáveis
cacto_img = pygame.transform.scale(cacto_img, (cacto_largura, cacto_altura))

for i in range(8):
    #baseado na largura total
    subsurface = sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_total))
    subsurface = pygame.transform.scale(subsurface, (50, 50)) #ajustado para 50x50 pra melhor proporcao
    dino_frames.append(subsurface)

#pontuação
pontos = 0
caminho_fonte = "assets/fonte Press_Start_2P/PressStart2P-Regular.ttf"
fonte = pygame.font.Font(caminho_fonte, 20)

def exibir_texto(mensagem, cor, x, y):
    texto_formatado = fonte.render(mensagem, True, cor)
    tela.blit(texto_formatado, (x, y))

rodando = True
while rodando:
    #entradas do jogador
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                #no menu espaco comeca o jogo
                if estado_jogo == 'menu':
                    estado_jogo = 'jogando'
                
                #durante o jogo espaco pula
                elif estado_jogo == 'jogando' and not pulando:
                    dino_vel_y = -15 #velocidade do pulo
                    pulando = True
                    som_pulo.play()
                
                #no game over espaco reinicia
                elif estado_jogo == 'game_over':
                    estado_jogo = 'jogando'
                    cacto_x = 800
                    pontos = 0
                    dino_y = 308
                    dino_vel_y = 0

            if evento.key == pygame.K_q:
                if estado_jogo == 'game_over':
                    rodando = False
            
    #telas
    if estado_jogo == 'menu':
        tela.fill((200, 200, 200))
        exibir_texto("DINO RUN 8-BIT", (83, 83, 83), 275, 150)
        exibir_texto("Pressione ESPAÇO para começar", (100, 100, 100), 120, 200)

        
    elif estado_jogo == 'jogando':
        tela.fill((200, 200, 200))

        # --- FÍSICA ---
        dino_vel_y += gravidade
        dino_y += dino_vel_y
        if dino_y > 308:
            dino_y = 308
            dino_vel_y = 0
            pulando = False

        # --- ANIMAÇÃO ---
        if not pulando:
            dino_timer += velocidade_animacao
            if dino_timer >= len(dino_frames):
                dino_timer = 0
            dino_index = int(dino_timer)
        else:
            dino_index = 1 #trava o frame enquanto pula

        # --- OBSTÁCULOS E PONTOS ---
        cacto_x -= velocidade_jogo
        if cacto_x < -cacto_largura:
            cacto_x = 800 + random.randint(0, 300)

        pontos += 0.1 #a cada frame adiciona 6 pontos
        velocidade_jogo += 0.001


        # --- DESENHO E COLISÃO ---
        # Criamos o Rect para colisão (invisível) e desenhamos a imagem por cima
        dino_rect = pygame.Rect(dino_x, dino_y, 40, 40)
        cacto_rect = pygame.Rect(cacto_x, cacto_y, cacto_largura, cacto_altura)
        
        #Dino animado
        tela.blit(dino_frames[dino_index], (dino_x - 5, dino_y - 10))

        #Cacto
        tela.blit(cacto_img, (cacto_x, cacto_y))

        #chão e texto
        pygame.draw.line(tela, (150, 150, 150), (0, 340), (800, 340), 2)
        exibir_texto(f"Pontos: {int(pontos)}", (83, 83, 83), 550, 20)

        if dino_rect.colliderect(cacto_rect):
            som_colisao.play()
            estado_jogo = 'game_over'
        
    elif estado_jogo == 'game_over':
        tela.fill((0, 0, 0))
        exibir_texto("GAME OVER", (200, 0, 0), 320, 150)
        exibir_texto(f"Pontuação Final: {int(pontos)}", (235, 235, 235), 235, 200)
        exibir_texto("Pressione ESPAÇO para reiniciar", (100, 100, 100), 90, 250)
        exibir_texto("Pressione Q para sair", (100, 100, 100), 190, 300)

    pygame.display.flip()
    clock.tick(60) #jogo travado a 60fps

pygame.quit()