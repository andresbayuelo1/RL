from consts import TILE_SIZE, TILE_MARGIN, TILE_LENGTH, GRID_SIZE, COLORS

class tile():
    def __init__(self, value):
        self.value = value
        
    def render(self, position, game, screen):
        font = game.font.SysFont('comicsansms', 32)
        text = font.render(str(self.value) , True, (0,0,0))

        text_rect = text.get_rect()
        text_rect.center = ( (position[0] * TILE_SIZE) + TILE_MARGIN + (TILE_LENGTH/2) , (position[1] * TILE_SIZE) + TILE_MARGIN + (TILE_LENGTH/2) )
        text_rect.width = TILE_LENGTH
        text_rect.height = TILE_LENGTH
        
        left = (position[0] * TILE_SIZE) + TILE_MARGIN 
        top  = (position[1] * TILE_SIZE) + TILE_MARGIN
        wh = (TILE_LENGTH, TILE_LENGTH)
        
        tile = game.Rect( (left, top), wh)
        try:
            color = COLORS[str(self.value)]
        except KeyError:
            if self.value > 2048:
                color = COLORS[str(2048)]
            else:
                color = (65, 65, 65)

        game.draw.rect(screen, color, tile)
        if self.value > 0:
            screen.blit(text, text_rect)
            game.display.update()

        
        
    
       
        
            
        
    
        