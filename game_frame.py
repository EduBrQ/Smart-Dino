import cv2
import pyautogui
import os
from mss import mss
import numpy as np


class GameFrame(object):

    def __init__(self, img_limite=.6):
        """
        :param img_limite: Confiança em que você encontra uma imagem correspondente
        """
        self.img_limite = img_limite
        self.roi = None
        self.found_roi = False
        self.__find_roi()
        self.obstaculos_vazios = [600, 0]

    def get_game_img(self):
        """
        :return: Uma imagem em escala de cinza da região de interesse (ou a tela inteira, se nenhum roi foi passado)
        """
        with mss() as sct:
            if self.roi is None:
                filename = sct.shot(output='Imagens/fullscreen.PNG')
                screen_shot = cv2.imread(filename)
            else:
                screen_shot = sct.grab(self.roi)

        screen_shot = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_BGR2GRAY)

        return screen_shot

    def find_obstaculos(self, game_img, max_gap=50):
        """
        Obtém os obstáculos no quadro.
        : param game_img: A imagem cinza do tabuleiro de jogo
        : param max_gap: quantidade máxima de pixels permitidos entre obstáculos antes de serem chamados de dois obstáculos diferentes
        : param none_distance: Distância usada se nenhum obstáculo for encontrado
        : param none_width: Largura do obstáculo se nenhum for encontrado
        : retorno: Estado dos obstáculos - [localização obst 1, largura obst 1, localização obst 2, largura obst 2, ...]
        """

        # Obter o valor médio de pixel padrão para toda a imagem do jogo
        media = np.mean(game_img)
        std = np.std(game_img)

        # Obter valor médio de pixel para cada coluna na imagem
        media_col = np.mean(game_img, axis=0)

        # Encontre as colunas que são mais escuras do que a média (por 1 std). É aqui que estão os obstáculos!
        obstaculos = np.where(media_col < media - std)
        obstaculos = list(obstaculos[0])

        # Se nenhum obstáculo for encontrado, retorne o estado padrão
        if len(obstaculos) < 1:
            return self.obstaculos_vazios

        obstaculos_limpos = []
        start_obs = obstaculos[0]
        for pixel, next_pixel in zip(obstaculos, obstaculos[1:]):
            if next_pixel - pixel > max_gap:
                obstaculos_limpos.append(start_obs)
                obstaculos_limpos.append(pixel - start_obs + 1)
                start_obs = next_pixel

        obstaculos_limpos.append(start_obs)
        obstaculos_limpos.append(obstaculos[-1] - start_obs + 1)

        # Apenas mantenha o primeiro obstáculo
        if len(obstaculos_limpos) > 2:
            return obstaculos_limpos[:2]

        return obstaculos_limpos

    def game_over(self, game_img):
        """
        Descobre se o jogo acabou
        : param game_img: captura de tela do jogo
        Passado para cv2.matchTemplate
        : return: Boolean se o jogo terminou
        """
        game_over_img = cv2.imread(os.path.join('Imagens', 'game_over.PNG'), 0)
        res = cv2.matchTemplate(game_img, game_over_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val > self.img_limite

    def pterodactilo(self, game_img):
        pter_img = cv2.imread(os.path.join('Imagens', 'pter.PNG'), 0)
        res = cv2.matchTemplate(game_img, pter_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val > self.img_limite

    def pterodactiloChao(self, game_img):
        pter_img = cv2.imread(os.path.join('Imagens', 'pter_chao.PNG'), 0)
        res = cv2.matchTemplate(game_img, pter_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val > self.img_limite        

    def go_to_roi(self):
        pyautogui.moveTo(self.roi['left'] + self.roi['width']/2,
                         self.roi['top'] + self.roi['height']/2)
        pyautogui.click()

    def game_overn(self, game_img):
        game_over_img = cv2.imread(os.path.join('Imagens', 'game_over_night.PNG'), 0)
        res = cv2.matchTemplate(game_img, game_over_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val > self.img_limite

    def __find_roi(self):
        """
        Obtém a região de interesse (o jogo) na captura de tela.
        : return: top, left, width e height da região de interesse
        """
        dino_info = self.__find_dino()
        if not dino_info:
            return None

        # Obtém a largura e a altura do tabuleiro de jogo
        game_frame = cv2.imread(os.path.join('Imagens', 'roi.PNG'), 0)
        h, w = game_frame.shape

        roi = {
            'top': dino_info['top_left'][1] - dino_info['h'],
            'left': int(dino_info['top_left'][0] + dino_info['w']*1.5),
            'width': w - dino_info['w'],
            'height': 2 * dino_info['h']
        }
        self.roi = roi
        self.found_roi = True
    

    def __find_dino(self):

        """
        A imagem do dino é ideal para usar como modelo para encontrar a região de interesse. 
        captura a tela e procura pelo dino.
        : return: A localização do dino na imagem.
        """
       
        dino = cv2.imread(os.path.join('Imagens', 'dino.PNG'), 0)
        h, w = dino.shape

        screen_shot = self.get_game_img()
        res = cv2.matchTemplate(screen_shot, dino, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < self.img_limite:
            return None

        top_left = max_loc
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        return {'top_left': top_left, 'bottom_right': bottom_right, 'h': h, 'w': w}
        


        # ++++++++ NOITE +++++++++

        '''
    def __find_roin(self):

        dino_info = self.__find_dinon()
        if not dino_info:
            return None

        game_frame = cv2.imread(os.path.join('Imagens', 'roi_night.PNG'), 0)
        h, w = game_frame.shape

        roi = {
            'top': dino_info['top_left'][1] - dino_info['h'],
            'left': int(dino_info['top_left'][0] + dino_info['w']*1.5),  # add 50% onto the width (dino moves at start)
            'width': w - dino_info['w'],
            'height': 2 * dino_info['h']
        }
        self.roi = roi
        self.encontrar_roin = True
    

    def __find_dinon(self):
      

        dino = cv2.imread(os.path.join('Imagens', 'dino.PNG'), 0)
        h, w = dino.shape

        screen_shot = self.get_game_img()
        res = cv2.matchTemplate(screen_shot, dino, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # return none se não conseguirmos encontrar o dino dentro do limite
        if max_val < self.img_limite:
            return None

        top_left = max_loc
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        return {'top_left': top_left, 'bottom_right': bottom_right, 'h': h, 'w': w}
    '''
