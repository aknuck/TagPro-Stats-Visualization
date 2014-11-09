# -*- coding: utf-8 -*-

import sys
import pygame
import math
import urllib2
from string import ascii_letters, digits

pygame.init()
pygame.display.set_caption("TagPro Player Stats Graphic")

screen = pygame.display.set_mode((900,700))

#colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
blue = pygame.Color(100,100,255)
blue2 = pygame.Color(0,0,200)
grey = pygame.Color(200,200,200)
green = pygame.Color(50,200,50)
red = pygame.Color(255,50,50)
red2 = pygame.Color(200,0,0)
grey2 = pygame.Color(100,100,100)
grey3 = pygame.Color(60,60,60)
grey4 = pygame.Color(225,225,225)

saveButton = pygame.Rect(740,650,120,25)
savedTimer = 0
saveStatsWithImage = False
saveCheckBoxYes = pygame.Rect(755,620,20,20)
saveCheckBoxNo = pygame.Rect(825,620,20,20)

typeFieldClicked = False
typeFieldRect = pygame.Rect(710,30,120,25)
compareFieldClicked = False
compareFieldRect = pygame.Rect(710,262,120,25)

# positions (all equadistant from eachother. basically just points on a circle the same distance apart)
CENTER = (348,398,4,4) #Center of the visualization

# max number of players from tagpro-stats.com, used to get shape of visualization
page = urllib2.urlopen("http://tagpro-stats.com/profile.php?userid=26447").read()
MAXPLAYERS = page[page.index("balls included in monthly ranking")-6:page.index("balls included in monthly ranking")]
print MAXPLAYERS

# Positions of the edges of the visualization shape, used for reference points and drawing white BG shape
Cp = (550,200,4,4)
Gr = (627,355,4,4)
CpPGr = (395,123,4,4)
TgPp = (479,650,4,4)
Pr = (308,677,4,4)
Rt = (150,600,4,4)
Sp = (72,441,4,4)
Tg = (99,270,4,4)
Wn = (600,526,4,4)
Hl = (224,150,4,4)
POINTSDICT = {"Cp":Cp,"Gr":Gr,"CpPGr":CpPGr,"TgPp":TgPp,"Pr":Pr,"Rt":Rt,"Sp":Sp,"Tg":Tg,"Wn":Wn,"Hl":Hl}

