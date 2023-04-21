from cmu_graphics import *
from PIL import Image
import random, time

class Bee:
    def __init__(self):
        #Load the frame
        
        #Load the bee gif
        myGif = Image.open('D:/CMU/semester2/15-112/term_project/giphy.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//10, myGif.size[1]//10))
            fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteList.append(fr)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)

        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, acceleration
        self.x, self.y = 100, 100
        self.dy = 0
        self.ddy = .1

    def draw(self,app):
        #Draw current bee sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        # if app.pollinated != False:
        #     drawCircle(self.x-18, self.y+45, 12, fill = 'black', opacity = 75)
        
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        
        if self.y >= 550:
            self.y = 550
            self.dy = 0



    def isColliding(self, orbs,app):
        for orb in orbs:
            if ((self.x - orb.x)**2 + (self.y - orb.y)**2)**0.5 < orb.r+5:
                orb.pollinated = True
                #return True
            return False


#-------------------------------------------------------------------
#The helperBee is clumsy
class helperBee:
    def __init__(self,app):
        #Load the bee gif
        myGif = Image.open('D:/CMU/semester2/15-112/term_project/giphy.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//10, myGif.size[1]//10))
            fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteList.append(fr)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)

        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, acceleration
        self.x, self.y = 500,500
        self.dy = random.randrange(-5,5)
        self.dx = random.randrange(-5,5)

        self.ddy = .1

    def draw(self,app):
        #Draw current bee sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        if app.pollinated1 != False:
            drawCircle(self.x-18, self.y+45, 12, fill = 'orange', opacity = 75)
        
    def doStep(self):
        self.y += self.dy
        self.x += self.dx
        if self.x <= 0 or self.x >= 600:
            self.dx = -1*self.dx
        if self.y <= 0 or self.y >= 600:
            self.dy = -1*self.dy
        self.stepCounter += 1
        if self.stepCounter >= 2000: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        #Update position and velocity
    



    def isColliding(self, orbs,app):
        for orb in orbs:
            if ((self.x - orb.x)**2 + (self.y - orb.y)**2)**0.5 < orb.r+5:
                orb.pollinated = True
                return True
            return False

