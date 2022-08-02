import msgParser
import carState
import carControl
import keyboard


class Driver(object):
    """
    A driver object for the SCRC
    """

    def __init__(self, stage):
        """Constructor"""
        self.WARM_UP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = 3
        self.stage = stage
        self.next_stage = ' '
        self.parser = msgParser.MsgParser()

        self.state = carState.CarState()

        self.control = carControl.CarControl()

        self.steer_lock = 0.785398
        self.max_speed = 100
        self.prev_rpm = None
        self.upwards = 0
        self.downwards = 0
        self.left = 0
        self.right = 0

    def init(self):
        """Return init string with rangefinder angles"""
        self.angles = [0 for x in range(19)]

        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15

        for i in range(5, 9):
            self.angles[i] = -20 + (i - 5) * 5
            self.angles[18 - i] = 20 - (i - 5) * 5

        return self.parser.stringify({'init': self.angles})

    def drive(self, msg):
        self.state.setFromMsg(msg)
        self.steer()
        self.gear()
        self.speed()
        # if keyboard.is_pressed("up"):
        #     rpm = self.state.getRpm()
        #     gear = self.state.getGear()
        #     self.control.setAccel(0.4)
        #     self.gear()
        #     # if rpm > 3000:
        #     #    gear += 1
        #     self.control.setGear(gear)
        # elif keyboard.is_pressed("down"):
        #     print("down arrow was pressed ")
        #     self.control.setAccel(-0.4)
        # elif keyboard.is_pressed("left"):
        #     steer = self.control.getSteer()
        #     steer = 0.15
        #     print("left arrow was pressed ")
        #     self.control.setSteer(steer)
        #     self.control.setSteer(0)
        # elif keyboard.is_pressed("right"):
        #     steer = self.control.getSteer()
        #     steer = -0.15
        #     print("right arrow was pressed ")
        #     self.control.setSteer(steer)
        #     self.control.setSteer(0)
        return self.control.toMsg()

    def steer(self):
        angle = self.state.angle
        dist = self.state.trackPos
        if self.next_stage == "Right":#keyboard.is_pressed("right"):
            self.control.setSteer(-0.5)  # (angle - dist * 0.5) / self.steer_lock
            self.upwards=0
            self.downwards=0
            self.right=1
            self.left=0
            self.next_stage=0
        elif self.next_stage == "Left":#keyboard.is_pressed("left"):
            self.control.setSteer(0.5)  # (angle - dist * 0.5) / self.steer_lock
            self.upwards = 0
            self.downwards = 0
            self.right = 0
            self.left = 1
            self.next_stage=0
        # else:
        #     self.control.setSteer(0.0)

    def gear(self):
        gear = self.state.getGear()
        rpm = self.state.getRpm()
        if self.prev_rpm is None:
            up = True
        else:
            if (self.prev_rpm - rpm) < 0:
                up = True
            else:
                up = False
        
        if up and rpm > 7000:
            gear += 1
        
        if not up and rpm < 3000:
            gear -= 1
        
        # speed = self.state.getSpeedX()
        # if speed >=0 and speed < 40:
        #     gear=1
        # elif speed >=40 and speed < 95:
        #     gear=2
        # elif speed >=95 and speed < 140:
        #     gear=3
        # elif speed >=140 and speed < 190:
        #     gear=5
        # elif speed >= 190:
        #     gear=6
        # else:
        #     gear=1
        self.control.setGear(gear)
    def speed(self):
        if self.next_stage == "Up":#keyboard.is_pressed("up"):
            self.control.setBrake(0)
            self.control.setAccel(0.6)
            self.upwards=1
            self.downwards=0
            self.control.setSteer(0.0)
            self.left=0
            self.right=0
            # self.next_stage=0
        elif self.next_stage == "Down":#keyboard.is_pressed("down"):
            self.control.setAccel(-0.5)
            self.control.setBrake(0.2)
            self.upwards = 0
            self.downwards = 1
            self.left = 0
            self.right = 0
            # self.next_stage=0
        else:
            self.control.setAccel(0.0)
            self.control.setBrake(0.0)

        # speed = self.state.getSpeedX()
        # accel = self.control.getAccel()
        #
        # if speed < self.max_speed:
        #     accel += 0.1
        #     if accel > 1:
        #         accel = 1.0
        # else:
        #     accel -= 0.1
        #     if accel < 0:
        #         accel = 0.0
        #
        # self.control.setAccel(accel)

    def onShutDown(self):
        pass

    def onRestart(self):
        pass
