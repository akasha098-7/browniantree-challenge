

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time

# Config
size = 501                 
center = size // 2
n_particles = 3500         
start_radius = 5           
kill_radius_buffer = 10    
max_steps_per_walk = 50000 

.
moves = [(1,0),(-1,0),(0,1),(0,-1)]

grid = np.zeros((size, size), dtype=np.uint8)
grid[center, center] = 1   
current_max_radius = 0

def is_adjacent_to_cluster(x, y):
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size and grid[ny, nx]:
            return True
    return False

def random_point_on_circle(radius):
    angle = random.random() * 2 * math.pi
    x = int(center + radius * math.cos(angle))
    y = int(center + radius * math.sin(angle))
    # clamp
    x = max(1, min(size-2, x))
    y = max(1, min(size-2, y))
    return x, y

start_time = time.time()
attached = 1
print("Starting DLA: grid", size, "x", size, "particles:", n_particles)
for i in range(n_particles):
    
    release_radius = max(start_radius, current_max_radius + 5)
    x, y = random_point_on_circle(release_radius)

    steps = 0
    while True:
      
        dx, dy = random.choice(moves)
        x += dx
        y += dy
        steps += 1

        
        if not (1 <= x < size-1 and 1 <= y < size-1):
            x, y = random_point_on_circle(release_radius)
            steps = 0

        
        if is_adjacent_to_cluster(x, y):
            grid[y, x] = 1
            attached += 1
           
            rx = x - center
            ry = y - center
            dist = math.sqrt(rx*rx + ry*ry)
            if dist > current_max_radius:
                current_max_radius = dist
            break

       
        if steps > max_steps_per_walk:
            x, y = random_point_on_circle(release_radius)
            steps = 0

   
    if (i+1) % 250 == 0 or i == n_particles-1:
        print(f"Particles attached: {i+1}/{n_particles}  radius approx: {int(current_max_radius)}")

elapsed = time.time() - start_time
print(f"Done — attached {attached} particles, time {elapsed:.1f}s")


plt.figure(figsize=(6,6))
plt.imshow(grid, origin='lower', cmap='inferno')  
plt.axis('off')
plt.tight_layout()
plt.savefig('brownian_tree.png', dpi=150, bbox_inches='tight', pad_inches=0)
plt.close()
print("Saved image: brownian_tree.png")