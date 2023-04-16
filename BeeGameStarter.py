from cmu_graphics import *
from PIL import Image
import random, time

class Kirb:
    def __init__(self):
        #Load the kirb gif
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
        #Draw current kirb sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        if app.pollinated != False:
            drawCircle(self.x-18, self.y+45, 12, fill = 'black', opacity = 75)
        
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        #Update position and velocity
        # self.y += self.dy
        # self.dy += self.ddy

        #Don't let your pal down
        if self.y >= 550:
            self.y = 550
            self.dy = 0

    def flap(self):
        self.dy = -3

    def isColliding(self, orbs,app):
        for orb in orbs:
            if ((self.x - orb.x)**2 + (self.y - orb.y)**2)**0.5 < orb.r+5:
                orb.pollinated = True
                #return True
            return False


#-------------------------------------------------------------------
class helperBee:
    def __init__(self,app):
        #Load the kirb gif
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
        self.x, self.y = 250,250
        self.dy = 0
        self.ddy = .1

    def draw(self,app):
        #Draw current kirb sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        if app.pollinated != False:
            drawCircle(self.x-18, self.y+45, 12, fill = 'black', opacity = 75)
        
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 2000: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        #Update position and velocity
        self.y += random.randrange(-10,10)
        self.x += random.randrange(-10,10)

        #Don't let your pal down



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
        self.dy = random.randrange(2, 5)
        self.dx = random.randrange(3, 4)
        self.r = random.randrange(10, 50)
        self.color = random.choice(['red', 'yellow', 'blue'])
        self.max_size = self.r * 1.5
        self.growth_rate = 1
        self.pollinated = False
        self.needToDraw = False
        self.pollinateCount = 0

    def doStep(self):
        self.y += self.dy
        #self.x += random.randrange(-2,2) * self.dx

    def draw(self,app):
        if self.needToDraw == False:
            drawCircle(self.x, self.y, self.r, fill = self.color, opacity = 75)
        elif self.needToDraw == True:
            drawCircle(self.x, self.y, self.r, fill = self.color, opacity = 75)
            drawCircle(self.x, self.y, (self.r)//2, fill = 'white', opacity = 75)

    def offLeftEdge(self):
            return self.x < 0 - self.r
    
    def offBottomEdge(self, app):
        return self.y > app.height
    def comesOut(self, app):
        return self.y >0 and self.y < app.height
    
    def pollination(self, bee):
        if ((self.x - bee.x)**2 + (self.y - bee.y)**2)**0.5 < self.r+5:
            
            return True
        return False
        
    
    def checkMaxSize(self):
        if self.r < self.max_size:
            self.r += self.growth_rate

#-------------------------------------------------------------------
def onAppStart(app):
    restart(app)

def restart(app):
    app.gameOver = False
    app.paused = False
    app.stepsPerSecond = 50
    app.kirb = Kirb()
    app.helperBee = helperBee(app)
    app.orbs = []
    app.pollinatedOrbs = []
    app.lastOrbTime = time.time()
    app.score = 0
    app.label = ''
    app.pollinateCount = 0
    app.pollinated = False
    app.helperShow = False
    app.needToDraw = False

    
    
def onStep(app):
    if app.paused == False and app.gameOver == False:
    #Update the kirb
        takeStep(app)
        

def takeStep(app):
    app.kirb.doStep()
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
        
        if orb.pollination(app.kirb) or orb.pollination(app.helperBee):
            # app.pollinateCount += 0.05
            # totalCount = int(app.pollinateCount//1)
            orb.pollinateCount += 0.05
            totalCount = int(orb.pollinateCount//1)
            if totalCount >=1:
                totalCount = 1
                orb.needToDraw = True
            app.pollinateCount += totalCount
            app.orbPollinated = True
            app.label = f'You have pollinate {app.pollinateCount} times'
            

        if app.kirb.isColliding(app.orbs,app) or app.helperBee.isColliding(app.orbs, app):
            app.pollinated = True
            
            
           
        else:
            i += 1
            

    if (time.time() - app.lastOrbTime > 2) and (len(app.orbs) < 5):
        app.orbs.append(Orb(app))
        app.lastOrbTime = time.time()

    if app.kirb.y > app.height or app.kirb.y < 0 or app.kirb.x > app.width or app.kirb.x < 0:
        app.gameOver = True

        app.label = 'Game over you dumb'
    # if app.kirb.isColliding(app.orbs,app) or app.helperBee.isColliding(app.orbs, app):
    #     app.pollinated = True
    #     app.pollinateCount += 1
    #     app.label = f'You have pollinate {app.pollinateCount} times'

def onMouseMove(app, mouseX, mouseY):
    # This is called when the user moves the mouse
    # while it is not pressed:
    if app.gameOver == False:
        app.kirb.x = mouseX
        app.kirb.y = mouseY

def onKeyPress(app, key):
    #Flappy kirb!
    #app.kirb.flap()
    if key == 'r':
        restart(app)
    elif key =='p':
        app.paused = not app.paused
    else:
        app.kirb.flap()

def redrawAll(app):
    #new BG of garden gif
    myBgGif = Image.open('D:/CMU/semester2/15-112/term_project/garden.gif')
    spriteList = []
    for frame in range(myBgGif.n_frames):  #For every frame index...
        #Seek to the frame, convert it, add it to our sprite list
        myBgGif.seek(frame)
        fr = myBgGif.resize((myBgGif.size[0] * 2, myBgGif.size[1]*3))
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        fr = CMUImage(fr)
        spriteList.append(fr)

    ##Fix for broken transparency on frame 0
    spriteList.pop(0)

    #Set sprite counters
    
    spriteCounter = 0


    #Draw current kirb sprite
    drawImage(spriteList[spriteCounter], 
                200, 300, align = 'center')
    #Background
    #drawRect(0, 0, app.width, app.height, fill='lightGreen')
    drawLabel(app.label, 200, 10, size = 12)
    drawLabel(f"Your score is: {app.score}", 200, 25, size = 12)
    #Call kirb's draw method
    app.kirb.draw(app)
    if app.helperShow == True:
        app.helperBee.draw(app)

    #Call each orb's draw method
    for orb in app.orbs:
        orb.draw(app)
    for orb in app.pollinatedOrbs:
        orb.draw(app)
    
#Change width and height to suit your needs    
runApp(width=600, height=600)
