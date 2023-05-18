import socket, threading, pickle, random, time
import fsm

MAX_CLIENTS     = 2
DEFAULT_PORT    = 30000
DEBUGMODE       = True

palavrasValidas = ["pular", "nadar", "andar", "corre", "atira", "lutar", "bater", "nados", "remar", "chute", "jogar", "ganha", "perde", "passa", "finta", "girar", "lança", "dardo", "tocha", "alvos", "remos", "cesta", "bolas", "redes", "arcos", "aneis", "metro", "pista", "faixa", "campo", "trave", "ponto", "grupo", "tempo", "prata", "ouros", "podio", "hinos", "bikes", "mesas", "jogos", "sedes", "barco", "velas", "areia", "grama", "pesos", "linha", "verao", "aguas", "mares", "ondas", "final", "veloz", "lento", "perto", "longe", "lenda", "fases", "marca", "praia", "paris", "china", "japao", "alema", "suica", "chile", "egito", "india", "skate", "volei", "surfe", "esqui", "lutas", "golfe", "salto", "tenis", "canoa", "bocha", "polos", "salto"]

#clientes = {}
#numClientes = 0

"""
esperarClientes ==> gameloop ==> wait
                       /\         ||
                       ||         ||
                       \\=========//  """

fsm = fsm.FiniteStateMachine()
fsm.createState("esperarclientes",["gameloop"])
fsm.createState("gameloop", ["wait"])
fsm.createState("wait", ["gameloop"])
fsm.changeState("esperarclientes")

# nome, addr, info, text
class ClienteInfo:
    nome = ""
    addr = ""
    info = ""
    text = ""

# info, code, seg
class ServerInfo:
    info = ""
    code = ""

class GameLogic:
    global fsm
    state = fsm
    word = "TESTE"
    seg = 80
    winner = ""
    clientes = {}
    numClientes = 0
    numClientesParaIniciar = 1

logic = GameLogic()

print("\n \
  ________________  __  _______  _____ __________ _    ____________  \n \
 /_  __/ ____/ __ \/  |/  / __ \/ ___// ____/ __ \ |  / / ____/ __ \ \n \
  / / / __/ / /_/ / /|_/ / / / /\__ \/ __/ / /_/ / | / / __/ / /_/ / \n \
 / / / /___/ _, _/ /  / / /_/ /___/ / /___/ _, _/| |/ / /___/ _, _/  \n \
/_/ /_____/_/ |_/_/  /_/\____//____/_____/_/ |_| |___/_____/_/ |_|   \n \
")
print("             Proudly created by Elieder & Jose Team\n")

"""Retorna o IP local do host.

Returns:
    str: O número de IP associado à NIC na interface local.

"""
def getMyIP():
    ip = socket.gethostbyname(socket.gethostname())
    print("IP local:", ip)
    return ip

"""Abre um socket para o servidor.

Args:
    str IP: O IP para usar ao criar o socket.
    int porta: O número da porta usada no socket.

Returns:
    socket: Um manipulador para o socket criado.

"""
def socketCreate( ip, porta ):
    print("Criando o servidor...")
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.ioctl(socket.SIO_KEEPALIVE_VALS, (1,60000,1000))
    try:
        #if sys.argv[1]:
        # serv.bind((getMyIP(), int(sys.argv[1])))
        #else:
        serv.bind((ip, porta))
        print("Servidor aberto no IP {}.".format(ip, porta))
    except socket.error as e:
        print("Erro:", e)
    return serv


serv = socketCreate(getMyIP(), DEFAULT_PORT)
serv.listen(MAX_CLIENTS)
print("Servidor ouvindo a porta {}.".format(DEFAULT_PORT))


def broadcast( serverInfoObject ):
    global logic
    removeQueue = []
    for w in logic.clientes:
        try:
            logic.clientes[w]["socket"].send(pickle.dumps(serverInfoObject))
        except:
            removeQueue.append(w)
            print("Removendo o cliente {}.".format(logic.clientes[w]["nome"]))
    
    for w in removeQueue:
        del logic.clientes[w]


def placar():
    global logic
    result = ""
    for w in logic.clientes:
        result += str(logic.clientes[w]["nome"]) + ": " + str(logic.clientes[w]["pontuacao"]) + "\n"  
    return result



