# QuadTree_and_KdTree

## Description
This project offers robust implementations of KD-Tree and QuadTree data structures for efficient spatial partitioning and searching. It includes well-documented code, interactive visualizations, thorough testing, and real-world examples, making it easy for developers and researchers to optimize spatial queries in multidimensional and two-dimensional spaces.

## KdTree and QuadTree
KdTree and QuadTree are data structures that allow you to efficiently search for points in multidimensional and two-dimensional spaces. 
Implementation of KdTree and QuadTree can be found in the `KdTree.py` and `QuadTree.py` files. Structures are implemented in the form of classes. The classes have the following methods:
- `if_contains(point)` - checks if the structure contains a given point
- `search_in_rectangle(rectangle)` - searches for points in a given rectangle

The data structure is fortified with robust data validation, ensuring the integrity and security. For unification of the data, geometric objects were implemented, but trees can also be used with any other objects like lists, tuples, etc.

<img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/rectangle_KdTree.png" width=49%> <img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/grid_QuadTree.png" width=50%>

## Documentation and presentation
Documentation  of the project contains a detailed description of the project, its implementation, examples of usage, and the results of the tests. The presentation contains a brief description of the project and the results of the tests.

Whole documentation and presentation of the project can be found in the `documentation` folder or by clicking the link below:

[Documentation pdf](https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/documentation.pdf)

[Documentation online](https://radoslawrolka.github.io/QuadTree_and_KdTree/documentation/index.html)

[Presentation pdf](https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/Presentation.pdf)

[Presentation canva](https://www.canva.com/design/DAF4sSijqic/-WQv5nAiUUL4ygehwcPBvw/edit?utm_content=DAF4sSijqic&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Comparison
The project includes a comparison of the performance of the QuadTree and KD-Tree data structures. The comparison was made on the basis of the time of initialization and searching for points in the structure. For better understanding of the results, the comparison was made for different numbers of points and different dimensions of the space. The results of the comparison are presented in the form of graphs and tables. The comparison was made for the following cases:
- uniform distribution
- normal distributione
- grid distribution
- clusters distribution
- outliers distribution
- cross distribution
- rectangle distribution

Also there is a comparison of the performance of the KD-Tree data structures for different numbers of points and different dimensions of the space. And a comparison of the performance of the QuadTree data structures for different numbers of maximum points in the node.

The results of the comparison can be found in the `Comparison.ipynb` file or by clicking the link below:

[Comparison.ipynb](https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/Comparison.ipynb)

<img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/cluster_graph_1.png">

## Visualization
The project includes interactive visualizations of the QuadTree and KD-Tree data structures. The visualizations are made in the form of gif animations. The visualizations show the process of creating a structure and searching for points in the structure. Visualizing the process of creating a structure is useful for understanding the structure of the structure. Visualizing the process of searching for points in the structure is useful for understanding the process of searching for points in the structure.

<img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/normal_KdTree.png" width=49%> <img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/cross_QuadTree.png" width=50%>

## Tests
The project includes a suite of unit tests covering all classes, written with python unittest. Also KdTree and QuadTree have their own integration tests. All tests are located in the `tests` folder and `TestManager.py`.

<img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/cluster.png" width=49%> <img src="https://github.com/radoslawrolka/QuadTree_and_KdTree/blob/master/documentation/resources/outlier.png" width=50%>
