import pygame
import time
import heapq
import math

pygame.init()


walkRight = [pygame.image.load('img/R1.png'), pygame.image.load('img/R2.png'), pygame.image.load('img/R3.png'),
             pygame.image.load('img/R4.png'), pygame.image.load('img/R5.png'), pygame.image.load('img/R6.png'),
             pygame.image.load('img/R7.png'), pygame.image.load('img/R8.png'), pygame.image.load('img/R9.png')]
walkLeft = [pygame.image.load('img/L1.png'), pygame.image.load('img/L2.png'), pygame.image.load('img/L3.png'),
            pygame.image.load('img/L4.png'), pygame.image.load('img/L5.png'), pygame.image.load('img/L6.png'),
            pygame.image.load('img/L7.png'), pygame.image.load('img/L8.png'), pygame.image.load('img/L9.png')]
bg = pygame.image.load('img/map.png')
bg = pygame.transform.scale(bg, (1700, 900))

char = pygame.image.load('img/standing.png')


class Anamy(object):
    walkRight = [
        pygame.image.load('img/R1E.png'), pygame.image.load('img/R2E.png'), pygame.image.load('img/R3E.png'),
        pygame.image.load('img/R4E.png'), pygame.image.load('img/R5E.png'), pygame.image.load('img/R6E.png'),
        pygame.image.load('img/R7E.png'), pygame.image.load('img/R8E.png'), pygame.image.load('img/R9E.png'),
        pygame.image.load('img/R10E.png'), pygame.image.load('img/R11E.png')
    ]
    
    walkLeft = [
        pygame.image.load('img/L1E.png'), pygame.image.load('img/L2E.png'), pygame.image.load('img/L3E.png'),
        pygame.image.load('img/L4E.png'), pygame.image.load('img/L5E.png'), pygame.image.load('img/L6E.png'),
        pygame.image.load('img/L7E.png'), pygame.image.load('img/L8E.png'), pygame.image.load('img/L9E.png'),
        pygame.image.load('img/L10E.png'), pygame.image.load('img/L11E.png')
    ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.val = 1.3  
        self.hitbox = (self.x + 17, self.y, 32, 70)
        self.direction = 1  
        self.path = [self.x, self.end]
        self.anamy_platform=5

    def teleport_to_next_platform(self, drum_optimal, graf):
        if not drum_optimal:
            return 
        next_platform_number = drum_optimal[1] 
        if next_platform_number != self.anamy_platform:
            
            next_platform = graf.platforme[next_platform_number]
            self.x = next_platform.x + next_platform.width // 2 
            self.y = next_platform.y - self.height+50  
            self.anamy_platform = next_platform_number 
            drum_optimal.pop(0)     

    def draw(self, window, player):
   
        self.move(player)
        if self.walkcount + 1 >= 33:
            self.walkcount = 0
        if self.direction > 0:  
            window.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
        else: 
            window.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
        self.walkcount += 1

       
        self.hitbox = (self.x + 17, self.y, 32, 70)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)

    def draw_default(self, window):
        self.move_default()
        if self.walkcount + 1 >= 33:
            self.walkcount = 0
        if self.val > 0:
            window.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1
        else:
            window.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1
        self.hitbox = (self.x + 17, self.y, 32, 70)  
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)  

    def move_default(self):
        if self.val > 0:
            if self.x + self.val < self.path[1]:
                self.x += self.val
            else:
                self.val *= -1
                self.walkcount = 0
        else:
            if self.x - self.val > self.path[0]:
                self.x += self.val
            else:
                self.val *= -1
                self.walkcount = 0        

    def move(self, player):
        
        print("goblinul se afla pe platforma ",self.anamy_platform) 

        
    def hit(self):
        print("hit")
class Platrforms:
    def __init__(self, platform_number, x, y, width, height):
        self.platform_number = platform_number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jump_force = 10
        self.vecini = []

    def draw(self, window, r, g, b):
        red_color = (r, g, b)  
        pygame.draw.rect(window, red_color, (self.x, self.y, self.width, self.height))

    def adauga_vecin(self, vecin, cost):
        self.vecini.append((vecin, cost))

    def distanta_euclidiana(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)  

    
