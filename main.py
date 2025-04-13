#ievieš nepieciešamās bibliotēkas
import pygame
import random
import math
import time
import pygame_gui
import pygame_gui
score_time = -1
player1vards = "1. Spēlētājs"
player2vards = "2. Spēlētājs"
#pygame uzstādīšana
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
def play():
    global score_time
    pygame.display.set_caption("Pong")
    running = True
    dt = 0

    #speju attēli
    kaulins = pygame.image.load('data/dice.png')
    rakete = pygame.image.load('data/rakete.png')
    mazaks = pygame.image.load('data/smaller.png')
    #spēles objekti
    rakete1_pos = pygame.Vector2(30, screen.get_height() / 2)
    rakete2_pos = pygame.Vector2(screen.get_width() - 50, screen.get_height() / 2)
    bumba_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    #bumbas rekvizīti
    bumba_radius = 10
    bumba_speed = 400  #sākuma ātrums
    bumba_velo = pygame.Vector2(0, 0)
    bumba_krasa = "white"
    #raketes izmēri
    rakete_width = 20
    rakete_height = 200

    #speletaju punkti
    score1 = 0
    score2 = 0

    #Spējas objekts
    spejas_pos = pygame.Vector2(random.uniform(screen.get_width()/2-150, screen.get_width()/2+150), random.uniform(20, screen.get_height()-80))
    spejas_veids = random.randint(1, 3) # 1 ir rakete, 2 ir smaller, 3 ir dice
    spejas_velo = 73
    #funkcija, lai atgrieztu bumbu centrā ar jaunu virzienu
    def reset_bumba():
        global score_time

        current_time = pygame.time.get_ticks()
        bumba_pos.x = screen.get_width() / 2
        bumba_pos.y = screen.get_height() / 2

        if current_time - score_time < 1000:
            veidot_tekstu("3", pygame.font.SysFont("Impact", 100), "red", screen.get_width() / 2 - 25, 50)
        elif current_time - score_time < 2000:
            veidot_tekstu("2", pygame.font.SysFont("Impact", 100), "yellow", screen.get_width() / 2  - 25, 50)
        elif current_time - score_time < 3000:
            veidot_tekstu("1", pygame.font.SysFont("Impact", 100), "green", screen.get_width() / 2  - 25, 50)
        if current_time - score_time < 3000:
            bumba_velo.x, bumba_velo.y = 0, 0
        else:
            # random angle: -45 to 45 deg or 135 to 225 deg
            lenkis = random.uniform(-0.25, 0.25) if random.choice([True, False]) else random.uniform(0.75, 1.25)
            lenkis *= math.pi  # convert to radians

            direction = pygame.Vector2(math.cos(lenkis), math.sin(lenkis)).normalize()
            bumba_velo.x = bumba_speed * direction.x
            bumba_velo.y = bumba_speed * direction.y
            score_time = 0
    def veidot_tekstu(teksts, fonts, krasa, x, y):
        temp = fonts.render(teksts, True, krasa)
        screen.blit(temp, (x, y))
    def uzzimet_speju():
        if spejas_veids==1:
            screen.blit(pygame.transform.scale(rakete, (60, 60)), (spejas_pos.x, spejas_pos.y))
        elif spejas_veids==2:
            screen.blit(pygame.transform.scale(mazaks, (60, 60)), (spejas_pos.x, spejas_pos.y))
        elif spejas_veids==3:
            screen.blit(pygame.transform.scale(kaulins, (60, 60)), (spejas_pos.x, spejas_pos.y))
    #sāk spēli ar bumbu kustībā
    reset_bumba()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black") #notīra ekrānu
        #pirmās raketes vadība (W un S taustiņi)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if rakete1_pos.y > 0:
                rakete1_pos.y -= 800 * dt
        if keys[pygame.K_s]:
            if rakete1_pos.y < screen.get_height() - rakete_height:
                rakete1_pos.y += 800 * dt
        
        #otrās raketes vadība (bultiņas uz augšu un uz leju)
        if keys[pygame.K_UP]:
            if rakete2_pos.y > 0:
                rakete2_pos.y -= 800 * dt
        if keys[pygame.K_DOWN]:
            if rakete2_pos.y < screen.get_height() - rakete_height:
                rakete2_pos.y += 800 * dt
                
        #bumbas kustība
        bumba_pos.x += bumba_velo.x * dt
        bumba_pos.y += bumba_velo.y * dt
        
        #spejas kustība
        spejas_pos.y = spejas_pos.y + spejas_velo * dt
        if spejas_pos.y <= 0:
            spejas_pos.y = 0
            spejas_velo = (-1)*spejas_velo
        if spejas_pos.y >= screen.get_height()-60:
            spejas_pos.y = screen.get_height()-60
            spejas_velo = (-1)*spejas_velo
        #bumbiņas sadursme ar speju
        if (bumba_pos.x+bumba_radius >= spejas_pos.x and 
            bumba_pos.x-bumba_radius <= spejas_pos.x+60 and
            bumba_pos.y+bumba_radius >= spejas_pos.y and
            bumba_pos.y-bumba_radius <= spejas_pos.y+60):

            if spejas_veids==1:
                bumba_velo.x =  2*bumba_velo.x
                bumba_velo.y =  2*bumba_velo.y
            elif spejas_veids==2:
                bumba_radius = bumba_radius/2
            elif spejas_veids==3:
                bumba_krasa = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # jauna speja parādās
            spejas_veids = random.randint(1, 3)
            spejas_pos = pygame.Vector2(random.uniform(screen.get_width()/2-150, screen.get_width()/2+150), random.uniform(20, screen.get_height()-60))
        #atlēkšana no apakšējās un augšējās sienas
        if bumba_pos.y - bumba_radius <= 0:
            bumba_pos.y = bumba_radius  #neļauj bumbai iziet ārpus ekrāna
            bumba_velo.y = -bumba_velo.y  #maina y virzienu
        elif bumba_pos.y + bumba_radius >= screen.get_height():
            bumba_pos.y = screen.get_height() - bumba_radius  #neļauj bumbai iziet ārpus ekrāna
            bumba_velo.y = -bumba_velo.y  #maina y virzienu
        
        #fiksēts 45 grādu leņķis bumbas atlēcieniem
        lenkis_45 = math.pi / 4  #leņķis radiānos
        
        #bumbas atlēkšana no raketēm
        #pirmā rakete
        if (bumba_pos.x - bumba_radius <= rakete1_pos.x + rakete_width and
            bumba_pos.y >= rakete1_pos.y and 
            bumba_pos.y <= rakete1_pos.y + rakete_height and
            bumba_velo.x < 0):  #pārbauda tikai ja bumba kustās raketes virzienā
            
            direction = -1 if bumba_velo.y < 0 else 1
            
            #iestatata fiksēto 45 grādu leņķi
            bumba_speed_current = pygame.math.Vector2(bumba_velo).length()
            bumba_velo.x = bumba_speed_current * math.cos(lenkis_45)
            bumba_velo.y = direction * bumba_speed_current * math.sin(lenkis_45)  
            
            #nodrošina, ka bumba neiesprūst raketē
            bumba_pos.x = rakete1_pos.x + rakete_width + bumba_radius
        
        #otrā rakete
        if (bumba_pos.x + bumba_radius >= rakete2_pos.x and
            bumba_pos.y >= rakete2_pos.y and 
            bumba_pos.y <= rakete2_pos.y + rakete_height and
            bumba_velo.x > 0):  #pārbauda tikai ja bumba kustās raketes virzienā
            
            direction = -1 if bumba_velo.y < 0 else 1
            
            #iestatata fiksēto 45 grādu leņķi
            bumba_speed_current = pygame.math.Vector2(bumba_velo).length()
            bumba_velo.x = -bumba_speed_current * math.cos(lenkis_45)
            bumba_velo.y = direction * bumba_speed_current * math.sin(lenkis_45)
            
            #nodrošina, ka bumba neiesprūst raketē
            bumba_pos.x = rakete2_pos.x - bumba_radius
        #bumbas sadursme ar labo vai kreiso sienu (punkta gūšana)
        if bumba_pos.x - bumba_radius <= 0:
            score2 += 1
            score_time = pygame.time.get_ticks()
            reset_bumba()
        elif bumba_pos.x + bumba_radius >= screen.get_width():
            score1 += 1
            score_time = pygame.time.get_ticks()
            reset_bumba()
        if score_time:
            reset_bumba()
        
        if score1==5: #Uzvar 1. spēlētājs
            screen.fill("black")
            veidot_tekstu(player1vards + " uzvarēja!", pygame.font.SysFont("Impact", 60), "red", 300, screen.get_height()/2 - 25)
            pygame.display.flip()
            time.sleep(2.5)
            main_menu()
        elif score2==5: #Uzvar 2. spēlētājs
            screen.fill("black")
            veidot_tekstu(player2vards + " uzvarēja!", pygame.font.SysFont("Impact", 60), "blue", 300, screen.get_height()/2 - 25)
            pygame.display.flip()
            time.sleep(2.5)
            main_menu()
        else:#uzzīmē objektus 
            pygame.draw.rect(screen, "white", (rakete1_pos.x, rakete1_pos.y, rakete_width, rakete_height))
            pygame.draw.rect(screen, "white", (rakete2_pos.x, rakete2_pos.y, rakete_width, rakete_height))
            pygame.draw.circle(screen, bumba_krasa, bumba_pos, bumba_radius)
            uzzimet_speju()
            veidot_tekstu(str(score1), pygame.font.SysFont("Impact", 30), "red", 20, 50)
            veidot_tekstu(str(score2), pygame.font.SysFont("Impact", 30), "blue", screen.get_width()-40, 50)
            veidot_tekstu(player1vards, pygame.font.SysFont("Impact", 30), "red", 20, 20)
            veidot_tekstu(player2vards, pygame.font.SysFont("Impact", 30), "blue", screen.get_width()-11*len(player2vards) - 29, 20)
            
            pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()

