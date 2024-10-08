import pygame
import numpy as np
import math

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("APS04")
preto = (0, 0, 0)
cor = (255, 50, 133)

# me senti fazendo uma tabela verdade
vert_cubo = np.array([
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1]
]) * 100
arestas_cubo = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), (0, 4), (1, 5), (2, 6), (3, 7)]


#tabela verdade pt2.0
vert_tri = np.array([
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1]
]) * 100
arestas_triangulo = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]



def rotacao(pts, angulo_x, angulo_y, angulo_z):
    Rx = np.array([[1, 0, 0],
                   [0, math.cos(angulo_x), -math.sin(angulo_x)],
                   [0, math.sin(angulo_x), math.cos(angulo_x)]])
    Ry = np.array([[math.cos(angulo_y), 0, math.sin(angulo_y)],
                   [0, 1, 0],
                   [-math.sin(angulo_y), 0, math.cos(angulo_y)]])
    Rz = np.array([[math.cos(angulo_z), -math.sin(angulo_z), 0],
                   [math.sin(angulo_z), math.cos(angulo_z), 0],
                   [0, 0, 1]])
    
    return np.dot(np.dot(np.dot(pts, Rx), Ry), Rz) #tudo em uma linha XD

'''
nao funciona de jeito nenhum a projeção da forma "correta" tive que fazer uma matriz um pouco diferente, 
talvez tenha feito besteira antes.
'''
def projecao_ponto(vertice, d):
    P = np.array([
        [0, 0, -d],
        [1, 0, 0],
        [0, 1/d, 0]
    ])
    
    ponto_proj = np.dot(P, vertice)
    return (largura // 2 + int(ponto_proj[1]), altura // 2 - int(ponto_proj[2]))


angulo_x, angulo_y, angulo_z = 0, 0, 0
v_rot = 0.01
rot = 0.005  
dis = 2
mov_x, mov_y, mov_z = 0, 0, 0
mov_v = 10
forma_atual = 'cubo' 

rodando = True
while rodando:
    tela.fill(preto)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_t:
                forma_atual = 'triangulo' if forma_atual == 'cubo' else 'cubo'  

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        angulo_y -= v_rot
    if teclas[pygame.K_RIGHT]:
        angulo_y += v_rot
    if teclas[pygame.K_UP]:
        angulo_x -= v_rot
    if teclas[pygame.K_DOWN]:
        angulo_x += v_rot
    if teclas[pygame.K_q]:
        angulo_z -= v_rot
    if teclas[pygame.K_e]:
        angulo_z += v_rot

    if teclas[pygame.K_w]:
        mov_y += mov_v
    if teclas[pygame.K_s]:
        mov_y -= mov_v
    if teclas[pygame.K_a]:
        mov_x -= mov_v
    if teclas[pygame.K_d]:
        mov_x += mov_v

    angulo_x += rot
    angulo_y += rot

    if forma_atual == 'cubo':
        vertices = vert_cubo
        arestas = arestas_cubo
    else:
        vertices = vert_tri
        arestas = arestas_triangulo

    vertices_rotacionados = rotacao(vertices, angulo_x, angulo_y, angulo_z)
    
    pontos_proj = [projecao_ponto(v + [mov_x, mov_y, mov_z], dis) for v in vertices_rotacionados]
    for aresta in arestas:
        pygame.draw.line(tela, cor, pontos_proj[aresta[0]], pontos_proj[aresta[1]], 2)
    
    pygame.display.flip()

    # se tirar isso ele fica girando que nem um maluco
    pygame.time.wait(10)

pygame.quit()
