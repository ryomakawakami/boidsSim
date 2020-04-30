# boidsSim

### Info

Based on boids: [https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/modeling-natural-systems/boids.html](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/modeling-natural-systems/boids.html)

### Current Implementation

Boids calculate cohesion by finding the CM of all boids in visible range excluding itself.

Boids calculate separation only with the boids in their bubble.

Boids calculate alignment by finding the average velocity of all boids  in visible range excluding itself.

There are some arbitrary decisions I've made to make this more realistic (a lot of random factors multplied in).

### Parameters
[]()  | []()
------|------
**vision** | cohesion and alignment radius (vision)
**avoidVision** | separation radius
**home** | lazy way to implement central attraction (like a nest)
**attract** | cohesion factor
**align** | alignment factor
**avoid** | separation factor
**maxVel** | maximum boid speed (in pixels * 30 Hz)
**maxAcc** | maximum boid acceleration (in pixels * 30 Hz / s)

TODO:

Add min speed?

Add blind spot

Flock color should be randomly chosen from flock, weighted pdf based on how close to average it is

Feed the boids
