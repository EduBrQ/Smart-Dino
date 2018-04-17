# Dino da Google

## Introdução

Trata-se de um jogo bem simples, onde o Dino precisa desviar dos obstaculos.

Para o código funcionar da melhor forma abra o jogo da seguinte forma:
	* Abra uma nova aba no Chrome;
	* Com o botão direito do mouse selecione "inspecionar";
	* Em network, marque a opção "offline";
	* Tente carregar qualquer link;
Pronto, nesse momento o game deve ter aparecido na tela.


#### Dependencias:

Crie uma virtualenv local, ou se preferir utilize alguma que já possui.
Então instale as dependências:
```
numpy
scipy
pyautogui
opnecv-python
mss
```
#### Iniciando:
```
$python treino.py
```
## Utilitarios

OpenCV para encontrar o local da tela onde está o jogo. 

Então é usado o MSS para capturar essa tela e deixar em escala de Cinza. 

Para encontrar os obstáculos: média dos valores dos pixels da coluna.
As colunas que forem escurar o suficiente serão obstáculos. 

A distancia entre a ação de pular do Dino e os obstaculos é definida assim:


<a href="http://www.codecogs.com/eqnedit.php?latex=s&space;=&space;\begin{bmatrix}&space;\text{Distancia&space;para&space;o&space;obstaculo&space;mais&space;proximo}&space;\\&space;\text{Largura&space;&space;do&space;obstaculo&space;mais&space;proximo}\\&space;\text{Segundos&space;desde&space;o&space;inicio}&space;\end{bmatrix}" target="_blank"><img src="http://latex.codecogs.com/gif.latex?s&space;=&space;\begin{bmatrix}&space;\text{Distance&space;to&space;the&space;nearest&space;obstacle}&space;\\&space;\text{Width&space;of&space;nearest&space;obstacle}\\&space;\text{Seconds&space;since&space;the&space;start}&space;\end{bmatrix}" title="s = \begin{bmatrix} \text{Distância para o obstáculo mais próximo} \\ \text{Largura do obstáculo mais próximo}\\ \text{Segundos desde o início} \end{bmatrix}" /></a>


## AIs 

Podemos pensar em nossa estratégia de IA como uma função que toma como entrada o estado * s * e retorna um escalar entre 0 e 1 de tal forma que se o escalar estiver acima de 0,5 o dinossauro deve pular.

O método fit da estratégia é o tempo de execução esperado do jogo. É impossivel medir diretamente o tempo de execução esperado, mas é possível obter uma estimativa usando a média de * n * execuções diferentes.


### Rule Based

Esta IA apenas diz "Se o obstáculo mais próximo estiver a menos de * x * pixels de distância, pule"


### SPSA

Foi utilizado o algoritmo SPSA (simultaneous perturbation stochastic approximation) para otimizar <a href="http://www.codecogs.com/eqnedit.php?latex=$\theta$" target="_blank"><img src="http://latex.codecogs.com/gif.latex?$\theta$" title="$\theta$" /></a> o vetor para obter a pontuação máxima esperada. O 'custo' de cada execução é implementado como a pontuação negativa para três execuções diferentes.

O SPSA foi escolhido porque usa somente medições de função, rápido (requer apenas duas medições de função de objetivo por iteração, independentemente da dimensão do problema de otimização).
