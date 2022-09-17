import numpy as np
from numpy.linalg import norm

class Event:
    def __init__(self, frameNO, pos, channel_pos, area, tolerances=[2,10]):
        self.frame1 = frameNO
        self.frame2 = 0
        self.pos1 = np.array(pos) # Entry position
        self.pos2 = np.array([0, 0]) # Exit position
        self.channel_pos = np.array(channel_pos) # Channel start and end in x coordinates [x1, x2]
        self.last_pos = pos # Last position the particle was seen in
        self.last_frame = frameNO # Last frame the particle was seen in
        self.area = area
        self.channel_pop = 1 # Total detected particles in the channel
        self.frame_tol = tolerances[0] # How many frames have to pass with no particle detected (or additional) to terminate event
        self.space_tol = tolerances[1] # From left/right how far (in pixels) can the particle be away from the border to be considered entering/exiting
        self.isvalid = True # Is the event valid
        self.t_tresspass = 0 # Frame at which an additional particle entered
        self.islost = False # If the particle is detected in current frame
        self.isdone = False # If the event ended
        self.t_loss = 0
        self.v_avg = 0

    def update(self, frameNO, population, pos):
        self.channel_pop = population
        if population == 1:
            self.last_pos = pos
            self.last_frame = frameNO
            self.isvalid = True
            self.islost = False

        elif population == 0:
            if self.islost == False:
                self.t_loss = frameNO
                self.islost = True

            Δt1 = frameNO - self.t_loss
            if Δt1 >= self.frame_tol:
                self.terminate()
        
        elif population > 1:
            if self.isvalid == True:
                self.t_tresspass = frameNO
            
            self.isvalid = False
            Δt2 = frameNO - self.t_tresspass

            if Δt2 >= self.frame_tol:
                self.terminate()
    
    def terminate(self):
        self.pos2 = self.last_pos
        self.frame2 = self.last_frame
        if (self.channel_pos[1] - self.pos2[1] > self.space_tol) or (self.pos1[1] - self.channel_pos[0] > self.space_tol):
            self.isvalid = False
        self.isdone = True
        
    def compute(self, fps, scale=106/100):
        Δt = (self.frame2 - self.frame1)/fps  # Delta time in terms of seconds
        Δx = norm(self.pos2 - self.pos1)/scale
        self.v_avg = Δx/Δt  # Average velocity in unit/seconds
        t_avg = (self.frame2 + self.frame1)/2
        x_avg = (self.pos2 + self.pos1)/(2*scale)
        # print(t_avg, t_avg/fps, self.v_avg, self.area/(scale**2), (x_avg[0], x_avg[1]))
        # print(self.isvalid, self.isdone)
        # print(self.frame2, self.pos2)
        return t_avg, t_avg/fps, self.v_avg, self.area/(scale**2), (x_avg[0], x_avg[1])


# event = Event(100, [50,300], [299, 330], 50)
# pops = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0]
# posses = [[53, 304], [53, 307], [53, 309], [53, 311], [53, 315], [], [], [], [53, 302], [53, 306], [53, 313], [53, 318], [], [], []]
# for i in range(100,100+len(pops)):
#     if not event.isdone:
#         event.update(i, pops[i-100], posses[i-100])
#     print(event.isdone)

# event.compute(1, 106/100)
