"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Shreyansh Kabir sk2827 George Margono gm564
# Dec 10 2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _trackmov: the movement direction (right or left) of aliens
    # Invariant: _trackmov is an int= 0 or 1, corresponding to right and left respectively
    #
    #Attribute _bolttime: The time elapsed from the last shot
    #Invariant: _bolttime is an int between 1 and BOLT_RATE
    #
    #Attribute _flagcollides: Keeps track of collision of player with alien bolts
    #Invariant: _flagcollides is an int either 1 or 0
    #Attribute _gameover: Keeps track of the game (all aliens dead or crossed defense line)
    #Invariant: _gameover is a bool either True or False

    #Attribute _winner: result of the game (Win or Lose)
    #Invariant: _winner is a bool either True (Win)/ False (Defeat) or None
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the player ship to control
        """
        return self._ship

    def getLives(self):
        """
        Returns the number of lives
        """
        return self._lives
    def getFlagcollides(self):
        """
        Returns whether or not there is a collision
        """
        return self._flagcollides
    def setFlagcollides(self):
        """
        Sets ship collision to 0 (no collision)
        """
        self._flagcollides=0
    def getGameover(self):
        """
        Returns whether or not the game is over
        """
        return self._gameover

    def getWinner(self):
        """
        Returns the result of the game
        """
        return self._winner

    def setWinner(self,value):
        self._winner=value
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        #intializing aliens
        self._aliens=[]
        self.aliens_in_wave()
        self._ship=Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM)
        self._dline=GPath(linewidth=2,points=[0,DEFENSE_LINE,\
        GAME_WIDTH,DEFENSE_LINE],linecolor='black')
        self._time=0
        self._trackmov= 0
        self._bolts=[]
        self._lives=SHIP_LIVES
        self._bolttime=0
        self._flagcollides=0
        self._gameover= False
        self._winner= None

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        #SHIP MOVEMENT
        self.shipmove(input)
        #Create PlayerBolt when up arrow pressed
        self.playerbolt(input)
        #Moving player bolts
        for bolt in self._bolts:
            bolt.y+=bolt.getBoltVel()

        #ALIENS MOVEMENT
        self.aliensmov(dt)
        #FIRING & MOVING ALIEN BOLTS
        t= random.randint(1,BOLT_RATE)
        if self._bolttime>=BOLT_RATE:
            #FIRE BOLT
            self.alienbolt()
            self._bolttime=0
        elif self._bolttime == t:
            #FIRE Bolt
            self.alienbolt()
            self._bolttime=0

        #Deleting bolts offscreen
        self.removbolt()
        #Checking collisions
        self.checkcollision()


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    #Helper for ship movement
    def shipmove(self,input):
        if input.is_key_down('left'):
            if self._ship != None:
                self._ship.x-=SHIP_MOVEMENT
        if input.is_key_down('right'):
            if self._ship != None:
                self._ship.x += SHIP_MOVEMENT
    #Helper for aliens movement
    def aliensmov(self,dt):
        if self._time>ALIEN_SPEED:
            if self._trackmov== 0:
                self.alien_f()
                self._time=0
            if self._trackmov==1:
                self.alien_b()
                self._time=0
            self._bolttime+=ALIEN_SPEED
        else:
            self._time+=dt


    #Helper for finding number of columns
    def number_col(self):
        count_col=0
        for i in range(0,ALIENS_IN_ROW):
            count_aliens=0
            for row in self._aliens:
                if row[i]==None:
                    count_aliens+=1
            if count_aliens != ALIEN_ROWS:
                count_col+=1
        return count_col

    #Helper for creating alien wave
    def aliens_in_wave(self):
        x= ALIEN_H_SEP+ALIEN_WIDTH/2
        y=GAME_HEIGHT-((ALIEN_ROWS-1)*(ALIEN_HEIGHT+ALIEN_V_SEP)+ALIEN_CEILING)
        for i in range(ALIEN_ROWS):
            a_row=[]
            for j in range(ALIENS_IN_ROW):
                a_row.append(Alien(x,y,source=ALIEN_IMAGES[(i//2)%3]))
                x=x+ALIEN_H_SEP+ALIEN_WIDTH
            x=ALIEN_H_SEP + ALIEN_WIDTH/2
            self._aliens.append(a_row)
            y=y + ALIEN_V_SEP + ALIEN_HEIGHT



    #Helper for moving aliens to the right
    def alien_f(self):
        '''
        Task1: right move
        Task2: if hit right wall
               then move every alien down
               check if lowest row touch defense line - game over
        Task3: change _trackmov=1
        '''
        flag_f=0
        r_alien = self.rightmost()
        for wave in self._aliens:
            if r_alien is not None:
                if r_alien.x >= GAME_WIDTH-(ALIEN_H_SEP+ALIEN_WIDTH/2):
                    flag_f=1
                    break
        if flag_f==1:
            #DO TASK 2
            for wave in self._aliens:
                for alien in wave:
                    if self.down_valid() and (alien is not None):
                        alien.y-=ALIEN_V_WALK
                    if not self.down_valid():
                        self._gameover=True
                        self._winner=False
            #DO TASK 3
            self._trackmov=1

        else:
            #DO TASK 1
            for wave in self._aliens:
                for alien in wave:
                    if alien is not None:
                        alien.x+=ALIEN_H_WALK

    #Finding rightmost alien when aliens moving forward
    def rightmost(self):
        rightmost_alien = None
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    rightmost_alien = alien
        return rightmost_alien




    #Helper for moving aliens to the left
    def alien_b(self):
        '''
        Task1: left move
        Task2: if hit left wall
               then move every alien down
               check if lowest row touch defense line - game over
        Task3: change _trackmov=0
        '''
        flag_b=0
        l_alien = self.leftmost()
        if l_alien is not None:
            if l_alien.x <= ALIEN_H_SEP+ALIEN_WIDTH/2:
                flag_b=1

        if flag_b==1:
            #DO TASK 2
            for wave in self._aliens:
                for alien in wave:
                    if self.down_valid() and (alien is not None):
                        alien.y-=ALIEN_V_WALK
                    if not self.down_valid():
                        self._gameover=True
                        self._winner=False
            #DO TASK 3
            self._trackmov=0
        else:
            #DO TASK 1
            for wave in self._aliens:
                for alien in wave:
                    if alien is not None:
                        alien.x-=ALIEN_H_WALK

    #Helper for finding leftmost element when aliens moving backward
    def leftmost(self):
        leftmost_alien = None
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    leftmost_alien = alien
                    break  # Break once the leftmost alien in the row is found
        return leftmost_alien




    #Helper for checking if any alien has crossed the defense line
    def down_valid(self):
        '''
        Checking if the any wave has crossed defense line or not
        '''
        for wave in self._aliens:
            for alien in wave:
                if alien is not None:
                    if alien.y < DEFENSE_LINE + ALIEN_HEIGHT/2:
                        return 0
                    else:
                        return 1

    #Helper for deleting bolts going offscreen from the list _bolts
    def removbolt(self):
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].y > GAME_HEIGHT:
                del self._bolts[i]
            else:
                i += 1

    #Helper for checking there is only one playerbolt
    def playerbolt(self, input):
        x=True
        if self._ship !=None:
            for bolt in self._bolts:
                if bolt.isPlayerBolt():
                    x=False
            if x and (input.is_key_pressed('up') or input.is_key_pressed('space')):
                bolt=Bolt(x=self._ship.x,y=SHIP_HEIGHT/2 + SHIP_BOTTOM, \
                velocity=BOLT_SPEED,fillcolor='blue')
                self._bolts.append(bolt)


    #Helper for choosing random bottomost alien and firing bolt
    def alienbolt(self):
        # randcol=random.randint(1,len(self._aliens[0])-1)
        # for row in self._aliens:
        #     for alien in self._aliens[][randcol]:
        alienb_flag=1
        l=[]
        while alienb_flag:
            randcol=random.randint(0,len(self._aliens[0])-1)
            for rows in self._aliens:
                if rows[randcol] != None:
                    alienb_flag=0
                l.append(rows[randcol])
        for i in range(0,len(l)-1,1):
            if self._aliens[i][randcol]!=None:
                self._bolts.append(Bolt(x=self._aliens[i][randcol].x,\
                y=self._aliens[i][randcol].y -(ALIEN_HEIGHT/2 + BOLT_HEIGHT/2),\
                velocity=-BOLT_SPEED,fillcolor='red'))
                break


    #Helper for finding a random column that is not None
    def NoneCol(self):
        random_flag=1
        while flag:
            randcol=random.randint(1,len(self._aliens[0])-1)
            for rows in self._aliens:
                if rows[randcol] is not None:
                    random_flag=0


    # HELPER METHODS FOR COLLISION DETECTION
    def checkcollision(self):
        for bolt in self._bolts:
            #alien collisions
            if bolt.isPlayerBolt():
                for row in range(ALIEN_ROWS):
                    for alien in range(ALIENS_IN_ROW):
                        if self._aliens[row][alien] is not None:
                                if self._aliens[row][alien].collides(bolt):
                                    self._aliens[row][alien] = None
                                    self._bolts.remove(bolt)
                                    if self.checkaliens():
                                        self._gameover=True
                                        self._winner=1

            #ship collisions
            if not bolt.isPlayerBolt():
                for bolt in self._bolts:
                    if self._ship !=None:
                        if self._ship.collides(bolt):
                            self._flagcollides=1
                            self._ship=None
                            self._bolts.remove(bolt)
                            self._lives-=1
    #Helper for creating a ship object
    def createship(self):
        self._ship=Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM)

    #Helper for when all aliens are killed
    def checkaliens(self):
        flag_aliens=True
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    flag_aliens= False
        return flag_aliens
