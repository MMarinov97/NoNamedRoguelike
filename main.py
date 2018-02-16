import pygame
import libtcodpy as libtcod
# Archivos del juego
import constants

#   _____ __                  __
#  / ___// /________  _______/ /___  __________
#  \__ \/ __/ ___/ / / / ___/ __/ / / / ___/ _ \
# ___/ / /_/ /  / /_/ / /__/ /_/ /_/ / /  /  __/
#/____/\__/_/   \__,_/\___/\__/\__,_/_/   \___/


class struct_Tile:

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


#   ____  __      _           __
#  / __ \/ /_    (_)__  _____/ /______
# / / / / __ \  / / _ \/ ___/ __/ ___/
#/ /_/ / /_/ / / /  __/ /__/ /_(__  )
#\____/_.___/_/ /\___/\___/\__/____/
#          /___/

class obj_Actor:  # Cualquier objeto existente en el mundo

    # Creature None es valor vacio si no pasas nada
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.creature = creature
        if creature:  # Si no es None se crea el atributo creature y se le asigna el valor
            self.creature = creature
            creature.owner = self
        self.ai = ai
        if ai:
            self.ai = ai
            ai.owner = self

    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        if(is_visible):
            SURFACE_MAIN.blit(
                self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

class obj_Game:
	def __init__(self):
		self.current_map = map_create() # Creamos el mapa
		self.message_history = [] # Inicializamos la lista en vacio
		self.current_objects = [] # Inicialiamos la lista de objetos en vacio
#   ______                                             __
#  / ____/___  ____ ___  ____  ____  ____  ___  ____  / /______
# / /   / __ \/ __ `__ \/ __ \/ __ \/ __ \/ _ \/ __ \/ __/ ___/
#/ /___/ /_/ / / / / / / /_/ / /_/ / / / /  __/ / / / /_(__  )
#\____/\____/_/ /_/ /_/ .___/\____/_/ /_/\___/_/ /_/\__/____/
#                    /_/


class com_Creature:
    '''
    Las criaturas tienen vida, pueden quitar puntos a otros objetos atacando. Pueden morir
    '''

    def __init__(self, name_instance, hp=10, death_function=None):  # name_instance = Criatura Bob
        self.name_instance = name_instance
        self.hp = hp
        self.maxhp = hp
        self.death_function = death_function

    def take_damage(self, damage):
        self.hp -= damage
        damage_msg = self.name_instance + "'s health is " + \
            str(self.hp) + "/" + str(self.maxhp)
        game_message(damage_msg, constants.COLOR_RED)
        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def attack(self, target, damage):
        print self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage"
        attack_msg = self.name_instance + " attacks " + \
  			target.creature.name_instance + " for " + str(damage) + " damage"
        game_message(attack_msg, constants.COLOR_WHITE)
        target.creature.take_damage(damage)

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx]
                        [self.owner.y + dy].block_path == True)

        # self para evitar danyarnos a nosotros mismos
        target = map_check_for_creatures(
            self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:  # Si no es nulo
            self.attack(target, libtcod.random_get_int(0, 3, 5))
        # Si un objeto que no somos nosotros esta en la posicion a la que nos
        # moveremos se le asigna como objetivo
        if not tile_is_wall and not target:
            self.owner.x += dx
            self.owner.y += dy


# TODO class com_Item:

# TODO class com_Container:

#    ___    ____
#   /   |  /  _/
#  / /| |  / /
# / ___ |_/ /
#/_/  |_/___/


class ai_Test:
        # Se ejecuta una vez por turno

    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                 libtcod.random_get_int(0, -1, 1))


def death_monster(monster):
    # Cuando mueren, la mayoria de los monstruos mueren
    print monster.creature.name_instance + " is dead!"
    monster.creature = None  # Quitamos el modulo de criatura
    monster.ai = None  # Le quitamos la IA
    monster.sprite = constants.S_BLOOD
