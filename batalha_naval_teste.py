import random
import time
import os
from colorama import Fore, Style


TAMANHO_TABULEIRO = 10
NAVIOS = {
    'navio_grande': {'emoji': '🛳', 'tamanho': 3, 'posicoes_restantes': 3},
    'navio_medio': {'emoji': '🚢', 'tamanho': 2, 'posicoes_restantes': 2},
    'navio_pequeno': {'emoji': '⚓', 'tamanho': 5, 'posicoes_restantes': 5}
}
TOTAL_NAVIOS_PARTES = sum(navio['tamanho'] for navio in NAVIOS.values())

nome_jogador = input("Informe seu Nome: ")
total_pontos = 0


tabuleiro_real = []
tabuleiro_jogador = []
tentativas_restantes = 10
partes_acertadas = 0

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_tabuleiro():
    
    return [['🌊' for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]

def colocar_navios_aleatoriamente():
    
    global tabuleiro_real
    tabuleiro_real = criar_tabuleiro()
    
    for tipo_navio, dados in NAVIOS.items():
        tamanho = dados['tamanho']
        colocado = False
        while not colocado:
            orientacao = random.choice(['horizontal', 'vertical'])
            if orientacao == 'horizontal':
                linha = random.randint(0, TAMANHO_TABULEIRO - 1)
                coluna = random.randint(0, TAMANHO_TABULEIRO - tamanho)
                posicoes = [(linha, coluna + i) for i in range(tamanho)]
            else: # vertical
                linha = random.randint(0, TAMANHO_TABULEIRO - tamanho)
                coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
                posicoes = [(linha + i, coluna) for i in range(tamanho)]

            
            caminho_livre = True
            for r, c in posicoes:
                if tabuleiro_real[r][c] != '🌊':
                    caminho_livre = False
                    break
            
            if caminho_livre:
                for r, c in posicoes:
                    tabuleiro_real[r][c] = dados['emoji']
                colocado = True
                
tempo_inicial = time.time()                

def mostra_tabuleiro_batalha():
    
    limpar_tela()
    print("="*30)
    print("      TABULEIRO DE BATALHA NAVAL")
    print("="*30)
    print('   ' + ' '.join([str(i) for i in range(TAMANHO_TABULEIRO)]))
    print('  ' + '-' * (TAMANHO_TABULEIRO * 2 + 1))
    for i, linha in enumerate(tabuleiro_jogador):
        print(f"{i} |" + ' '.join(linha))
    print()

def faz_jogada():
    
    global tentativas_restantes, partes_acertadas, total_pontos
    
    while True:
        try:
            jogada = input("Digite a coordenada (ex: 2,5 para linha 2, coluna 5): ")
            if ',' not in jogada:
                raise ValueError("Formato incorreto. Use 'linha,coluna'.")
            
            linha, coluna = map(int, jogada.split(','))

            if not (0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO):
                print(Fore.RED + "Coordenada fora do tabuleiro. Tente novamente." + Style.RESET_ALL)
                time.sleep(2)
                continue
            
            if tabuleiro_jogador[linha][coluna] != '🌊':
                print(Fore.YELLOW + "Você já atirou aqui. Tente outra coordenada." + Style.RESET_ALL)
                time.sleep(2)
                continue
            
            
            if tabuleiro_real[linha][coluna] == '🌊':
                print(Fore.CYAN + "🌊 Você acertou a água! Sua vez termina." + Style.RESET_ALL)
                tabuleiro_jogador[linha][coluna] = '💧'
                tentativas_restantes -= 1
                time.sleep(2)
                return False 
            else:
                emoji_acertado = tabuleiro_real[linha][coluna]
                print(Fore.GREEN + f"🎉 Você acertou um navio! Continue atirando!" + Style.RESET_ALL)
                tabuleiro_jogador[linha][coluna] = emoji_acertado
                partes_acertadas += 1
                total_pontos += 10
                time.sleep(2)
                return True 
        
        except (ValueError, IndexError):
            print(Fore.RED + "Entrada inválida. Digite a linha e a coluna separadas por vírgula." + Style.RESET_ALL)
            time.sleep(2)

def main():
    
    global tabuleiro_jogador, tentativas_restantes, partes_acertadas
    
    print("="*30)
    print("      Batalha Naval")
    print("="*30)
    print(f"\nBem-vindo(a), {nome_jogador}! Vamos começar a Batalha Naval.")
    print("Tente afundar todos os navios em 10 tentativas!")
    input("Pressione Enter para começar...")
    
    colocar_navios_aleatoriamente()
    tabuleiro_jogador = criar_tabuleiro()

    while tentativas_restantes > 0 and partes_acertadas < TOTAL_NAVIOS_PARTES:
        mostra_tabuleiro_batalha()
        print(f"Tentativas restantes: {tentativas_restantes}")
        faz_jogada()
        
    
    limpar_tela()
    if partes_acertadas == TOTAL_NAVIOS_PARTES:
        print(f"{Fore.GREEN}PARABÉNS, {nome_jogador.upper()}! VOCÊ AFUNDOU TODOS OS NAVIOS E VENCEU! 🏆{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}SUAS TENTATIVAS ACABARAM. FIM DE JOGO!{Style.RESET_ALL}")
    
    print("\nEste era o tabuleiro dos navios:")
    print('   ' + ' '.join([str(i) for i in range(TAMANHO_TABULEIRO)]))
    print('  ' + '-' * (TAMANHO_TABULEIRO * 2 + 1))
    for i, linha in enumerate(tabuleiro_real):
        print(f"{i} |" + ' '.join(linha))

if __name__ == '__main__':
    main()
    
tempo_final = time.time()
duracao_jogo = tempo_final - tempo_inicial    
    
#----- Rotina para salvar os dados no arquivo ranking.txt
dados = []
if os.path.isfile("ranking.txt"):
  with open("ranking.txt", "r") as arq:
    dados = arq.readlines()

dados.append(f"{nome_jogador};{total_pontos};{int(duracao_jogo)}\n")

with open("ranking.txt", "w") as arq:
  for dado in dados:
    arq.write(dado)

#  (Ranking)
nomes = []
pontos = []
tempos = []

for dado in dados:
  partes = dado.split(";")
  nomes.append(partes[0])
  pontos.append(int(partes[1]))
  tempos.append(int(partes[2])*-1)


juntas = sorted(zip(pontos, tempos, nomes), reverse=True)

pontos2, tempos2, nomes2 = zip(*juntas)

print()
print("="*43)
print("---------< RANKING DOS JOGADORES >---------")
print("="*43)
print("Nº Nome do Jogador.........: Pontos Tempo.:")
        
for num, (nome, ponto, tempo) in enumerate(zip(nomes2, pontos2, tempos2), start=1):
  if nome == nome_jogador and ponto == total_pontos:    
    print(Fore.RED + f"{num:2d} {nome:25s}   {ponto:2d}   {tempo*-1:3d} seg", end="")
    print(Style.RESET_ALL)
  else:
    print(f"{num:2d} {nome:25s}   {ponto:2d}   {tempo*-1:3d} seg")    