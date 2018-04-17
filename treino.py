import numpy as np
import AIs
import pickle
import run

# SPSA - Simultaneous perturbacao stochastic approx
def spsa(f, teta, file_name = 'spsa_export',alfa=0.602, gamma=.101, a=5, big_a=None, c=20, iteracoes_max=1000, relatorio=10):
    """
    : param f: função para minimizar
    : param teta: input inicial
    : param alfa: Parâmetro - Ótimo mostrado para ser .101
    : param gamma: Parâmetro - Ótimo mostrado para ser 0,602
    : param big_a: menos de 10% de iteracoes_max
    : param a: a / (A + 1) ^ alfa aproximadamente igual às menores magnitudes de mudança desejadas
    : param c: Set c no nível aproximadamente igual ao st dev pode ser est. Não precisa ser preciso
    : param iteracoes_max: Número máximo de iterações permitido
    : param relatório: quantas vezes você deseja ver o relatório impresso
    : retorno: teta ótimo
    """

    if big_a is None:
        big_a = (iteracoes_max * .05)

    K = 0
    pontuacoes = []
    tetas = []
    # Para entender essas operações SPSA melhor, veja: http://www.jhuapl.edu/SPSA/PDF-SPSA/Matlab-SPSA_Alg.pdf
    while K < iteracoes_max:

        #Seleção Automática de Ganho
        a_n = a/(K + 1 + big_a)**alfa
        c_n = c/(K + 1)**gamma

        perturbacao = np.random.choice([1, -1], teta.shape)

        teta_maior = teta + c_n * perturbacao
        teta_menor = teta - c_n * perturbacao

        custo_maior = f(teta_maior)
        custo_menor = f(teta_menor)

        # - custo é específico para esta aplicação
        tetas.append(teta)

        ghat = (custo_maior - custo_menor)/(2 * c_n * perturbacao)
        teta = teta - a_n * ghat

        if relatorio > 0 and K > 0 and K % relatorio == 0:

            pontuacao = f(teta)
            pontuacoes.append(pontuacao)

            print('Execução {0}, pontuação da nova estratégia: {2}'
                  .format(K, relatorio, pontuacao))
            print('teta atual {0}'.format(teta))

            pickle.dump((teta, pontuacoes, tetas), open(file_name + ".p", "wb" ))

        K += 1

    return teta, pontuacoes, tetas


if __name__ == "__main__":
    
    # I.A. Baseada em Regras - (Rule Based)  #################
    regra_pontuacoes = []
    for regra in range(60, 81):
        ai = AIs.RuleBased(regra)
        for run in range(20):
            pontuacao = -ai.get_custo_performance(num_runs=1)
            regra_pontuacoes.append((pontuacao))
            print('++++++++++ PONTUAÇÃO +++++++++++ ' )
            print(regra_pontuacoes)
            pickle.dump(regra_pontuacoes, open("rule_cost_curve.p", "wb"))

    
    result = spsa(ai.get_performance_custo, ai.strategy, file_name='rule_based_60')


    run.run(ai=ai)
