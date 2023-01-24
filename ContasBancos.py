from datetime import datetime
import pytz # ajuste de fuso horário
from random import randint


# criação da classe ContaCorrente
class ContaCorrente:
    """
    Cria um objeto ContaCorrente para gerenciar as contas dos clientes.

    Atributos:
        nome (str): Nome do cliente
        cpf (str): CPF do cliente
        agencia (int): Codigo da agência responsável pela conta do cliente
        num_conta (int): Número da conta do cliente
        saldo (float): Saldo disponível na conta do cliente (alterado apenas através dos métodos da classe)
        limite (float): Limite disponível em conta para cheque especial (definido no método _limite_conta)
        transacoes (list): Histórico das transações realizadas na conta do cliente (alterado apenas através dos métodos da classe)
    """

    # método estático para armazenar informações de data e hora
    @staticmethod
    def _data_hora():
        fuso_br = pytz.timezone('Brazil/East')
        horario_br = datetime.now(fuso_br)
        return horario_br.strftime('%d/%m/%Y %H:%M:%S')

    # atributos de instância
    def __init__(self, nome, cpf, agencia, num_conta):
        self.nome = nome
        self.cpf = cpf
        self._saldo = 0
        self._limite = None
        self.agencia = agencia
        self.num_conta = num_conta
        self._transacoes = []
        self.cartoes_credito = []

    # método consulta do saldo da conta
    def consultar_saldo(self):
        print('Seu saldo atual é de R$ {:_.2f}'.format(self._saldo).replace('.', ',').replace('_', '.'))

    # método depósito de valor
    def depositar_valor(self, valor):
        self._saldo += valor
        self._transacoes.append(('Depósito: R$ {}, Novo saldo: R$ {}, Data/Hora: {}'.format(valor, self._saldo, ContaCorrente._data_hora())))

    # método privado que define o limite para cheque especial
    def _limite_conta(self):
        self._limite = -1000
        return self._limite

    # método saque de valor
    def sacar_valor(self, valor):
        if self._saldo - valor < self._limite_conta():
            print('Saldo insuficiente para realizar a transação.')
            self.consultar_saldo()
        else:
            self._saldo -= valor
            self._transacoes.append(('Saque: R$ {}, Novo saldo: R$ {}, Data/Hora: {}'.format(-valor, self._saldo, ContaCorrente._data_hora())))

    # método para consultar limite de cheque especial
    def consultar_limite_chequeespecial(self):
        print('Seu limite de cheque especial é de R$ {:_.2f}'.format(self._limite_conta()).replace('.', ',').replace('_', '.'))

    # método para consulta do histórico de transações
    def historico_transacoes(self):
        print('Histórico de transações')
        for transacao in self._transacoes:
            print(transacao)

    # método para tranferência de valores entre instâncias (contas)
    def transferir_valor(self, conta_destino, valor):
        self._saldo -= valor
        self._transacoes.append(('Transferência: R$ {}, Novo saldo: R$ {}, Data/Hora: {}'.format(-valor, self._saldo, ContaCorrente._data_hora())))
        conta_destino._saldo += valor
        conta_destino._transacoes.append(('Transferência: R$ {}, Novo saldo: R$ {}, Data/Hora: {}'.format(valor, conta_destino._saldo, ContaCorrente._data_hora())))


class CartaoCredito:

    """
    Cria um objeto CartaoCredito para gerênciar os cartões de credito do cliente

    Atributos:
        num_cartao (int): Número do cartão do cliente (gerado aleatóriamente)
        validade (str):
    """

    # método estático para armazenar informações de data e hora
    @staticmethod
    def _data_hora():
        fuso_br = pytz.timezone('Brazil/East')
        horario_br = datetime.now(fuso_br)
        return horario_br

    # atributos de instância
    def __init__(self, titular, conta_corrente):
        self.num_cartao = randint(1000000000000000, 9999999999999999)
        self.validade = '{}/{}'.format(CartaoCredito._data_hora().month, CartaoCredito._data_hora().year + 5)
        self.cod_seguranca = '{}{}{}'.format(randint(0, 9), randint(0, 9), randint(0, 9))
        self.limite = 1000
        self.titular = titular
        self.conta_corrente = conta_corrente
        self._senha = '1234'
        conta_corrente.cartoes_credito.append(self)

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, valor):
        if len(valor) == 4 and valor.isnumeric():
            self._senha = valor
        else:
            print('Nova senha inválida.')