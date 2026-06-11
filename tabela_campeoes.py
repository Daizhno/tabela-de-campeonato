import json    # jose M , importa a biblioteca json para manipulação de arquivos JSON
import random   # jose M , importa a biblioteca random para gerar números aleatórios 

times = {}    # jose M , vai servir como uma lista para cada time, porem cada time tera valores a mais com ele 
partidas = []   # jose M lista
artilheiros = {}  # jose M , dicionário para armazenar os artilheiros de cada time

def cadastrar_time(nome):   
    if nome in times:
        print(f"Time '{nome}' ja existe.")
        return
    times[nome] = {
        "pontos": 0,
        "vitorias": 0,
        "empates": 0,
        "derrotas": 0,
        "gols_pro": 0,
        "gols_contra": 0
    }
    artilheiros[nome] = {}
    print(f"Time '{nome}' cadastrado com sucesso!")


def registrar_partida(time_casa, gols_casa, time_fora, gols_fora, artilheiros_casa=None, artilheiros_fora=None):
    if time_casa not in times or time_fora not in times:            # jose m , none é um valor nulo , mas nao e zero , ele é usado para evitar que o codigo quebre 
        print("Um ou ambos os times nao estao cadastrados.")
        return  # Matheus  ele funciona como um while , so sai do loop quando a condiçao for falsa

    times[time_casa]["gols_pro"] += gols_casa
    times[time_casa]["gols_contra"] += gols_fora
    times[time_fora]["gols_pro"] += gols_fora
    times[time_fora]["gols_contra"] += gols_casa

    if gols_casa > gols_fora:
        times[time_casa]["pontos"] += 3
        times[time_casa]["vitorias"] += 1
        times[time_fora]["derrotas"] += 1
        resultado = f"{time_casa} venceu"
    elif gols_fora > gols_casa:
        times[time_fora]["pontos"] += 3
        times[time_fora]["vitorias"] += 1
        times[time_casa]["derrotas"] += 1
        resultado = f"{time_fora} venceu"
    else:
        times[time_casa]["pontos"] += 1
        times[time_fora]["pontos"] += 1
        times[time_casa]["empates"] += 1
        times[time_fora]["empates"] += 1
        resultado = "Empate"

    partida = {
        "casa": time_casa,
        "gols_casa": gols_casa,
        "fora": time_fora,
        "gols_fora": gols_fora,
        "resultado": resultado
    }
    partidas.append(partida)   # jose M , adiciona a partida ao histórico de partidas a lista 

    if artilheiros_casa:
        for jogador, gols in artilheiros_casa.items():
            artilheiros[time_casa][jogador] = artilheiros[time_casa].get(jogador, 0) + gols

    if artilheiros_fora:
        for jogador, gols in artilheiros_fora.items():
            artilheiros[time_fora][jogador] = artilheiros[time_fora].get(jogador, 0) + gols

    print(f"Partida registrada: {time_casa} {gols_casa} x {gols_fora} {time_fora} — {resultado}")


def exibir_tabela():
    if not times:
        print("Nenhum time cadastrado.")
        return

    ranking = sorted(       #jose M ,   o key, você diz pelo quê ordenar. Do maior paro o menor etc... 
        times.items(),     #Jose M , O lambda x é uma 'função anônima'. O x recebe cada item da lista, ou seja, cada tupla (nome, dados).
        key=lambda x: (x[1]["pontos"], x[1]["vitorias"], x[1]["gols_pro"] - x[1]["gols_contra"]),
        reverse=True   #jose M , o sorted ordena do menor pro maior. O reverse=True inverte a ordem para do maior pro menor, ou seja, os times com mais pontos aparecem primeiro.
    )

    print("\n" + "=" * 65)
    print(f"{'Pos':<4} {'Time':<15} {'Pts':>4} {'J':>4} {'V':>4} {'E':>4} {'D':>4} {'GP':>4} {'GC':>4} {'SG':>4}")
    print("=" * 65)        #jose  M esses:< sao quantos espaçoc (tecla espaco) tem de uma letra para outra

    for pos, (nome, s) in enumerate(ranking, start=1):   #para cada posiçao em (nome , s) in enumerate , que é a posiçao de cada elemento em sequencia 
        jogos = s["vitorias"] + s["empates"] + s["derrotas"]
        saldo = s["gols_pro"] - s["gols_contra"]
        print(f"{pos:<4} {nome:<15} {s['pontos']:>4} {jogos:>4} {s['vitorias']:>4} {s['empates']:>4} {s['derrotas']:>4} {s['gols_pro']:>4} {s['gols_contra']:>4} {saldo:>4}")

    print("=" * 65)


