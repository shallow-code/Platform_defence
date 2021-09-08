import pyglet
import pyglet.clock
import random
import math
from pyglet.window import key
from pyglet.window import mouse

# special move give points?
check_special_points = True
#start
check_gameRUNNING = True    #check if game over
fase_of_game = 'intro'
main_batch = pyglet.graphics.Batch()
window_height = 600
window_width = 400
freq = 60.0
n_enemy_per_second = 2
lives = 10
score = 0
k_special = 0
level = 0
points_new_level = 50 ###################
N_levels = 5
N_character = N_levels
threshold_special_TRUE = 35 ##################
threshold_special_FALSE = 20
oscillation_x_enemy_4 = 40
scale_speed_enemy = 1.0
hitbox_alfa = 1.0
hitbox_alfa_MAX = 2.0
if check_special_points:
    threshold_special = threshold_special_TRUE
else:
    threshold_special = threshold_special_FALSE
# window
game_window = pyglet.window.Window(window_width, window_height)
game_window.set_mouse_visible(False)
game_window.set_exclusive_mouse(True)


# resources ********************************************************************************************
# order of images
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
forestrings = pyglet.graphics.OrderedGroup(2)
#path
pyglet.resource.path=['./resources']
pyglet.resource.reindex()
#load img
arrow_left_image = pyglet.resource.image("arrow_left.png")
arrow_right_image = pyglet.resource.image("arrow_right.png")
#ammo
bullet_image_0 = pyglet.resource.image("lancette.png")
bullet_image_1 = pyglet.resource.image("sword.png")
bullet_image_2 = pyglet.resource.image("cross.png")
bullet_image_3 = pyglet.resource.image("bullet_plane.png")
bullet_image_4 = pyglet.resource.image("Jolly_joker.png")
bullet_image_5 = pyglet.resource.image("axe.png")
special_image_1A = pyglet.resource.image("proiettile_invisibile.png")
special_image_1B = pyglet.resource.image("ship_viking.png")
special_image_3 = pyglet.resource.image("missile.png")
#enemy
enemy_image_0 = pyglet.resource.image("clock.png")
enemy_image_1 = pyglet.resource.image("viking.png")
enemy_image_2 = pyglet.resource.image("quadrato_BIG.png")
enemy_image_3 = pyglet.resource.image("plane.png")
enemy_image_4 = pyglet.resource.image("joker.png")
enemy_image_special_1 = pyglet.resource.image("viking_boat.png")
enemy_image_special_2 = pyglet.resource.image("quadrato_LIT.png")
#backround
background_image_0 = pyglet.resource.image("background_0.png")
background_image_1 = pyglet.resource.image("background_1.png")
background_image_2 = pyglet.resource.image("background_2.png")
background_image_3 = pyglet.resource.image("background_3.png")
background_image_4 = pyglet.resource.image("background_4.png")
explosion_image_0 = pyglet.resource.image("explosion_0.png")
explosion_image_1 = pyglet.resource.image("explosion_1.png")
explosion_image_2 = pyglet.resource.image("explosion_2.png")
#player
player_image_0 = pyglet.resource.image("player_0.png")
player_image_1 = pyglet.resource.image("player_1.png")
player_image_2 = pyglet.resource.image("player_2.png")
player_image_3 = pyglet.resource.image("player_3.png")
player_image_4 = pyglet.resource.image("player_4.png")
player_question_1 = pyglet.resource.image("domanda_sx.png")
player_question_2 = pyglet.resource.image("domanda_dx.png")
player_question_3 = pyglet.resource.image("explosion_2.png")
berseker_player_imm = pyglet.resource.image("bomb.png")
death_imm = pyglet.resource.image("death.png")
# ********************************************************************************************


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

#centro immagini
center_image(arrow_left_image)
center_image(arrow_right_image)
center_image(bullet_image_0)
center_image(bullet_image_1)
center_image(bullet_image_2)
center_image(bullet_image_3)
center_image(bullet_image_4)
center_image(bullet_image_5)
center_image(special_image_1A)
center_image(special_image_1B)
center_image(special_image_3)
center_image(berseker_player_imm)
center_image(enemy_image_0)
center_image(enemy_image_1)
center_image(enemy_image_2)
center_image(enemy_image_3)
center_image(enemy_image_4)
center_image(enemy_image_special_1)
center_image(enemy_image_special_2)
center_image(explosion_image_0)
center_image(explosion_image_1)
center_image(player_image_0)
center_image(player_image_1)
center_image(player_image_2)
center_image(player_image_3)
center_image(player_image_4)
center_image(player_question_1)
center_image(player_question_2)
center_image(player_question_3)