class Graf:
    def __init__(self):
        self.platforme = {}

    def adauga_platforma(self, number, x, y, w, h):
        platforma = Platrforms(number, x, y, w, h)
        self.platforme[number] = platforma
        return platforma

    def adauga_legatura(self, num_1, num_2, cost):
        if num_1 in self.platforme and num_2 in self.platforme:
            self.platforme[num_1].adauga_vecin(self.platforme[num_2], cost)
            self.platforme[num_2].adauga_vecin(self.platforme[num_1], cost)

    def a_star(self, start, end):
        deschis = []  
        heapq.heappush(deschis, (0, self.platforme[start]))  
        costuri = {nume: float('inf') for nume in self.platforme}  
        costuri[start] = 0
        parinte = {nume: None for nume in self.platforme} 

        while deschis:
            f_current, current = heapq.heappop(deschis) 
         
            if current.platform_number == end:
                drum = []
                while current:
                    drum.append(current.platform_number)
                    current = parinte[current.platform_number]
                return drum[::-1] 
      
            for vecin, cost in current.vecini:
                g_cost = costuri[current.platform_number] + cost
               
                f_cost = g_cost + current.distanta_euclidiana(self.platforme[end]) 

            
                if g_cost < costuri[vecin.platform_number]:
                    costuri[vecin.platform_number] = g_cost
                    parinte[vecin.platform_number] = current
                    heapq.heappush(deschis, (f_cost, vecin)) 

        return None 

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.prev_y=0
        self.width = width
        self.height = height
        self.step = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count=True
        self.jump_speed=0.15
        self.repause = True
        self.hitbox = (self.x + 17, self.y, 32, 70)
        self.platform=0

    
        
        
        
    def on_platform(self, platform_1, platform_2, platform_3, platform_4, platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platform_left,base_platfor_right):

        if self.platform==platform_1.platform_number:
              
           

            if self.x>platform_5.x+platform_5.width+100:

                self.x=platform_6.x
                self.platform=platform_6.platform_number
                return platform_6.y



        if self.platform==base_platform_left.platform_number:    
            if self.x > platform_1.x and self.x < platform_1.x + platform_1.width and self.y == base_platform_left.y:
                self.platform = platform_1.platform_number
                
                return platform_1.y

            if self.x>base_platform_left.x+base_platform_left.width-180:
                self.platform=platform_3.platform_number
                return platform_3.y    
            
        if self.platform==base_platform_left.platform_number:
              if self.x > platform_2.x and self.x < platform_2.x + platform_2.width and self.y == base_platform_left.y:
                self.platform = platform_2.platform_number
                return platform_2.y

        if self.platform==base_platfor_right.platform_number:
              if self.x > platform_4.x and self.y == base_platform_left.y:
                self.platform = platform_4.platform_number
                return platform_4.y

            
        if self.platform==platform_1.platform_number or self.platform==platform_2.platform_number:    
              if self.x > platform_5.x and self.x < platform_5.x + platform_5.width and self.y==platform_1.y or self.y==platform_2.y :
                
                self.platform = platform_5.platform_number
                return platform_5.y
              
              

        if self.platform==platform_5.platform_number:    
              if self.x >= platform_8.x and self.x < platform_8.x + platform_8.width and self.y==platform_5.y  :
                
                self.platform = platform_8.platform_number
                return platform_8.y
              if self.x>platform_5.x+165 and self.x<=platform_5.x+platform_5.width/2+80:
                  self.x=platform_13.x+20
                  self.platform=platform_13.platform_number
                  return platform_13.y
        if self.platform==base_platform_left.platform_number:    
              if self.x>platform_3.x and self.x<platform_3.width+platform_3.x and self.y==base_platform_left.y:

                self.platform=platform_3.platform_number
                return platform_3.y
        
        if self.platform==platform_3.platform_number:
            if self.x>platform_3.x and self.x < platform_3.x+40 and self.y==platform_3.y:
                
                self.platform=platform_6.platform_number
                self.x+platform_6.x+platform_6.width-10
                return platform_6.y

            if self.x>platform_3.x+platform_3.width/2+20:
                self.platform=platform_7.platform_number 
                self.x=platform_7.x+10   
                return platform_7.y
            
        if self.platform==platform_6.platform_number:

            if self.x>platform_6.x and self.x<platform_6.x+200:
                self.platform=platform_8.platform_number
                self.x=platform_8.x+platform_8.width-20
                return platform_8.y           
        

        if self.platform==platform_7.platform_number or self.platform==platform_4.platform_number:

            if self.x>platform_3.x+platform_3.width/2 and self.x<platform_3.x+platform_3.width:
                self.x=platform_7.x
                self.platform=platform_7.platform_number
                return platform_7.y
            if self.x>platform_4.x and self.x<platform_4.x+50 and self.y==platform_4.y:
                self.x=platform_7.x+platform_7.width-20
                self.platform=platform_7.platform_number
                return platform_7.y


        if self.platform==platform_8.platform_number:
                
            if self.x>platform_8.x+platform_8.width/2 and self.x<platform_8.x+platform_8.width and self.y==platform_8.y:
               
               
               self.x=platform_9.x+30
               self.platform=platform_9.platform_number
               return platform_9.y



        if self.platform==platform_7.platform_number:

            if self.x>platform_7.x+platform_7.width/2:
                self.platform=platform_11.platform_number
                return platform_11.y

        if self.platform==platform_11.platform_number:
            if self.x>platform_11.x and self.x<platform_11.x+platform_11.width/2 and self.y==platform_11.y:

                self.x=platform_10.x+platform_10.width
                self.platform=platform_10.platform_number
                return platform_10.y
            if self.x>platform_11.x+platform_11.width/2+10 and self.y==platform_11.y:

                self.x=platform_16.x
                self.platform=platform_16.platform_number
                return platform_16.y
        if self.platform==platform_10.platform_number:
             if self.x>platform_10.x+platform_10.width/2 and self.x<platform_10.x+platform_10.width and self.y==platform_10.y:
                self.x=platform_11.x
                self.platform=platform_11.platform_number
                return platform_11.y
             if self.x>platform_10.x and self.x<platform_10.x+platform_10.width/2 and self.y==platform_10.y:
                self.x=platform_14.x+platform_14.width-10
                self.platform=platform_14.platform_number
                return platform_14.y
        if self.platform==platform_9.platform_number:
            if self.x>platform_9.x+platform_9.width/2+30:
                self.x=platform_10.x+20
                self.platform=platform_10.platform_number
                return platform_10.y
            if self.x>platform_9.x and self.x<platform_9.x+platform_9.width/2+30:
                self.x=platform_14.x
                self.platform=platform_14.platform_number
                return platform_14.y
        if self.platform==platform_13.platform_number:
            if self.x>platform_13.x and self.x<platform_13.x+50 and self.y==platform_13.y:
                self.platform=platform_12.platform_number
                self.x=platform_12.x+platform_12.width-10
                return platform_12.y 

        if self.platform==platform_12.platform_number:

            if self.x>platform_12.x+platform_12.width/2 and self.x<platform_12.x+platform_12.width and self.y==platform_12.y:
                
                self.x=platform_13.x+10
                self.platform=platform_13.platform_number
                return platform_13.y

        if self.platform==platform_14.platform_number:

            if self.x>platform_14.x+platform_14.width/2 and self.y==platform_14.y:
                self.x=platform_15.x
                self.platform=platform_15.platform_number
                return platform_15.y        

        if self.platform==platform_15.platform_number:

            if self.x>platform_15.y+platform_15.width/2 and self.y==platform_15.y:
                self.x=platform_16.x
                self.platform=platform_16.platform_number
                return platform_16.y

        if self.platform==platform_16.platform_number:

            if self.x>platform_16.x and self.x<platform_16.x+platform_16.width/2 and self.y==platform_16.y:
                self.x=platform_15.x+platform_15.wifth-10
                self.platform=platform_15.platform_number
                return platform_15.y


        return self.y
    
          

    def fall(self, platform_1, platform_2, platform_3, platform_4, platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platform_left,base_platform_right):
        if self.platform == platform_1.platform_number:
            if self.x < platform_1.x or self.x > platform_1.x + platform_1.width and self.y == platform_1.y:
                self.platform=base_platform_left.platform_number
                return base_platform_left.y
            else:
                return platform_1.y
            


        if self.platform == platform_2.platform_number:
            if  self.x > platform_2.x + platform_2.width and self.y == platform_2.y:
                self.platform=base_platfor_left.platform_number
                return base_platform_left.y
            else:
                return platform_2.y
            
         
        
                
        if self.platform == platform_5.platform_number:
            if  self.x > platform_5.x + platform_5.width and self.y == platform_5.y:
                self.platform=platform_1.platform_number
                return platform_1.y
            
            if self.x < platform_5.x and self.y == platform_5.y:
                self.platform=platform_2.platform_number
                return platform_2.y

            else:
                return platform_5.y
            
        if self.platform == platform_8.platform_number:
            
            if  self.x > platform_8.x + platform_8.width and self.y == platform_8.y:
                
                self.platform=platform_6.platform_number
                return platform_6.y
           
            
            
            elif self.x < platform_8.x and self.y == platform_8.y:
                self.platform=platform_5.platform_number
                return platform_5.y

            else:
                return platform_8.y
        
        if self.platform==platform_6.platform_number:

            if self.x>(platform_6.x+platform_6.width) and self.y==platform_6.y:
                self.platform=platform_3.platform_number
                return platform_3.y
            elif self.x<platform_6.x and self.y==platform_6.y:
                self.platform=platform_1.platform_number
                self.x=platform_1.x+platform_1.width-50
                return platform_1.y
            else:
                return platform_6.y    
        if self.platform==platform_3.platform_number:

            if self.x<platform_3.x or self.x>platform_3.x+platform_3.width and self.y==platform_3.y:
                
                self.platform=base_platform_left.platform_number
                return base_platform_left.y
            else:
                return platform_3.y 
        
       
        if self.platform==platform_4.platform_number:

            if self.x<platform_4.x and self.y==platform_4.y:
                self.platform=base_platform_right.platform_number
                return base_platform_right.y     
            else:
                return platform_4.y

        if self.platform==platform_7.platform_number:

            if self.x<platform_7.x and self.y==platform_7.y:
                self.x=platform_3.x+platform_3.width
                self.platform=platform_3.platform_number
                return platform_3.y    

            if self.x>platform_7.x+platform_7.width and self.y==platform_7.y:
               self.x=platform_4.x
               self.platform=platform_4.platform_number
               return platform_4.y     

        if self.platform==platform_9.platform_number:

            if self.x<platform_9.x and self.y==platform_9.y:

                self.platform=platform_6.platform_number
                self.x=platform_6.x+50
                return platform_6.y
                    
            elif self.x>platform_9.x+platform_9.width and self.y==platform_9.y:

                self.platform=platform_3.platform_number
                self.x=platform_3.x+50
                return platform_3.y

        if self.platform==platform_11.platform_number:
            if self.x<platform_11.x and self.y==platform_11.y:
                  self.platform=platform_7.platform_number
                  return platform_7.y
            
        if self.platform==platform_10.platform_number:
            
            if self.x>platform_10.x+platform_10.width and self.y==platform_10.y:
                self.platform=platform_7.platform_number
                return platform_7.y   
            
            if self.x<platform_10.x and self.y==platform_10.y:
                self.platform=platform_3.platform_number
                return platform_3.y
            

        if self.platform==platform_13.platform_number:

            if self.x>platform_13.x+platform_13.width and self.y==platform_13.y:
                self.platform=platform_8.platform_number
                return platform_8.y  

            if self.x<platform_13.x and self.y==platform_13.y:
                self.platform=platform_5.platform_number
                return platform_5.y  
            
        if self.platform==platform_12.platform_number:

            if self.x>platform_12.x+platform_12.width and self.y==platform_12.y:
                self.platform=platform_5.platform_number
                return platform_5.y

        if self.platform==platform_14.platform_number:

            if self.x<platform_14.x and self.y==platform_14.y:
                self.platform=platform_9.platform_number
                return platform_9.y

            if self.x>platform_14.x+platform_14.width and self.y==platform_14.y:
                self.x=platform_10.x+10
                self.platform=platform_10.platform_number
                return platform_10.y


        if self.platform==platform_15.platform_number:
            if self.x<platform_15.x and self.y==platform_15.y:
                self.platform=platform_10.platform_number
                return platform_10.y


            if self.x>platform_15.x+platform_15.width and self.y==platform_15.y:
                self.platform=platform_11.platform_number
                return platform_11.y    


        if self.platform==platform_16.platform_number:
            if self.x<platform_16.x and self.y==platform_16.y:
                self.platform=platform_11.platform_number
                return platform_11.y
        if self.platform==base_platform_left.platform_number:

            if self.x>base_platform_left.x+base_platform_left.width and self.y==base_platform_left.y:
                self.x=0
        if self.platform==base_platfor_right.platform_number:

            if self.x<base_platform_right.x and self.y==base_platform_right.y:
                self.x=0
                self.platform=base_platform_left.platform_number
                return base_platform_left.y

        return self.y

                       
       

  


    def draw(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.repause:
            if self.left:
                window.blit(walkLeft[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                window.blit(walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                window.blit(walkLeft[0], (self.x, self.y))
            else:
                window.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y, 32, 70)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)


class projectil(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

      










transparent_color = (245, 10, 225, 100) 
win_width = 1700
win_height = 900
window = pygame.display.set_mode((win_width, win_height))


goblin = Anamy(5, 1200, 64, 64, win_width-100)
goblin_2 = Anamy(10, 730, 64, 64, win_width-100)


base_platfor_left=Platrforms(1,0,730,885,50)
base_platfor_right=Platrforms(5,1280,730,485,50)
platform_1 = Platrforms(2, 300, 538, 280, 50)
platform_2 = Platrforms(3, 0, 545, 100, 50)
platform_3 = Platrforms(4, 850, 520, 260, 50)
platform_4 = Platrforms(6, 1450, 600, 230, 50)
platform_5 = Platrforms(16, 90, 370, 320, 50)
platform_6 = Platrforms(15, 620, 420, 295, 50)
platform_7=Platrforms(7,1155,460,330,50)
platform_8 = Platrforms(14, 400, 280, 230, 50)
platform_9=Platrforms(13,700,230,230,50)
platform_10=Platrforms(11,1050,225,180,50)
platform_11=Platrforms(8,1350,260,330,50)
platform_12=Platrforms(18,30,170,185,50)
platform_13=Platrforms(17,290,60,325,50)
platform_14=Platrforms(12,850,100,180,50)
platform_15=Platrforms(10,1220,60,250,50)
platform_16=Platrforms(9,1580,100,120,50)


jony = player(50, base_platfor_left.y, 64, 64)
jony.platform=base_platfor_left.platform_number

graf = Graf()

graf.adauga_platforma(1,0,730,885,50)
graf.adauga_platforma(5,1280,730,485,50)
graf.adauga_platforma(2, 300, 538, 280, 50)
graf.adauga_platforma(3, 0, 545, 100, 50)
graf.adauga_platforma(4, 850, 520, 260, 50)
graf.adauga_platforma(6, 1450, 600, 230, 50)
graf.adauga_platforma(16, 90, 370, 320, 50)
graf.adauga_platforma(15, 620, 420, 295, 50)
graf.adauga_platforma(7, 1155, 460, 330, 50)
graf.adauga_platforma(14, 400, 280, 230, 50)
graf.adauga_platforma(13, 700, 230, 230, 50)
graf.adauga_platforma(11, 1050, 225, 180, 50)
graf.adauga_platforma(8, 1350, 260, 330, 50)
graf.adauga_platforma(18, 30, 170, 185, 50)
graf.adauga_platforma(17, 290, 60, 325, 50)
graf.adauga_platforma(12, 850, 100, 180, 50)
graf.adauga_platforma(10, 1220, 60, 250, 50)
graf.adauga_platforma(9, 1580, 100, 120, 50)

graf.adauga_legatura(1, 2, math.sqrt((platform_1.x - base_platfor_left.x)**2 + (platform_1.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 3, math.sqrt((platform_2.x - base_platfor_left.x)**2 + (platform_2.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 4, math.sqrt((platform_3.x - base_platfor_left.x)**2 + (platform_3.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 5, math.sqrt((platform_4.x - base_platfor_left.x)**2 + (platform_4.y - base_platfor_left.y)**2))
graf.adauga_legatura(2, 16, math.sqrt((platform_5.x - platform_1.x)**2 + (platform_5.y - platform_1.y)**2))
graf.adauga_legatura(2, 15, math.sqrt((platform_6.x - platform_1.x)**2 + (platform_6.y - platform_1.y)**2))
graf.adauga_legatura(3, 16, math.sqrt((platform_5.x - platform_2.x)**2 + (platform_5.y - platform_2.y)**2))
graf.adauga_legatura(4, 15, math.sqrt((platform_6.x - platform_3.x)**2 + (platform_6.y - platform_3.y)**2))
graf.adauga_legatura(4, 7, math.sqrt((platform_7.x - platform_3.x)**2 + (platform_7.y - platform_3.y)**2))
graf.adauga_legatura(6, 5, math.sqrt((platform_4.x - base_platfor_right.x)**2 + (platform_7.y - base_platfor_right.y)**2))
graf.adauga_legatura(6, 7, math.sqrt((platform_7.x - platform_4.x)**2 + (platform_7.y - platform_4.y)**2))  
graf.adauga_legatura(16, 14, math.sqrt((platform_8.x - platform_5.x)**2 + (platform_8.y - platform_5.y)**2))
graf.adauga_legatura(16, 17, math.sqrt((platform_13.x - platform_5.x)**2 + (platform_13.y - platform_5.y)**2))
graf.adauga_legatura(15, 2, math.sqrt((platform_1.x - platform_6.x)**2 + (platform_1.y - platform_6.y)**2))
graf.adauga_legatura(15, 4, math.sqrt((platform_3.x - platform_6.x)**2 + (platform_3.y - platform_6.y)**2))
graf.adauga_legatura(15, 14, math.sqrt((platform_8.x - platform_6.x)**2 + (platform_8.y - platform_6.y)**2))
graf.adauga_legatura(7, 4, math.sqrt((platform_3.x - platform_7.x)**2 + (platform_3.y - platform_7.y)**2))
graf.adauga_legatura(7, 6, math.sqrt((platform_4.x - platform_7.x)**2 + (platform_4.y - platform_7.y)**2))
graf.adauga_legatura(7, 8, math.sqrt((platform_11.x - platform_7.x)**2 + (platform_11.y - platform_7.y)**2))
graf.adauga_legatura(14, 13, math.sqrt((platform_9.x - platform_8.x)**2 + (platform_9.y - platform_8.y)**2))
graf.adauga_legatura(14, 15, math.sqrt((platform_6.x - platform_8.x)**2 + (platform_6.y - platform_8.y)**2))
graf.adauga_legatura(13, 12, math.sqrt((platform_14.x - platform_9.x)**2 + (platform_14.y - platform_9.y)**2))
graf.adauga_legatura(13, 11, math.sqrt((platform_10.x - platform_9.x)**2 + (platform_10.y - platform_9.y)**2))
graf.adauga_legatura(13, 4, math.sqrt((platform_3.x - platform_9.x)**2 + (platform_3.y - platform_9.y)**2))
graf.adauga_legatura(11, 8, math.sqrt((platform_11.x - platform_10.x)**2 + (platform_11.y - platform_10.y)**2))
graf.adauga_legatura(11, 12, math.sqrt((platform_14.x - platform_10.x)**2 + (platform_14.y - platform_10.y)**2))
graf.adauga_legatura(11, 7, math.sqrt((platform_7.x - platform_10.x)**2 + (platform_7.y - platform_10.y)**2))
graf.adauga_legatura(8, 7, math.sqrt((platform_7.x - platform_11.x)**2 + (platform_7.y - platform_11.y)**2))
graf.adauga_legatura(8, 9, math.sqrt((platform_16.x - platform_11.x)**2 + (platform_16.y - platform_11.y)**2))
graf.adauga_legatura(8, 11, math.sqrt((platform_10.x - platform_11.x)**2 + (platform_10.y - platform_11.y)**2))
graf.adauga_legatura(18, 16, math.sqrt((platform_5.x - platform_12.x)**2 + (platform_5.y - platform_12.y)**2))
graf.adauga_legatura(18, 17, math.sqrt((platform_13.x - platform_12.x)**2 + (platform_13.y - platform_12.y)**2))
graf.adauga_legatura(17, 16, math.sqrt((platform_5.x - platform_13.x)**2 + (platform_5.y - platform_13.y)**2))
graf.adauga_legatura(17, 14, math.sqrt((platform_8.x - platform_13.x)**2 + (platform_8.y - platform_13.y)**2))
graf.adauga_legatura(12, 13, math.sqrt((platform_9.x - platform_14.x)**2 + (platform_9.y - platform_14.y)**2))
graf.adauga_legatura(12, 11, math.sqrt((platform_10.x - platform_14.x)**2 + (platform_10.y - platform_14.y)**2))
graf.adauga_legatura(12, 10, math.sqrt((platform_15.x - platform_14.x)**2 + (platform_15.y - platform_14.y)**2))
graf.adauga_legatura(10, 11, math.sqrt((platform_10.x - platform_15.x)**2 + (platform_10.y - platform_15.y)**2))
graf.adauga_legatura(10, 8, math.sqrt((platform_11.x - platform_15.x)**2 + (platform_11.y - platform_15.y)**2))
graf.adauga_legatura(10, 9, math.sqrt((platform_16.x - platform_15.x)**2 + (platform_16.y - platform_15.y)**2))
graf.adauga_legatura(9, 10, math.sqrt((platform_15.x - platform_16.x)**2 + (platform_15.y - platform_16.y)**2))
graf.adauga_legatura(9, 8, math.sqrt((platform_11.x - platform_16.x)**2 + (platform_11.y - platform_16.y)**2))

start_platform = 1 
current_platform = None  
drum_optimal = []



pygame.display.set_caption("My Game")

clock = pygame.time.Clock()
FPS = 60


def redraw_game_window():
    window.blit(bg, (0, 0))
    jony.draw(window)
    goblin.draw(window, jony)
    goblin_2.draw_default(window) 
   
    for bomb in bombs:
        bomb.draw(window)
    pygame.display.update()


run = True
bombs = []
is_on_nivel_0=True
is_on_nivel_1=False
is_on_nivel_2=False

ori=0
jump_cooldown = 200  
last_jump_time = 0

start_platform = goblin.anamy_platform
end = jony.platform
last_teleport_time = 0
teleport_cooldown = 3000 

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bomb in bombs:
        if bomb.y - bomb.radius < goblin.hitbox[1] + goblin.hitbox[3] and bomb.y + bomb.radius > goblin.hitbox[1]:
            if bomb.x + bomb.radius > goblin.hitbox[0] and bomb.x - bomb.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bombs.pop(bombs.index(bomb))

        if 0 < bomb.x < 1700:
            bomb.x += bomb.vel
        else:
            bombs.pop(bombs.index(bomb))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        facing = -1 if jony.left else 1
        if len(bombs) < 5:
            bombs.append(projectil(round(jony.x + jony.width // 2), round(jony.y + jony.height // 2), 5, (247, 120, 2), facing))

    if keys[pygame.K_LEFT] and jony.x > 0:
        jony.x -= jony.step
        jony.left = True
        jony.right = False
        jony.repause = False
        
    elif keys[pygame.K_RIGHT] and jony.x + jony.width < win_width:
        jony.x += jony.step
        jony.right = True
        jony.left = False
        jony.repause = False
        
    else:
        jony.repause = True
        jony.walk_count = 0

  
    current_time = pygame.time.get_ticks()

                   
    if keys[pygame.K_UP] and (current_time - last_jump_time > jump_cooldown):
                        
                        last_jump_time = current_time
                        jony.is_jump = True
                        jony.walk_count = 0

                        
                        
                        jony.y=jony.on_platform(platform_1,platform_2,platform_3,platform_4,platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platfor_left,base_platfor_right)
                       
                        print("platform", jony.platform)
                   

                  
    jony.y=jony.fall(platform_1,platform_2,platform_3,platform_4,platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platfor_left,base_platfor_right)           
   
   
   
    current_platform_jucator = jony.platform
    current_platform_goblin = goblin.anamy_platform

  
    if current_platform_jucator != current_platform_goblin:
        start_platform = goblin.anamy_platform 
        end = jony.platform  
        drum_optimal = graf.a_star(start_platform, end)

   
    if drum_optimal:
        current_time = pygame.time.get_ticks()  

        if current_time - last_teleport_time >= teleport_cooldown:
            goblin.teleport_to_next_platform(drum_optimal, graf)
            last_teleport_time = current_time  
          
            if goblin.anamy_platform == jony.platform:
                drum_optimal = None  
                start_platform = goblin.anamy_platform  #
         
                

    #print("x=",jony.x)  
    # print("y=",jony.y)    
    redraw_game_window()

pygame.quit()
