import math

def point_distance(p1, p2) -> float:
    return math.sqrt(math.pow(p2[0] - p1[0],2) + math.pow(p2[1]-p1[1],2))


def calc_angle_to_axis_x(p1, p2) -> float:
    if p1.y == p2.y:
        return 0.0
    if p1.x == p2.x:
        return math.pi/2


def get_angle_from_center(center_point, p, radius):
    if p[1] == center_point[1]:
        if p[0] > center_point[0]:
            return 0
        return math.pi
    
    if p[0] == center_point[0]:
        if p[1] > center_point[1]:
            return math.pi/2
        return math.pi + math.pi/2
    print(center_point, p)
    angle = math.asin(abs(center_point[1]-p[1])/radius)    
    print(angle)
    if p[0] > center_point[0]:
        if p[1] > center_point[1]:
            return angle
        return 2*math.pi - angle
    
    if p[0] < center_point[0]:
        if p[1] > center_point[1]:
            return math.pi - angle
        return math.pi + angle




def get_center_start_end_angle(p1, p2, radius):
    if(p1[0] > p2[0]):
        p1,p2 = p2, p1 
      
    # calc the mid point of start point and end point
    mid_point = (p1[0]+p2[0]/2,(p1[1]+p2[1])/2)
    # calc distance between start point and endpoint. AB is the line determined by start point to end point
    square_distance_AB = (p2[0]-p1[0]) ** 2 + (p2[1]-p1[1]) ** 2  
    distance_AB = math.sqrt(math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2))
    # calc distance from midpoint to center point
    square_d = radius ** 2 - square_distance_AB /4 
    # calc offset from midpoint to center point
    center_point=None
    delta_x = None
    delta_y = None
    if p1[0] == p2[0]:
        delta_x = math.sqrt(square_d)
        delta_y = 0
    elif p1[1] == p2[1]:
        delta_x = 0
        delta_y = math.sqrt(square_d) 
    elif abs(p2[0]-p1[0]) == radius:
        center_point=(p1[0], p2[1])
    else:
        # Here alpha is the angle of AB and Axis X
        square_sinus_alpha = (p2[1]-p1[1])**2/square_distance_AB        
        square_cosinus_alpha = 1 - square_sinus_alpha
        print(square_sinus_alpha, square_cosinus_alpha)
        delta_x = math.sqrt(square_d*square_sinus_alpha)
        delta_y = math.sqrt(square_d*square_cosinus_alpha)
    
    if center_point is None:        
        center_point_x = mid_point[0]-delta_x
        print(delta_x, delta_y, mid_point)
        
        if p1[1] < p2[1]:
            center_point_y = mid_point[1] + delta_y
        else:
            center_point_y = mid_point[1] - delta_y
        center_point = (center_point_x, center_point_y)        

    start_angle = get_angle_from_center(center_point, p1, radius)
    end_angle = get_angle_from_center(center_point, p2, radius)
    return center_point, start_angle, end_angle

def get_polygon_points(num_edges, edge_length, center_point=(0.0, 0.0)):
    # Calculate the radius of the circumscribed circle
    radius = edge_length / (2 * math.sin(math.pi / num_edges))

    points = []
    for i in range(num_edges):
        angle = 2 * math.pi * i / num_edges
        x = radius * math.cos(angle) + center_point[0]
        y = radius * math.sin(angle) + center_point[1]
        x = round(x, 3)
        y = round(y,3)
        points.append((x, y))

    return points

# if __name__ == "__main__":
#     print(get_center_start_end_angle((0.559,0.341),(0.0,-1.611),1.367))
#     # Get points of a polygon with 6 edges, each of length 100
#     points = get_polygon_points(6, 100)
#     for point in points:
#         print(point)