def main_menu():
    global player1vards, player2vards
    Manager = pygame_gui.UIManager((1280, 720))
    dt = 0
    pygame.display.set_caption("Main menu")
    menu = pygame.image.load('data/main_menu.png')
    menu_sakt = pygame.image.load('data/main_menu_sakt.png')
    menu_iest = pygame.image.load('data/main_menu_options.png')
    menu_beigt = pygame.image.load('data/main_menu_exit.png')
    cursor = pygame.image.load('data/cursor.png')
    running = True
    pygame.mouse.set_visible(False)

    player1in = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(50, 350, 200, 30), manager=Manager, object_id="#player1_text_entry")
    player2in = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(screen.get_width()-250, 200, 200, 30), manager=Manager, object_id="#player2_text_entry")

    def player1Display(teksts):
        fonts = pygame.font.SysFont("Calibri", 30)
        temp = fonts.render(teksts, True, "BLUE")
        screen.blit(temp, (50, 300))
    def player2Display(teksts):
        fonts = pygame.font.SysFont("Calibri", 30)
        temp = fonts.render(teksts, True, "RED")
        screen.blit(temp, (screen.get_width()-250, 150))
    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#player1_text_entry":
                player1vards = event.text[:8]
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#player2_text_entry":
                player2vards = event.text[:8]
            Manager.process_events(event)
        Manager.update(dt)
        posx, posy = pygame.mouse.get_pos()
        if posx >= 535 and posy >= 250 and posx <= 840 and posy <= 350:
            screen.blit(menu_sakt , (0, 0))
            if pygame.mouse.get_pressed()[0] == True:
                play()
        elif posx >= 590 and posy >= 390 and posx <= 770 and posy <= 440:
            screen.blit(menu_iest , (0, 0))
        elif posx >= 590 and posy >= 480 and posx <= 770 and posy <= 530:
            screen.blit(menu_beigt , (0, 0))
            if pygame.mouse.get_pressed()[0] == True:
                running = False
        else:
            screen.blit(menu , (0, 0))
        Manager.draw_ui(screen)
        player1Display(player1vards)
        player2Display(player2vards)
        screen.blit(cursor, (posx, posy-25))
        pygame.display.flip()
        dt = clock.tick(60)/1000
    pygame.quit()

def options():
    pygame.display.set_caption("Options")
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

main_menu()