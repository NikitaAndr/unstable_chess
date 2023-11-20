from Game.Visual_game import VisualGame


def main():
    game = VisualGame()
    print(game._board)
    game.load_gambit('Итальянка')
    game.start()


if __name__ == '__main__':
    main()
