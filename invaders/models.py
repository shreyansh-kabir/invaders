"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Shreyansh Kabir sk2827 George Margono gm564
# Dec 10 2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _ship: _ship is a Ship object
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y):
        '''
        Initializes ship at position x,y.

        Parameter x: the x-coordinate of ship
        Precondition: x is a number (int or float)

        Parameter y: the y-coordinate of ship
        Precondition: y is a number (int or float)
        '''
        super().__init__(x=x,y=y, width=SHIP_WIDTH, height= SHIP_HEIGHT, source='ship.png')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    ####ADD MOVING THE SHIP LEFT OR RIGHT METHOD HERE FROM THE WAVE CLASS AND THEN JUST CALL IT THERE
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt():
            return False

        if self.contains((bolt.x-BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)):
            return True


    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,source):
        '''
        Initializes an alien at position x,y.

        Parameter x: the x-coordinate of alien
        Precondition: x is a number (int or float)

        Parameter y: the y-coordinate of alien
        Precondition: y is a number (int or float)
        '''
        assert isinstance(x,int) or isinstance(x,float)
        assert isinstance(y,int) or isinstance(y,float)

        super().__init__(x=x,y=y,width=ALIEN_WIDTH,\
        height=ALIEN_HEIGHT,source=source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #CHECK FOR ALL  CORNER corners
        if not bolt.isPlayerBolt():
            return False

        if self.contains((bolt.x-BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x-BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2)):
            return True
        elif self.contains((bolt.x+BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)):
            return True

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _trackvel: keeps track of velocity (up or down)
    #Invariant: _trackvel is 0(up- playerbolt) or 1(down- alienbolt)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBolt(self):
        return self._bolt
    def getBoltVel(self):
        return self._velocity
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,velocity,fillcolor):
        assert isinstance(x,int) or isinstance(x,float)
        assert isinstance(y,int) or isinstance(y,float)
        assert isinstance(velocity,int) or isinstance(velocity,float)
        super().__init__(x=x,y=y, width=BOLT_WIDTH,height= BOLT_HEIGHT,\
        fillcolor=fillcolor)
        self._velocity=velocity
        self._trackvel=0
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        '''
        Checks if the given bolt is fired by a player
        '''
        if self._velocity>0:
            return True
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