class Player:

    def __init__(self,playerID):
        self.ID = playerID
        self.validID = False
        self.surface = pygame.Surface((900,700))
        self.surface.fill(pygame.Color(255,255,255))
        self.surface.set_colorkey(pygame.Color(255,255,255))
        self.surface.set_alpha(200)
        #compareFieldRect = pygame.Rect(710,262,120,25)

    def getData(self): #gets all player data if ID is valid
        if self.validID:
            self.statsPage = urllib2.urlopen("http://tagpro-stats.com/profile.php?userid="+self.ID).read()
            self.profilePage = urllib2.urlopen(self.getStatsPage(self.ID)).read()
            self.name = self.getName()
            self.dict = self.getDict()
            self.info = self.getPlayerInfo()
            self.plotPoints = self.getPlotPoints()
            
            
    def setColor(self,c): #sets thier color
        self.color = c

    def checkID(self): #checks if their id is valid
        page = urllib2.urlopen("http://tagpro-stats.com/profile.php?userid="+self.ID).read()
        return page[page.index("Minutes/Game")+45:page.index("Minutes/Game")+50] != "0.000"

    def getName(self): #returns their name
        n = ""
        for x in range(20):
            if self.statsPage[self.statsPage.index("Career stats for ")+96+x:self.statsPage.index("Career stats for ")+97+x] != "<":
                n = n+self.statsPage[self.statsPage.index("Career stats for ")+96+x:self.statsPage.index("Career stats for ")+97+x]
            else:
                print n
                break
        return n

    def getDict(self): #returns a dict of their place with all their stats
        stats = {"taggame":0,"tagpop":0,
                 "grabgame":0,"winpercent":0,"holdhour":0,
                 "capgame":0,"preventhour":0,"returngame":0,
                 "supportgame":0,"capgrab":0}
        page = self.statsPage
        
        for stat in stats:
            stats[stat] = int(self.grabPlace(page,stat))
        page = self.profilePage
        stats["degrees"] = page[page.index("<h3>"+self.name)+9+len(self.name):page.index("&deg")]

        return stats
    
    def getStatsPage(self,userid): #gets a link to the player's profile page based on their ID
        page = urllib2.urlopen("http://tagpro-stats.com/profile.php?userid="+userid).read()
        linkExtension = page[page.index(".koalabeast.com/profile/")+24:page.index(".koalabeast.com/profile/")+48]
        return "http://tagpro-origin.koalabeast.com/profile/"+linkExtension

    def getPlayerInfo(self): #gets player info
        stats = {"name":self.name,
                 "games":0,"degrees":0,"winpercent":0}
        page = self.statsPage
        games = page[page.index('month&stat=games')-78:page.index('month&stat=games')-66]
        for letter in games:
            if letter not in digits:
                 games = games.replace(letter,"")
        stats["games"] = games
        stats["winpercent"] = page[page.index("month&stat=winpercent")-80:page.index("month&stat=winpercent")-74]
        page = self.profilePage
        stats["degrees"] = page[page.index("<h3>"+self.name)+9+len(self.name):page.index("&deg")]

        return stats

    def grabPlace(self,page,statName): #gets place for a certain stat
        raw = page[page.index('month&stat='+statName)+56+len(statName):page.index('month&stat='+statName)+63+len(statName)]
        for letter in raw:
            if letter not in digits:
                raw = raw.replace(letter,"")
        return raw

    def getPlotPoints(self): #returns the plot points of the player's visualization
        global CENTER
        global MAXPLAYERS
        global POINTSDICT
        
        points = []
        m = 1 - self.dict["capgame"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Cp"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Cp"][1])*m) #calc y
        points.append((x,y)) #captures

        m = 1 - self.dict["capgrab"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["CpPGr"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["CpPGr"][1])*m) #calc y
        points.append((x,y)) #captures per grab

        m = 1 - self.dict["holdhour"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Hl"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Hl"][1])*m) #calc y
        points.append((x,y)) #hold

        m = 1 - self.dict["taggame"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Tg"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Tg"][1])*m) #calc y
        points.append((x,y)) #tags

        m = 1 - self.dict["supportgame"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Sp"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Sp"][1])*m) #calc y
        points.append((x,y)) #support

        m = 1 - self.dict["returngame"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Rt"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Rt"][1])*m) #calc y
        points.append((x,y)) #returns

        m = 1 - self.dict["preventhour"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Pr"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Pr"][1])*m) #calc y
        points.append((x,y)) #prevent

        m = 1 - self.dict["tagpop"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["TgPp"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["TgPp"][1])*m) #calc y
        points.append((x,y)) #K/D ratio

        m = 1 - self.dict["winpercent"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Wn"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Wn"][1])*m) #calc y
        points.append((x,y)) #Win Percent

        m = 1 - self.dict["grabgame"]/float(MAXPLAYERS) #get fraction of max
        x = ((POINTSDICT["Gr"][0]-CENTER[0])*m)+CENTER[0] #calc x
        y = CENTER[1] - ((CENTER[1]-POINTSDICT["Gr"][1])*m) #calc y
        points.append((x,y)) #grabs

        return points #returns the points of the player's visualization


def write(x,y,color,msg,size): #prints onto the screen in selected font
    #fontObj = pygame.font.SysFont('arial rounded MT bold',size)
    fontObj = pygame.font.Font('freesansbold.ttf',size)
    msgSurfaceObj = fontObj.render(msg, False, color)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (x,y)
    screen.blit(msgSurfaceObj,msgRectobj)

def getDistance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def drawVisualization(player):
    if player.plotPoints != []:
        pygame.draw.polygon(surface,blue,player.plotPoints)

