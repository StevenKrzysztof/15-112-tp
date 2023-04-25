from cmu_graphics import *
from PIL import Image
import random, time
import math

class Bee:
    def __init__(self):
        #Load the frame
        
        #Load the bee gif
        myGif = Image.open('./bee1.gif')
        self.spriteList = []
        self.spriteListTrans = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//10, myGif.size[1]//10))
            fr2 = fr.transpose(Image.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            fr2 = CMUImage(fr2)
            self.spriteList.append(fr)
            self.spriteListTrans.append(fr2)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)

        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        self.spriteListTrans.pop(0)

        

        #Set initial position, velocity, acceleration
        self.x, self.y = 100, 100
        self.dy = 0
        self.ddy = .1
        self.speed = 0
        self.donotMove = False

    def draw(self,app):
        #Draw current bee sprite
        if app.mousePosX > self.x:
        # Bee is moving right, so don't flip the image
            drawImage(self.spriteList[self.spriteCounter], 
                    self.x, self.y, align = 'center')
        else:
            # Bee is moving left, so flip the image horizontally
            drawImage(self.spriteListTrans[self.spriteCounter], self.x, self.y, align='center')
        # if app.pollinated != False:
        #     drawCircle(self.x-18, self.y+45, 12, fill = 'black', opacity = 75)
        
    def doStep(self,app):
        # Calculate the distance to the mouse position
        dist = math.sqrt((self.x - app.mousePosX)**2 + (self.y - app.mousePosY)**2)

        # Set the bee's speed to be proportional to the distance
        self.speed += dist / 10000

        # Limit the bee's speed to a maximum of 10
        if self.speed > 10:
            self.speed = 10

        # Calculate the direction to the mouse position
        dx = app.mousePosX - self.x
        dy = app.mousePosY - self.y

        # Normalize the direction vector
        # length = math.sqrt(dx**2 + dy**2)
        if dist > 5:
            dx /= dist
            dy /= dist
        #     self.donotMove = False
        # else:
        #     self.donotMove = True


        # Update the bee's position
        self.x += dx * self.speed
        self.y += dy * self.speed


        # Increase the speed of the bee's animation as its speed increases
        if self.speed < 1:
            stepsPerSprite = 10*2
        elif self.speed < 2:
            stepsPerSprite = 8
        elif self.speed < 4:
            stepsPerSprite = 6/2
        else:
            stepsPerSprite = 4/2
        self.stepCounter += 1
        if self.stepCounter >= stepsPerSprite: #Update the sprite every Nth call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        
        



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
        myGif = Image.open('./bee2.gif')
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
        self.x, self.y = app.width//2,app.height//2
        self.dy = random.randrange(-5,5)
        self.dx = random.randrange(-5,5)

        self.ddy = .1
        self.speed = 0
        
        self.closestOrb = None # Store the closest orb
        self.pollinating = False
        self.pollinatedOrb = None
        
    def draw(self,app):
        #Draw current bee sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        if app.pollinated1 != False:
            drawCircle(self.x-18, self.y+45, 12, fill = 'orange', opacity = 75)
        
    def doStep(self, app):
        if not self.pollinating:
            # Find nearest unpollinated orb
            minDist = float('inf')
            closestOrb = None
            for orb in app.orbs:
                if not orb.pollinated:
                    dist = ((self.x - orb.x) ** 2 + (self.y - orb.y) ** 2) ** 0.5
                    if dist < minDist:
                        minDist = dist
                        closestOrb = orb

            if closestOrb is not None:
                # Move towards nearest orb
                dx = closestOrb.x - self.x
                dy = closestOrb.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance != 0:
                    dx /= distance
                    dy /= distance
                self.dx += dx * 0.5
                self.dy += dy * 0.5

                # Limit the bee's speed to a maximum of 5
                self.speed = (self.dx ** 2 + self.dy ** 2) ** 0.5
                if self.speed > 5:
                    self.speed = 5

                # Check if bee has reached orb
                if distance <= closestOrb.r:
                    self.pollinating = True
                    self.pollinatedOrb = closestOrb

        else:
            # Move towards pollinated orb
            dx = self.pollinatedOrb.x - self.x
            dy = self.pollinatedOrb.y - self.y
        # Update bee position and velocity
        self.y += self.dy / 10
        self.x += self.dx / 10
        if self.x <= 0 or self.x >= app.width:
            self.dx = -1 * self.dx
        if self.y <= 0 or self.y >= app.height:
            self.dy = -1 * self.dy

        # Update bee sprite
        self.stepCounter += 1
        if self.stepCounter >= 2000:  # Update the sprite every 10th call
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
        self.x = random.randrange(30,app.width-30)
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
        self.offset = random.uniform(0, 2*math.pi)

    def doStep(self,app):
        self.y += self.dy//2
        self.x += self.dx
        # Add sinusoidal movement to the y-coordinate
        amplitude = 5
        frequency = 0.03
        self.x = amplitude*math.sin(frequency*self.y + self.offset) + self.x
        
        if self.x <= 0:
            self.x = 0
            self.dx = -1*self.dx
        elif self.x >= app.width:
            self.x = app.width
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
class UnpoFlow:
    def __init__(self, app):
        self.x = random.randrange(50, app.width-50)
        self.y = 0
        self.dy = random.randrange(2, 4)
        self.dx = random.randrange(-1, 1)
        
        self.r = random.randrange(15, 30)
        self.color = random.choice(['red', 'yellow', 'blue'])
        self.pollinated = False
        self.needToDraw = False
        self.pollinateCount = 0
        self.needToDrawAgain = False
        self.pollenDraw = False
        self.alreadyPollinated = False
        self.max_size = self.r * 1.5
        self.growth_rate = 0.25
        self.offset = random.uniform(0, 2*math.pi)

    def doStep(self,app):
        self.y += self.dy//2
        self.x += self.dx
        # Add sinusoidal movement to the y-coordinate
        amplitude = 5
        frequency = 0.03
        self.x = amplitude*math.sin(frequency*self.y + self.offset) + self.x
        if self.pollinated== True and self.r <= self.max_size:
        
            self.r += self.growth_rate
        if self.x <= 0:
            self.x = 0 
            self.dx = -1*self.dx
            
        elif self.x >= app.width:
            self.x = app.width
            self.dx = -1*self.dx
            
        

        

    def draw(self,app):
        if self.pollinated == False and self.needToDraw == False:
            drawCircle(self.x, self.y, self.r-5, fill = self.color, opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//2, fill = 'black', opacity = 75)
        # drawCircle(self.x, self.y, (self.r-5)//4, fill = self.color, opacity = 75)
        elif self.needToDraw == True:
            drawCircle(self.x, self.y, self.r-5, fill = self.color, opacity = 75)
            drawCircle(self.x, self.y, (self.r-5)//2, fill = 'purple', opacity = 75)
        

    # def offLeftEdge(self):
    #         return self.x < 0 - self.r
    
    def offBottomEdge(self, app):
        return self.y > app.height
    def comesOut(self, app):
        return self.y >0 and self.y < app.height
    

    def pollination(self, bee,pollen):
        #a pollen list color or a bee list color
        for color in pollen.colorList:
            if color == self.color:
                
                index = pollen.colorList.index(self.color)
                
        
                if (((self.x - bee.x)**2 + (self.y - bee.y)**2)**0.5 < self.r+5) and self.alreadyPollinated == False:
                    
                    if (self.color in pollen.colorList) and (self.color not in pollen.beeColor):
                        pollen.colorList.pop(index)
                    else:
                        
                        index2 = len(pollen.beeColor) - pollen.beeColor[::-1].index(self.color) - 1
                        pollen.colorList.pop(index)

                        pollen.beeColor.pop(index2)
                    self.alreadyPollinated = True
                    self.pollinated = True
                
                    return True
                
                return False
            
            
                
            
        
        
#-------------------------------------------------------------------
class Pollen:
    def __init__(self):
        self.r = 12
        self.counter = 0
        self.colorList = []
        self.beeColor = []
        self.needToDraw = False
        self.alreadyPop = False


    def draw(self,bee,orbs):
        
            
        for orb in orbs:
            if orb.needToDraw == True and orb.needToDrawAgain == False:
                #color = random.choice(['red', 'yellow', 'blue'])
                self.colorList.append(orb.color)
                self.beeColor.append(orb.color)
                
                self.counter += 1
                orb.needToDraw = False
                orb.needToDrawAgain = True
                self.needToDraw = True
            
            
            for i in range(len(self.colorList)):
                
                if i <=5:
                    drawCircle(100+20*i, 50, 20, fill = self.colorList[i], opacity = 75)   

                if i > 5:
                    self.colorList.pop(0)
            
            for j in range(len(self.beeColor)):
                
                if j <=2:
                    drawCircle(bee.x-18+10*j, bee.y+45, self.r, fill = self.beeColor[j], opacity = 75)
                

                if j > 2:
                    self.beeColor.pop(0)
                    
                
            

        
#-------------------------------------------------------------------
def onAppStart(app):
    game_restart(app)

def game_restart(app):
    app.gameOver = False
    app.paused = False
    app.stepsPerSecond = 40
    app.bee = Bee()
    app.helperBee = helperBee(app)
    app.unpolls = []
    app.orbs = []
    app.pollinatedOrbs = []
    app.lastOrbTime = time.time()
    app.lastunpollTime = time.time()
    app.score = 0
    app.label = ''
    app.pollinateCount = 0
    app.pollinated = False
    app.pollinated1 = False
    app.helperShow = False
    app.needToDraw = False
    app.pollen = Pollen()
    app.mousePosX = 100
    app.mousePosY = 100
    app.url = 'https://as2.ftcdn.net/v2/jpg/02/90/87/69/1000_F_290876973_mCltaYqk3G8FWiszXxrCwzUL5wmbGHSt.jpg'
    
    
    
def game_onStep(app):
    if app.paused == False and app.gameOver == False:
    
        game_takeStep(app)
        
def game_onKeyPress(app):
    if app.key =='p':
        app.paused = not app.paused
def game_takeStep(app):
    dist = math.sqrt((app.bee.x - app.mousePosX)**2 + (app.bee.y - app.mousePosY)**2)
    if dist > 5:
        app.bee.doStep(app)
    if app.helperShow == True:
        app.helperBee.doStep(app)
    i = 0

    #Update the orbs
    while i < len(app.orbs):
        orb = app.orbs[i]
        orb.doStep(app)
        if orb.offBottomEdge(app):
            app.orbs.pop(i)
            print('pop')
            app.score += 1
            if app.score >= 1 and app.score<=10:
                app.helperShow = True
        
        if orb.pollination(app.bee):
            # app.pollinateCount += 0.05
            # totalCount = int(app.pollinateCount//1)
            orb.pollinateCount += 0.1
            totalCount = int(orb.pollinateCount//1)
            if totalCount >=1:
                
                orb.needToDraw = True
                app.pollinated = True

            app.pollinateCount += totalCount
            app.orbPollinated = True
            
            app.label = 'You need some time to get pollen'
            

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
            

    if (time.time() - app.lastOrbTime > 2) and (len(app.orbs) < 4):
        app.orbs.append(Orb(app))
        app.lastOrbTime = time.time()


    #update the unpollinated flowers
    j = 0
    while j < len(app.unpolls):
        
        unpoll = app.unpolls[j]
        unpoll.doStep(app)
        if unpoll.offBottomEdge(app):
            app.unpolls.pop(j)
            print('pop2')
        
        if unpoll.pollination(app.bee,app.pollen):
            
                
            unpoll.needToDraw = True
            
            

        if unpoll.pollination(app.helperBee,app.pollen):
                
            unpoll.needToDraw = True
            
            
            
        
        else:
            j += 1
            

    if (time.time() - app.lastunpollTime > 6) and (len(app.unpolls) < 2):
        app.unpolls.append(UnpoFlow(app))
        app.lastunpollTime = time.time()

    if app.bee.y > app.height or app.bee.y < 0 or app.bee.x > app.width or app.bee.x < 0:
        app.gameOver = True

        app.label = 'Game over you dumb'
        setActiveScreen('gameOver')
  

def game_onMouseMove(app, mouseX, mouseY):
    # This is called when the user moves the mouse
    # while it is not pressed:
    if app.gameOver == False:
        app.mousePosX = mouseX
        app.mousePosY = mouseY

def game_onKeyPress(app, key):
    
    if key == 'r':
        game_restart(app)
    elif key =='p':
        app.paused = not app.paused
    

def game_redrawAll(app):
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
    drawRect(0, 0, app.width, app.height, fill='lightGreen')
    drawLabel(app.label, 200, 10, size = 12)
    drawLabel("Press r to restart or p to pause", 200, 25, size = 12)
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
    for unpoll in app.unpolls:
        unpoll.draw(app)
    
#Change width and height to suit your needs    
# runApp(width=800, height=600)
def welcome_redrawAll(app):
    drawImage(app.url,0,0)
    drawLabel("Welcome to The Game", app.width/2, app.height/2, size = 24)
    drawCircle(200,200,50,fill='blue')
    



def welcome_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')
def welcome_onMousePress(app, mouseX, mouseY):
    # This is called when the user presses the mouse.
    # For this example, we just have to update the
    # model to move the dot to this location:
    if ((mouseX-200)**2 + (mouseY-200)**2)**0.5 <= 50:
        setActiveScreen('game')
    
#---------------------------------------------------
#Game Over screen
def gameOver_redrawAll(app):
    drawImage(app.url,0,0)
    drawLabel("Your Game is Over.", app.width/2, app.height/2, size = 24)
    drawLabel("Good Game", app.width/2, 35+app.height/2, size = 20)
    drawLabel("Press R to restart", app.width/2, 75+app.height/2, size = 24)
    drawCircle(200,200,50,fill='blue')
    



def gameOver_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('game')
        game_restart(app)
def gameOver_onMousePress(app, mouseX, mouseY):
    # This is called when the user presses the mouse.
    # For this example, we just have to update the
    # model to move the dot to this location:
    if ((mouseX-200)**2 + (mouseY-200)**2)**0.5 <= 50:
        setActiveScreen('game')
        game_restart(app)

#---------------------------------------------------

# Your screen names should be strings
runAppWithScreens(initialScreen='welcome',width=1000, height=500)