#    __  ___
#   /  |/  /___ _____
#  / /|_/ / __ `/ __ \
# / /  / / /_/ / /_/ /
#/_/  /_/\__,_/ .___/
#            /_/


def map_create():
    new_map = [[struct_Tile(False) for y in range(0, constants.MAP_HEIGHT)]
               for x in range(0, constants.MAP_WIDTH)]
    for x in range(0, constants.MAP_WIDTH):

        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True
    for y in range(0, constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True
    for dy in xrange(3, constants.MAP_HEIGHT - 3):
        for dx in xrange(3, constants.MAP_WIDTH - 3):
            if dx % 3 == 0:
                new_map[dx][dy].block_path = True
    map_make_fov(new_map)
    return new_map


def map_check_for_creatures(x, y, exclude_object=None):
    target = None
    if exclude_object:  # Busca excluyendo al objeto exclude_object
        for object in GAME.current_objects:
            if (object is not exclude_object and  # Si el objeto no es el que excluimos, x e y coinciden y es una criatura, devuelve el objeto
                    object.x == x and
                    object.y == y and object.creature):
                target = object
            if target:
                return target
    else:
        for object in GAME.current_objects:
            # Si x e y coinciden y es una criatura, devuelve el objeto
            if (object.x == x and object.y == y and object.creature):
                target = object
            if target:
                return target


def map_make_fov(incoming_map):
    global FOV_MAP
    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            '''
            map_set_properties(map, x, y, isTransparent, isWalkable)
            Lo que tenemos en el lugar de isTransparent hara que si el blockpath = True entre un False. Es decir,
            si hay pared, no es transparente. Lo mismo con isWalkable.
            '''
            libtcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][
                y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
    global FOV_CALCULATE
    if FOV_CALCULATE:
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS,
                                constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)
#    ____                      _
#   / __ \_________ __      __(_)___  ____ _
#  / / / / ___/ __ `/ | /| / / / __ \/ __ `/
# / /_/ / /  / /_/ /| |/ |/ / / / / / /_/ /
#/_____/_/   \__,_/ |__/|__/_/_/ /_/\__, /
#                                  /____/


def draw_game():
    global SURFACE_MAIN
    # TODO limpiar la superficie antes de dibujar
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    # Dibujar el mapa
    draw_map(GAME.current_map)
    # Dibujar los objetos
    for object in GAME.current_objects:
        object.draw()
    draw_debug()
    draw_messages()
    pygame.display.flip()


