import pygame, sys
from random import randint
from pygame.math import Vector2
pygame.init()

cell_size = 40
cell_number = 20
screen_l = cell_size*cell_number

screen = pygame.display.set_mode((screen_l, screen_l))
clock = pygame.time.Clock()

color1 = ((242, 211, 123))
color2 = ((240, 222, 173))
txt_font = pygame.font.Font('Python/Snake Game/Amatic-Bold.ttf', 40)

menu_text = txt_font.render("Press SPACE to start!", True, "White")

cake = pygame.image.load("Python/Snake Game/cake.png")
cake = pygame.transform.scale(cake, (cell_size, cell_size))
cake_rect = cake.get_rect()

eat_cake = pygame.mixer.Sound("Python/Snake Game/eat.mp3")
background_song = pygame.mixer.Sound("Python/Snake Game/soundtrack.mp3")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)
background_song.play(-1)

class Fruit():
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        cake_rect = pygame.Rect(self.x_pos, self.y_pos, cell_size, cell_size)
        #pygame.draw.rect(screen, "Yellow", cake_rect)
        screen.blit(cake, cake_rect)

    def randomize(self):
        self.x_pos = randint(0, cell_number-1) * cell_size
        self.y_pos = randint(0, cell_number-1) * cell_size
        self.pos = Vector2(self.x_pos, self.y_pos)

class Snake():
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10)]
        self.move_direction = Vector2(0, 0)

    def draw_snake(self):
        for bdsnake in self.body:
            part = pygame.Rect(bdsnake.x * cell_size, bdsnake.y * cell_size, cell_size, cell_size)
            pygame.draw.ellipse(screen, (148, 116, 242), part)

    def snake_move(self):
        copy_b = self.body[:-1]
        copy_b.insert(0, copy_b[0] + self.move_direction)
        self.body = copy_b[:]  

class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        
        self.snake.snake_move()
        self.check_collision()
        self.draw_elements()
        

    def draw_elements(self):
        self.draw_board()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
        
    def add_body(self):
        copy_s = self.snake.body
        copy_s.append(copy_s[-1])
        self.snake.body = copy_s
        eat_cake.play()
        

    def check_collision(self):
        if self.fruit.pos // cell_size == self.snake.body[0]:
            self.add_body()
            self.fruit.randomize()
            if self.fruit.pos in self.snake.body:
                  self.fruit.randomize()

        if not (0 <= self.snake.body[0].x <= cell_number) or not(0 <= self.snake.body[0].y <= cell_number):
            self.draw_gameover()

            
            
        if (self.snake.body[0] in self.snake.body[1:]) and (len(self.snake.body) > 2):
            self.draw_gameover()
        
    def draw_board(self):
        for lin in range(cell_number):
            for col in range(cell_number):
                if (lin + col) % 2 == 0:
                    pygame.draw.rect(screen, color1, pygame.Rect(col * cell_size, lin * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, color2, pygame.Rect(col * cell_size, lin * cell_size, cell_size, cell_size))

    def draw_score(self):
        score = f"Score: {str(len(self.snake.body) - 2)}"
        score_surf = txt_font.render(score, True, "Black")
        screen.blit(score_surf, (30, 30))   

    def draw_menu(self):
        screen.fill((174, 214, 184))
        menu_text = txt_font.render("Press SPACE to start!", True, "White")
        menu_text = pygame.transform.scale(menu_text, (200, 50))
        menu_text_rect = menu_text.get_rect(center = (screen_l/2, screen_l/2 + 50)) 

        welcome_text = txt_font.render("Hello! Welcome to my Snake Game!", True, "White")
        welcome_text_rect = welcome_text.get_rect(center = (screen_l/2, screen_l/2 + -100))  

        screen.blit(menu_text, menu_text_rect)
        screen.blit(welcome_text, welcome_text_rect)  

    def draw_gameover(self):
        screen.fill((223, 214, 184))

        menu_text = txt_font.render("Uf... Game Over! :(", True, "White")
        menu_text = pygame.transform.scale(menu_text, (240, 50))
        menu_text_rect = menu_text.get_rect(center = (screen_l/2, screen_l/2 - 100))

        score = txt_font.render(f"Your score: {len(self.snake.body) - 2}", True, "White")
        score_rect = score.get_rect(center = (screen_l/2, screen_l/2))

        options = txt_font.render("Press R to restart or Q to quit the game!", True, "White")
        options_rect = options.get_rect(center = (screen_l/2, screen_l/2 + 100))

        screen.blit(menu_text, menu_text_rect)
        screen.blit(score, score_rect)
        screen.blit(options, options_rect)
        pygame.display.flip()

       

        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False

                    self.snake.body = [Vector2(7, 10), Vector2(6, 10)]
                    self.snake.move_direction = Vector2(0, 0)
                    pygame.display.flip()


                    
                

    
main_game = Main()

pygame.display.set_caption("Snake by Agu")


game_over = False
run = True
menu = True

while run:
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE and game_over == False:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if main_game.snake.move_direction.x != -1:
                    main_game.snake.move_direction.x = 1
                    main_game.snake.move_direction.y = 0
            if event.key == pygame.K_a:
                if main_game.snake.move_direction.x != 1:
                    main_game.snake.move_direction.x = -1
                    main_game.snake.move_direction.y = 0
            if event.key == pygame.K_w:
                if main_game.snake.move_direction.y != 1:
                    main_game.snake.move_direction.x = 0
                    main_game.snake.move_direction.y = -1
            if event.key == pygame.K_s:
                if main_game.snake.move_direction.y != -1:
                    main_game.snake.move_direction.x = 0
                    main_game.snake.move_direction.y = 1
            if event.key == pygame.K_SPACE:
                menu = False
                game_over = False
        
   
    if menu == True:
            main_game.draw_menu()
    else:
            main_game.draw_elements()

    
    
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()