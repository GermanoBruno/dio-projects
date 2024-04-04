import textwrap

class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []
        
    def __str__(self):
        return f"{', '.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}"
    
    def cadastrar_usuario(self, cpf, nome):
        if cpf in self.clientes:
            print("Usuario já cadastrado")
            return None
        
        usuario = Cliente(cpf, nome)
        self.clientes.append(usuario)
        
        return usuario
    
    def criar_conta(self, cpf):
        conta = ContaCorrente(cpf, len(self.contas)+1)
        self.contas.append(conta)
        return conta
        
    def acessar_usuario(self, cpf):
        if cpf in self.clientes:
            return self.clientes[self.clientes.index(cpf)]
        print("Usuário não encontrado")
        return None

class Cliente:
    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome
        self.contas = []    
    
    def __eq__(self, s) -> bool:
        return self.cpf == s
    
    def criar_conta(self, banco):
        conta = banco.criar_conta(self.cpf)
        self.contas.append(conta)
        print(f"Nova conta criada de numero {conta.numero}")
        return conta
    
    def acessar_conta(self, numero):
        if numero in self.contas:
            return self.contas[self.contas.index(numero)]
        print("Conta não encontrada")
        return None
    
    def listar_contas(self):
        print(f"Contas do cpf {self.cpf}:")
        print(f"{[each.numero for each in self.contas]}")

class ContaCorrente:
    def __init__(self, cpf, numero):
        self.usuario = cpf
        self.numero = numero
        self.saldo = 0
        self.limite = 500
        self.transacoes = []
        self.numero_saques = 0
        self.limite_saques = 5
    
    def __eq__(self, conta) -> bool:
        return self.numero == conta
        
    def depositar(self, quantia):
        self.saldo += quantia
        self.transacoes.append(f"DEPOSITO: {quantia}")
        print(f"Você depositou {quantia} reais. O seu novo saldo é de {self.saldo} reais")
        return self.saldo
    
    def sacar(self, quantia):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques excedido")
            return self.saldo
        if quantia > self.saldo:
            print("Não foi possível sacar. O saldo não é suficiente")
            return self.saldo
        self.saldo -= quantia
        self.numero_saques += 1
        self.transacoes.append(f"SAQUE: {quantia}")
        print(f"Você sacou {quantia} reais. O seu novo saldo é de {self.saldo} reais")
        
        return self.saldo

    def extrato(self, quantidade_transacoes=5):
        print("\n".join(self.transacoes[:quantidade_transacoes]))
        print(f"SALDO ATUAL: {self.saldo}")
        return self.transacoes

def menu(state):
    match state:
        case 0:
            # Menu inicial
            menu = """\n
            ================ MENU ================
            [l]\tLogin
            [c]\tCriar Usuario
            [q]\tSair
            => """
        case 1:
            # Usuario fora de conta
            menu = """\n
            ================ MENU ================
            [ac]\tAcessar conta
            [lc]\tListar contas
            [nc]\tNova conta
            [tu]\tTrocar usuário
            [q]\tSair
            => """
        case 2:
            # Usuario em conta
            menu = """\n
            ================ MENU ================
            [d]\tDepositar
            [s]\tSacar
            [e]\tExtrato
            [tc]\tTrocar conta
            [q]\tSair
            => """
    return input(textwrap.dedent(menu))


def main():
    b = Banco()
    state = 0
    while True:
        opcao = menu(state)
        match state:
            case 0:
                match opcao:
                    case "l":
                        cpf = input("Digite o seu CPF\n => ")
                        user = b.acessar_usuario(int(cpf))
                        if user is not None:
                            state = 1
                    case "c":
                        cpf = input("Digite o seu CPF\n => ")
                        nome = input("Digite o seu nome\n => ")
                        user = b.cadastrar_usuario(int(cpf), nome)
                        if user is not None:
                            state = 1
                    case "q":
                        break
                    case _:
                        print("Comando não disponível")
            case 1:
                match opcao:
                    case "ac":
                        num = input("Digite o seu numero de conta\n => ")
                        conta = user.acessar_conta(int(num))
                        if conta is not None:
                            state = 2
                    case "lc":
                        user.listar_contas()
                    case "nc":
                        conta = user.criar_conta(b)
                    case "tu":
                        print(f"Saindo do usuario {user.cpf}")
                        state = 0
                    case "q":
                        break
                    case _:
                        print("Comando não disponível")
            case 2:
                match opcao:
                    case "d":
                        quantia = input("Qual a quantia a ser depositada?\n=> ")
                        conta.depositar(int(quantia))
                    case "s":
                        quantia = input("Qual a quantia a ser sacada?\n=> ")
                        conta.sacar(int(quantia))
                    case "e":
                        conta.extrato()
                    case "tc":
                        print(f"Saindo da conta {conta.numero}")
                        state = 1
                    case "q":
                        break
                    case _:
                        print("Comando não disponível")

main()