import pygame
import numpy as np
import math

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("APS04")

preto = (0, 0, 0)
vermelho = (255, 50, 133)


#me senti fazendo uma tabela verdade
vertices_cubo = np.array([
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1]
]) * 100

#tabela verdade pt2.0
vertices_tetraedro = np.array([
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1]
]) * 100

arestas_cubo = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
arestas_tetraedro = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]

def proj_ponto(ponto, dist):
    if ponto[2] != 0:
        fator_proj = dist / (dist - ponto[2])
    else:
        fator_proj = 1
    x = ponto[0] * fator_proj + largura // 2
    y = ponto[1] * fator_proj + altura // 2
    return [int(x), int(y)]

def rotacao(pts, angulo_x, angulo_y, angulo_z):
    rot_x = np.array([[1, 0, 0],
                      [0, math.cos(angulo_x), -math.sin(angulo_x)],
                      [0, math.sin(angulo_x), math.cos(angulo_x)]])
    
    rot_y = np.array([[math.cos(angulo_y), 0, math.sin(angulo_y)],
                      [0, 1, 0],
                      [-math.sin(angulo_y), 0, math.cos(angulo_y)]])
    
    rot_z = np.array([[math.cos(angulo_z), -math.sin(angulo_z), 0],
                      [math.sin(angulo_z), math.cos(angulo_z), 0],
                      [0, 0, 1]])

    
    #tudo em uma matriz só XD
    M = np.dot(np.dot(rot_x, rot_y), rot_z)
    
    rot_pts = np.dot(pts, M)
    
    return rot_pts

angulo_x, angulo_y, angulo_z = 0, 0, 0
velocidade_rot = 0.003
dist_proj = 500

mov_x, mov_y, mov_z = 0, 0, 0
mov_velocidade = 10

forma_atual = 'cubo' 

rodando = True
while rodando:
    tela.fill(preto)
    
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_t:
                forma_atual = 'tetraedro' if forma_atual == 'cubo' else 'cubo' #trocar entre os dois de forma bacana!!
    

    teclas = pygame.key.get_pressed()

    #fazer rodar doidamente
    if teclas[pygame.K_LEFT]:
        angulo_y -= 0.02
    if teclas[pygame.K_RIGHT]:
        angulo_y += 0.02
    if teclas[pygame.K_UP]:
        angulo_x -= 0.02
    if teclas[pygame.K_DOWN]:
        angulo_x += 0.02


    #"andar" 
    if teclas[pygame.K_a]:
        mov_x -= mov_velocidade
    if teclas[pygame.K_d]:
        mov_x += mov_velocidade
    if teclas[pygame.K_w]:
        mov_z += mov_velocidade
    if teclas[pygame.K_s]:
        mov_z -= mov_velocidade

    #cubo ou triangulo
    if forma_atual == 'cubo':
        vertices = vertices_cubo
        arestas = arestas_cubo
    else:
        vertices = vertices_tetraedro
        arestas = arestas_tetraedro

    forma_rot = rotacao(vertices, angulo_x, angulo_y, angulo_z)
    
    pontos_proj = []
    for vert in forma_rot:
        vert[0] += mov_x
        vert[1] += mov_y
        vert[2] += mov_z
        pontos_proj.append(proj_ponto(vert, dist_proj))
    
    for aresta in arestas:
        pygame.draw.line(tela, vermelho, pontos_proj[aresta[0]], pontos_proj[aresta[1]], 3)
    
    for vertice in pontos_proj:
        pygame.draw.circle(tela, vermelho, vertice, 5)
    
    angulo_x += velocidade_rot
    angulo_y += velocidade_rot
    angulo_z += velocidade_rot

    angulo_x %= 2 * math.pi
    angulo_y %= 2 * math.pi
    angulo_z %= 2 * math.pi

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
