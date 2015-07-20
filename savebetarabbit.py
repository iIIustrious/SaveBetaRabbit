def answer(food, grid):
    #paths will hold how much food we've used on this path
	paths = {}
	size = len(grid) -1
	current = (0,0)
	came_from = (0,0)
	currentA = 0
	currentB = 0
	fromA = 0
	fromB = 0
	goal = (size, size)
	stack = []
    #test if 1x1
	if size == 0:
		return 0
	#create storage for our used food	
	for (i,x) in enumerate(grid):
		print(i)
		for (j,y) in enumerate(grid[i]):
				paths[i,j] = 0

	#tests to see which branch is better			
	def heuristic (a,b,spent):
		if a+1 <= size:
			pathA = grid[a+1][b] + spent
		else: pathA = food+1

		if b+1 <= size:
			pathB = grid[a][b+1] + spent
		else: pathB = food+1
        #send the new nodes in order of preference
		if food >= pathA >= pathB :
		    return(a+1,b),(a,b+1) 
		elif food >= pathB >= pathA:
			return (a,b+1),(a+1,b)
		elif food >= pathA:
			return (a+1,b),(-1,-1)
		elif food >= pathB:
			return (a,b+1),(-1,-1)
		else:
			return (-1,-1),(-1,-1)

    #obtain first nodes, slightly different then subsequent steps to test
    #for initial failure 
	newNodes = heuristic(currentA, currentB, paths[fromA,fromB])
	if newNodes[0] == (-1,-1):
		return -1
	elif newNodes[1] == (-1,-1):
		paths[currentA,currentB] = paths[(fromA) ,( fromB )] + grid[currentA][currentB]
		stack.append( (newNodes[0], current) )
	else:
		paths[currentA,currentB] = paths[fromA,fromB] + grid[currentA][currentB]
		stack.append( (newNodes[1], current) )
		stack.append( (newNodes[0], current) )

	if stack == []:
		paths[size,size] = -1


    #main loop, will continue until it's determined we can't get to the exit, or the
    #path with the most food used is found
	while (current != goal) and stack != []:
	    #set all the variables to refer to this node
		node = stack.pop()
		current = node[0]
		came_from = node[1]
		currentA = current[0]
		currentB = current[1]
		fromA = came_from[0]
		fromB = came_from[1]
		newNodes = heuristic(currentA, currentB, paths[fromA,fromB])
		#if we're at the goal, make sure we haven't gone over our food limit
		if current == goal:
			paths[currentA,currentB] = paths[fromA,fromB] + grid[currentA][currentB]
			if paths[currentA,currentB] > food:
				current = came_from
		#before we traverse further, update the spent food, and see if we have any 
		#useable nodes to add to the stack. Otherwise next run will just go back to
		#older entries waiting.
		else:
			paths[currentA,currentB] = paths[fromA,fromB] + grid[currentA][currentB]
			if newNodes[1] != (-1,-1):
				stack.append( (newNodes[1], current) )
			if newNodes[0] != (-1,-1):
				stack.append( (newNodes[0], current) )
		if stack == []:
			paths[size,size] = -1
			
	if paths[goal] < 0:
		return -1
	else:
		return food - paths[goal]