#create animation explosion
seq_image_ani = [explosion_image_0, explosion_image_1,explosion_image_0, explosion_image_1,explosion_image_0, explosion_image_1, explosion_image_2]
anim_exp = pyglet.image.Animation.from_image_sequence(seq_image_ani, 0.25, False) #create animation
seq_image_question = [player_question_1, player_question_2, player_question_3]
anim_question = pyglet.image.Animation.from_image_sequence(seq_image_question, 0.25, False)

#create dictonary images background
dict_backgroung_img = {0:background_image_0 ,1:background_image_1, 2:background_image_2, 3:background_image_3, 4:background_image_4}
dict_enemy_img = {0:enemy_image_0 ,1:enemy_image_1, 2:enemy_image_2, 3:enemy_image_3, 4:enemy_image_4}
dict_choose_chr_img = {0:player_image_0 ,1:player_image_1, 2:player_image_2, 3:player_image_3, 4:player_image_4}
dict_SELECTED_chr_img = {0:enemy_image_0 ,1:enemy_image_1, 2:enemy_image_special_2, 3:enemy_image_3, 4:enemy_image_4}
dict_bullet_img = {0:bullet_image_0 ,1:bullet_image_1, 2:bullet_image_2, 3:bullet_image_3, 4:bullet_image_4, 5:bullet_image_5}


#change level
def change_level(level):
    global background_game, N_levels, dict_backgroung_img

    level_to_use = level % N_levels
    background_game.delete()
    background_game = pyglet.sprite.Sprite(img=dict_backgroung_img[level_to_use] ,x=0 ,y=0, batch = main_batch, group=background)


# select enemy for different levels
def select_enemy(level):
    type_enemy = int(random.random()*(min(level + 1,N_levels)))
    if type_enemy == 4:
        delta = dict_enemy_img[type_enemy].width + oscillation_x_enemy_4
    else:
        delta = dict_enemy_img[type_enemy].width
    x_new = random.random()*(window_width - delta) + delta//2

    if type_enemy == 0:
        enemy = Enemy_0(x=x_new ,y=window_height ,batch = main_batch, group=foreground)
    if type_enemy == 1:
        enemy = Enemy_1(x=x_new ,y=window_height ,batch = main_batch, group=foreground)
    if type_enemy == 2:
        enemy = Enemy_2(x=x_new ,y=window_height ,batch = main_batch, group=foreground)
    if type_enemy == 3:
        enemy = Enemy_3(x=x_new ,y=window_height ,batch = main_batch, group=foreground)
    if type_enemy == 4:
        enemy = Enemy_4(x=x_new ,y=window_height ,batch = main_batch, group=foreground)

    #output
    return enemy


# reset speed enemies
def reset_speed_enemies(dt):
    global scale_speed_enemy, enemies_game
    for emeny in enemies_game:
        emeny.bullet_speed /= scale_speed_enemy
    scale_speed_enemy = 1.0


