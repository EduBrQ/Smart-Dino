import pyautogui
import time
import game_frame

def run(ai=None, report=True):
    """
    Função principal, executar uma jogada

    : param ai: estratégia para usar
    """
    
    print('Iniciando em: ')
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    # Encontra a região de interesse e clica nela
    frame = game_frame.GameFrame()
    if frame.found_roi:
        frame.go_to_roi()
    else:
        print("Não consegui encontrar o jogo, mas não vou desistir!")
        return 0

    # dá um tempo para o jogo carregar e pressiona espaço para iniciar
    pyautogui.press('space')
    time.sleep(1)  # tempo da animação inicial passar
    game_on = True
    score = 0

    obstaculos_anteriores = frame.obstaculos_vazios
    ult_verificacao = time.time()

    # Inicia tempo de jogo
    game_start = time.time()
    while game_on:

        # Captura a tela e encontra os obstáculos e da uma pontuação-(score)
        game_img = frame.get_game_img()
        obstaculos = frame.find_obstaculos(game_img)
        score = time.time() - game_start

        # Às vezes, demora muito para carregar e nunca inicia, nesse caso, fica empacado.
        # Reinicia a função se ela for longa o suficiente no jogo, vendo um tabuleiro vazio e isso aconteceu no último loop
        if time.time() - ult_verificacao > 10:
            ult_verificacao = time.time()

            if obstaculos_anteriores == obstaculos:
                print('Parece que o jogo empacou. Reiniciando...')
                return run(ai=ai, report=report)

            obstaculos_anteriores = obstaculos

        # Chama a IA do jogo com o estado do jogo
        if ai.jump(obstaculos, score) >= .5:
            pyautogui.press('space')
            time.sleep(.5)  # para não apertarmos a barra de espaço e estragar tudo
            #pyautogui.keyDown('down')

        if frame.game_over(game_img):
            score = time.time() - game_start
            game_on = False
            # REINICIA
            pyautogui.hotkey('ctrl', 'r')

        #if frame.game_overn(game_img):
        #    score = time.time() - game_start
        #    game_on = False
            # REINICIA
        #    pyautogui.hotkey('ctrl', 'r')
        
        #if frame.pterodactiloChao(game_img):
        #    time.sleep(0.5)
        #    pyautogui.press('space') 

    return score

