from copy import deepcopy

# with points in each node
class KdTree:
    def __init__(self, points, depth=0):
        self.points = deepcopy(points) # points in the node
        self.left = None               # left subtree [lower or equal to the root]
        self.right = None              # right subtree [greater than the root]
        self.depth = depth             # even: x-axis, odd: y-axis
        self.axis = None               # axis to split on
        self.build(self.points, depth)

    def build(self, points, depth):
        if len(points) == 1:
            return None
        points.sort(key=lambda x: x[depth % 2])
        median = (len(points)-1) // 2
        self.axis = points[median][depth % 2]
        self.left = KdTree(points[:median+1], depth + 1)
        self.right = KdTree(points[median+1:], depth + 1)


# tests to check the correctness of the implementation
# todo - add more tests
#      - move tests to a separate file
test1 = [(1,2), (2,5), (3,1), (0,7), (4,6), (8,0), (5,3), (9,1), (6,7), (7,5)]
tree1 = KdTree(test1)

assert tree1.axis == 4
assert tree1.left.left.left.left.points[0] == test1[0]
assert tree1.left.left.left.right.points[0] == test1[1]
assert tree1.left.left.right.points[0] == test1[2]
assert tree1.left.right.left.points[0] == test1[3]
assert tree1.left.right.right.points[0] == test1[4]
assert tree1.right.left.left.left.points[0] == test1[5]
assert tree1.right.left.left.right.points[0] == test1[6]
assert tree1.right.left.right.points[0] == test1[7]
assert tree1.right.right.left.points[0] == test1[8]
assert tree1.right.right.right.points[0] == test1[9]

test2 = [(1,1)]
tree2 = KdTree(test2)

assert tree2.left == None
assert tree2.right == None
assert tree2.axis == None
assert tree2.depth == 0
assert tree2.points == test2

print("done")