def exibir_artilheiros():
    print("\n--- ARTILHEIROS POR TIME ---")     # jose M , esse \n é uma quebra de linha
    for time, jogadores in artilheiros.items():
        if jogadores:
            print(f"\n{time}:")   # jose m , o f formata string para facilitar a leitura e a escrita de variáveis dentro de strings. O \n é uma quebra de linha, ou seja, ele pula para a próxima linha antes de imprimir o nome do time.
            ranking = sorted(jogadores.items(), key=lambda x: x[1], reverse=True)   # jose m , oq ocorre o sorteio é que ele ordena os jogadores pelo número de gols, do maior para o menor, graças ao reverse=True. O lambda x: x[1] indica que a ordenação deve ser feita com base no segundo elemento da tupla (nome do jogador, número de gols), ou seja, o número de gols.
            for jogador, gols in ranking:
                print(f"  {jogador}: {gols} gol(s)")


def exibir_historico():
    if not partidas:
        print("Nenhuma partida registrada ainda.")
        return
    print("\n--- HISTORICO DE PARTIDAS ---")
    for i, p in enumerate(partidas, start=1):
        print(f"{i}. {p['casa']} {p['gols_casa']} x {p['gols_fora']} {p['fora']} — {p['resultado']}")


def simular_rodada():
    nomes = list(times.keys())
    if len(nomes) < 2:   # Matheus , len é quantos times tem 
        print("Precisa de pelo menos 2 times para simular.")
        return # tem basicamente a mesma funçao do while , ele vai ficar em loop ate a condiçao ser falsa

    random.shuffle(nomes)
    print("\n--- SIMULACAO DE RODADA ---")  # Matheus , esse \n e uma quebra de linha , pulando para a proxima

    i = 0 # indice 
    while i + 1 < len(nomes):
        casa = nomes[i]
        fora = nomes[i + 1]              # Matheus , ele vai pegar o nome do time da casa e do time visitante , e depois gerar um numero aleatorio de gols para cada um
        gols_casa = random.randint(0, 4)
        gols_fora = random.randint(0, 4)
        registrar_partida(casa, gols_casa, fora, gols_fora)
        i += 2


def salvar_campeonato(arquivo="campeonato.json"):
    dados = {
        "times": times,
        "partidas": partidas,
        "artilheiros": artilheiros
    }
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"Campeonato salvo em '{arquivo}'.")


def carregar_campeonato(arquivo="campeonato.json"):
    global times, partidas, artilheiros
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        times = dados["times"]
        partidas = dados["partidas"]
        artilheiros = dados["artilheiros"]
        print(f"Campeonato carregado de '{arquivo}'.")
    except FileNotFoundError:
        print("Arquivo nao encontrado.")


def menu():
    #jose M , exibição do menu e loop de opções
    while True:
        print("\n=== SISTEMA DE CAMPEONATO ===")
        print("1. Cadastrar time")
        print("2. Registrar partida")
        print("3. Exibir tabela")
        print("4. Exibir artilheiros")
        print("5. Historico de partidas")
        print("6. Simular rodada")
        print("7. Salvar campeonato")
        print("8. Carregar campeonato")
        print("0. Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            nome = input("Nome do time: ").strip()
            cadastrar_time(nome)

        elif opcao == "2":
            casa = input("Time da casa: ").strip()
            gols_casa = int(input(f"Gols de {casa}: "))
            fora = input("Time visitante: ").strip()
            gols_fora = int(input(f"Gols de {fora}: "))
            art_casa = {}
            print(f"Artilheiros de {casa} (deixe em branco para encerrar):")
            while True:
                jogador = input("  Nome do jogador: ").strip()
                if jogador == "":
                    break
                gols = int(input(f"  Gols de {jogador}: "))
                art_casa[jogador] = art_casa.get(jogador, 0) + gols

            art_fora = {}
            print(f"Artilheiros de {fora} (deixe em branco para encerrar):")
            while True:
                jogador = input("  Nome do jogador: ").strip()
                if jogador == "":
                    break
                gols = int(input(f"  Gols de {jogador}: "))
                art_fora[jogador] = art_fora.get(jogador, 0) + gols

            registrar_partida(casa, gols_casa, fora, gols_fora, art_casa, art_fora)
        elif opcao == "3":
            exibir_tabela()

        elif opcao == "4":
            exibir_artilheiros()

        elif opcao == "5":
            exibir_historico()

        elif opcao == "6":
            simular_rodada()

        elif opcao == "7":
            salvar_campeonato()

        elif opcao == "8":
            carregar_campeonato()

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu()
