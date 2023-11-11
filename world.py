#I am begginer and code was created just for fun so don`t judge

import pygame
import random
import copy


class Creature:
    def __init__(self, x, y, speed, vision):
        self.vision=vision
        self.speed=speed
        self.x=x
        self.y=y
        self.old_x=x
        self.old_y=y
        self.hunger = 2
    #checking for food
    def think(self):
        self.good_moves=[]
        self.hunger-=self.vision/10
        for A in range(self.vision*-1, self.vision+1):
            for B in range(self.vision*-1, self.vision+1):
                #creating copies of 'a' and 'b' in case they will be changed
                a=copy.copy(A)
                b=copy.copy(B)
                if self.y+a>=grid_size_width:
                    a -= grid_size_width
                if self.x+b>=grid_size_length:
                    b -= grid_size_length
                if board[self.y+a][self.x+b].food == True:
                    #eating
                    if a==b==0:
                        board[self.y][self.x].food = False
                        self.hunger+=2
                    else:
                        #using created copies
                        A=round(A/1.5)
                        B=round(B/1.5)
                        self.good_moves.append([A, B])
    def move(self):
        for i in range(self.speed):
            self.hunger-=0.2
            self.possible_surface=[]
            self.old_x=self.x
            self.old_y=self.y
            for A in [-1, 0, 1]:
                for B in [-1, 0, 1]:
                    #copies
                    a=copy.copy(A)
                    b=copy.copy(B)
                    if self.y+a>=grid_size_width:
                        a -= grid_size_width
                    if self.x+b>=grid_size_length:
                        b -= grid_size_length
                    if board[self.y+a][self.x+b].surface != 'water' and not a==b==0:
                        self.possible_surface.append([A, B])
                        
            abc = random.choice(self.possible_surface)
            end = False
            try:
                for try_move in self.possible_surface:
                    if end == True:
                        break
                    for good_move in self.good_moves:
                        if try_move == good_move:
                            abc = try_move
                            end=True
                            break
            except:
                pass


            try:
                self.y_move = abc[0]
                self.x_move = abc[1]
            except:
                pass

            self.x += self.x_move
            self.y += self.y_move
            if self.x>=grid_size_length:
                self.x-=grid_size_length
            elif self.x<=-1:
                self.x+=grid_size_length
            if self.y>=grid_size_width:
                self.y-=grid_size_width
            elif self.y<=-1:
                self.y+=grid_size_width
    def check_hit(self):
        for another_animal in alive_creatures:
            if another_animal.x == self.x and another_animal.y == self.y and another_animal != 'dead' and another_animal != self and self != 'dead':
                ind=alive_creatures.index(self)
                alive_creatures[ind]='dead'
                ind=alive_creatures.index(another_animal)
                alive_creatures[ind]='dead'


#Generation
class Cell:
    def __init__(self):
        self.clicked = False
        self.surface = None
        self.earth_chance = 0
        self.water_chance = 0
        self.sand_chance = 0
        self.food = False

alive_creatures = []

#using 1580, 
grid_size_length = 38
grid_size_width = 18
square_size = 1500//grid_size_length
board = [[Cell() for _ in range(grid_size_length)] for _ in range(grid_size_width)]

def Generation():
    for x in range(grid_size_width):
        for y in range(grid_size_length):
            board[x][y].food=False
            board[x][y].surface=None
            board[x][y].earth_chance=0
            board[x][y].water_chance=0
            board[x][y].sand_chance=0
    #food
    for i in range(15):
        board[random.randint(0,grid_size_width-1)][random.randint(0, grid_size_length-1)].food=True
    for x in range(grid_size_width):
        for y in range(grid_size_length):

            #Chances
            #earth_chance=int(input('Шанс землі'))
            #water_chance=int(input('Шанс води'))
            #sand_chance=int(input('Шанс піска'))
            sand_chance=2
            water_chance=5
            earth_chance=15
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if a==b==0:
                        pass
                    elif a==0 or b==0:
                        try:
                            earth_chance+=board[x+a][y+b].earth_chance*3
                            water_chance+=board[x+a][y+b].water_chance*3
                            sand_chance+=board[x+a][y+b].sand_chance*3
                        except:
                            pass
                    else:
                        try:
                            earth_chance+=board[x+a][y+b].earth_chance
                            water_chance+=board[x+a][y+b].water_chance
                            sand_chance+=board[x+a][y+b].sand_chance
                        except:
                            pass

            #Generation
                    if board[x][y].surface == None:
                        number = random.randint(1, sand_chance+water_chance+earth_chance)
                        if number <= earth_chance:
                            if random.randint(1, 5)==1:
                                board[x][y].surface='earth'
                            else:
                                board[x][y].surface='earth'
                            board[x][y].earth_chance+=20
                        elif number > earth_chance and number <= earth_chance+water_chance:
                            board[x][y].surface='water'
                            board[x][y].water_chance+=8
                        else:
                            board[x][y].surface='sand'
                            board[x][y].sand_chance+=15

