def normalizeRanges(rangeList):
	'''Takes a list of [_in, _out] range Arrays and
	returns a normalized list of [_in, _out] range
	Arrays with no overlaps.'''
	if len(rangeList) <= 1:
		return rangeList
	stack = []
	sorted_rangeList = sorted(rangeList, key=lambda x: x[0])
	stack.append(sorted_rangeList.pop(0))
	while sorted_rangeList:
		stack_top = stack[-1]
		next_range = sorted_rangeList.pop(0)
		print 'stack top:', stack_top
		print 'next range:', next_range
		if stack_top[1] < next_range[0]:
			print 'next range appended'
			stack.append(next_range)
		elif stack_top[1] < next_range[1]:
			print 'stack top updated'
			stack_top[1] = next_range[1]
	return stack