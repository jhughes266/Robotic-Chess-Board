from managers.base_game_manager import GameManager

if __name__ == '__main__':
    gameManager = GameManager()
    while gameManager.startOrQuit():
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    print("Thanks for playing!")