def drawShape(surface):
    Cp,Gr,CpPGr,TgPp,Pr,Rt,Sp,Tg,Wn,Hl = POINTSDICT["Cp"],POINTSDICT["Gr"],POINTSDICT["CpPGr"],POINTSDICT["TgPp"],POINTSDICT["Pr"],POINTSDICT["Rt"],POINTSDICT["Sp"],POINTSDICT["Tg"],POINTSDICT["Wn"],POINTSDICT["Hl"]

    #outside rim
    pygame.draw.polygon(surface,white,[(Cp[0],Cp[1]),(CpPGr[0],CpPGr[1]),(Hl[0],Hl[1]),(Tg[0],Tg[1]),(Sp[0],Sp[1]),(Rt[0],Rt[1]),(Pr[0],Pr[1]),(TgPp[0],TgPp[1]),(Wn[0],Wn[1]),(Gr[0],Gr[1])])
    pygame.draw.polygon(surface,black,[(Cp[0],Cp[1]),(CpPGr[0],CpPGr[1]),(Hl[0],Hl[1]),(Tg[0],Tg[1]),(Sp[0],Sp[1]),(Rt[0],Rt[1]),(Pr[0],Pr[1]),(TgPp[0],TgPp[1]),(Wn[0],Wn[1]),(Gr[0],Gr[1])],3)

def drawLines(surface):
    global CENTER
    global POINTSDICT #a dict of points for the outside shape
    Cp,Gr,CpPGr,TgPp,Pr,Rt,Sp,Tg,Wn,Hl = POINTSDICT["Cp"],POINTSDICT["Gr"],POINTSDICT["CpPGr"],POINTSDICT["TgPp"],POINTSDICT["Pr"],POINTSDICT["Rt"],POINTSDICT["Sp"],POINTSDICT["Tg"],POINTSDICT["Wn"],POINTSDICT["Hl"]

    #write names, draw lines/circles. Needed to be separate for adjusted positioning
    pygame.draw.ellipse(screen,black,Cp) #caps
    write(Cp[0],Cp[1]-16,grey4,"Captures/Game",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Cp[0]+1,Cp[1]+1),1)

    pygame.draw.ellipse(screen,black,Hl) #hold
    write(Hl[0]-40,Hl[1]-18,grey4,"Hold/Hour",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Hl[0]+1,Hl[1]+1),1)

    pygame.draw.ellipse(screen,black,Wn) #drops
    write(Wn[0],Wn[1]+15,grey4,"Winpercent",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Wn[0]+1,Wn[1]+1),1)

    pygame.draw.ellipse(screen,black,Tg) #tags
    write(Tg[0]-48,Tg[1]-16,grey4,"Tags/",12)
    write(Tg[0]-48,Tg[1],grey4,"Game",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Tg[0]+1,Tg[1]+1),1)

    pygame.draw.ellipse(screen,black,Sp) #support
    write(Sp[0]-60,Sp[1]-16,grey4,"Support/",12)
    write(Sp[0]-56,Sp[1],grey4,"Game",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Sp[0]+1,Sp[1]+1),1)

    pygame.draw.ellipse(screen,black,Rt) #returns
    write(Rt[0]-60,Rt[1]+20,grey4,"Returns/Game",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Rt[0]+1,Rt[1]+1),1)

    pygame.draw.ellipse(screen,black,Pr) #prevent
    write(Pr[0]-40,Pr[1]+10,grey4,"Prevent/Hour",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Pr[0]+1,Pr[1]+1),1)

    pygame.draw.ellipse(screen,black,TgPp) #popped
    write(TgPp[0],TgPp[1]+10,grey4,"Tags/Popped",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(TgPp[0]+1,TgPp[1]+1),1)

    pygame.draw.ellipse(screen,black,Gr) #Grabs
    write(Gr[0]+6,Gr[1]-12,grey4,"Grabs/",12)
    write(Gr[0]+6,Gr[1],grey4,"Game",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(Gr[0]+1,Gr[1]+1),1)

    pygame.draw.ellipse(screen,black,CpPGr) #capture per grab
    write(CpPGr[0]+5,CpPGr[1]-16,grey4,"Captures/Grab",12)
    pygame.draw.line(screen,black,(CENTER[0],CENTER[1]),(CpPGr[0]+1,CpPGr[1]+1),1)