def draw_messages():
    to_draw = GAME.message_history  # Esto nos devuelve los 4 ultimos elementos de la lista
    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)
    # Establecemos el punto donde empezaran los mensajes en relacion a la posicion del jugador
    i = 0
    if PLAYER.y > constants.MAP_HEIGHT / 2:
    	start_y = 0
    else:
    	start_y = constants.MAP_HEIGHT * constants.CELL_HEIGHT - \
        	(constants.NUM_MESSAGES * text_height)
    if PLAYER.x > constants.MAP_WIDTH / 2:
    	start_x = 0
    else:
    	start_x = constants.MAP_WIDTH * constants.CELL_WIDTH - ((constants.MAP_WIDTH/2 +2)*constants.CELL_WIDTH)
   
    # Dibujamos los mensajes
    for message, color in to_draw:
     # Sacamos el msg y el color de la lista
        draw_text(SURFACE_MAIN, message, (start_x, (start_y +
                                              (i * text_height))), color, constants.COLOR_GREY)
        i += 1


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:  # Es una pared
                    # Dibujamos la pared
                    SURFACE_MAIN.blit(
                        constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # Dibujamos el suelo
                    SURFACE_MAIN.blit(
                        constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            elif map_to_draw[x][y].explored:
                if map_to_draw[x][y].block_path == True:  # Es una pared
                    # Dibujamos la pared
                    SURFACE_MAIN.blit(
                        constants.S_WALL_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # Dibujamos el suelo
                    SURFACE_MAIN.blit(
                        constants.S_FLOOR_EXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_debug():
    text = str(int(CLOCK.get_fps()))
    draw_text(SURFACE_MAIN, text, (0, 2),
              constants.COLOR_WHITE, constants.COLOR_GREY)


def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None):  # T means tuple
    # Cogemos un texto y lo muestra en la superficie de referencia
    text_surface, text_rect = helper_text_object(
        text_to_display, text_color, back_color)  # Recogemos la superficie y su rectangulo
    text_rect.topleft = T_coords  # Asignamos las coordenadas
    display_surface.blit(text_surface, text_rect)  # Mostramos por pantalla


#    __  __     __
#   / / / /__  / /___  ___  __________
#  / /_/ / _ \/ / __ \/ _ \/ ___/ ___/
# / __  /  __/ / /_/ /  __/ /  (__  )
#/_/ /_/\___/_/ .___/\___/_/  /____/
#            /_/

def helper_text_object(incoming_text, incoming_color, incoming_bg):
    # Transforma un texto en una superficie
    if incoming_bg:
        # False porq no queremos antialiasing
        Text_surface = constants.FONT.render(
            incoming_text, False, incoming_color, incoming_bg)
    else:
        # False porq no queremos antialiasing
        Text_surface = constants.FONT.render(
            incoming_text, False, incoming_color)
    # Devolvemos la superficie y su rectangulo
    return Text_surface, Text_surface.get_rect()


def helper_text_height(font):  # Nos devuelve la altura de la fuente
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()
    return font_rect.height

#   ______
#  / ____/___ _____ ___  ___
# / / __/ __ `/ __ `__ \/ _ \
#/ /_/ / /_/ / / / / / /  __/
#\____/\__,_/_/ /_/ /_/\___/


def game_main_loop():
    game_quit = False
    player_action = "no-action"
    while not game_quit:
        map_calculate_fov()
        player_action = "no-action"
        player_action = game_handle_keys()
        if player_action == "QUIT":
            game_quit = True
        elif player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai != None:
                    obj.ai.take_turn()
        draw_game()
        CLOCK.tick(constants.GAME_FPS)
    pygame.quit()
    exit()


def game_initialize():
    # Inicializa la ventana y pygame
    global SURFACE_MAIN, CLOCK, GAME, PLAYER, ENEMY, FOV_CALCULATE

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    CLOCK = pygame.time.Clock()
    GAME = obj_Game()

    FOV_CALCULATE = True
    # Creamos el pj
    creature_com1 = com_Creature("Bob")

    PLAYER = obj_Actor(1, 1, "humano", constants.S_PLAYER,
                       creature=creature_com1)
    # Creamos el enemigo
    creature_com2 = com_Creature("Monster1", death_function=death_monster)
    creature_com3 = com_Creature("Monster2", death_function=death_monster)
    ai_com = ai_Test()
    ai_com2 = ai_Test()
    
    ENEMY = obj_Actor(2, 10, "monstruo", constants.S_ENEMY,
                      creature=creature_com2, ai=ai_com)
    ENEMY2 = obj_Actor(libtcod.random_get_int(0, 1, 20), libtcod.random_get_int(
        0, 1, 20), "monstruo", constants.S_ENEMY, creature=creature_com3, ai=ai_com2)
    GAME.current_objects = [PLAYER, ENEMY, ENEMY2]



def game_handle_keys():  # Funcion que maneja los eventos aka teclas que se pulsan
    global FOV_CALCULATE
    events_list = pygame.event.get()
    for event in events_list:
        if event.type == pygame.QUIT:  # pygame.QUIT = Apretar boton X roja
            return "QUIT"
        if event.type == pygame.KEYDOWN:  # Si se aprieta un boton
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player-moved"
            elif event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player-moved"
            elif event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player-moved"
            elif event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player-moved"
    return "no-action"


def game_message(game_msg, msg_color):
    # Metemos en la lista de mensajes el msg y el color
    GAME.message_history.append((game_msg, msg_color))
    if len(GAME.message_history) > 4:
        GAME.message_history.pop(0)


# Funcion para iniciar el juego
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
