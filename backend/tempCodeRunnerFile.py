
   # print(game.board)
   # print(game.utility())
   # game.back(80)
   # print(game.board)
   # print(game.utility())
   while game.util.calculate_winner() == None:
      game.render()
      print("bot is thinking")
      move = game.ai_move()
      print(move)
      game.move(move)
      game.render()
      print('your turn: ')
      x = int(input())
      y = int(input())
      game.move(x * self.size + y)