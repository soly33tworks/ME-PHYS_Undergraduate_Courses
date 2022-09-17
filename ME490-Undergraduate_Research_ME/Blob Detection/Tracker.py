import math
import numpy as np

def shift(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

class EuclideanDistTracker:
    def __init__(self, distance_tol=110, memory_length=5):
        self.center_points = {} # Dictionary that stores the center positions and areas of the particles
        self.id_count = 0 # Keep the count of the IDs, increase when new particle detected
        self.frameNO = 0
        self.distance_tol = distance_tol
        self.memory_length = memory_length

    def update(self, particles):
        objects_bbs_ids = np.empty((0,4), int) # Particle boxes and ids

        for particle in particles:
            x, y, area = particle # Get center point of new particle

            # Find out if that particle was detected already
            same_object_detected = False
            for id, memory in self.center_points.items():
                for pt in memory:
                    dist = math.hypot(x - pt[0], y - pt[1])

                    if (dist < self.distance_tol) and (id not in objects_bbs_ids[:,3]):
                        self.center_points[id] = shift(self.center_points[id], -1, [x,y, area])
                        objects_bbs_ids = np.append(objects_bbs_ids,[[x, y, area, id]], axis=0)
                        same_object_detected = True
                        break

                if same_object_detected is True: # if the particle is detected in this ID
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                blank = np.zeros((self.memory_length, 3))
                blank[-1] = [x,y, area]
                self.center_points[self.id_count] = blank
                objects_bbs_ids = np.append(objects_bbs_ids,[[x, y, area, self.id_count]], axis=0)
                self.id_count += 1
        
        for id, memory in self.center_points.items():
            if id not in objects_bbs_ids[:,3]: # if the particle is not detected in this ID
                self.center_points[id] = shift(self.center_points[id], -1, [0,0,0])

        self.frameNO += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        # Update dictionary with IDs not used removed
        new_center_points = {}
        average_areas = {}
        for id, memory in self.center_points.items():
            if np.all(memory==0): # check if no memory left about the particle with this id
                pass
            else:
                new_center_points[id] = memory
                average_area = np.true_divide(memory[:,2].sum(),(memory[:,2]!=0).sum())
                average_areas[id] = average_area

        self.center_points = new_center_points.copy()
        #print(self.center_points)
        return objects_bbs_ids, average_areas
