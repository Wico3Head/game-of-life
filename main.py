import pygame, time, os, random
import numpy as np

pygame.init()

current_dir = os.path.dirname(__file__)

randomButton = pygame.transform.rotozoom(pygame.image.load(os.path.join(current_dir, 'Assets/random.png')), 0, 1.8)
randomButtonRect = randomButton.get_rect(topright=(590, 40))
playButton = pygame.transform.rotozoom(pygame.image.load(os.path.join(current_dir, 'Assets/play.png')), 0, 1.8)
playButtonRect = playButton.get_rect(topright=(590, 80))

screenWidth = 600
screenHeight = 750
cells = 30
cellLength = screenWidth/cells

black = (0, 0, 0)
grey = (179, 179, 179)
darkGrey = (105, 105, 105)
backgroundColor = (252, 177, 0)
colors = [(255, 255-i*15, 0) for i in range(17)]
white = (255, 255, 255)


screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Conway's Game of Life")

def main():
    global game, gameState,  cells, cellLength
    game = np.zeros((cells, cells))
    gameState = np.zeros((cells, cells))
    play = False
    sliderRail = pygame.Rect(30, 65, 400, 20)
    sliderKnob = pygame.Rect(215, 55, 25, 40)
    randomClick()
    draw(sliderRail, sliderKnob)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    game = np.zeros((cells, cells))   
                    gameState = np.zeros((cells, cells))
                    draw(sliderRail, sliderKnob)
                elif event.key == pygame.K_ESCAPE:
                    print("return to menu")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[1] >= 150:
                    for i in range(cells):
                        for j in range(cells):
                            if i * cellLength <= mouse[0] < (i + 1) * cellLength and  j * cellLength <= mouse[1] - 150 < (j + 1) * cellLength:
                                game[i, j] = 1 if game[i, j] != 1 else 0
                                gameState[i, j] = 1 if game[i, j] == 1 else 0
                                draw(sliderRail, sliderKnob)
                elif sliderKnob.x <= mouse[0] < sliderKnob.x + sliderKnob.width and sliderKnob.y <= mouse[1] < sliderKnob.y + sliderKnob.height and not play:
                    dragging = True
                    while dragging:
                        for event in pygame.event.get():
                            if event.type != pygame.MOUSEBUTTONUP:
                                knobPos = pygame.mouse.get_pos()[0]
                                if knobPos < sliderRail.x:
                                    knobPos = sliderRail.x
                                elif knobPos > sliderRail.x + sliderRail.width - sliderKnob.width/2:
                                    knobPos = sliderRail.x + sliderRail.width - sliderKnob.width/2
                                sliderKnob.update((knobPos, 55), (25, 40))
                                draw(sliderRail, sliderKnob)
                            else:
                                dragging = False

                        changedCells = round((sliderKnob.x - sliderRail.x)/sliderRail.width*50) + 10
                        cellLength = screenWidth/changedCells
                        newGame = np.zeros((changedCells, changedCells))
                        newGameState = np.zeros((changedCells, changedCells))
                        for i in range(changedCells):
                            for j in range(changedCells):
                                if i < (changedCells if changedCells < cells else cells) and j < (changedCells if changedCells < cells else cells):
                                    newGame[i, j] = game[i, j]
                                    newGameState[i, j] = gameState[i, j]
                        game = newGame.copy()
                        gameState = newGameState.copy()
                        cells = changedCells
                        draw(sliderRail, sliderKnob)
                elif randomButtonRect.collidepoint(mouse):
                    randomClick()
                    draw(sliderRail, sliderKnob)
                elif playButtonRect.collidepoint(mouse):
                    play = not play
                    for i in range(cells):
                        for j in range(cells):
                            if game[i, j] == 1:
                                gameState[i, j] = 1
                    draw(sliderRail, sliderKnob)
    
        if play:
            move = (-1, 0, 1)
            newGame = np.zeros((cells, cells))
            for i in range(cells):
                for j in range(cells):
                    liveCells = 0
                    for xMove in move:
                        for yMove in move:
                            if not xMove == yMove == 0 and 0 <= i + xMove < cells and 0 <= j + yMove < cells:
                                liveCells += game[i + xMove][j + yMove]
                    if game[i, j] == 0:
                        newGame[i, j] = 1 if liveCells == 3 else 0
                    else:
                        newGame[i, j] = 1 if 2 <= liveCells <= 3 else 0

            play = False
            for i in range(cells):
                for j in range(cells):
                    if game[i, j] != newGame[i, j]:
                        play = True

            for i in range(cells):
                for j in range(cells):
                    if newGame[i, j] == 1:
                        gameState[i, j] += 1 if gameState[i, j] < 17 else 0
                    else:
                        gameState[i, j] = 0

            game = newGame.copy()
            if not play:
                for i in range(cells):
                    for j in range(cells):
                        if game[i, j] == 1:
                            gameState[i, j] = 1
            draw(sliderRail, sliderKnob)
            time.sleep(0.2)

    
    pygame.quit()

def randomClick():
    global game, gameState
    cellQuantity = cells**2
    game = np.zeros((cells, cells))
    gameState = np.zeros((cells, cells))
    amount = random.randint(int(cellQuantity*0.2), int(cellQuantity*0.4))
    while amount != 0:
        x = random.randint(0, cells-1)
        y = random.randint(0, cells-1)
        if game[y, x] == 0:
            game[y, x] = 1
            gameState[y, x] = 1
            amount -= 1

def draw(rail, knob):
    screen.fill(backgroundColor)
    pygame.draw.rect(screen, black, pygame.Rect(0, 150, 600, 600))
    railBorder = pygame.Rect(rail.x - 2, rail.y - 2, rail.width + 4, rail.height + 4)
    pygame.draw.rect(screen, black, railBorder)
    pygame.draw.rect(screen, darkGrey, rail)
    pygame.draw.rect(screen, grey, knob)
    knobBorder = pygame.Rect(knob.x - 2, knob.y - 2, knob.width + 4, knob.height + 4)
    pygame.draw.rect(screen, black, knobBorder)
    pygame.draw.rect(screen, grey, knob)
    screen.blit(playButton, playButtonRect)
    screen.blit(randomButton, randomButtonRect)

    for i in range(cells):
        for j in range(cells):
            if game[i, j] == 1:
                pygame.draw.circle(screen, colors[int(gameState[i, j])-1], (cellLength/2 + i*cellLength, 150 + cellLength/2 + j*cellLength), cellLength/2-1)
    pygame.display.update()

if __name__ == "__main__":
    main()