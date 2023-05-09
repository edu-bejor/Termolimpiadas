import socket, threading, pickle, random, time
import fsm

MAX_CLIENTS     = 2
DEFAULT_PORT    = 30000
DEBUGMODE       = True

palavrasValidas = ["termo","suite","avido","festa","bebia","honra","ouvir","pesco","fungo","pagam","ginga", \
    "pinta","poder","utero","pilha","sarar","fruta","piano","notar","musgo","tensa","melao","feliz","miojo",\
    "pagos","texto","mamae","ameno","chuva","coral","forte","tonta","temor","ligar","rolar","navio","limbo",\
    "calvo","fedor","balde","oxala","talco","labia","crime","grade","carta","flora","comum","fatal","pecar",\
    "feroz","virus","armar","couro","exito","ecoar","balao","falir","tecer","arena","justo","arido","ruiva",\
    "mumia","fogao","dupla","touca","sogro","osseo","treta","atomo","sadio","colon","patio","molas","certo",\
    "risco","bossa","porre","tigre","vocal","treze","sueco","verbo","latim","povos","longo","lotar","depor",\
    "cento","trava","latao","ditos","torax","polir","cacos","tunel","lindo","pegar","pilar","passo","piada",\
    "puxar","tacas","manta","barba","subir","tosse","adega","veias","mesma","mirim","mansa","nobre","grama",\
    "ritmo","samba","ardor","daqui","bravo","surfe","tanto","imune","lucro","finos","bocas","toldo","major",\
    "cabos","estar","focal","acões","queda","juros","elite","burro","fundo","duelo","breve","bolso","linha",\
    "parir","furar","quina","pasta","suino","dosar","cervo","sujar","corda","macia","reler","musas","verme",\
    "focar","macas","nocao","anual","aerea","cerco","socio","porca","fraco","punho","acima","varao","bolha",\
    "tanga","globo","rampa","goela","reais","cheio","fosso","pouco","danos","salas","mimar","sanha","oxido",\
    "suave","epoca","antro","total","joias","polvo","jejum","atriz","recuo","ageis","treno","fluir","muito",\
    "opera","ficar","bucha","magro","frota","serie","acido","apice","lider","idoso","multa","primo","garca",\
    "banal","juiza","jorro","sismo","merce","ponei","etapa","modas","colar","muita","papel","ruela","meias",\
    "gripe","causa","menor","nulos","caule","rubor","optar","redor","nacao","galho","roubo","parto","cenas",\
    "podio","lesar","telao","reuso","odiar","usual","latir","altos","livre","vosso","geada","etnia","trevo",\
    "rezar","bucal","vetor","filho","miolo","ordem","valor","filha","antes","vetar","surra","prata","ceder",\
    "pirao","frear","quilo","rombo","lomba","praia","urnas","aveia","picar","arcar","unica","magoa","jaula",\
    "gerar","trena","gemer","riste","labio","busto","visar","velha","aereo","adaga","crase","feras","missa",\
    "cobra","ideia","briga","dardo","berco","palmo","ralar","reles","blusa","super","grata","longa","tarso",\
    "vulto","lenda","grego","pinos","fluor","obeso","sauna","assim","troco","uteis","infra","pudor","cofre",\
    "prece","junho","manco","pisar","posse","copas","ninfa","gruta","regra","citar","mural","giria","ruina",\
    "fases","farao","miope","mando","frios","gelar","chave","sobra","opaco","lagos","corpo","doses","basco",\
    "caida","vinda","sujos","igual","lapis","julho","acaso","dados","favor","pente","beata","chulo","rumos",\
    "cubos","tento","toque","polpa","ombro","raras","pneus","canil","funil","perto","coala","amplo","orgia",\
    "doces","sobre","tedio","pinca","motel","trufa","voraz","azedo","coeso","acaro","calmo","enfim","mitos",\
    "feios","palha","andar","crepe","pingo","avela","malte","saida","monge","salto","lotus","rimel","lauda",\
    "damas","sadia","truco","serio","oeste","selva","reter","bolsa","anexo","renda","lobos","vicio","zebra",\
    "modos","praxe","pudim","birra","praca","pedra","olhar","pizza","banho","bucho","afins","maior","cabra",\
    "visao","irado","razao","macio","troca","salmo","casta","midia","trupe","morna","falso","lidar","afeto",\
    "verso","belos","pareo","video","denso","heroi","moeda","vaiar","copia","cocar","aulas","ganho","chapa",\
    "jarra","velho","grilo","sigma","farsa","sigla","clone","cesta","anjos","rugir","luzes","ardua","parvo",\
    "censo","virar","apito","gosto","casto","fraca","agudo","sovar","fatos","torso","tumba","veste","leões",\
    "secar","berro","sutis","bispo","locao","pesar","digno","bamba","broca","hiato","clube","totem","prumo",\
    "meios","vulgo","esqui","epico","minha","ainda","remar","manso","ousar","viral","ovulo","trote","artes",\
    "facas","brava","meiga","campo","levar","preta","lebre","pobre","gesso","sabia","freio","marte","clara",\
    "magos","reino","murro","calar","prosa","feita","folga","terco","patas","vogal","ziper","divas","borda",\
    "penar","errar","nevoa","morto","forma","aureo","vapor","circo","faixa","beijo","bufao","pedir","tropa",\
    "vital","vento","carie","vespa","negro","pardo","local","beato","quais","frase","sucos","botao","balsa",\
    "foice","nozes","dente","cedro","aceno","repor","leque","drama","forno","tarde","sarro","certa","trama",\
    "milho","dreno","carma","poeta","mafia","lenco","nunca","ficha","otica","molho","barao","cutis","toada",\
    "trens","chale","ciclo","leigo","golpe","haver","varal","ritos","fibra","nervo","irmas","sagaz","gente",\
    "pombo","zinco","pavor","feixe","pular","titia","deter","axila","brejo","rever","naipe","arder","entao",\
    "pleno","parma","juizo","noite","seiva","furor","janta","mover","vidro","votar","pilha","brasa","areal",\
    "jarro","pocos","ninja","nossa","boiar","outra","pires","regar","boato","sumir","lenta","loira","cinza",\
    "fisco","agora","lazer","pista","pulga","fosca","males","conto","tocha","retas","cuspe","persa","gemeo",\
    "tenda","aguia","meros","robos","lados","areia","impor","vigor","medio","matiz","orgao","senso","novas",\
    "turco","densa","balas","bicho","galao","atual","monte","tribo","tarda","baita","ampla","floco","banjo",\
    "olhos","gasto","facil","acesa","torto","horta","alcar","vivos","gaita","solto","cetro","redes","criar",\
    "sacro","banir","prato","gorro","miudo","moida","aliar","bater","fauna","norte","haste","alado","bloco",\
    "pinga","etico","corja","morno","ideal","fusao","verao","vozes","bilis","impar","sogra","jovem","testa",\
    "metal","falsa","bruto","tenso","dique","fator","sutil","grupo","matar","motor","meses","vazio","cujos",\
    "parda","carpa","arabe","plebe","advir","punir","rival","trave","trico","lento","sarda","gozar","caber",\
    "sexta","sacra","rolha","acude","casos","cisao","chata","ossos","expor","venda","casco","banco","bomba",\
    "sinal","horto","ramos","fonte","leito","cobre","tibia","cinco","noiva","ponto","aluno","traje","canal",\
    "rouco","boate","mutuo","caros","lente","lares","sacar","porem","feudo","vezes","carga","inves","presa",\
    "geral","negar","atuar","ciume","fiado","forca","corvo","gordo","tutor","duros","exame","caldo","cupim",\
    "otimo","mamar","indio","autos","pavio","fobia","jeito","votos","tesao","lagoa","pampa","diodo","parte",\
    "ambas","farda","sonar","bacon","gatas","banca","meigo","pavao","fixos","doido","valer","girar","fofas",\
    "caspa","opcao","macro","prego","perda","enjoo","longe","icone","ferro","braco","unida","licao","rocar",\
    "bambu","dorso","moral","ameba","viril","amora","magna","rural","penal","abuso","sunga","pocao","erros",\
    "surda","beber","cifra","movel","atras","farol","fugaz","zerar","menta","estes","venus","vista","final",\
    "nevar","norma","leste","nudez","telas","tinto","saber","bingo","cacau","fardo","morar","bioma","domar",\
    "grega","coice","ervas","medir","mista","atroz","raios","tosar","muros","santa","desde","posto","cesto",\
    "abril","penta","celta","mudar","cacho","bando","caixa","resto","libra","regua","calda","preto","tenue",\
    "vazar","reger","usina","vazia","todos","durar","rimar","angra","selos","alias","preco","bufar","nuvem",\
    "etica","lapso","uniao","civis","grito","bonus","cinto","matos","safra","algoz","letra","dogma","pesca",\
    "linho","tchau","graxa","casal","lidos","zonas","lorde","larva","gnomo","casca","botar","tinta","prado",\
    "ânimo","bacia","magia","saque","grato","bares","rolos","loura","obvio","viola","linda","sabio","cueca",\
    "santo","couve","susto","ostra","altar","furia","limpo","trair","idolo","deusa","usura","cacar","todas",\
    "obter","tampa","fossa","lavar","gueto","lunar","panda","vacuo","rigor","humor","pulso","terno","aneis",\
    "donos","coxao","civil","bocal","aroma","soldo","morro","coxas","cupom","jogos","furos","arcos","louca",\
    "peste","crise","homem","duplo","taxis","pauta","canja","cauda","dizer","rapaz","atlas","jogar","sitio",\
    "guiar","babar","trono","trigo","novos","massa","horas","junto","omega","salsa","pinho","brisa","ambos",\
    "guria","brega","motim","rumor","sutia","ducha","misto","farto","polen","debil","dicas","canto","cargo",\
    "seita","graus","baile","zelar","apelo","arroz","canoa","perna","tarja","vasos","fluxo","falar","dobro",\
    "orfao","leite","curso","comer","cisne","femea","cheia","lugar","prazo","letal","secao","fiapo","vinte",\
    "puxao","reves","clipe","tomar","manto","gesto","praga","audio","ânsia","tripe","licor","alibi","inato",\
    "lance","redea","mutua","vagao","lesma","beira","abono","salao","russo","caqui","pelos","servo","facao",\
    "barro","filme","rouca","nisto","corar","idade","lisos","selim","peixe","untar","sanar","grana","panos",\
    "relva","plena","besta","banda","sodio","feira","pompa","veloz","belas","poema","tecla","adeus","dobra",\
    "fruto","sorte","sabao","sushi","quibe","corno","tenis","tosco","valsa","lacre","fosco","nenem","clero",\
    "dever","duzia","racao","terca","sotao","fuzue","aviso","prole","costa","manga","metro","pirar","verde",\
    "unico","vacas","suado","fixar","loiro","fogos","dunas","radar","baixa","frevo","terra","calva","harpa",\
    "dueto","prova","pluma","irmao","justa","pagar","farpa","cerca","volei","rosca","euros","curar","fenda",\
    "farra","areas","unhas","nomes","tabua","gosma","capuz","ileso","lenha","perua","padre","fazer","tocar",\
    "bruxo","lojas","lerdo","nisso","golfo","topar","usada","ruivo","saude","nadar","lixar","vidas","pomba",\
    "exodo","acola","dotar","raiar","batom","ontem","torpe","oasis","cloro","curva","surto","ricos","ursos",\
    "hiena","vasta","risos","febre","fumar","forum","lutar","catar","trela","litro","surdo","menos","choro",\
    "chefe","vasto","cetim","traco","cilio","extra","greve","tapar","tufao","sarau","rosas","touro","trapo",\
    "lirio","abano","delta","cacao","anzol","sarna","clave","refem","hifen","claro","nasal","burra","conde",\
    "ponte","ondas","quota","mexer","verba","aonde","obras","idosa","signo","frias","lesao","mundo","genio",\
    "legal","tempo","âmbar","culta","vinho","livro","ninho","germe","culto","pasto","podre","mirar","teses",\
    "ebrio","naves","afago","laudo","ditar","selar","garra","folia","pedal","ninar","tirar","fugir","calor",\
    "naval","porta","âmago","ponta","calma","capaz","genro","almas","feias","senao","barco","zonzo","senha",\
    "focos","ossea","rosto","socar","carne","garfo","luvas","chiar","vazao","porco","gases","umido","boina",\
    "lacos","ferir","media","roupa","duque","bonde","tiros","avaro","exato","docil","basta","viver","placa",\
    "disso","poros","arame","outro","sopas","otima","bruxa","raiva","museu","astro","rente","lombo","bordo",\
    "cinta","manha","palco","peões","folha","treco","casar","louco","turvo","radio","tipos","somar","achar",\
    "macho","ajuda","times","meter","graca","mosca","milha","carro","algum","conta","nicho","sabor","natal",\
    "tatil","cerne","torta","apoio","simio","fetal","hotel","setor","vesgo","amada","firma","habil","calca",\
    "aspas","latas","quase","creme","telha","teias","assar","lousa","baque","rubro","fotos","adiar","dolar",\
    "polar","limao","lanca","coroa","pomar","tripa","mesmo","jegue","album","custo","futil","laico","dedos",\
    "ganso","visor","abrir","dedao","bazar","gerir","mania","rodar","turno","anões","sexto","palma","parco",\
    "pouso","moela","otico","aries","tenor","amido","solar","poste","urubu","coisa","seara","xampu","dieta",\
    "rocha","turma","paiol","vilao","nivel","pouca","vinil","frade","tonto","cavar","lilas","nariz","torre",\
    "parar","supor","gamba","cravo","arduo","tosca","clima","sosia","chato","moita","vagar","pausa","truta",\
    "podar","fucar","posar","autor","cruel","quica","aviao","retro","dores","credo","hinos","capim","tango",\
    "voces","jurar"]

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
