import pygame
from pygame import *
from sys import exit
from numpy import sign
import math as m

game_title="I wanna hello world!"

pygame.init()
#pygame.mixer.init()
screen_size=(900,600)
screen=pygame.display.set_mode(screen_size,0,32)
pygame.display.set_caption(game_title)
my_font1=pygame.font.SysFont("arial",18)
my_font2=pygame.font.SysFont("arial",30)
white=(255,255,255)

w_save1=my_font1.render("sa", True, white)
w_save2=my_font1.render("ve", True, white)
lv_name=[my_font2.render("O The Fool", True, white),my_font2.render("I The Magician", True, white),my_font2.render("II The High Priestess", True, white),my_font2.render("III The Empress", True, white),my_font2.render("IV The Emperoe", True, white),
my_font2.render("V The Empress", True, white)]
pass_word=my_font2.render("4 7 9 5",True,(25,25,25))

#pygame.mixer.music.load("./music/Nyan Cat.mp3")
#pygame.mixer.music.play(-1)


full_screen=False
play_music=True
pi=m.pi
e_speed=0.2
e_g=30
F_f=e_speed/2
F_g=e_speed/100
F_n=1
kid_color=[255,255,255]
x=10
lv=0

class Kid():
	def __init__(self,pos,speed,aspeed,state,jump=2):#aspeed为水平加速度; state:0活1死
		self.screen=screen
		self.pos=pos
		self.speed=speed
		self.aspeed=aspeed
		self.state=state
		self.jump=jump
	def draw(self):
		pygame.draw.circle(self.screen,kid_color,(int(self.pos[0]),int(self.pos[1])),x,1)
		if self.state:
			pygame.draw.circle(self.screen,(255,0,255),(int(self.pos[0]),int(self.pos[1])),int(3/4*x),1)
	def set(self):
		if self.state==1:
			self.aspeed=0
			self.speed=[0,0]
		if -e_speed*2<self.speed[0]<e_speed*2:
			self.speed[0]+=self.aspeed
		if F_n==0:
			self.speed[1]+=F_g
		self.pos[0]+=self.speed[0]
		self.pos[1]+=self.speed[1]
		self.speed[0]-=sign(self.speed[0])*F_f
		if self.speed[0]<e_speed/100:
			self.speed[0]=0

class Elf():
	def __init__(self,pos,speed,aspeed,state):
		self.screen=screen
		self.pos=pos
		self.speed=speed
		self.aspeed=aspeed
		self.state=state
	def draw(self):
		#print(self.pos)
		pygame.draw.circle(self.screen,self.state[0],(int(self.pos[0]),int(self.pos[1])),int(x/3),1)
	def set(self,Kid):
		global x
		speed=1
		if self.pos[0]<0 or self.pos[0]>screen_size[0]:
			self.speed[0]*=-1/2
		if self.pos[1]<0 or self.pos[1]>screen_size[1]:
			self.speed[1]*=-1/2
		len=m.sqrt((self.pos[0]-Kid.pos[0])**2+(self.pos[1]-Kid.pos[1])**2)
		if len>60:
			speed=1/2
		else:
			speed=1
		if not int(len):
			len=1
		f=4-16*x/(len**2)
		self.aspeed[0]=f*(Kid.pos[0]-self.pos[0])/len
		self.aspeed[1]=f*(Kid.pos[1]-self.pos[1])/len
		self.speed[0]+=self.aspeed[0]/100
		self.speed[1]+=self.aspeed[1]/100
		self.pos[0]+=self.speed[0]*speed
		self.pos[1]+=self.speed[1]*speed
		