screen.fill(200)
player1 = Player("")
player2 = Player("")

while True:
    screen.fill(grey3)# BG
    pygame.draw.rect(screen,black,(700,65,200,155))# first black box on right, for 1st player's stats
    pygame.draw.rect(screen,black,(700,300,200,155))# second black box, for 2nd player's stats
    pygame.draw.line(screen,black,(700,0),(700,700),2)# separating line between visualization and stats

    drawShape(screen)

    #save button
    pygame.draw.rect(screen,grey2,saveButton)
    write(748,651,grey4,"save image",18)
    pygame.draw.rect(screen,white,saveCheckBoxYes)
    pygame.draw.rect(screen,black,saveCheckBoxYes,2)
    pygame.draw.rect(screen,white,saveCheckBoxNo)
    pygame.draw.rect(screen,black,saveCheckBoxNo,2)
    if saveStatsWithImage == True:
        pygame.draw.line(screen,green,(758,630),(765,635),5)#checkmark
        pygame.draw.line(screen,green,(765,635),(773,613),4)
    else:
        pygame.draw.line(screen,green,(828,630),(835,635),5)#"X"
        pygame.draw.line(screen,green,(835,635),(843,613),4)

    #first type field
    pygame.draw.rect(screen,white,typeFieldRect)
    if typeFieldClicked:
        pygame.draw.rect(screen,green,typeFieldRect,2)
    else:
        pygame.draw.rect(screen,grey2,typeFieldRect,2)
    write(740,32,black,player1.ID,18)
    write(710,8,grey4,"Player ID:",20)

    #Player 1 info
    write(710,75,grey4,"Games Played: ",18)
    write(710,120,grey4,"Degrees: ",18)
    write(710,165,grey4,"Win Percentage: ",18)
  
    #comparing type field
    pygame.draw.rect(screen,white,compareFieldRect)
    if compareFieldClicked:
        pygame.draw.rect(screen,green,compareFieldRect,2)
    else:
        pygame.draw.rect(screen,grey2,compareFieldRect,2)
    write(740,264,black,player2.ID,18)
    write(710,230,grey4,"Compare To:",20)
    write(710,251,grey4,"(optional)",10)

    #Player 2 info
    write(710,310,grey4,"Games Played: ",18)
    write(710,355,grey4,"Degrees: ",18)
    write(710,400,grey4,"Win Percentage: ",18)

    if player1.validID:
        pygame.draw.line(screen,green,(716,46),(723,51),5)
        pygame.draw.line(screen,green,(723,52),(727,33),4)
        player1.surface.fill(white)
        pygame.draw.polygon(player1.surface,blue,player1.plotPoints)
        pygame.draw.polygon(player1.surface,blue2,player1.plotPoints,2)
        pygame.draw.ellipse(screen,blue,(835,35,15,15))
        screen.blit(player1.surface,(0,0))
        write(18,22,black,"Stats For "+player1.info["name"],28)
        write(20,20,grey4,"Stats For "+player1.info["name"],28)
        write(710,95,grey2,player1.info["games"],16)
        write(710,140,grey2,player1.info["degrees"],16)
        write(710,185,grey2,player1.info["winpercent"],16)
    else:
        pygame.draw.line(screen,red,(716,33),(730,52),5)
        pygame.draw.line(screen,red,(716,52),(730,33),5)

    if player2.validID:
        pygame.draw.line(screen,green,(716,278),(723,283),5)
        pygame.draw.line(screen,green,(723,283),(727,265),4)
        if player1.validID:
            player2.surface.fill(white)
            pygame.draw.polygon(player2.surface,red,player2.plotPoints)
            pygame.draw.polygon(player2.surface,red2,player2.plotPoints,2)
            pygame.draw.ellipse(screen,red,(835,267,15,15))
            screen.blit(player2.surface,(0,0))
            write(18,57,black,"Compared to "+player2.info["name"],14)
            write(20,55,grey4,"Compared to "+player2.info["name"],14)
            write(710,330,grey2,player2.info["games"],16)
            write(710,375,grey2,player2.info["degrees"],16)
            write(710,420,grey2,player2.info["winpercent"],16)
    else:
        pygame.draw.line(screen,red,(716,265),(730,284),5)
        pygame.draw.line(screen,red,(716,284),(730,265),5)

    if savedTimer > 0:
        savedTimer -= 1
        write(760,680,green,"Image Saved!",12)

    drawLines(screen)

    #Other text to be written
    write(710,565,grey4,"Do you want to",12)
    write(710,577,grey4,"show the sidebar with the",12)
    write(710,589,grey4,"visualization when you save?",12)
    write(725,620,grey4,"Yes",12)
    write(800,620,grey4,"No",12)
    write(629,15, grey4,"Graphic By",10)
    write(611,39,grey4,"AKA Knuckball",10)
    write(579,27,grey4,"doctorprofessortaco",10)

    #get input
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #if 'x' button pressed
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEMOTION: #if move mouse
            mx,my = event.pos
            
        elif event.type == pygame.MOUSEBUTTONUP: #if press mouse
            mx,my = event.pos
            
            if typeFieldRect.collidepoint(mx,my): #if clicked in first type field
                compareFieldClicked = False
                if not typeFieldClicked:
                    typeFieldClicked = True
                    player1.ID = ""
                    
            elif compareFieldRect.collidepoint(mx,my): #if clicked in second type field
                typeFieldClicked = False
                if not compareFieldClicked:
                    compareFieldClicked = True
                    player2.ID = ""
                    
            elif saveButton.collidepoint(mx,my) and player1.checkID(): #if clicked save button
                if player1.checkID():
                    savedTimer = 50
                    if saveStatsWithImage:
                        saveSurface = pygame.Surface((900,700))
                    else:
                        saveSurface = pygame.Surface((700,700))
                    pygame.draw.rect(screen,grey3,(705,500,195,200))
                    if not player2.checkID():
                        pygame.draw.rect(screen,grey3,(702,220,198,480))
                    saveSurface.blit(screen,(0,0))
                    if player2.checkID():
                        pygame.image.save(saveSurface,player1.info["name"]+" vs "+player2.info["name"]+" stats.png")
                    else:
                        pygame.image.save(saveSurface,player1.info["name"]+" stats.png")

            elif saveCheckBoxNo.collidepoint(mx,my): #if clicked "no" checkbox
                saveStatsWithImage = False
                
            elif saveCheckBoxYes.collidepoint(mx,my): #if clicked "yes" checkboc
                saveStatsWithImage = True
                
            else: #if clicked elsewhere on screen
                typeFieldClicked = False
                compareFieldClicked = False
                
        elif event.type == pygame.KEYDOWN: #if pressed a key
            
            if pygame.key.name(event.key) in ascii_letters + digits: #if a valid key
                if typeFieldClicked:
                    player1.ID += pygame.key.name(event.key)
                elif compareFieldClicked:
                    player2.ID += pygame.key.name(event.key)
                    
            elif event.key == pygame.K_BACKSPACE: #if backspace
                if typeFieldClicked:
                    player1.ID = player1.ID[:-1]
                elif compareFieldClicked:
                    player2.ID = player2.ID[:-1]
                    
            elif event.key == pygame.K_RETURN: #if enter
                if typeFieldClicked:
                    player1.validID = player1.checkID()
                    typeFieldClicked = False
                    if player1.validID:
                        player1.getData() #to get info with URL
                elif compareFieldClicked:
                    player2.validID = player2.checkID()
                    compareFieldClicked = False
                    if player2.validID:
                        player2.getData() #to get info with URL

    pygame.display.update()
