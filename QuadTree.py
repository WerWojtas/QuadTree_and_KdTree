from utilities.Point import Point
from utilities.Rectangle import Rectangle

class QuadTree:
    def __init__(self, points, max_capacity=1, points_in_node=False):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == 2 for point in points):
            raise ValueError("The points have different dimensions than 2.")
        points = [Point(point) for point in points]
        if len(set(points)) != len(points):
            raise ValueError("Not all points are unique.")
        self._root = QuadTreeNode(points, Rectangle.from_points(points), max_capacity, points_in_node)
        self._max_capacity = max_capacity
        self._points_in_node = points_in_node

    def if_contains(self,point):
        if len(point) != 2:
            raise ValueError("The point has different dimension than 2.")
        if not isinstance(point, Point):
            point = Point(point)
        if self._root._rectangle.contains(point):
            return self._root._if_contains(point)
        return False

    def search_in_rectangle(self, rectangle, raw = False):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != 2:
            raise ValueError("The rectangle has different dimension than 2.")
        area = rectangle.intersection(self._root._rectangle)
        if area is None:
            return []
        result = list(self._root._search_in_rectangle(area, self._points_in_node))
        if raw:
            return [point.point for point in result]
        return result
        
        

class QuadTreeNode:
    def __init__(self, points, rectangle, max_capacity=1, points_in_node=False):
        if points_in_node:
            self.points = points.copy()    # points in the node
        elif len(points) <= max_capacity:
            self.points = points           # points in the leaf
        self._left_up = None               # left up subtree
        self._right_up = None              # right up subtree
        self._left_down = None             # left down subtree
        self._right_down = None            # right down subtree
        self._rectangle = rectangle        # rectangle that contains all points in the node
        self._build(points, max_capacity, points_in_node)

    def _build(self, points, max_capacity, points_in_node):
        if len(points) > max_capacity:
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = self._rectangle.to_quaters()
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            center = self._rectangle.center()
            for point in points:
                if point.x <= center.x:
                    if point.y <= center.y:
                        points_left_down.append(point)
                    else:
                        points_left_up.append(point)
                else:
                    if point.y <= center.y:
                        points_right_down.append(point)
                    else:
                        points_right_up.append(point)
            self._left_up = QuadTreeNode(points_left_up, rec_left_up, max_capacity, points_in_node)
            self._right_up = QuadTreeNode(points_right_up, rec_right_up, max_capacity, points_in_node)
            self._left_down = QuadTreeNode(points_left_down, rec_left_down, max_capacity, points_in_node)
            self._right_down = QuadTreeNode(points_right_down, rec_right_down, max_capacity, points_in_node)

    def _if_contains(self, point):
        if self._left_up is None:
            return point in self.points
        center = self._rectangle.center()
        ld = lu = rd = ru = False
        if point.x <= center.x:
            if point.y <= center.y:
                return self._left_down._if_contains(point)
            return self._left_up._if_contains(point)
        else:
            if point.y <= center.y:
                return self._right_down._if_contains(point)
            return self._right_up._if_contains(point)
    
    def _add_leaves(self, points_in_node=False):
        if points_in_node:
            return set(self.points)
        else:
            if self._left_down is None:
                return set(self.points)
            return self._left_up._add_leaves() \
                 | self._right_up._add_leaves() \
                 | self._left_down._add_leaves() \
                 | self._right_down._add_leaves()
        
    def _search_in_rectangle(self, rectangle, points_in_node=False):
        if self._left_up is None:
            return set([point for point in self.points if rectangle.contains(point)])
        if rectangle.contains(self._rectangle):
            return self._add_leaves(points_in_node)
        if rectangle.does_intersect(self._rectangle):
            return self._left_up._search_in_rectangle(rectangle, points_in_node) \
                 | self._right_up._search_in_rectangle(rectangle, points_in_node) \
                 | self._left_down._search_in_rectangle(rectangle, points_in_node) \
                 | self._right_down._search_in_rectangle(rectangle, points_in_node)
        return set()
        

# ------------------------------------------------------------------------------------------------------------------------
        
from utilities.Point import Point
from utilities.Rectangle import Rectangle
from visualizer.main import Visualizer
from copy import deepcopy



