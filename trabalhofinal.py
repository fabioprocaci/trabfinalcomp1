
import random
import tkinter as tk
import time
from PIL import ImageTk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk
from tkinter import font


def main():
    dif_escolhida = dificuldade()
    global colunas
    colunas = dif_escolhida[0]
    global linhas
    linhas = dif_escolhida[1]

    while dif_escolhida[0]==0:
        scores=tk.Tk()
        scores.title("Scores")
        scores.resizable(0, 0)
        scores.geometry("+450+250")
        scores.config(background='SeaGreen1')
        mostrar_scores(scores)
        scores.mainloop()

        dif_escolhida=dificuldade()
        colunas = dif_escolhida[0]
        linhas = dif_escolhida[1]

    

    
    jogo = tk.Tk()
    jogo.title("Jogo da memoria")
    jogo.geometry("+450+150")
    jogo.resizable(0, 0)
    mesa(jogo)
    jogo.mainloop() 

def add(linhas, colunas,dif,janela_dif):
    dif.append(linhas)
    dif.append(colunas)
    janela_dif.destroy()


def dificuldade():
    dif = []
    janela_dif = tk.Tk()
    janela_dif.title("Dificuldade")
    janela_dif.resizable(0, 0)
    janela_dif.geometry("+450+250")
    facil = tk.Button(text="Fácil\n 12 cartas", width="20", height="10", bg="pale green",
                  command=lambda linhas=3, colunas=4: add(linhas, colunas,dif,janela_dif))
    facil['font']=font.Font(family='Helvetica',weight='bold',slant='italic',size=10)
    facil.pack(side=tk.LEFT)
    medio = tk.Button(text="Médio\n 24 cartas", width="20", height="10", bg="yellow green",
                  command=lambda linhas=4, colunas=6: add(linhas, colunas,dif,janela_dif))
    medio['font']=font.Font(family='Helvetica',weight='bold',slant='italic',size=10)
    medio.pack(side=tk.LEFT)
    dificil = tk.Button(text="Difícil\n 40 cartas", width="20", height="10", bg="saddle brown",
                  command=lambda linhas=5, colunas=8: add(linhas, colunas,dif,janela_dif))
    dificil['font']=font.Font(family='Helvetica',weight='bold',slant='italic',size=10)
    dificil.pack(side=tk.LEFT)


    scores = tk.Button(text="Pontuações Salvas", width="20", height="10", bg="green",
                  command=lambda linhas=0, colunas=0: add(linhas, colunas,dif,janela_dif))
    scores['font']=font.Font(family='Helvetica',weight='bold',slant='italic',size=10)
    scores.pack(side=tk.BOTTOM)

    janela_dif.mainloop()
    return dif




def mostrar_scores(scores):
    fonte=font.Font(family='MathJax_Fraftur',weight='bold',slant='italic',size=10)
    pontuacao=open('scores.txt','r')
    pontos=pontuacao.readlines()
    pontuacao.close()
    for i in range(len(pontos)):
        pontu= tk.Label(scores,text=pontos[i],bg='SeaGreen1',font=fonte)

        pontu.grid(column=6,row=6*i)
        



def ajustar(lista_desajustada):
    ajustada = []
    for i in range(0, len(lista_desajustada), linhas):
        ajustada.append(lista_desajustada[i:i + linhas])
    return ajustada


def mesa(jogo):
    tempo_inicial = time.time()
    valores = sortear_valores(jogo)
    imagem_padrao = ImageTk.PhotoImage(master=jogo, file="imagens/padrao.png")
    cartas = []
    for linha in range(colunas):
        for coluna in range(linhas):
            carta = tk.Button(jogo, image=imagem_padrao,
                                    command=lambda linha=linha, coluna=coluna:
                                    virar_carta(cartas, linha, coluna, valores, jogo, imagem_padrao, tempo_inicial))
            cartas.append(carta)
            carta.grid(column=coluna, row=linha)
    cartas = ajustar(cartas)
    return cartas


def sortear_valores(jogo):
    num_cartas = int(linhas*colunas/2)
    valores = []
    for i in range(num_cartas):
        caminho = 'imagens/valores/foto' + str(i) + '.png'
        imagem = ImageTk.PhotoImage(master=jogo, file=caminho)
        valores.append(imagem)
        valores.append(imagem)
    random.shuffle(valores)
    valores = ajustar(valores)
    return valores


def virar_carta(cartas, linha, coluna, valores, jogo, imagem_padrao, tempo_inicial):
    cartas[linha][coluna].config(image=valores[linha][coluna], bg="black")
    if not primeira(cartas):
        coord_primeira_carta = coordenadas_primeira(cartas, linha, coluna)
        x = coord_primeira_carta[0]
        y = coord_primeira_carta[1]
        if valores[linha][coluna] == valores[x][y]:
            cartas[linha][coluna].config(state=tk.DISABLED, bg="grey")
            cartas[x][y].config(state=tk.DISABLED, bg="grey")
            if ganhou(cartas):
                tempo_total = int(time.time() - tempo_inicial)
                pontuacao=105-tempo_total
                if pontuacao <0:
                    pontuacao=0
                
                salvar=messagebox.askquestion(title="parabéns!", message="Sua pontuação foi de: " + str(pontuacao) +' \n deseja salvar a pontuação?',)
                if salvar=='yes':

                    nome=simpledialog.askstring('Nome','Digite seu Nome')
                    arquivo= open('scores.txt','a')
                    arquivo.write(nome + ' : ' + str(pontuacao) + ' pontos ' + '\n')
                    arquivo.close()
                    
                cartas[linha][coluna].after(900, mesa, jogo)

        else:
            cartas[linha][coluna].after(600, desvirar, cartas, linha, coluna, x, y, imagem_padrao)


def primeira(cartas):
    j = 0
    for linha in range(colunas):
        for coluna in range(linhas):
            carta = cartas[linha][coluna]
            if carta["bg"] == "black":
                j += 1
    return j % 2 == 1


def coordenadas_primeira(cartas, linha, coluna):
    coord = []
    for i in range(colunas):
        for j in range(linhas):
            carta = cartas[i][j]
            if carta["bg"] == "black" and cartas[linha][coluna] != cartas[i][j]:
                coord.append(i)
                coord.append(j)
    return coord


def desvirar(cartas, linha, coluna, x, y, imagem_padrao):
    cartas[linha][coluna].config(image=imagem_padrao, bg="grey")
    cartas[x][y].config(image=imagem_padrao, bg="grey")


def ganhou(cartas):
    k = 0
    for i in range(colunas):
        for j in range(linhas):
            carta = cartas[i][j]
            if carta["state"] != tk.DISABLED:
                k += 1
    return k == 0



if __name__ == "__main__":
    main()