import numpy as np
from scipy.special import expit
from abc import ABCMeta, abstractmethod
import os
import pickle
import run


# Classe abstrata para todas os IAs
class AI(object):

    __metaclass__ = ABCMeta

    def __init__(self, estrategia_inicial=None):
        self.strategy = estrategia_inicial

    @abstractmethod
    def jump(self, obstacles, score):
        return 0

    # retorna a pontuação negativa
    # se a estratégia não funcionar, não há necessidade de executar o programa
    def get_custo_performance(self, strategy=None, num_runs=3):

        if strategy is not None:
            self.strategy = strategy

        estado_vazio = [600, 0]
        precisa_pular = [5, 1]

        # se ele pular quando não há nada na tela, então isso é ruim.
        if self.jump(estado_vazio, 1) > .5:
            return 0

        # É melhor pular se o obstáculo estiver mais proximo
        if self.jump(precisa_pular, 1) < .5:
            return 0

        custo = 0
        for _ in range(num_runs):
            custo += -run.run(ai=self, report=False)
        custo = custo/num_runs
        custo = int(round(custo))
        return custo


class RuleBased(AI):

    nome_arq = 'ruleBased.p'

    # Se nenhuma estratégia inicial for dada, procure se existe um modelo escolhido, se não tiver, crie um modelo aleatório
    def __init__(self, estrategia_inicial=None):

        if estrategia_inicial is not None:
            self.strategy = estrategia_inicial

        elif Logistic.nome_arq in os.listdir('AI_files'):
            self.strategy = pickle.load(open(os.path.join('AI_files', Logistic.nome_arq), 'rb'))

        else:
            print('nenhuma estratégia dada! Configurando para: random gaussian (0,1)')
            self.strategy = np.random.normal()

    def jump(self, obstacles, score):
        return obstacles[0] <= self.strategy

class RedeNeuralGenetica(AI):

    # Futura rede neural com algoritmo genetico
    # Instancia uma rede neural com 10 nós na camada oculta
    #nn = NeuralNetwork([10])
    #nn.fit(x_train, y_train)
    # saídas // probabilidades
    #nn.predict(x_test)

    pass


if __name__ == "__main__":
    print('Execute o arquivo treino.py')