class Ground():
	def __init__(self,poses,color):
		self.screen=screen
		self.poses=poses
		self.color=color
	def draw(self):
		for i in range(len(self.poses)):
			pygame.draw.rect(self.screen,(0,0,0),(self.poses[i][0],self.poses[i][1],e_g,e_g),0)
			pygame.draw.rect(self.screen,self.color,(self.poses[i][0],self.poses[i][1],e_g,e_g),4)
	def set(self,Kid):
		global F_n
		edge=3
		for i in range(len(self.poses)):
			if 0<=Kid.pos[1]-self.poses[i][1]+edge<5 and self.poses[i][0]-edge<Kid.pos[0]<self.poses[i][0]+e_g+edge and Kid.speed[1]>=0:
				Kid.pos[1]=self.poses[i][1]-edge
				Kid.speed[1]=0
				F_n=1
				Kid.jump=2
			elif -5<Kid.pos[1]-e_g-self.poses[i][1]-edge<0 and self.poses[i][0]-edge<Kid.pos[0]<self.poses[i][0]+e_g+edge:
				Kid.pos[1]=self.poses[i][1]+e_g+edge
				Kid.speed[1]=0
			if 0<Kid.pos[0]-self.poses[i][0]+edge<5 and self.poses[i][1]-edge<Kid.pos[1]<self.poses[i][1]+e_g+edge:
				Kid.pos[0]=self.poses[i][0]-edge
				Kid.speed[0]=0
			elif -5<Kid.pos[0]-e_g-self.poses[i][0]-edge<0 and self.poses[i][1]-edge<Kid.pos[1]<self.poses[i][1]+e_g+edge:
				Kid.pos[0]=self.poses[i][0]+e_g+edge
				Kid.speed[0]=0

class UpSpine():
	def __init__(self,poses):
		self.screen=screen
		self.poses=poses
	def draw(self):
		for i in range(len(self.poses)):
			pygame.draw.polygon(self.screen,(220,223,227),[(self.poses[i][0],self.poses[i][1]+e_g),(self.poses[i][0]+e_g,self.poses[i][1]+e_g),(self.poses[i][0]+e_g/2,self.poses[i][1])])
	def set(self,Kid):
		for i in range(len(self.poses)):
			if (abs(Kid.pos[0]*2+Kid.pos[1]-self.poses[i][0]*2-self.poses[i][1]-e_g)/m.sqrt(5)<x and 0<Kid.pos[1]-self.poses[i][1]+x/m.sqrt(5)<e_g+8 and Kid.pos[0]-self.poses[i][0]<e_g/2) or (abs(Kid.pos[0]*2-Kid.pos[1]-self.poses[i][0]*2+self.poses[i][1]-e_g)/m.sqrt(5)<x and 0<Kid.pos[1]-self.poses[i][1]+x/m.sqrt(5)<e_g+8 and Kid.pos[0]-self.poses[i][0]>e_g/2):
				Kid.state=1

class Door():
	def __init__(self,pos,state):
		self.screen=screen
		self.pos=pos
		self.state=state
	def draw(self):
		if self.state==0:
			pygame.draw.circle(self.screen,(255,0,255),self.pos,int(3/2*x),4)
		else:
			pygame.draw.circle(self.screen,(255,255,0),self.pos,int(3/2*x),4)
	def set(self,Kid):
		if m.sqrt((self.pos[0]-Kid.pos[0])**2+(self.pos[1]-Kid.pos[1])**2)<5/2*x:
			self.state=2

class UpBad():
	def __init__(self,pos):
		self.screen=screen
		self.pos=pos
		self.posx=pos[0]
		self.posy=pos[1]
		self.state=0
	def draw(self):
		for i in range(len(self.pos)):
			pygame.draw.polygon(self.screen,(220,223,227),[(self.pos[0],self.pos[1]+e_g),(self.pos[0]+e_g,self.pos[1]+e_g),(self.pos[0]+e_g/2,self.pos[1])])
	def set(self,Kid):
		if 0<Kid.pos[0]-self.pos[0]<e_g and 0<self.pos[1]-Kid.pos[1]<5 and self.state==0:
			self.state=200
		if self.state>100:
			self.state-=1
			self.pos[1]-=e_g/100
		if (abs(Kid.pos[0]*2+Kid.pos[1]-self.pos[0]*2-self.pos[1]-e_g)/m.sqrt(5)<x and 0<Kid.pos[1]-self.pos[1]+x/m.sqrt(5)<e_g+2 and Kid.pos[0]-self.pos[0]<e_g/2) or (abs(Kid.pos[0]*2-Kid.pos[1]-self.pos[0]*2+self.pos[1]-e_g)/m.sqrt(5)<x and 0<Kid.pos[1]-self.pos[1]+x/m.sqrt(5)<e_g+2 and Kid.pos[0]-self.pos[0]>e_g/2):
			Kid.state=1

