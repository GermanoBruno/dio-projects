menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
class ContaCorrente:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.transacoes = []
        self.numero_saques = 0
        self.limite_saques = 5
        
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
    
cc = ContaCorrente()
while True:
    opcao = input(menu)

    if opcao == "d":
        quantia = input("Qual a quantia a ser depositada?\n=> ")
        cc.depositar(int(quantia))

    elif opcao == "s":
        quantia = input("Qual a quantia a ser sacada?\n=> ")
        cc.sacar(int(quantia))
    elif opcao == "e":
        cc.extrato()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")