def gameLogicThread():
    global logic
    svinfo = ServerInfo()
    serverTicks = 0
    while True:
        serverTicks += 1
        if serverTicks > 2**31:
            serverTicks = 0
        if logic.state.getState() == "esperarclientes":
            if logic.numClientes == logic.numClientesParaIniciar:
                logic.state.changeState("gameloop")
                logic.word = palavrasValidas[random.randrange(0, len(palavrasValidas))].upper()
                print("\nIniciando uma nova rodada, palavra alvo: {}".format(logic.word))
                svinfo.code = 200
                svinfo.info = "gameloop"
                broadcast(svinfo)
            else:
                svinfo.code = 200
                svinfo.info = "Esperando por mais {} jogadores.".format(logic.numClientesParaIniciar - logic.numClientes)
                broadcast(svinfo)
        elif logic.state.getState() == "gameloop":
            if logic.numClientes > 0:
                if logic.seg > 0:
                    if logic.seg % 10 == 0:
                        print("Esta rodada terminará em {}s.".format(logic.seg))
                    logic.seg -= 1
                    svinfo.code = 700
                    svinfo.info = "Esta rodada terminará em {}s.".format(logic.seg)
                    broadcast( svinfo )
                    time.sleep(1)
                else:
                    logic.winner = "ninguem"
                    logic.seg = 9
                    logic.state.changeState("wait")
            else:
                logic.seg = 80
        elif logic.state.getState() == "wait":
            if logic.seg > 0 and not logic.winner == "ninguem":
                if logic.seg == 8:
                    print("{} ganhou e tem {} pontos. A palavra certa era {}.".format(logic.clientes[logic.winner]["nome"], logic.clientes[logic.winner]["pontuacao"], logic.word))
                print("Nova rodada em {}s".format(logic.seg))
                logic.seg -= 1
                svinfo.info = "{} ganhou.\nPONTUAÇÃO:\n{}\nA palavra certa era {}.\n\nNova rodada em {}s\n".format(logic.clientes[logic.winner]["nome"], placar(), logic.word, logic.seg)
                svinfo.code = 910
                broadcast( svinfo )
                time.sleep(1)
            elif logic.seg > 0 and logic.winner == "ninguem":
                if logic.seg == 8:
                    print("Ninguém ganhou. A palavra certa era {}.".format(logic.word))
                print("Nova rodada em {}s".format(logic.seg))
                logic.seg -= 1
                svinfo.info = "Ninguém ganhou.\nA palavra certa era {}.\n================\nPLACAR:\n\n{}\n================\nNova rodada em {}s\n".format(logic.word, placar(), logic.seg)
                svinfo.code = 910
                broadcast( svinfo )
                time.sleep(1)
            else:
                logic.state.changeState("gameloop")
                logic.word = palavrasValidas[random.randrange(0, len(palavrasValidas))].upper()
                print("\nIniciando uma nova rodada, palavra alvo: {}".format(logic.word))
                logic.seg = 80
                svinfo.info = "gameloop"
                svinfo.code = 200
                broadcast( svinfo )


def checarPalavra( palavra ):
    global logic
    palavra = palavra.upper()
    palavraCopia = logic.word
    resultado = ""
    for w in range( 5 ):
        if palavra[w] == logic.word[w]:
            resultado += "c"  # Letra Certa (posição certa)
        else:
            index = palavraCopia.find(palavra[w])
            if index > -1:
                resultado += "q"  # Letra Quase certa (posição errada)
                palavraCopia = palavraCopia[0:index:] + palavraCopia[index+1::]
            else:
                resultado += "e"  # Letra Errada

    if resultado == "ccccc":
        return True, resultado
    else:
        return False, resultado


def clientThread( con, IPPORT):
    global logic
    svInfo = ServerInfo()

    while True:
        try:
            data = con.recv(2048)
            data = pickle.loads(data)
            if data:
                if data.info == "login":
                    temp = ServerInfo()
                    temp.code = 200
                    temp.info = "Conectado!"
                    con.send(pickle.dumps(temp))
                    print("\n================ NOVO CLIENTE ================")
                    print("Usuário: {}, {}".format(data.nome, IPPORT))
                    print("Clientes online: {}\n\n".format(logic.numClientes))
                    logic.clientes[IPPORT]["nome"] = data.nome
                elif data.info == "gameloop":
                    print("{} enviou {}".format(data.nome, data.text))
                    teste, erros = checarPalavra( data.text )
                    if not teste:
                        temp.code = 900
                        temp.info = erros #c = letra certa, q = quase certa, e = letra errada
                        con.send(pickle.dumps(temp))
                    else:
                        logic.winner = IPPORT
                        logic.clientes[IPPORT]["pontuacao"] += 1
                        logic.seg = 9
                        logic.state.changeState("wait")
            else:
                print("Erro no recebimento de dados da conexão {}".format(con))
                break

        except socket.error as e:
            print(e)
            break

    logic.numClientes -= 1
    print("Clientes online:", logic.numClientes)
      

threading.Thread(target=gameLogicThread).start()

running = True
while running:
    sock, addr = serv.accept()
    tempNome = str(addr[0]) + ":" + str(addr[1])
    # TODO: tempNome é ip:porta, porém para bloquear ips que se conectam 2 vezes,
    # precisaria guardar o ip em logic.clientes de forma separada e checar apenas ele
    if tempNome in logic.clientes and not DEBUGMODE:
        print("IP {} chutado por tentar se conectar novamente.".format(addr[0]))
        temp = ServerInfo()
        temp.code = 404
        sock.send(pickle.dumps(temp))
    elif logic.numClientes == MAX_CLIENTS:
        temp = ServerInfo()
        temp.code = 502
        sock.send(pickle.dumps(temp))
    else:
        logic.clientes[tempNome] = {}
        logic.clientes[tempNome]["socket"] = sock
        logic.clientes[tempNome]["pontuacao"] = 0
        logic.numClientes += 1
        thread = threading.Thread(target=clientThread, args=(sock, tempNome)).start()
