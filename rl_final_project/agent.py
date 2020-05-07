import random
import time
GAMMA = .9
actions = ['up', 'down', 'left', 'right']
states = []
class agent():
    def __init__(self):
        self.score = 0
        self.episode = 0
        self.iteration = 0
        self.history = []
        self.text = dict(episode = 0, iteration = 0)

    def reset(self, grid):
        grid.reset()
        self.score = 0
        self.iteration = 0

    def step(self, grid):
        
        action = random.choice(grid.possible_moves())
        grid.move(action)
        self.history.append( action )
        self.iteration += 1
        self._calculate_score(grid)

    def _calculate_score(self, grid):
        if grid.is_gameover():
            self.episode += 1
            self.reset(grid)
            time.sleep(5)
            self.score = grid.score
        else:
            self.score = grid.score

    def render(self, grid):
        self.text['episode'] = self.episode
        self.text['iteration'] = self.iteration
        grid.render(**self.text)

            

