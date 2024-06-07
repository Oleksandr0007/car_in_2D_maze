import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.transforms import Affine2D

def plot_maze(grid, start, end, path):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')

    x, y = start
    car_length = 1.0
    car_width = 0.5
    rect = Rectangle((y - car_width / 2, x - car_length / 2), car_width, car_length, facecolor='gray', edgecolor='black')

    wheel_length = 0.2
    wheel_width = 0.1
    wheel_offset_x = car_width / 2
    wheel_offset_y = car_length / 2 - wheel_length

    rear_left_wheel = Rectangle((y - wheel_offset_x - wheel_width / 2, x - wheel_offset_y), wheel_width, wheel_length, facecolor='black')
    rear_right_wheel = Rectangle((y + wheel_offset_x - wheel_width / 2, x - wheel_offset_y), wheel_width, wheel_length, facecolor='black')
    front_left_wheel = Rectangle((y - wheel_offset_x - wheel_width / 2, x + wheel_offset_y - wheel_width), wheel_width, wheel_length, facecolor='black')
    front_right_wheel = Rectangle((y + wheel_offset_x - wheel_width / 2, x + wheel_offset_y - wheel_width), wheel_width, wheel_length, facecolor='black')

    headlight_size = 0.05
    headlight_offset_x = car_width / 2 * 0.7
    headlight_offset_y = car_length / 2

    left_headlight = Circle((y - headlight_offset_x, x + headlight_offset_y), headlight_size, facecolor='yellow')
    right_headlight = Circle((y + headlight_offset_x, x + headlight_offset_y), headlight_size, facecolor='yellow')

    plt.gca().add_patch(rect)
    plt.gca().add_patch(rear_left_wheel)
    plt.gca().add_patch(rear_right_wheel)
    plt.gca().add_patch(front_left_wheel)
    plt.gca().add_patch(front_right_wheel)
    plt.gca().add_patch(left_headlight)
    plt.gca().add_patch(right_headlight)

    plt.scatter([end[1]], [end[0]], c='red', s=200, label='End')

    for point in path:
        plt.scatter([point[1]], [point[0]], c='blue', s=50)

    plt.legend()
    plt.xticks([]), plt.yticks([])
    plt.show()

def move_car_along_path(grid, path, car_length=1.0, car_width=0.5, speed=0.05, wheel_base=1.0, max_steering_angle=np.pi/4):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')

    x, y = path[0]
    theta = 0  # Початкова орієнтація вгору

    def create_car_patches(x, y, theta, steering_angle=0):
        transform = Affine2D().rotate_around(y, x, theta) + plt.gca().transData

        rect = Rectangle((y - car_width / 2, x - car_length / 2), car_width, car_length, facecolor='gray', edgecolor='black', transform=transform)
        wheel_length = 0.2
        wheel_width = 0.1
        wheel_offset_x = car_width / 2
        wheel_offset_y = car_length / 2 - wheel_length

        rear_left_wheel = Rectangle((y - wheel_offset_x - wheel_width / 2, x - wheel_offset_y), wheel_width, wheel_length, facecolor='black', transform=transform)
        rear_right_wheel = Rectangle((y + wheel_offset_x - wheel_width / 2, x - wheel_offset_y), wheel_width, wheel_length, facecolor='black', transform=transform)

        # Поворот передніх коліс
        front_left_wheel_transform = Affine2D().rotate_around(y - wheel_offset_x, x + wheel_offset_y - wheel_width / 2, steering_angle) + transform
        front_right_wheel_transform = Affine2D().rotate_around(y + wheel_offset_x, x + wheel_offset_y - wheel_width / 2, steering_angle) + transform

        front_left_wheel = Rectangle((y - wheel_offset_x - wheel_width / 2, x + wheel_offset_y - wheel_width), wheel_width, wheel_length, facecolor='black', transform=front_left_wheel_transform)
        front_right_wheel = Rectangle((y + wheel_offset_x - wheel_width / 2, x + wheel_offset_y - wheel_width), wheel_width, wheel_length, facecolor='black', transform=front_right_wheel_transform)

        headlight_size = 0.05
        headlight_offset_x = car_width / 2 * 0.7
        headlight_offset_y = car_length / 2

        left_headlight = Circle((y - headlight_offset_x, x + headlight_offset_y), headlight_size, facecolor='yellow', transform=transform)
        right_headlight = Circle((y + headlight_offset_x, x + headlight_offset_y), headlight_size, facecolor='yellow', transform=transform)

        patches = [rect, rear_left_wheel, rear_right_wheel, front_left_wheel, front_right_wheel, left_headlight, right_headlight]

        return patches

    car_patches = create_car_patches(x, y, theta)
    for patch in car_patches:
        plt.gca().add_patch(patch)

    def update_position(x, y, theta, speed, steering_angle, wheel_base):
        if abs(steering_angle) > 1e-4:  # Якщо є поворот
            turning_radius = wheel_base / np.tan(steering_angle)
            angular_velocity = speed / turning_radius
            x += turning_radius * (np.sin(theta + angular_velocity) - np.sin(theta))
            y += turning_radius * (np.cos(theta) - np.cos(theta + angular_velocity))
            theta += angular_velocity
        else:  # Якщо рух прямо
            x += speed * np.cos(theta)
            y += speed * np.sin(theta)
        return x, y, theta

    for i in range(1, len(path) - 1):
        x_next, y_next = path[i]
        x_after_next, y_after_next = path[i + 1]

        x_diff = x_next - x
        y_diff = y_next - y
        x_after_diff = x_after_next - x_next
        y_after_diff = y_after_next - y_next

        while np.hypot(x_next - x, y_next - y) > 0.1:
            dx = x_next - x
            dy = y_next - y
            distance = np.hypot(dx, dy)
            x += dx * speed / distance
            y += dy * speed / distance

            steering_angle = 0
            if x_diff != x_after_diff or y_diff != y_after_diff:
                if x_after_diff > 0:
                    theta_next = 0  # Прямо вниз
                elif x_after_diff < 0:
                    theta_next = np.pi  # Прямо вгору
                elif y_after_diff > 0:
                    theta_next = -np.pi / 2  # Поворот вліво
                elif y_after_diff < 0:
                    theta_next = np.pi / 2  # Поворот вправо

                if theta != theta_next:
                    steering_angle = np.arctan2(np.sin(theta_next - theta), np.cos(theta_next - theta))
                    if abs(steering_angle) > max_steering_angle:
                        steering_angle = np.sign(steering_angle) * max_steering_angle

                    radius = wheel_base / np.tan(steering_angle)
                    delta_theta = speed / radius

                    theta += delta_theta
                    if theta > np.pi:
                        theta -= 2 * np.pi
                    elif theta < -np.pi:
                        theta += 2 * np.pi

            for patch in plt.gca().patches:
                patch.remove()

            car_patches = create_car_patches(x, y, theta, steering_angle)
            for patch in car_patches:
                plt.gca().add_patch(patch)

            plt.draw()
            plt.pause(0.05)

    plt.show()
