import pygame
import pytmx 
import pyscroll
from player import Player 


class Game :
    def __init__(self) :
        self.map = 'world'
        #creer fenetre
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pokemon-Python")
        
        #chargement carte
        tmx_data = pytmx.util_pygame.load_pygame('./nature.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        
        #generer un player 
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        #definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "col":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #dessin groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)
        

        #definir le rect de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
            
            
        pressed = pygame.key.get_pressed()
    
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')

            
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        elif pressed[pygame.K_RIGHT]:                
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
         #chargement carte
        tmx_data = pytmx.util_pygame.load_pygame('./house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        player_position = tmx_data.get_object_by_name("exit_house")
        self.player = Player(player_position.x, player_position.y)
        

        #definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "col":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #dessin groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)
        

        #definir le rect de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #recup spawn
        spawn = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn.x
        self.player.position[1] = spawn.y - 20


    def switch_world(self):
        
         #chargement carte
        tmx_data = pytmx.util_pygame.load_pygame('nature.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        player_position = tmx_data.get_object_by_name("enter_house_exit")
        self.player = Player(player_position.x, player_position.y)

      #definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:
             if obj.type == "col":
                    self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            #dessin groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        self.group.add(self.player)
            

            #definir le rect de collision pour entrer dans la maison
        exit_house = tmx_data.get_object_by_name('exit_house')
        self.enter_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        #recup spawn
        spawn = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn.x
        self.player.position[1] = spawn.y + 20


    def update(self):
        self.group.update()


        #verif entrer
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        if self.map == 'house' and self.player.feet.colliderect(self.enter_rect):
            self.switch_world()
            self.map = 'world'
            


        #verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 :
                sprite.move_back()


    def run(self):

        clock = pygame.time.Clock()

        #boucle jeu
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()