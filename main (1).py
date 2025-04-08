#ievieš nepieciešamās bibliotēkas
import pygame
import random
import math




def play():
        #pygame uzstādīšana
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    #spēles objekti
    rakete1_pos = pygame.Vector2(30, screen.get_height() / 2)
    rakete2_pos = pygame.Vector2(screen.get_width() - 50, screen.get_height() / 2)
    bumba_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    #bumbas rekvizīti
    bumba_radius = 10
    bumba_speed = 400  #sākuma ātrums
    bumba_velo = pygame.Vector2(0, 0)

    #raketes izmēri
    rakete_width = 20
    rakete_height = 200

    #speletaju punkti
    score1 = 0
    score2 = 0
    #funkcija, lai atgrieztu bumbu centrā ar jaunu virzienu
    def reset_bumba():
        bumba_pos.x = screen.get_width() / 2
        bumba_pos.y = screen.get_height() / 2
        
        #nejaušs leņķis star -45 līdz 45 grādiem vai 135 līdz 225 grādiem
        lenkis = random.uniform(-0.25, 0.25) if random.choice([True, False]) else random.uniform(0.75, 1.25)
        lenkis *= math.pi  #pārvērš uz radiāniem
        
        bumba_velo.x = bumba_speed * pygame.math.Vector2.normalize(pygame.Vector2(math.cos(lenkis), math.sin(lenkis))).x
        bumba_velo.y = bumba_speed * pygame.math.Vector2.normalize(pygame.Vector2(math.cos(lenkis), math.sin(lenkis))).y
    def veidot_tekstu(teksts, fonts, krasa, x, y):
        temp = fonts.render(teksts, True, krasa)
        screen.blit(temp, (x, y))
    

    #sāk spēli ar bumbu kustībā
    reset_bumba()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            reset_bumba()
            count_down()
        elif bumba_pos.x + bumba_radius >= screen.get_width():
            score1 += 1
            reset_bumba()
            count_down()
        #uzzīmē objektus

        screen.fill("black")

        pygame.draw.rect(screen, "white", (rakete1_pos.x, rakete1_pos.y, rakete_width, rakete_height))
        pygame.draw.rect(screen, "white", (rakete2_pos.x, rakete2_pos.y, rakete_width, rakete_height))
        pygame.draw.circle(screen, "white", bumba_pos, bumba_radius)

        veidot_tekstu(str(score1), pygame.font.SysFont("Impact", 30), "red", 20, 20)
        veidot_tekstu(str(score2), pygame.font.SysFont("Impact", 30), "blue", screen.get_width()-40, 20)

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        def count_down():
            t = 1
            while t > 0:
                screen.fill("black")
                veidot_tekstu("3", pygame.font.SysFont("Impact", 100), "white", screen.get_width() / 2 - 100, screen.get_height() / 2 - 100)
                pygame.display.flip()
                pygame.time.wait(1000)
                screen.fill("black")
                veidot_tekstu("2", pygame.font.SysFont("Impact", 100), "white", screen.get_width() / 2 - 100, screen.get_height() / 2 - 100)
                pygame.display.flip()
                pygame.time.wait(1000)
                screen.fill("black")
                veidot_tekstu("1", pygame.font.SysFont("Impact", 100), "white", screen.get_width() / 2 - 100, screen.get_height() / 2 - 100)
                pygame.display.flip()
                pygame.time.wait(1000)
                t = 0
    pygame.quit()
play()