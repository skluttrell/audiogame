# fills in the circle
def _fill_circle(circle, xCenter, yCenter, radius):
	# Function variables
	l = len(circle) # Store the current dictionary size so it is not lost as it grows
	# Remember that, of the circle edge coordinate pairs, the first is always the x and the next is always y

	# Fill in the circle by iterating through the coordinates of the outer edge and moving toward the center point line by line.
	for c in range(0, l):
		# Exclude the top and bottom most edges (since they are already solid).
		if yCenter + radius > circle[c][1] > yCenter - radius:
			# check the coordinate to see if it is left or right of center.
			if circle[c][0] < xCenter: # Left of
				# Fill a line from the left most edge to the center point (excluding the actual edge since it is already solid).
				for x in range(circle[c][0] + 1, xCenter):
					circle.append((x, circle[c][1]))
			else: # Right of
				# Fill a line from center point to the right most edge (excluding the edge since it is already solid).
				for x in range(xCenter, circle[c][0]):
					circle.append((x, circle[c][1]))

	return circle

# Draw the outer edge of the circle
def _circle_edge(circle, xCenter, yCenter, x, y):
	# Use the coordinates to fill the outer edge
	if x == 0:
		circle.append((xCenter, yCenter + y))
		circle.append((xCenter, yCenter - y))
		circle.append((xCenter + y, yCenter))
		circle.append((xCenter - y, yCenter))
	elif x == y:
		circle.append((xCenter + x, yCenter + y))
		circle.append((xCenter - x, yCenter + y))
		circle.append((xCenter + x, yCenter - y))
		circle.append((xCenter - x, yCenter - y))
	elif x < y:
		circle.append((xCenter + x, yCenter + y))
		circle.append((xCenter - x, yCenter + y))
		circle.append((xCenter + x, yCenter - y))
		circle.append((xCenter - x, yCenter - y))
		circle.append((xCenter + y, yCenter + x))
		circle.append((xCenter - y, yCenter + x))
		circle.append((xCenter + y, yCenter - x))
		circle.append((xCenter - y, yCenter - x))

	return circle

# Draws a circle given the attributes: a center point and a radius
def Circle(xCenter, yCenter, radius, fill=False):
	# Function variables
	x = 0
	y = radius
	p = (5 - radius * 4) / 4
	circle = []

	# Draw the outer edge of the circle
	# Start with the top and bottom, left and right
	circle = _circle_edge(circle, xCenter, yCenter, x, y)

	# Connect the sides with arches at each corner
	while x < y:
		x = x + 1 # Advance x

		# Find y and/or advance p
		if p < 0:
			p = p + (2 * x + 1)
		else:
			y = y - 1
			p = p + (2 * (x - y) + 1)

		# Send the new coordinates to the circle_edge function to draw the arches
		circle = _circle_edge(circle, xCenter, yCenter, x, y)

	# Sort the edge tiles into a proper circle
	q1 = []
	q2 = []
	q3 = []
	q4 = []

	# Separate into quadrants
	for c in circle:
		if c[0] >= 0 and c[1] >= 0:
			q1.append(c)
		if c[0] < 0 and c[1] >= 0:
			q2.append(c)
		if c[0] < 0 and c[1] < 0:
			q3.append(c)
		if c[0] >=0 and c[1] < 0:
			q4.append(c)

	# sort each quadrant
	q1 = sorted(q1, key = lambda x: x[0], reverse = True) # Sort x in descending order
	q1 = sorted(q1, key = lambda x: x[1]) # Sort y in ascending order
	q2 = sorted(q2, key = lambda x: x[1], reverse = True) # Sort y in descending order
	q2 = sorted(q2, key = lambda x: x[0], reverse = True) # Sort x in descending order
	q3 = sorted(q3, key = lambda x: x[0]) # Sort x in ascending order
	q3 = sorted(q3, key = lambda x: x[1], reverse = True) # Sort y in descending order
	q4 = sorted(q4, key = lambda x: x[0]) # Sort x in ascending order
	q4 = sorted(q4, key = lambda x: x[1]) # Sort y in ascending order
	circle = q1 + q2 + q3 + q4

	# If the fill boolian is set to true, fill the circle in
	if fill:
		circle = _fill_circle(circle, xCenter, yCenter, radius)

	return circle # Returns a tuple of x and y coordinates

# Draws a line given the attributes: two pairs of coordinates representing each end of the line
def Line(x1, y1, x2, y2):
	# Function variables
	line = []

	# Set the first x and y coordinates and insert them into the dictionary
	x = x1
	y = y1
	line.append((x, y))

	  # Calculate the difference between the two points
	distanceX = abs(x2 - x1)
	distanceY = abs(y2 - y1)

	# Find the step between each point
	if distanceX > distanceY:
		step = distanceX
	else:
		step = distanceY

	# Calculate the incroment between each point
	if distanceX > 0: incromentX = distanceX / step
	else: incromentX = 0
	if distanceY > 0: incromentY = distanceY / step
	else: incromentY = 0

	#  Populate the rest of the line coordinates
	for i in range(step):
		if x1 > x2: x = x - incromentX
		else: x = x + incromentX
		if y1 > y2: y = y - incromentY
		else: y = y + incromentY

		line.append((round(x), round(y)))

	return line

# Draws a rectangle given the attributes: two pairs of coordinates representing the top left and bottom right corner of the rectangle respectively
def Rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=False):
	# Function variables
	rectangle = []

	# Draw the bottom edge
	for x in range(topLeftX, bottomRightX + 1):
		rectangle.append((x, bottomRightY))

	# Fill in the sides and center (if fill is True)
	for y in range(bottomRightY + 1, topLeftY):
		# Draw the right edge
		rectangle.append((bottomRightX, y))

		# Fill in the body if fill is set to True
		if fill:
			# Iterate through the x coordinates
			for x in range(topLeftX + 1, bottomRightX):
				rectangle.append((x, y))

		# Draw the left edge
		rectangle.append((topLeftX, y))

	# Draw the top edge
	for x in range(topLeftX, bottomRightX + 1):
		rectangle.append((x, topLeftY))

	return rectangle

# Draws a triangle given the attributes: three pairs of coordinates representing the left, right, and top verticies
def Triangle(leftX, leftY, rightX, rightY, topX, topY, fill=False):
	# Function variables
	triangle = []
	leg1 = []
	leg2 = []
	leg3 = []

	# draw the first leg
	temp = Line(leftX, leftY, topX, topY)
	for i in range(0, len(temp) - 1): leg1.append(temp[i])
	for l in leg1: triangle.append(l)

	# draw the second leg
	temp = Line(topX, topY, rightX, rightY)
	for i in range(0, len(temp) - 1): leg2.append(temp[i])
	for l in leg2: triangle.append(l)

	# Draw the third leg
	temp = Line(rightX, rightY, leftX, leftY)
	for i in range(0, len(temp) - 1): leg3.append(temp[i])
	for l in leg3: triangle.append(l)

	# Fill the body if fill is set to True
	if fill:
		tempA = []
		tempB = []
		if leg1[0][1] == leg3[0][1]:
			tempA = leg1
			tempB = leg2
		elif leg1[0][1] > leg3[0][1]:
			tempA += leg1 + leg3
			tempB = leg2
		else:
			tempA = leg1
			tempB += leg2 + leg3

		while len(tempA) > 0:
			for t in tempB:
				if t[1] == tempA[0][1]:
					temp = Line(t[0], t[1], tempA[0][0], tempA[0][1])
					triangle += temp
					del t
			del tempA[0]

	return triangle