#*****************************************************************************************************************************
#CLASS
#player
class Player(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_bullet = False
        self.dead = False

#bullet
class Bullet(pyglet.sprite.Sprite):

    def __init__(self, angular_speed, can_die, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_bullet = True   #etichetta per dire che è un proiettile
        self.bullet_speed = 300.0
        self.angular_speed = angular_speed
        self.can_die = can_die
        self.dead = False

    def die(self):
        if self.can_die:
            self.dead = True

    def update(self,dt):
        self.y += self.bullet_speed * dt
        self.rotation += self.angular_speed * dt
        if self.y > window_height:
            self.dead = True


#ENEMIES
#
class Enemy_0(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=enemy_image_0, *args, **kwargs)
        self.is_bullet = False   
        self.bullet_speed = -150.0 * scale_speed_enemy
        self.dead = False
        self.minus_life = False
        self.make_points = True
        self.duplicate = False

    def die(self):
        self.dead = True

    def update(self,dt):
        self.y += self.bullet_speed * dt
        if self.y < 0:
            self.minus_life = True
            self.dead = True

#
class Enemy_1(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=enemy_image_1, *args, **kwargs)
        self.is_bullet = False 
        self.bullet_speed = -150.0 * scale_speed_enemy
        self.dead = False
        self.minus_life = False
        self.make_points = True
        self.duplicate = False
        pyglet.clock.schedule_interval(self.turbo, random.random()*3)

    def die(self):
        self.dead = True

    def update(self,dt):
        self.y += self.bullet_speed * dt
        if self.y < 0:
            self.minus_life = True
            self.dead = True

    def turbo(self, dt):
        self.bullet_speed = - 200.0 * scale_speed_enemy
        if self.dead == False:
            self.image = enemy_image_special_1

#
class Enemy_2(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=enemy_image_2, *args, **kwargs)
        self.is_bullet = False   
        self.bullet_speed = -75.0 * scale_speed_enemy
        self.dead = False
        self.minus_life = False
        self.make_points = True
        self.duplicate = False
        self.BIG = True

    def die(self):
        self.dead = True
        if self.BIG == True:
            self.duplicate = True

    def update(self,dt):
        self.y += self.bullet_speed * dt
        if self.y < 0:
            self.minus_life = True
            self.dead = True

#
class Enemy_3(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=enemy_image_3, *args, **kwargs)
        self.is_bullet = False   
        self.bullet_speed = -165.0 * scale_speed_enemy
        self.dead = False
        self.minus_life = False
        self.make_points = True
        self.duplicate = False

    def die(self):
        self.dead = True

    def update(self,dt):
        self.y += self.bullet_speed * dt
        if self.y < 0:
            self.minus_life = True
            self.dead = True
            
#
class Enemy_4(pyglet.sprite.Sprite):
    
    def __init__(self, *args, **kwargs):
        super().__init__(img=enemy_image_4, *args, **kwargs)
        self.is_bullet = False   
        self.bullet_speed = -150.0 * scale_speed_enemy
        self.dead = False
        self.minus_life = False
        self.make_points = True
        self.duplicate = False
        self.x_0 = self.x

    def die(self):
        self.dead = True

    def update(self,dt):
        self.x = self.x_0 + oscillation_x_enemy_4 * math.sin(self.y*math.pi/100)
        self.y += self.bullet_speed * dt
        if self.y < 0:
            self.minus_life = True
            self.dead = True

            

#*****************************************************************************************************************************
# starting screen
starting_labels = []
label_start_0 = pyglet.text.Label('ISTRUZIONI',font_name='Impact',font_size=30, x=window_width//2, y=window_height//2 + 250,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_0)
label_start_1 = pyglet.text.Label('- Usa il mouse per muoverti',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 +150,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_1)
label_start_2 = pyglet.text.Label('- Spara con MOUSE SINISTRO',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 +100,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_2)
label_start_3 = pyglet.text.Label('- Usa SPACE per usare l\' attacco speciale',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 + 50,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_3)
label_start_4 = pyglet.text.Label('  dopo ' +str(threshold_special)+' uccisioni (tranne il quadrato)',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 ,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_4)
label_start_5 = pyglet.text.Label('- Hai '+str(lives)+' vite',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 -50,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_5)
label_start_6 = pyglet.text.Label('- Personaggio scelto con le freccie',font_name='Impact',font_size=15, x=window_width//2- 160, y=window_height//2 -100,
                                                 anchor_x='left', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_6)
label_start_last = pyglet.text.Label('[ premi SPACE per inziare ]',font_name='Impact',font_size=15, x=window_width//2, y=window_height//2 -200,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
starting_labels.append(label_start_last)


def update(dt):
    global lives, check_gameRUNNING, fase_of_game, score, k_special, Player, label_score_value, anim_exp, anim_sprite, background_game, level
    global hitbox_alfa, n_type_player, anim_sprite_question
    

    if fase_of_game == 'main_game':
        for bullet in bullets_game:
            bullet.update(dt)
        for enemy in enemies_game:
            enemy.update(dt)

        #create enemy
        check = random.random()*freq < n_enemy_per_second
        if check:
            enemy = select_enemy(level)
            enemies_game.append(enemy)

        #check hit
        for bullet in bullets_game:
            for enemy in enemies_game:
                if (abs(bullet.x - enemy.x) <= enemy.image.width//2 *hitbox_alfa) and (abs(bullet.y - enemy.y) <= enemy.image.height//2):
                    bullet.die()
                    enemy.die()
                    if (bullet.can_die == False) and (check_special_points == False):
                        enemy.make_points = False
                    if enemy.duplicate:
                        for i_SMALL in range(2):
                            enemy_SMALL = Enemy_2(x=enemy.x +enemy_image_special_2.width*(i_SMALL-0.5),y=enemy.y ,batch = main_batch, group=foreground)
                            enemy_SMALL.BIG = False
                            enemy_SMALL.image = enemy_image_special_2
                            enemies_game.append(enemy_SMALL)


        #rimuovo dalla lista degli oggetti gli oggetti morti
        for to_remove in [obj for obj in bullets_game if obj.dead]:
            to_remove.delete()
            bullets_game.remove(to_remove)
        for to_remove in [obj for obj in enemies_game if obj.dead]:
            if (to_remove.minus_life == True) and check_gameRUNNING:
                lives -= 1
                if lives >= 0:
                    icons_livies[len(icons_livies)-1].delete()
                    icons_livies.pop()
                
            if (to_remove.minus_life == False) and (to_remove.make_points == True):
                score += 1
                k_special_OLD = k_special
                k_special = min(k_special + 1, threshold_special)
                if (k_special_OLD == (threshold_special-1)) and (k_special == threshold_special) and (n_type_player != 2):
                    Player.image = berseker_player_imm
                    #flashing
                    anim_sprite = pyglet.sprite.Sprite(anim_exp, x=Player.x, y=Player.y,batch = main_batch, group=forestrings)
                    
                # score display
                label_score_value.delete()
                label_score_value = pyglet.text.Label(str(score),font_name='Impact',font_size=20, x=window_width-5, y=window_height-30,
                                                 anchor_x='right', anchor_y='top',batch = main_batch, group=forestrings)
                label_score_value.color = (0,0,0,255)
                
            to_remove.delete()
            enemies_game.remove(to_remove)

        #Game Over
        if lives == 0:
            check_gameRUNNING = False
            Player.image = death_imm
            x_0 = window_width//2
            y_0 = window_height//2
            f_0 = 45

            # black written and white border
            label_GO_border1 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 + 2, y=y_0 + 2,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            label_GO_border2 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 + 2, y=y_0 - 2,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            label_GO_border3 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 - 2, y=y_0 + 2,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            label_GO_border4 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 - 2, y=y_0 - 2,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            label_GO_border1.color = (255,255,255,255)
            label_GO_border2.color = (255,255,255,255)
            label_GO_border3.color = (255,255,255,255)
            label_GO_border4.color = (255,255,255,255)
            label_GO = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0, y=y_0,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            label_GO.color = (0,0,0,255)

        #change level
        OLD_level = level
        level = score // points_new_level
        if OLD_level != level:
            change_level(level)


            
        
@game_window.event
def on_mouse_motion(x, y, dx, dy):
    if (check_gameRUNNING == True) and (fase_of_game == 'main_game'):
        Player.x += dx
        if Player.x < 0:
            Player.x = 0
        if Player.x > window_width:
            Player.x = window_width
        #move explosion
        try:
            anim_sprite.x = Player.x
        except:
            None
        #move question marks
        try:
            anim_sprite_question.x = Player.x
        except:
            None
        

@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if (check_gameRUNNING == True) and (fase_of_game == 'main_game'):
        Player.x += dx
        if Player.x < 0:
            Player.x = 0
        if Player.x > window_width:
            Player.x = window_width
        #move explosion
        try:
            anim_sprite.x = Player.x
        except:
            None
        #move question marks
        try:
            anim_sprite_question.x = Player.x
        except:
            None

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    if (check_gameRUNNING == True) and (fase_of_game == 'main_game'):
        if button == pyglet.window.mouse.LEFT:
            if n_type_player == 1:
                if random.random() < 0.5:
                    B_i = dict_bullet_img[1]
                else:
                    B_i = dict_bullet_img[5]
            else:
                B_i = dict_bullet_img[n_type_player]
            
            bullet = Bullet(img=B_i, angular_speed=300.0, can_die=True,
                            x=Player.x, y=10+player_imm.height, batch = main_batch, group=foreground)
            bullets_game.append(bullet)

@game_window.event
def on_key_press(symbol, modifiers):
    global fase_of_game, background_game, Player, bullets_game, enemies_game, k_special, icons_livies, score, label_score_value, anim_sprite
    global label, n_type_player, player_chr_choose, player_imm, scale_speed_enemy, hitbox_alfa, threshold_special, anim_sprite_question
    
    if symbol == key.SPACE:
        #choose player
        if fase_of_game == 'choose_chr':
            fase_of_game = 'main_game'
            #inizialization
            for label in starting_labels:
                label.delete()
            background_game = pyglet.sprite.Sprite(img=background_image_0 ,x=0 ,y=0, batch = main_batch, group=background)
            player_imm = dict_SELECTED_chr_img[n_type_player]
            Player = Player(img=player_imm, x=window_width//2 ,y=10+player_imm.height//2, batch = main_batch, group=foreground)
            bullets_game = []
            enemies_game = []
            icons_livies = []
            # lives icons
            label_lives_text = pyglet.text.Label('Vite:',font_name='Impact',font_size=20, x=0, y=window_height,
                                                 anchor_x='left', anchor_y='top',batch = main_batch, group=forestrings)
            label_lives_text.color = (0,0,0,255)
            for i in range(lives):
                icon_life = pyglet.sprite.Sprite(img=player_imm, x=10, y=window_height - 40 -i*20 ,batch = main_batch, group=forestrings)
                icon_life.scale = 0.5
                icons_livies.append(icon_life)
            # score icons
            label_score_text = pyglet.text.Label('Punti:',font_name='Impact',font_size=20, x=window_width, y=window_height,
                                                 anchor_x='right', anchor_y='top',batch = main_batch, group=forestrings)
            label_score_text.color = (0,0,0,255)
            label_score_value = pyglet.text.Label(str(score),font_name='Impact',font_size=20, x=window_width-5, y=window_height-30,
                                                 anchor_x='right', anchor_y='top',batch = main_batch, group=forestrings)
            label_score_value.color = (0,0,0,255)
            #bonus special hitbox
            if n_type_player == 1:
                threshold_special = threshold_special // 2
            if n_type_player == 2:
                hitbox_alfa = hitbox_alfa_MAX

        #intro
        if fase_of_game == 'intro':
            fase_of_game = 'choose_chr'
            for label in starting_labels:
                label.delete()
            label_choose_0 = pyglet.text.Label('Scegli il personaggio',font_name='Impact',font_size=20, x=window_width//2, y=window_height//2 + 250,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            starting_labels.append(label_choose_0)
            label_choose_1 = pyglet.text.Label('[ premi SPACE per inziare ]',font_name='Impact',font_size=15, x=window_width//2, y=window_height//2 -200,
                                                 anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
            starting_labels.append(label_choose_1)
            arrow_left = pyglet.sprite.Sprite(img=arrow_left_image ,x=20+arrow_left_image.width//2 ,y=window_height//2, batch = main_batch, group=background)
            starting_labels.append(arrow_left)
            arrow_right = pyglet.sprite.Sprite(img=arrow_right_image ,x=window_width-(20+arrow_right_image.width//2) ,y=window_height//2, batch = main_batch, group=background)
            starting_labels.append(arrow_right)
            n_type_player = 3
            player_chr_choose = pyglet.sprite.Sprite(img=dict_choose_chr_img[n_type_player] ,x=window_width//2 ,y=window_height//2, batch = main_batch, group=background)
            starting_labels.append(player_chr_choose)
            
        # main game, special attack
        if (check_gameRUNNING == True) and (fase_of_game == 'main_game'):
            if k_special == threshold_special:
                n_type_player_OLD = n_type_player
                #
                if n_type_player == 4:
                    #flashing
                    anim_sprite_question = pyglet.sprite.Sprite(anim_question, x=Player.x, y=Player.y,batch = main_batch, group=forestrings)
                    #
                    n_type_player = random.randint(0,3)
                    if n_type_player == 2:
                        hitbox_alfa = hitbox_alfa_MAX
                    else:
                        hitbox_alfa = 1.0
                #
                if n_type_player == 0:
                    scale_speed_enemy = 0.5
                    for emeny in enemies_game:
                        emeny.bullet_speed *= scale_speed_enemy
                    pyglet.clock.schedule_interval(reset_speed_enemies, 15.0)
                #
                if n_type_player == 1:
                    for i in range(-2,3,1):
                        if i == 0:
                            S_image = special_image_1B
                        else:
                            S_image = special_image_1A


                        bullet = Bullet(img=S_image, angular_speed=0.0, can_die=False,
                                        x=Player.x+i*S_image.width, y=10+player_imm.height, batch = main_batch, group=foreground)
                        bullets_game.append(bullet)
                #
                if n_type_player == 3:
                    for i in range(400//special_image_3.width):
                        bullet = Bullet(img=special_image_3, angular_speed=0.0, can_die=False,
                                        x=i*special_image_3.width + special_image_3.width//2, y=random.random()*100-100, batch = main_batch, group=foreground)
                        bullets_game.append(bullet)
                #
                n_type_player = n_type_player_OLD
                        
                k_special = 0
                Player.image = player_imm
                anim_sprite.delete()


    if symbol == key.LEFT:
        if fase_of_game == 'choose_chr':
            n_type_player = (n_type_player-1) % N_character
            player_chr_choose.image = dict_choose_chr_img[n_type_player]


    if symbol == key.RIGHT:
        if fase_of_game == 'choose_chr':
            n_type_player = (n_type_player+1) % N_character
            player_chr_choose.image = dict_choose_chr_img[n_type_player]

            

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


if __name__=='__main__':
    pyglet.clock.schedule_interval(update, 1/freq)
    pyglet.app.run()