class QuadTree_visualizer:
    def __init__(self, points, max_capacity=1, points_in_node=False, visualize_gif=True, title="QuadTree", filename="QuadTree-construction"):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == 2 for point in points):
            raise ValueError("The points have different dimensions than 2.")
        points = [Point(point) for point in points]
        if len(set(points)) != len(points):
            raise ValueError("Not all points are unique.")
        self.vis = Visualizer()
        self.vis.add_title(title)
        self.vis.add_point(points)
        self.vis.add_polygon(Rectangle.from_points(points).vertices2D, color="blue", fill = False )
        self._root = QuadTreeNode_v(points, self.vis, Rectangle.from_points(points), max_capacity, points_in_node)
        self._max_capacity = max_capacity
        if visualize_gif:
            self.vis.save_gif(filename=filename)
        else:
            self.vis.save(filename=filename)
        self._points_in_node = points_in_node

    def if_contains(self,point, title="QuadTree", filename="QuadTree-contains"):
        if len(point) != 2:
            raise ValueError("The point has different dimension than 2.")
        if not isinstance(point, Point):
            point = Point(point)
        vis = deepcopy(self.vis)
        vis.add_title(title)
        if self._root._rectangle.contains(point):
            contains_result = self._root._if_contains(point, vis)
            vis.save_gif(filename=filename)
            return contains_result
        else:
            return False

    def search_in_rectangle(self, rectangle, raw = False, title="QuadTree", filename="QuadTree-search"):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != 2:
            raise ValueError("The rectangle has different dimension than 2.")
        area = rectangle.intersection(self._root._rectangle)
        vis = deepcopy(self.vis)
        vis.add_title(title)
        ll, lr, ur, ul = rectangle.vertices2D
        vis.add_line_segment([(ll,lr), (ll,ul), (ul,ur),(lr,ur)], color="red")
        if area is None:
            return []
        result = list(self._root._search_in_rectangle(area, vis, self._points_in_node))
        vis.save_gif(filename=filename)
        if raw:
            return [point.point for point in result]
        return result
        
        

class QuadTreeNode_v:
    def __init__(self, points, vis, rectangle, max_capacity=1, points_in_node=False):
        if points_in_node:
            self.points = points.copy()    # points in the node
        elif len(points) <= max_capacity:
            self.points = points           # points in the leaf
        self._left_up = None               # left up subtree
        self._right_up = None              # right up subtree
        self._left_down = None             # left down subtree
        self._right_down = None            # right down subtree
        self._rectangle = rectangle        # rectangle that contains all points in the node
        self._build(points, vis, max_capacity, points_in_node)

    def _build(self, points, vis, max_capacity, points_in_node):
        if len(points) > max_capacity:
            rec = vis.add_polygon(self._rectangle.vertices2D, color="orange",alpha=0.3)
            point = vis.add_point(points, color = "red")
            vis.remove_figure(point)
            vis.remove_figure(rec)
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = self._rectangle.to_quaters()
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            vis.add_line_segment([rec_right_down.lowerleft,rec_left_up.upperright], color="blue")
            vis.add_line_segment([(rec_left_down.lowerleft._point[0],rec_left_down.upperright[1]),rec_right_down.upperright], color="blue")
            center = self._rectangle.center()
            for point in points:
                if point.x <= center.x:
                    if point.y <= center.y:
                        points_left_down.append(point)
                    if point.y >= center.y:
                        points_left_up.append(point)
                if point.x >= center.x:
                    if point.y <= center.y:
                        points_right_down.append(point)
                    if point.y >= center.y:
                        points_right_up.append(point)
            self._left_up = QuadTreeNode_v(points_left_up, vis, rec_left_up, max_capacity, points_in_node)
            self._right_up = QuadTreeNode_v(points_right_up, vis, rec_right_up, max_capacity, points_in_node)
            self._left_down = QuadTreeNode_v(points_left_down, vis, rec_left_down, max_capacity, points_in_node)
            self._right_down = QuadTreeNode_v(points_right_down, vis, rec_right_down, max_capacity, points_in_node)
        else:
            vis.add_point(points, color = "orange")

    def _if_contains(self, point, vis):
        vis.remove_figure(vis.add_polygon(self._rectangle.vertices2D, color="orange",alpha=0.3))
        if self._left_up is None:
            if point in self.points:
                vis.add_point([point], color = "green")
                return True
            else:
                vis.add_point([point], color = "black")
                return False
        center = self._rectangle.center()
        if point.x <= center.x:
            if point.y <= center.y:
                return self._left_down._if_contains(point,vis)
            return self._left_up._if_contains(point,vis)
        else:
            if point.y <= center.y:
                return self._right_down._if_contains(point,vis)
            return self._right_up._if_contains(point,vis)
    
    
    def _add_leaves(self, points_in_node=False):
        if points_in_node:
            return set(self.points)
        else:
            if self._left_down is None:
                return set(self.points)
            return self._left_up._add_leaves() \
                 | self._right_up._add_leaves() \
                 | self._left_down._add_leaves() \
                 | self._right_down._add_leaves()
        
    def _search_in_rectangle(self, rectangle, vis, points_in_node=False):
        if self._left_up is None:
            vis.remove_figure(vis.add_polygon(self._rectangle.vertices2D, color="orange",alpha=0.3))
            my_set = set()
            for point in self.points:
                if rectangle.contains(point):
                    vis.add_point([point], color = "black")
                    my_set.add(point) 
            return my_set
        if rectangle.contains(self._rectangle):
            return self._add_leaves(points_in_node)
        if rectangle.does_intersect(self._rectangle):
            return self._left_up._search_in_rectangle(rectangle, vis, points_in_node) \
                 | self._right_up._search_in_rectangle(rectangle, vis, points_in_node) \
                 | self._left_down._search_in_rectangle(rectangle, vis, points_in_node) \
                 | self._right_down._search_in_rectangle(rectangle, vis, points_in_node)
        return set()
    