class BadGround():
	def __init__(self,pos):
		self.screen=screen
		self.pos=pos
		self.color=(255,255,255)
		self.state=0
	def draw(self):
		if self.state==0:
			pygame.draw.rect(self.screen,(0,0,0),(self.pos[0],self.pos[1],e_g,e_g),0)
			pygame.draw.rect(self.screen,self.color,(self.pos[0],self.pos[1],e_g,e_g),4)
	def set(self,Kid):
		if 0<Kid.pos[0]-self.pos[0]<e_g and 0<Kid.pos[1]-self.pos[1]<e_g:
			self.state=1

class HideGround():
	def __init__(self,pos):
		self.screen=screen
		self.pos=pos
		self.color=(255,255,255)
		self.state=0
	def draw(self):
		if self.state:
			pygame.draw.rect(self.screen,(0,0,0),(self.pos[0],self.pos[1],e_g,e_g),0)
			pygame.draw.rect(self.screen,self.color,(self.pos[0],self.pos[1],e_g,e_g),4)
	def set(self,Kid):
		global F_n
		edge=3
		if -edge<Kid.pos[0]-self.pos[0]<e_g+edge and -edge<Kid.pos[1]-self.pos[1]<e_g+edge:
			self.state=1 
		if 0<=Kid.pos[1]-self.pos[1]+edge<5 and self.pos[0]-edge<Kid.pos[0]<self.pos[0]+e_g+edge and Kid.speed[1]>=0:
			Kid.pos[1]=self.pos[1]-edge
			Kid.speed[1]=0
			F_n=1
			Kid.jump=2
		elif -5<Kid.pos[1]-e_g-self.pos[1]-edge<0 and self.pos[0]-edge<Kid.pos[0]<self.pos[0]+e_g+edge:
			Kid.pos[1]=self.pos[1]+e_g+edge
			Kid.speed[1]=0
		if 0<Kid.pos[0]-self.pos[0]+edge<5 and self.pos[1]-edge<Kid.pos[1]<self.pos[1]+e_g+edge:
			Kid.pos[0]=self.pos[0]-edge
			Kid.speed[0]=0
		elif -5<Kid.pos[0]-e_g-self.pos[0]-edge<0 and self.pos[1]-edge<Kid.pos[1]<self.pos[1]+e_g+edge:
			Kid.pos[0]=self.pos[0]+e_g+edge
			Kid.speed[0]=0