Generation()

#Settings
pygame.init()
pygame.display.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([1580, 820])
text_surface_123 = my_font.render('1-Earth    2-Water    3-Sand', False, (0, 0, 0))
text_surface_space = my_font.render('SPACE-Regenerate', False, (0, 0, 0))
year_now=1
year_old=0

#Main loop
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        #editer
        elif event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                try:
                    col = (event.pos[1]-80) // square_size
                    row = (event.pos[0]-25) // square_size
                    click=True
                    color = (25, 25, 50)
                    while click==True:
                        clock.tick(30)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                    click = False
                                    running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                click=False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    click=False       
                                elif event.key == pygame.K_1:
                                    board[col][row].surface = 'earth'
                                    color = (0, 255, 0)
                                elif event.key == pygame.K_2:
                                    board[col][row].surface = 'water'
                                    color = (0, 0, 255)
                                elif event.key == pygame.K_3:
                                    board[col][row].surface = 'sand'
                                    color = (255, 255, 0)
                                #creating new creatures
                                elif event.key == pygame.K_f:
                                    alive_creatures.append(Creature(row, col, 1, 2))
                                    click=False
                                #create/destroy food
                                elif event.key == pygame.K_h:
                                    if board[col][row].food == False:
                                        board[col][row].food = True
                                    else:
                                        board[col][row].food = False
                        
                        pygame.draw.rect(screen, (color), (row*square_size+25, col*square_size+80, square_size-1, square_size-1))
                        pygame.display.flip()
                except:
                    pass
        #Regenerate
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                year_now+=1
            elif event.key == pygame.K_SPACE:
                try:
                    Generation()
                except:
                    pass

    #Draw cells/food
    screen.fill((255, 255, 255))
    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            if cell.surface=='sand':
                color = (255, 255, 0) 
            elif cell.surface=='water':
                color = (0, 0, 255)
            elif cell.surface=='earth':
                color = (0, 255, 0)
            elif cell.surface=='forest':
                color = (30, 85, 35)
            if cell.clicked==True:
                color = (25, 25, 50)
            pygame.draw.rect(screen, (color), (ix*square_size+25, iy*square_size+80, square_size-1, square_size-1))
            if cell.food==True:
                pygame.draw.rect(screen, (255, 0, 0), (ix*square_size+50, iy*square_size+105, square_size//4, square_size//4))
    #Draw creatures
    try:
        for animal in alive_creatures:
            pygame.draw.line(screen, (255, 0, 0), (animal.old_x*square_size+50, animal.old_y*square_size+105), (animal.x*square_size+50, animal.y*square_size+105), square_size//10)
            pygame.draw.rect(screen, (0, 0, 0), (animal.x*square_size+40, animal.y*square_size+95, square_size//2, square_size//2))
    except:
        pass
    #New year
    if year_now != year_old:
        year_old=year_now
        try:
            for animal in alive_creatures:
                    animal.think()
                    animal.move()
                    animal.check_hit()
                    if animal.hunger <= 0:
                        ind=alive_creatures.index(animal)
                        alive_creatures[ind]='dead'
        except:
            pass
    
    #Clear list from dead
    for x in range((len(alive_creatures)-1)):
        try:
            alive_creatures.remove('dead')
        except:
            break

    #Draw other
    screen.blit(text_surface_123, (25, 0))
    screen.blit(text_surface_space, (1250, 0))
    pygame.display.flip()   



pygame.quit()
