import numpy as np
import copy as copy
import matplotlib.pyplot as plt

def calc_accel(car, follow_dist):
    """Accelearion is calculated to be max_pos_accel if the car is >30m behind
        the car infront of it, and 0 acceleration if at follow_dist. Linear map
        between the two. If the car is too close, it will decelerate
        according to max_neg_accel if follow_dist is less than 2m and 0 if at
        follow_dist"""
    follow_dist = abs(follow_dist)
    if follow_dist < 2:
        return max_neg_accel
    elif follow_dist < car.follow_dist:
        return -max_neg_accel * (follow_dist - car.follow_dist) / (car.follow_dist - 2)
    elif follow_dist > car.follow_dist:
        accel = max_pos_accel * (follow_dist - car.follow_dist) / (30 - car.follow_dist)
        if accel > max_pos_accel:
            return max_pos_accel
        else:
            return accel 
    else:
        return 0  # no acceleration if at follow_dist

# car class that has position, velocity and acceleration as attributes
class Car:
    def __init__(self, position, velocity, acceleration, follow_dist=10):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.follow_dist = follow_dist

    def __str__(self):
        return f"Car at position {self.position} with velocity {self.velocity} and acceleration {self.acceleration}"

# initialse cars equally spaced in the 0 - 1000 m domain
num_cars = 18
cars = []
acceleration = 0 # initially no cars will accelerate
t = 0
dt = 0.1
simulation_time = 1000
max_pos_accel = 5  # m/s^2
max_neg_accel = -8  # m/s^2
max_vel_diff = 5  # m/s
des_follow_dist = 10  # m
max_dist = 200  # m
for i in range(num_cars):
    # cars have speeds between roughly 85 and 120 km/h
    velocity = np.random.normal(20.5, 0.05)
    velocity_mps = velocity * 1000 / 3600 # convert to m/s
    position = (num_cars - i) * (num_cars*des_follow_dist)*np.random.normal(1, 0.01) / num_cars
    cars.append(Car(position, velocity, acceleration, des_follow_dist))

while t < simulation_time:
    # update the position of each car
    for i in range(len(cars)):
        # update the position of the car
        cars[i].position += cars[i].velocity * dt
        # update the velocity of the car (front car does not accelerate)
        if i == 0:
            cars[i].velocity = cars[i].velocity
        else:
            cars[i].velocity += cars[i].acceleration * dt
        # car velocity cannot be negative
        if cars[i].velocity < 0:
            cars[i].velocity = 0
        # cars can have a max velocity of 120 km/h
        if cars[i].velocity > 120 * 1000 / 3600:
            cars[i].velocity = 120 * 1000 / 3600
        # cars can only ever go 7km/h faster than the car directly in front of them
        if i > 0:
            if cars[i].velocity - cars[i - 1].velocity > max_vel_diff:
                cars[i].velocity = cars[i - 1].velocity + max_vel_diff

    # acceleration is dependent on the distance to the car in front
    for i in range(1, len(cars)):
        follow_dist = cars[i - 1].position - cars[i].position
        cars[i].acceleration = calc_accel(cars[i], follow_dist)

    for i in range(len(cars)):
        if cars[i].position > max_dist:
            cars[i].position -= max_dist
            # create deep copy of old list
            old_list = copy.deepcopy(cars)
            # move the car that has gone off the end to the front of the list
            cars = [cars[i]] + cars[:i] + cars[i+1:]

    # plot the positions of the cars in a dynamic plot
    plt.clf()
    plt.plot([car.position for car in cars], [0 for car in cars], "k.")
    # adjust the x axis to be between the max and min car position
    plt.xlim(0, max_dist)
    plt.ylim(-1, 1)
    plt.title(f"Time: {t}")
    plt.pause(0.1)
    t += dt
plt.show()