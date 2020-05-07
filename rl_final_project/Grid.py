from consts import GRID_SIZE, game_actions, WIN_VALUE, tile_MARGIN, GRID_SCREEN_SIZE, SCREEN_SIZE, BLACK
from tile import tile
from copy import deepcopy
import random

class grid():
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.score = 0
        self.highscore = 0
        self.reset()

    #Grid Initialization
    @staticmethod
    def _generate_empty_grid():
        grid = []
        for i in range(GRID_SIZE):
            grid.append([])
            for _ in range(GRID_SIZE):
                grid[i].append(tile(0))
        return grid
       
    def reset(self, hardreset=False):
        if self.score > self.highscore:
            self.highscore = self.score if not hardreset else 0
        self.score = 0
        self.grid = self._generate_empty_grid()
        self.spawn_new_tile()
        self.spawn_new_tile()

    def spawn_new_tile(self):
        new_tile = tile(4) if random.random() > .75 else tile(2)
        (i,j) = random.choice([(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j].value == 0])
        self.grid[i][j] = new_tile
    
    #Grid kinematics
    def move(self, event):
        def move_row_left(row):
            def tighten(row):
                new_row = [tile for tile in row if tile.value != 0]
                new_row += [tile(0) for i in range(len(row) - len(new_row))]
                return new_row
 
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(tile(2 * row[i].value))
                        self.score += 2 * row[i].value
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i].value == row[i + 1].value:
                            pair = True
                            new_row.append(tile(0))
                        else:
                        	new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))
        moves = {}
        moves['left']  = lambda _grid: [move_row_left(row) for row in _grid]
        moves['right'] = lambda _grid: self.reverse(moves['left'](self.reverse(_grid)))
        moves['up']    = lambda _grid: self.transpose(moves['left'](self.transpose(_grid)))
        moves['down']  = lambda _grid: self.transpose(moves['right'](self.transpose(_grid)))

        if event in game_actions.values():
            action = event
        elif event in game_actions:
            action = game_actions[event]
        else:
            return False

        if self.move_is_possible(action):
            self.grid = moves[action](self.grid)
            self.spawn_new_tile()
            return True
        else:
            return False

    def move_is_possible(self, direction):
        def row_is_left_moveable(row):
            def change(i):
                if row[i].value == 0 and row[i+1].value != 0:
                    return True
                if row[i].value != 0 and row[i+1].value == row[i].value:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))
        
        check = {}
        check['left']  = lambda _grid: any(row_is_left_moveable(row) for row in _grid)
        check['right'] = lambda _grid : check['left'](self.reverse(_grid))
        check['up']    = lambda _grid : check['left'](self.transpose(_grid))
        check['down']  = lambda _grid : check['right'](self.transpose(_grid))
        if direction in check:
            return check[direction](self.grid)
        else:
            return False
    
    def possible_moves(self):
        return [move for move in set(game_actions.values()) if self.move_is_possible(move)]
    
    #Grid Logic
    def reverse(self, grid):
        new_grid = []
        for i in range(GRID_SIZE):
            new_grid.append([])
            for j in range(GRID_SIZE):
                new_grid[i].append(grid[i][len(grid[0]) - j - 1])
        return new_grid
        
    def transpose(self, grid):
        new_grid = []
        for i in range(GRID_SIZE):
            new_grid.append([])
            for j in range(GRID_SIZE):
                new_grid[i].append(grid[j][i])
        return new_grid

    def is_win(self):
        return any(any(tile.value >= WIN_VALUE for tile in row) for row in self.grid)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in game_actions.values())
 
    # Grid rendering
    def _draw_text(self, **kwargs):
        font = self.game.font.SysFont('comicsansms', 24)
        #SCORE
        score_text = font.render('score: {}'.format(self.score) , True, BLACK)
        score_rect = score_text.get_rect()
        score_rect.left   = tile_MARGIN 
        score_rect.top    = GRID_SCREEN_SIZE
        self.screen.blit(score_text, score_rect)

        #HIGH SCORE
        highscore_text = font.render('highscore: {}'.format(self.highscore) , True, BLACK)
        highscore_rect = score_text.get_rect()
        highscore_rect.left   = score_rect.left 
        highscore_rect.top    = score_rect.top + score_rect.height
        self.screen.blit(highscore_text, highscore_rect)
        # other text to display
        prev_rect = score_rect
        for i, (key, value) in enumerate(kwargs.items()):
            text = font.render('{}: {}'.format(key, value), True, BLACK)
            rect = text.get_rect()
            rect.left = prev_rect.left + prev_rect.width
            rect.top  = prev_rect.top  + prev_rect.height
            self.screen.blit(text, rect)
            prev_rect = rect

    def render(self, **kwargs):
        update_text_rect = self.game.Rect(0, GRID_SCREEN_SIZE + tile_MARGIN , SCREEN_SIZE, SCREEN_SIZE - GRID_SCREEN_SIZE)
        self.game.draw.rect(self.screen, (127,127,127), update_text_rect)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # for some reason indices must be transposed
                self.grid[i][j].render((j,i), self.game, self.screen)
        self._draw_text(**kwargs)
        self.game.display.flip()

