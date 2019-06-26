import math


def ballPath(startx, starty, power, ang, time):
    angle = ang
    velx = math.cos(angle) * power
    vely = math.sin(angle) * power

    distX = velx * time
    distY = (vely * time) + ((-9.8 * (time ** 2)) / 2)

    newx = round(distX + startx)
    newy = round(starty - distY)

    return (newx, newy)


def findPower(power, angle, time):
    velx = math.cos(angle) * power
    vely = math.sin(angle) * power

    vfy = vely + (-9.8 * time)
    vf = math.sqrt((vfy**2) + (velx**2))

    return vf


def findAngle(power, angle):
    vely = math.sin(angle) * power
    velx = math.cos(angle) * power

    ang = math.atan(abs(vely) / abs(velx))

    return ang


def maxTime(power, angle):
    vely = math.sin(angle) * power
    time = ((power * -1) - (math.sqrt(power**2))) / -9.8

    return time / 2