save_pos=[[115,485],[45,465]]
kid=Kid([115,485],[0,0],0,0)	
elf=Elf([100,100],[0,0],[0,0],[(255,255,0)])
grounds=[
[[100,500],[130,500],[160,500],[190,500],[220,500],[250,500],[280,500],[310,500],[340,470],[370,440],[400,410],[400,380],[430,350],[430,320],[370,260],[340,260],[280,200],[250,200],[280,140],[310,140],[340,140],[370,140],[400,140],[430,140],[460,140],[490,140],[520,140],[550,140],[580,140],[610,140],[640,140],[670,140]],
[[30,480],[60,480],[90,480],[120,480],[150,480], [240,420],[270,420],[300,420],[330,420],[360,420], [450,360],[480,360],[510,360],[540,360],[570,360], [660,300],[690,300],[720,300],[750,300],[780,300], [660,150],[690,150],[720,150],[750,150],[780,150],[490,135],[530,135],[510,150],[510,120], [120,90],[120,120],[120,150],[240,150],[270,150],[300,150],[330,150],[360,150], [870,240],[870,210],[870,180]]]
ground=[Ground(grounds[0],[255,255,255]),Ground(grounds[1],[255,255,255])]
upSpines=[
[[370,110]],[[60,450],[90,450],[120,450], [270,390],[300,390],[330,390],[360,415], [480,330],[510,330],[540,330], [690,270],[720,270],[750,270], [690,120],[720,120],[750,120], [873,150], [510,90]]]
upSpine=[UpSpine(upSpines[0]),UpSpine(upSpines[1])]
upBad=[[UpBad([-100,-100])],[UpBad([660,150])]]
badGround=[[BadGround([-100,-100])],[BadGround([150,150]),BadGround([180,150]),BadGround([210,150])]]
hideGround=[[HideGround([-100,-100])],[HideGround([570,280]),HideGround([600,280])]]
door=[Door([700,110],0),Door([60,90],0)]
while True:
	
	for event in pygame.event.get():#键盘控制
		if event.type==QUIT:
			exit()
		if event.type==KEYDOWN:
			#if event.key==K_m:#播放音乐
			#	play_music=not play_music
			#	if play_music:
			#		pygame.mixer.music.play(-1)
			#	else:
			#		pygame.mixer.music.stop()
			if event.key==K_f:#全屏
				full_screen=not full_screen
				if full_screen:
					screen=pygame.display.set_mode((900,600),FULLSCREEN,32)
				else:
					screen=pygame.display.set_mode((900,600),0,32)
			if event.key==K_r:
				kid.state=0
				kid.pos[0]=save_pos[lv][0]
				kid.pos[1]=save_pos[lv][1]
				for i in range(len(upBad[lv])):
					upBad[lv][i].pos[0]=upBad[lv][i].posx
					upBad[lv][i].pos[1]=upBad[lv][i].posy
					upBad[lv][i].state=0
				for i in range(len(badGround[lv])):
					badGround[lv][i].state=0
				for i in range(len(hideGround[lv])):
					hideGround[lv][i].state=0
			if event.key==K_LEFT:
				kid.aspeed=-e_speed*1.05
			if event.key==K_RIGHT:
				kid.aspeed=e_speed*1.05
			if event.key==K_SPACE and kid.jump>0:
				kid.jump-=1
				kid.speed[1]=-2*e_speed
		elif event.type==KEYUP:
			if event.key==K_LEFT or event.key==K_RIGHT:
				kid.aspeed=0
	
	x_mouse,y_mouse=pygame.mouse.get_pos()
	if pygame.mouse.get_pressed()[0]:#鼠标控制
		kid.pos=[x_mouse,y_mouse]
		kid.speed=[0,0]
		kid.jump=2
	if pygame.mouse.get_pressed()[2]:
		elf.pos=[x_mouse,y_mouse]
		elf.speed=[0,0]
	
	F_n=0
	kid.set()
	elf.set(kid)
	ground[lv].set(kid)
	upSpine[lv].set(kid)
	for i in range(len(upBad[lv])):
		upBad[lv][i].set(kid)
	for i in range(len(badGround[lv])):
		badGround[lv][i].set(kid)
	for i in range(len(hideGround[lv])):
		hideGround[lv][i].set(kid)
	door[lv].set(kid)
	if door[lv].state==2 and lv<len(door)-1:
		door[lv].state=0
		lv+=1
		kid.pos[0]=save_pos[lv][0]
		kid.pos[1]=save_pos[lv][1]
	if not(0<kid.pos[0]<900) or not(0<kid.pos[1]<600):
		kid.state=1

#-------------------------------显示模块----------------------------------------
	screen.fill((0,0,0))
	screen.blit(w_save1,[save_pos[lv][0]-x,save_pos[lv][1]-x-2])
	screen.blit(w_save2,[save_pos[lv][0]-x,save_pos[lv][1]])
	upSpine[lv].draw()
	for i in range(len(upBad[lv])):
		upBad[lv][i].draw()
	for i in range(len(badGround[lv])):
		badGround[lv][i].draw()
	for i in range(len(hideGround[lv])):
		hideGround[lv][i].draw()
	door[lv].draw()
	ground[lv].draw()
	kid.draw()
	elf.draw()
	screen.blit(lv_name[lv],[10,0])
	if door[lv].state==2 and lv==len(door)-1:
		screen.blit(pass_word,[800,0])
	pygame.display.update()