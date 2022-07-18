import math
from unittest import result
import numpy as np

""" Cálculo de Area y Caras"""
def total_area(model2d):
	area, shown, hidden = 0,0,0
	for face in model2d.F:
		vertices =np.array([model2d.vP[vertex-1] for vertex in face])
		if np.max(vertices[:,[0,1]])>1.0 or np.min(vertices[:,[0,1]])<-1.0: return 0,0
		# vertices = []
		# for vertex  in face:
		# 	vertices.append(model2d.vP[vertex-1])

		result= shoeLaceFormula(vertices, model2d)
		area += result[0]
		if result[1]: shown += 1
		else: hidden += 1
	ratio = shown/len(model2d.F)
	return area,ratio

"""Cálculo de area de polinomio"""	
def shoeLaceFormula(vertices, model2d):
	area=0
	faces=False
	for i in range(0,len(vertices)):
		"""Calculo del area del polinomio"""
		area += vertices[i-1][0]*vertices[i][1] - vertices[i][0]*vertices[i-1][1]
	if(area>0): faces = True

	return abs(area)/2, faces

"""Cálculo de cruces"""
def count_crossed(model2d):
	count = 0
	vertices = 0
	parallels = 0
	near = 0
	for i in range(len(model2d.L)):
		for j in range(i+1,len(model2d.L)):
			# Get the locations
			crosses = False
			L1=model2d.L[i]
			L2=model2d.L[j]
			[x1,y1],[x2,y2] = model2d.vP[L1[0]][0:2],model2d.vP[L1[1]][0:2]
			[x3,y3],[x4,y4] = model2d.vP[L2[0]][0:2],model2d.vP[L2[1]][0:2]
			den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1) # equals 0 if the lines are parallel

			ua = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
			ub = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
			# If the fraction is between 0 and 1 for both lines then they cross each other
			if ua>0.01 and ua<0.99 and ub>0.01 and ub<0.99: 
				crosses = True
				count += 1
				

			# if ( math.isclose(abs(den), 0, abs_tol=0.01) ): # abs(den) <= 0.01):	#SI PARALELAS OBTENER DISTANCIA ENTRE LINEAs
			# 	distance=pDistance(x1,y1,x3,y3,x4,y4)
			# 	print(b.WARN, "Distance from parallel lines:" ,distance, b.END)
				
			
			# # Otherwise ua and ub are the fraction of the
			# # line where they cross

			# if ( angle(x1,y1,x2,y2,x3,y3,x4,y4) <=10 ):
			# 	distance=min(pDistance(x1,y1,x3,y3,x4,y4),
			# 				 pDistance(x2,y2,x3,y3,x4,y4),
			# 				 pDistance(x3,y3,x1,y1,x2,y2),
			# 				 pDistance(x4,y4,x1,y1,x2,y2))
				
			if( not crosses and not any(item in L1 for item in L2) ): #and (math.isclose(abs(den), 0, abs_tol=0.1))
				# distance=13
				# if(angle(x1,y1,x2,y2,x3,y3,x4,y4) <=10 ):
				distance=min(pDistance(x1,y1,x3,y3,x4,y4),
								pDistance(x2,y2,x3,y3,x4,y4),
								pDistance(x3,y3,x1,y1,x2,y2),
								pDistance(x4,y4,x1,y1,x2,y2))
				# print(distance)
				near += rep_force(distance)


	return 2*count/len(model2d.L), near

""" Vertices cercanos """
def count_node_collisions(model2d):
	vP = model2d.vP
	count = 0
	for i in range(len(vP)):
		for j in range(i+1,len(vP)):
			# Get the nodes location
			(x1,y1) = vP[i][0], vP[i][1]
			(x2,y2) = vP[j][0], vP[j][1]
			# Get the distance between them
			dist = math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
			count += rep_force(dist)
	return count


""" Funcion de repulsion """
def rep_force(d, t=0.1):
	r= 1/ (1 + np.exp( (1/t)*(d/t-1/2) ))
	return r

""" Distancia del punto a una recta """
def pDistance(x,y,x1,y1,x2,y2):
	A=x-x1
	B=y-y1
	C=x2-x1
	D=y2-y1

	dot = A*C+B*D
	len_sq=C*C+D*D
	param=-1
	if len_sq!=0:
		param = dot/len_sq

	if param < 0:
		xx = x1
		yy=y1
	elif param > 1:
		xx=x2
		yy=y2
	else:
		xx = x1 + param*C
		yy = y1 + param*D
	dx = x - xx
	dy = y -yy

	return math.sqrt(dx*dx + dy*dy)

""" Angulo entre dos aristas """
def angle(x1,y1,x2,y2,x3,y3,x4,y4):
	M1 = (y2-y1)/(x2-x1)
	M2 = (y4-y3)/(x4-x3)
	angle = abs((M2 - M1) / (1 + M1 * M2))
    # Calculate tan inverse of the angle
	ret = math.atan(angle)
    # Convert the angle from radian to degree
	val = (ret * 180) / np.pi
	return abs(val)










# A Python3 program to find if 2 given line segments intersect or not

class Point:
 def __init__(self, x, y):
  self.x = x
  self.y = y

# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
 if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
  (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
  return True
 return False

def orientation(p, q, r):
 # to find the orientation of an ordered triplet (p,q,r)
 # function returns the following values:
 # 0 : Collinear points
 # 1 : Clockwise points
 # 2 : Counterclockwise

 # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
 # for details of below formula.

 val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
 if (val > 0):

  # Clockwise orientation
  return 1
 elif (val < 0):

  # Counterclockwise orientation
  return 2
 else:

  # Collinear orientation
  return 0

# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1,q1,p2,q2):

 # Find the 4 orientations required for
 # the general and special cases
 o1 = orientation(p1, q1, p2)
 o2 = orientation(p1, q1, q2)
 o3 = orientation(p2, q2, p1)
 o4 = orientation(p2, q2, q1)

 # General case
 if ((o1 != o2) and (o3 != o4)):
  return True

 # Special Cases

 # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
 if ((o1 == 0) and onSegment(p1, p2, q1)):
  return True

 # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
 if ((o2 == 0) and onSegment(p1, q2, q1)):
  return True

 # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
 if ((o3 == 0) and onSegment(p2, p1, q2)):
  return True

 # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
 if ((o4 == 0) and onSegment(p2, q1, q2)):
  return True

 # If none of the cases
 return False



