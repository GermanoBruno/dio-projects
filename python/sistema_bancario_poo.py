from abc import ABC, abstractmethod
import textwrap

# Banco
class Banco:
    def __init__(self):
        self.agencia = "0001"
        self.clientes = []
        self.contas = []
        
    def __str__(self):
        return f"{', '.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}"
    
    def cadastrar_usuario(self, cpf, nome):
        if cpf in self.clientes:
            print("Usuario já cadastrado")
            return None
        
        usuario = PessoaFisica(cpf, nome)
        self.clientes.append(usuario)
        
        return usuario
    
    def criar_conta(self, numero, tipo):
        conta = Conta.nova_conta(tipo, numero, len(self.contas)+1)
        self.contas.append(conta)
        return conta
        
    def acessar_usuario(self, cpf):
        if cpf in self.clientes:
            return self.clientes[self.clientes.index(cpf)]
        print("Usuário não encontrado")
        return None

## Contas
class Conta:
    def __init__(self, numero, cliente, banco) -> None:
        self._saldo = 0
        self._numero = 1
        self._agencia = Conta.agencia
        self._cliente = cliente
        self._historico = Historico()
        self._banco = banco
        
        @classmethod
        def nova_conta(cls, numero, cliente):
            return cls(numero, cliente)
        
        @property
        def saldo(self):
            return self._saldo
        
        @property
        def numero(self):
            return self._numero
        
        @property
        def agencia(self):
            return self._agencia
        
        @property
        def cliente(self):
            return self._cliente
        
        @property
        def historico(self):
            return self._historico
        
        def sacar(self, valor):
            if valor < 0:
                print("Valor inválido")
                return False
            if saldo < valor:
                print("Operação falhou, saldo insuficiente")
                return False
            
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso!")
            return True
        
        def depositar(self, valor):
            if valor < 0:
                print("Valor inválido")
                return False
            
            self._saldo += valor
            print(f"Depósito de {valor} realizado com sucesso!")
            return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        if self._historico.contagem_tipo("Saque") >= self.limite_saques:
            print("Saque não permitido. Limite de saques excedido")
            return False
        if valor > self.limite_saques:
            print("Saque não permitido. Valor maior que o limite")
            return False
        
        return super().sacar(valor)

    def __str__(self) -> str:
        return f"Agência: {self.agencia}\nConta: {self.numero}\nTitular: {self.cliente.nome}"

## Clientes
class Cliente:
    def __init__(self) -> None:
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome) -> None:
        super().__init__()
        self.cpf = cpf
        self.nome = nome

## Transações
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod 
    @classmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        self.tipo = "Deposito"

    @property
    def valor(self):    
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        self.tipo = "Saque"
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
    
# Historico
class Historico:
    def __init__(self) -> None:
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
    
    def contagem_tipo(self, tipo):
        return len(filter(lambda x: x == tipo, [each.tipo for each in self.transacoes]))


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