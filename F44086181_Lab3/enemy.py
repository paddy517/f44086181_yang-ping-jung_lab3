import pygame
import math
import os

from pygame import draw
from settings import PATH ,GREEN ,RED


pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))#匯入圖像

#定義Enemy(類別)
class Enemy:
    #初始化並傳入key_press參數來決定左右邊出病毒
    def __init__(self,key_press):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        #self.path_num定義左右,self.path_pos定義點，存放在self.path二維串列中
        self.path=PATH[key_press]
        self.path_num = 0
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win ,GREEN,[self.x-8,self.y-40,(self.health/self.max_health)*30,5])
        pygame.draw.rect(win ,RED,[self.x+7,self.y-40,30-((self.health/self.max_health)*30),5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        now_x, now_y = self.path[self.path_pos]     #當前位置
        target_x,target_y = self.path[self.path_pos+1]      #目標位置
        distance_twopoint = math.sqrt((target_x - now_x)**2 + (target_y - now_y)**2)    #計算距離
        max_count = int(distance_twopoint / self.stride)    #計算次數
        
        if  self.move_count < max_count:
            #運算單位向量
            unit_vector_x = (target_x - now_x) / distance_twopoint
            unit_vector_y = (target_y - now_y) / distance_twopoint
            #運算每次距離
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride
            #修改位置
            self.x += delta_x
            self.y += delta_y
            self.move_count+= 1

        else:
            #將當前位置與目標位置往下一個前進
            self.path_pos+=1  
            #歸零移動次數計算
            self.move_count=0 
        
                


       

#定義一群EnemyGroup(類別)
class EnemyGroup:
    #初始化參數
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  
        self.period=self.gen_period
        self.key_press=0

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # Hint: self.expedition.append(self.reserved_members.pop())

        self.period+=1
        if self.reserved_members and self.period > self.gen_period:
            self.expedition.append(self.reserved_members.pop())
            self.period=1
        

        
        

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        
        self.gen_num=num
        #透過self.key_press參數改值來交換邊輸出病毒
        if self.key_press == 0:
            for i in range(self.gen_num):
                self.reserved_members.append(Enemy(self.key_press))
            self.key_press = 1
        else:
            for i in range(self.gen_num):
                self.reserved_members.append(Enemy(self.key_press))
            self.key_press=0
        

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