#-------------------------------------------------------------------
class Orb:
    def __init__(self, app):
        self.x = random.randrange(app.width)
        self.y = 0
        self.dy = random.randrange(2, 4)
        self.dx = random.randrange(-3, 3)
        
        self.r = random.randrange(10, 35)
        self.color = random.choice(['red', 'yellow', 'blue'])
        self.max_size = self.r * 1.5
        self.growth_rate = 0.2
        self.pollinated = False
        self.needToDraw = False
        self.pollinateCount = 0
        self.immature =False
        self.needToDrawAgain = False
        self.pollenDraw = False

    def doStep(self):
        self.y += self.dy
        self.x += self.dx
        if self.x <= 0 or self.x >= 600:
            self.dx = -1*self.dx
        if self.r <= self.max_size:
            self.r += self.growth_rate
        #self.x += random.randrange(-2,2) * self.dx

    def draw(self,app):
        if self.immature == True:
            drawCircle(self.x, self.y, (self.r)//2, fill = 'green')
            drawCircle(self.x, self.y, self.r, fill = self.color, opacity = 25)
            
            drawLabel("immature", self.x, self.y, size = 8)
        if self.needToDraw == False and self.needToDrawAgain == False:
            drawCircle(self.x, self.y, self.r, fill = self.color, opacity = 75)
        elif self.needToDraw == False and self.needToDrawAgain == True:
            drawCircle(self.x, self.y, self.r-5, fill = self.color, opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//2, fill = 'white', opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//4, fill = self.color, opacity = 75)
        elif self.needToDraw == True:
            drawCircle(self.x, self.y, self.r-5, fill = self.color, opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//2, fill = 'white', opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//4, fill = self.color, opacity = 75)

    def offLeftEdge(self):
            return self.x < 0 - self.r
    
    def offBottomEdge(self, app):
        return self.y > app.height
    def comesOut(self, app):
        return self.y >0 and self.y < app.height
    
    def pollination(self, bee):
        if self.r >=30:
            if ((self.x - bee.x)**2 + (self.y - bee.y)**2)**0.5 < self.r+5:
                
                return True
            
        else:
            if self.max_size<30:
                self.immature = True
            return False
        

#-------------------------------------------------------------------
class Pollen:
    def __init__(self):
        self.r = 12
        self.counter = 0
        self.colorList = []
        self.needToDraw = False


    def draw(self,bee,orbs):
        
            
        for orb in orbs:
            if orb.needToDraw == True and orb.needToDrawAgain == False:
                #color = random.choice(['red', 'yellow', 'blue'])
                self.colorList.append(orb.color)
                
                self.counter += 1
                orb.needToDraw = False
                orb.needToDrawAgain = True
                self.needToDraw = True
            if self.counter ==1:
                drawCircle(bee.x-10, bee.y+45, self.r, fill = self.colorList[self.counter-1], opacity = 75)
            elif self.counter ==2:
                drawCircle(bee.x-18, bee.y+45, self.r, fill = self.colorList[self.counter-2], opacity = 75)
                drawCircle(bee.x, bee.y+45, self.r, fill = self.colorList[self.counter-1], opacity = 75)
            elif self.counter ==3:
                drawCircle(bee.x-30, bee.y+45, self.r, fill = self.colorList[self.counter-3], opacity = 75)
                drawCircle(bee.x-10, bee.y+45, self.r, fill = self.colorList[self.counter-2], opacity = 75)
                drawCircle(bee.x+10, bee.y+45, self.r, fill = self.colorList[self.counter-1], opacity = 75)
            elif self.counter > 3:
                drawCircle(bee.x-18, bee.y+45, self.r, fill = self.colorList[self.counter-3], opacity = 75)
                drawCircle(bee.x-6, bee.y+45, self.r, fill = self.colorList[self.counter-2], opacity = 75)
                drawCircle(bee.x+6, bee.y+45, self.r, fill = self.colorList[self.counter-1], opacity = 75)
            for i in range(len(self.colorList)):
                #if ppollen in trash can
                drawCircle(100+20*i, 50, 20, fill = self.colorList[i], opacity = 75)

            

        
#-------------------------------------------------------------------
def onAppStart(app):
    restart(app)

def restart(app):
    app.gameOver = False
    app.paused = False
    app.stepsPerSecond = 50
    app.bee = Bee()
    app.helperBee = helperBee(app)
    app.orbs = []
    app.pollinatedOrbs = []
    app.lastOrbTime = time.time()
    app.score = 0
    app.label = ''
    app.pollinateCount = 0
    app.pollinated = False
    app.pollinated1 = False
    app.helperShow = False
    app.needToDraw = False
    app.pollen = Pollen()

    
    
def onStep(app):
    if app.paused == False and app.gameOver == False:
    
        takeStep(app)
        

def takeStep(app):
    app.bee.doStep()
    if app.helperShow == True:
        app.helperBee.doStep()
    i = 0

    #Update the orbs
    while i < len(app.orbs):
        orb = app.orbs[i]
        orb.doStep()
        if orb.offBottomEdge(app):
            app.orbs.pop(i)
            print('pop')
            app.score += 1
            if app.score >= 1 and app.score<=10:
                app.helperShow = True
        
        if orb.pollination(app.bee):
            # app.pollinateCount += 0.05
            # totalCount = int(app.pollinateCount//1)
            orb.pollinateCount += 0.05
            totalCount = int(orb.pollinateCount//1)
            if totalCount >=1:
                
                orb.needToDraw = True
                app.pollinated = True

            app.pollinateCount += totalCount
            app.orbPollinated = True
            
            app.label = f'You have pollinate {app.score} times'
            

        if orb.pollination(app.helperBee):
            # app.pollinateCount += 0.05
            # totalCount = int(app.pollinateCount//1)
            orb.pollinateCount += 0.05
            totalCount = int(orb.pollinateCount//1)
            if totalCount >=1:
                totalCount = 1
                orb.needToDraw = True
                app.pollinated1 = True
            app.pollinateCount += totalCount
            app.orbPollinated = True
            
            

        if app.bee.isColliding(app.orbs,app) or app.helperBee.isColliding(app.orbs, app):
            app.pollinated = True
            
            
           
        else:
            i += 1
            

    if (time.time() - app.lastOrbTime > 2) and (len(app.orbs) < 5):
        app.orbs.append(Orb(app))
        app.lastOrbTime = time.time()

    if app.bee.y > app.height or app.bee.y < 0 or app.bee.x > app.width or app.bee.x < 0:
        app.gameOver = True

        app.label = 'Game over you dumb'
  

def onMouseMove(app, mouseX, mouseY):
    # This is called when the user moves the mouse
    # while it is not pressed:
    if app.gameOver == False:
        app.bee.x = mouseX
        app.bee.y = mouseY

def onKeyPress(app, key):
    
    if key == 'r':
        restart(app)
    elif key =='p':
        app.paused = not app.paused
    else:
        app.bee.flap()

def redrawAll(app):
    # #new BG of garden gif
    # myBgGif = Image.open('D:/CMU/semester2/15-112/term_project/garden.gif')
    # spriteList = []
    # for frame in range(myBgGif.n_frames):  #For every frame index...
    #     #Seek to the frame, convert it, add it to our sprite list
    #     myBgGif.seek(frame)
    #     fr = myBgGif.resize((myBgGif.size[0] * 2, myBgGif.size[1]*3))
    #     fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    #     fr = CMUImage(fr)
    #     spriteList.append(fr)

    # ##Fix for broken transparency on frame 0
    # spriteList.pop(0)

    # #Set sprite counters
    
    # spriteCounter = 0


    # #Draw current bee sprite
    # drawImage(spriteList[spriteCounter], 
    #             200, 300, align = 'center')
    #Background
    #drawRect(0, 0, app.width, app.height, fill='lightGreen')
    drawLabel(app.label, 200, 10, size = 12)
    drawLabel(f"Your score is: {app.score}", 200, 25, size = 12)
    #Call bee's draw method
    app.bee.draw(app)
    if app.helperShow == True:
        app.helperBee.draw(app)

    app.pollen.draw(app.bee,app.orbs)

    #Call each orb's draw method
    for orb in app.orbs:
        orb.draw(app)
    for orb in app.pollinatedOrbs:
        orb.draw(app)
    
#Change width and height to suit your needs    
runApp(width=600, height=600)
