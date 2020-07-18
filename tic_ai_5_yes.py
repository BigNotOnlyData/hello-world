from math import inf as infinity
import random

random.seed(42)

class TicTacToe:
    def __init__(self):
        self.cords = [(1, 3), (2, 3), (3, 3),
                      (1, 2), (2, 2), (3, 2), 
                      (1, 1), (2, 1), (3, 1)]
        self.cords_d = {k: v for v, k  in enumerate(self.cords)}

    def display(self, board):
        print(f'''
    ---------
    | {" ".join(board[0:3])} |
    | {" ".join(board[3:6])} |
    | {" ".join(board[6:9])} |
    ---------
            ''')

    def move_sign(self, board, index):
        if board.count('X') > board.count('O'):
            board[index] = 'O'
        else:
            board[index] = 'X'
        return board   


    def get_winning_combos(self, board):
        return [
            {0: board[0], 1: board[1], 2: board[2]},
            {3: board[3], 4: board[4], 5: board[5]},
            {6: board[6], 7: board[7], 8: board[8]},
            {0: board[0], 3: board[3], 6: board[6]},
            {1: board[1], 4: board[4], 7: board[7]},
            {2: board[2], 5: board[5], 8: board[8]},
            {0: board[0], 4: board[4], 8: board[8]},
            {2: board[2], 4: board[4], 6: board[6]},
        ]


    def game_over(self, board):
        combo_win = self.get_winning_combos(board)
        combo_values = [list(c.values()) for c in [combo for combo in combo_win]]
        for com in combo_values:
            if com.count('X') == 3:
                return "X wins"
            elif com.count('O') == 3:
                return "O wins"
        if board.count(' ') == 0:
            return "Draw"        

                
    def start(self):
        option = ['user', 'easy', 'medium', 'hard']
        while True:
            command = input('Input command:').split()
            if command[0] == 'exit':
                exit()
            elif len(command) == 3 and command[0] == 'start' and\
                         command[1] in option and command[2] in option:
                play = Player()         
                play.players(command[1], command[2])
            else:
                print('Bad parameters!')    


class Player(TicTacToe):
    def __init__(self):
        super().__init__()
        self.board = [" "] * 9


    def players(self, x_player, o_player):
        if x_player == "user":
            self.x_player = User()
        else:
            self.x_player = Bot(x_player, 'X')

        if o_player == "user":
            self.o_player = User()
        else:
            self.o_player = Bot(o_player, 'O')

        self.play_round(self.board)    


    def play_round(self, board):
        while True:
            self.display(board)
            if board.count('X') > board.count('O'):
                self.o_player.make_move(board)
            else:
                self.x_player.make_move(board)

            if self.game_over(board) == "X wins":
                self.display(board)
                print("X wins")
                break
            elif self.game_over(board) == "O wins":
                self.display(board)
                print("O wins")
                break
            elif self.game_over(board) == "Draw":
                self.display(board)
                print("Draw")
                break        

class User(Player):
    def __init__(self):
        super().__init__()

    
    def make_move(self, board):
        valid = '123'                  
        while True:                 
            cells = tuple(input("Enter the coordinates: ").split())
            if not cells[0].isdigit() or not cells[1].isdigit():
                print("You should enter numbers!")  
                continue
            elif cells[0] not in valid or cells[1] not in valid:
                print("Coordinates should be from 1 to 3!")
                continue    
            else:
                cells = tuple(map(int, cells))
                index = self.cords_d[cells]
                if board[index] != ' ':
                    print("This cell is occupied! Choose another one!")
                    continue   
                self.move_sign(board, index)    
                break

class Bot(Player):
    def __init__(self, level, sign):
        super().__init__()
        self.sign = sign
        self.opponent_sign = 'X' if self.sign == "O" else 'O' 
        self.level = level
        self.scores = {self.opponent_sign: -100,
                   self.sign: 100,
                 'draw': 0}
        
           
    def make_move(self, board):
        if self.level == 'easy':
            print('Making move level "easy"')
            self.easy(board)
        elif self.level =='medium':
            print('Making move level "medium"')
            self.medium(board)
        elif self.level =='hard':
            print('Making move level "hard"')
            self.hard(board)    
    
    
    def easy(self, board):
        index = self.random_move(board)
        self.move_sign(board, index)

    
    def random_move(self, board): 
        possible_index =[ind for ind, val in enumerate(board) if val == ' '] 
        index = random.choice(possible_index)
        return index
        
    
    def medium(self, board):
        if board.count('X') > board.count('O'):
            index = self.priority(board, 'O', 'X')
        else:
            index = self.priority(board, 'X', 'O')

        if not index:
            index = self.random_move(board)                
        self.move_sign(board, index)   
    
    
    def priority(self, board, sign_1, sign_2):
        combo_win = self.get_winning_combos(board)
        combo_values = [list(c.values()) for c in [combo for combo in combo_win]]
        for ind, com in enumerate(combo_values):
            if com.count(sign_1) == 2 and com.count(' ') == 1:
                index = self.search_index(com, ind, board)
                return index
            elif com.count(sign_2) == 2 and com.count(' ') == 1:
                index = self.search_index(com, ind, board)
                return index

    
    def search_index(self, com, ind, board):
        combo_win = self.get_winning_combos(board)
        combo_keys = [list(c.keys()) for c in [combo for combo in combo_win]]                          
        index_val = com.index(' ')
        index_key = ind
        index = combo_keys[index_key][index_val]
        return index 

    
    def minimax(self, board, depth, TURN):
        if self.sign == 'O':
            if self.game_over(board) == "X wins":
                return self.scores[self.opponent_sign]
            if self.game_over(board) == "O wins":
                return self.scores[self.sign]
        else:
            if self.game_over(board) == "X wins":
                return self.scores[self.sign]
            if self.game_over(board) == "O wins":
                return self.scores[self.opponent_sign]            
        if self.game_over(board) == "Draw":
            return self.scores['draw']

        if depth == 0 or depth % 2 == 0:
            TURN = 'MAX'
            char = self.sign
        else:
            TURN = 'MIN'
            best_score = infinity
            char = self.opponent_sign

        all_scores = []
        for i in range(9):
            if board[i] == ' ':
                board[i] = char
                score = self.minimax(board, depth + 1, TURN)
                board[i] = ' '
                all_scores.append((i, score))

        best_score = max(all_scores, key=lambda k: k[1]) if TURN == 'MAX' else min(all_scores, key=lambda k: k[1]) 
        if depth == 0:
            return best_score[0]
        else:           
            return best_score[1]       

    
    def hard(self, board):
        index = self.minimax(board, 0, 'MAX')
        self.move_sign(board, index)
   

test = TicTacToe()
test.start()




        