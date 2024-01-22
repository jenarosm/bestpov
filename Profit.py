import math
import numpy as np
from Settings import*

shoeLaceFormula = lambda vertices: sum([vertices[i-1][0]*vertices[i][1] - vertices[i][0]*vertices[i-1][1] for i in range(len(vertices))])/2

""" RATIOS AND REPULSION """
def face_balance_ratio(front, back):
	if(front and back):
		return round((front*back)*(2*front)/(front+back),2)

rep_force = lambda d, t: 1/ (1 + np.exp( (1/t)*(d/t-1/2) ))

""" CHECK IF LINES ARE ADJACENT """
isAdjacent = lambda l1,l2: any(v in l1 for v in l2)

""" SEGMENTS ANGLE CALCULATION """
v2Module = lambda v: math.sqrt(v[0]**2+v[1]**2)
v2Angle = lambda v1,v2: np.arccos(np.dot(v1,v2)/(v2Module(v1)*v2Module(v2))) * 180/np.pi

""" SEGMENT DISTANCE CALCULATION"""
def pDistance(x,y,x1,y1,x2,y2):
	A=x-x1
	B=y-y1
	C=x2-x1
	D=y2-y1

	dot = A*C+B*D
	len_sq=C*C+D*D
	param=-1
	if len_sq!=0: param = dot/len_sq

	if param < 0:
		xx = x1
		yy = y1
	elif param > 1:
		xx=x2
		yy=y2
	else:
		xx = x1 + param*C 
		yy = y1 + param*D
	dx = x - xx
	dy = y -yy

	return math.sqrt(dx*dx + dy*dy)
segment_distance = lambda p1,p2,p3,p4: min(pDistance(*p1,*p3,*p4), pDistance(*p2,*p3,*p4), pDistance(*p3,*p1,*p2), pDistance(*p4,*p1,*p2))

""" AREA CALCULATION """
def total_area(model2d):
	total_area, front, back = 0,0,0
	#Check object is inside canvas
	if any( (not isBetween(x,[-1,1]) or not isBetween(y,[-1,1])) for x, y in model2d.vertex[:,[0,1]]): return 0,0,0,0
	#Detect faces area and orientation
	for face in model2d.faces:
		vertices =np.array([model2d.vertex[vertex-1] for vertex in face])
		face_area = shoeLaceFormula(vertices)
		if (face_area>=0): front += 1
		else: back += 1
		total_area += abs(face_area)

	return round(total_area,2), face_balance_ratio(front,back), front, back

""" TOTAL VERTEX REPULSION FORCE """
def vertex_repulsion(model2d):
	total_force = 0
	for i in range(len(model2d.vertex)):
		for j in range(i+1,len(model2d.vertex)):
			# Get the nodes location
			(x1,y1) = model2d.vertex[i][0], model2d.vertex[i][1]
			(x2,y2) = model2d.vertex[j][0], model2d.vertex[j][1]
			# Get the distance between them
			dist = math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
			total_force += rep_force(dist,VERTEX_THRESHOLD)
	return total_force/len(model2d.lines)

""" EDGE PENALTIES CALCULATION """
def edge_penalties(model2d):
	tight_angles,parallel_repulsion,crossing_edges = 0,0,0
	for i in range(len(model2d.lines)):
		l1 = model2d.lines[i]
		p1, p2 = model2d.vertex[l1[0]-1][0:2],model2d.vertex[l1[1]-1][0:2]
		for j in range(i+1,len(model2d.lines)):
			l2=model2d.lines[j]
			p3, p4 = model2d.vertex[l2[0]-1][0:2],model2d.vertex[l2[1]-1][0:2]
			
			angle = v2Angle(np.array(p2-p1),np.array(p4-p3))
			if(isAdjacent(l1,l2)):
				#If adjacent edges with a tight angle
				if(angle<10): tight_angles+=1
			else:
				den=(p4[1]-p3[1])*(p2[0]-p1[0])-(p4[0]-p3[0])*(p2[1]-p1[1])
				if(isBetween(den,[-0.05,0.05])):
				# if( angle < 1):
					#If is parallel
					parallel_repulsion += rep_force(segment_distance(p1,p2,p3,p4),EDGES_THRESHOLD)
				else:
					ua = ((p4[0]-p3[0])*(p1[1]-p3[1])-(p4[1]-p3[1])*(p1[0]-p3[0]))/den
					ub = ((p2[0]-p1[0])*(p1[1]-p3[1])-(p2[1]-p1[1])*(p1[0]-p3[0]))/den
					#If is cross
					if isBetween(ua,[-0.01,1.01]) and isBetween(ub,[-0.01,1.01]):
						crossing_edges += 1

	return tight_angles/len(model2d.lines), parallel_repulsion/len(model2d.lines), crossing_edges/len(model2d.lines)