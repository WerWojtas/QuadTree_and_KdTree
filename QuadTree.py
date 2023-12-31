from utilities.Point import Point
from utilities.Rectangle import Rectangle

class QuadTree:
    def __init__(self, points, depth=0):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        self._root = QuadTreeNode(points, Rectangle.from_points(points), depth)
        self._dimension = len(points[0])
        self._build(self._root)

    def _build(self,root):
        if root is None:
            return
        if len(root.points) < 2:
            return
        else:
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = root._rectangle.to_quaters()
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            for point in root.points:
                if rec_left_up.contains(point):
                    points_left_up.append(point)
                elif rec_right_up.contains(point):
                    points_right_up.append(point)
                elif rec_left_down.contains(point):
                    points_left_down.append(point)
                else:
                    points_right_down.append(point)

            root._left_up = QuadTreeNode(points_left_up, rec_left_up, root._depth + 1)
            root._right_up = QuadTreeNode(points_right_up, rec_right_up, root._depth + 1)
            root._left_down = QuadTreeNode(points_left_down, rec_left_down, root._depth + 1)
            root._right_down = QuadTreeNode(points_right_down, rec_right_down, root._depth + 1)

            self._build(root._left_up)
            self._build(root._right_up)
            self._build(root._left_down)
            self._build(root._right_down)

    def if_contains(self,point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        def search_point(root, point):
            if root is None:
                return False
            if len(root.points) == 1:
                return point == root.points[0]
            if root._rectangle.contains(point):
                return search_point(root._left_up, point) or search_point(root._right_up, point) or search_point(root._left_down, point) or search_point(root._right_down, point)
            else:
                return False
            
        return search_point(self._root, point)
        

    
    def search_in_rectangle(self, rectangle, raw = False):
        result = []

        def search(root, rectangle):
            if root is None:
                return
            if len(root.points) == 1:
                if rectangle.contains(root.points[0]):
                    result.append(root.points[0])
                else:
                    return
            intersection = root._rectangle.intersection(root._rectangle)
            if intersection != None:
                search(root._left_up, rectangle)
                search(root._right_up, rectangle)
                search(root._left_down, rectangle)
                search(root._right_down, rectangle)
            else:
                return
        search(self._root, rectangle)
        if not raw:
            return result
        else:
            for i in range(len(result)):
                result[i] = result[i]._point
            return result
        

class QuadTreeNode:
    def __init__(self, points, rectangle, depth=0):
        self.points = points                    # points in the node
        self._left_up = None                     # left up subtree
        self._right_up = None                    # right up subtree
        self._left_down = None                   # left down subtree
        self._right_down = None                  # right down subtree
        self._rectangle = rectangle           # rectangle that contains all points in the node
        self._depth = depth                   # depth of the node



# ------------------------------------------------------------------------------------------------------------------------
        
from utilities.Point import Point
from utilities.Rectangle import Rectangle
from visualizer.main import Visualizer



class QuadTree_visualizer:
    def __init__(self, points, depth=0):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        self.vis = Visualizer()
        self.vis.add_point(points)
        self._root = QuadTreeNode(points, Rectangle.from_points(points), depth)
        self.vis.add_polygon(self._root._rectangle.vertices2D)
        self._dimension = len(points[0])
        self._build(self._root)

    def _build(self,root):
        if root is None:
            return
        if len(root.points) < 2:
            return
        else:
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = root._rectangle.to_quaters()
            self.vis.add_polygon(rec_left_down.vertices2D)
            self.vis.add_polygon(rec_right_down.vertices2D)
            self.vis.add_polygon(rec_right_up.vertices2D)
            self.vis.add_polygon(rec_left_up.vertices2D)
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            for point in root.points:
                if rec_left_up.contains(point):
                    points_left_up.append(point)
                elif rec_right_up.contains(point):
                    points_right_up.append(point)
                elif rec_left_down.contains(point):
                    points_left_down.append(point)
                else:
                    points_right_down.append(point)

            root._left_up = QuadTreeNode(points_left_up, rec_left_up, root._depth + 1)
            root._right_up = QuadTreeNode(points_right_up, rec_right_up, root._depth + 1)
            root._left_down = QuadTreeNode(points_left_down, rec_left_down, root._depth + 1)
            root._right_down = QuadTreeNode(points_right_down, rec_right_down, root._depth + 1)

            self._build(root._left_up)
            self._build(root._right_up)
            self._build(root._left_down)
            self._build(root._right_down)

    def if_contains(self,point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        def search_point(root, point):
            if root is None:
                return False
            if len(root.points) == 1:
                return point == root.points[0]
            if root._rectangle.contains(point):
                return search_point(root._left_up, point) or search_point(root._right_up, point) or search_point(root._left_down, point) or search_point(root._right_down, point)
            else:
                return False
            
        return search_point(self._root, point)
        

    
    def search_in_rectangle(self, rectangle, raw = False):
        result = []

        def search(root, rectangle):
            if root is None:
                return
            if len(root.points) == 1:
                if rectangle.contains(root.points[0]):
                    result.append(root.points[0])
                else:
                    return
            intersection = root._rectangle.intersection(root._rectangle)
            if intersection != None:
                search(root._left_up, rectangle)
                search(root._right_up, rectangle)
                search(root._left_down, rectangle)
                search(root._right_down, rectangle)
            else:
                return
        search(self._root, rectangle)
        if not raw:
            return result
        else:
            for i in range(len(result)):
                result[i] = result[i]._point
            return result
    