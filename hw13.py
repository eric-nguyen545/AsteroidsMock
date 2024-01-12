import turtle, random, math

class Game:
    '''
    Purpose:
        Create a space game, where the user has to dodge meteors, and succesfully land a spaceship on the surface of the moon. 
    Instance variables:
        This class does not contain any instance variables
    Methods:
        gameloop: Loop through the move and gravity functions associated with the Spaceship and Meteorite classes. 
                    Also checks the position of the spaceship and meteors to see if they collide, thus ending the game.
                    Also checks the position of the spaceship to determine if it has landed. 
    '''
    def __init__(self):
        #Bottom left corner of screen is (0, 0)
        #Top right corner is (500, 500)
        turtle.setworldcoordinates(0, 0, 500, 500)
        cv = turtle.getcanvas()
        cv.adjustScrolls()
    
        #Ensure turtle is running as fast as possible
        turtle.delay(0)

        #Create the 'moon' 
        turtle.goto(250, -460)
        turtle.dot(1250, 'gray') 
        
        self.player = SpaceCraft(random.uniform(100,400), random.uniform(250, 450), random.uniform(-4, 4), random.uniform(-2, 0))
        self.obj = []
        for i in range(20):
            self.obj.append(Meteorite(random.uniform(0,500), 510, random.uniform(-4, 4), random.uniform(-4, 0)))

        self.gameloop()

        turtle.onkeypress(self.player.thrust, 'Up')
        turtle.onkeypress(self.player.left_turn, 'Left')
        turtle.onkeypress(self.player.right_turn, 'Right')

        #These two lines must always be at the BOTTOM of __init__
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        if self.player.pos()[1] <= 20:
            if -3 <= self.player.x_velo <= 3 and -3 <= self.player.y_velo <= 3:
                turtle.hideturtle()
                turtle.penup()
                turtle.goto(130,300)
                turtle.write('Succesful Landing!', font = ('fixedsys', 20, 'normal'))
                turtle.done()
            else:
                turtle.hideturtle()
                turtle.penup()
                turtle.goto(160,300)
                turtle.write('You crashed!', font = ('fixedsys', 20, 'normal'))
                turtle.done()
        else:
            self.player.move()
            crash = False
            for i in range(len(self.obj)):
                if (abs(self.player.xcor() - self.obj[i].xcor()) < 7) and (abs(self.player.ycor() - self.obj[i].ycor()) < 7):
                    turtle.hideturtle()
                    turtle.penup()
                    turtle.goto(160,300)
                    turtle.write('You crashed!', font = ('fixedsys', 20, 'normal'))
                    crash = True
                else:
                    self.obj[i].gravity()
            if crash == False:
                turtle.ontimer(self.gameloop, 30)

        
class Meteorite(turtle.Turtle):
    '''
    Purpose:
        This class produces a turtle object representing a meteor
    Instance variables:
        obj_x_pos: The starting x coordinate of the meteor
        obj_y_pos: The starting y coordinate of the meteor
        obj_x_velo: The starting x velocity of the meteor
        obj_y_velo: The starting x velocity of the meteor
    Methods: 
        gravity: slowly move the meteor down towards the bottom of the screen, if it hits one of the borders, it will bounce off of it. 
    '''
    def __init__(self, obj_x_pos, obj_y_pos, obj_x_velo, obj_y_velo):
        turtle.Turtle.__init__(self)
        self.penup()
        self.ht()
        self.goto(obj_x_pos, obj_y_pos)
        self.st()
        self.shape('circle')
        self.shapesize(0.7)
        self.color('blue')
        self.xv = obj_x_velo
        self.yv = obj_y_velo
    def gravity(self):
        gravity = self.yv - 0.0486
        newx = self.xcor() + self.xv
        newy = self.ycor() + gravity
        if newx > 500:
            newx = 500
            self.xv *= -1
        if newx < 0:
            newx = 0
            self.xv *= -1
        if newy < 0:
            newy = 0
            self.yv *= -1
        else:
            self.goto(newx, newy)

class SpaceCraft(turtle.Turtle):
    '''
    Purpose:
        This class creates a turtle object representing a spaceship.
    Instance variables:
        obj_x_pos: The starting x coordinate of the spaceship
        obj_y_pos: The starting y coordinate of the spaceship
        obj_x_velo: The starting x velocity of the spaceship
        obj_y_velo: The starting x velocity of the spaceship
    Methods:
        move: Slowly moves the spaceship down, representing the gravitational pull of the moon. 
        thrust: Allow the user to input the up arrow key to move the spaceship forwards, and print the remaining fuel.
        left_turn: Allow the user to input the left arrow key to turn the spaceship to the left, and print the remaining fuel.
        right_turn: Allow the user to input the right arrow key to turn the spaceship to the right, and print the remaining fuel.
    '''
    def __init__(self, start_x_pos, start_y_pos, start_x_velo, start_y_velo):
        turtle.Turtle.__init__(self)
        self.x_velo = start_x_velo
        self.y_velo = start_y_velo
        self.x_pos = start_x_pos
        self.y_pos = start_y_pos
        self.fuel = 40
        self.left(90)
        self.penup()
        self.speed(0)
        self.goto(self.x_pos, self.y_pos)
    def move(self):
        gravity = self.y_velo - 0.0486
        self.x_pos = self.xcor() + self.x_velo
        self.y_pos = self.ycor() + gravity
        self.goto(self.x_pos, self.y_pos)
    def thrust(self):
        if self.fuel > 0:
            self.fuel -= 1
            angle = math.radians(self.heading())
            self.x_velo = math.cos(angle) + self.x_velo
            self.y_velo = math.sin(angle) + self.y_velo
            print(self.fuel)
        else:
            print("Out of fuel")
    def left_turn(self):
        if self.fuel > 0:
            self.fuel -= 1
            self.left(15)
            print(self.fuel)
            
        else:
            print("Out of fuel")
    def right_turn(self):
        if self.fuel > 0:
            self.fuel -= 1
            self.right(15)
            print(self.fuel)
        else:
            print("Out of fuel")

if __name__ == '__main__':
    Game()