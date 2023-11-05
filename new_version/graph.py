from abc import ABC, abstractmethod


class IGraph(ABC):
    @abstractmethod
    def nodes(self):
        pass

    @abstractmethod
    def edges(self):
        pass

    @abstractmethod
    def neighbors(self, node):
        pass

    @abstractmethod
    def has_node(self, node):
        pass

    @abstractmethod
    def add_node(self, node, attrs=None):
        pass

    @abstractmethod
    def add_edge(self, edge, wt=1, label='', attrs=None):
        pass

    @abstractmethod
    def has_edge(self, edge):
        pass

    @abstractmethod
    def edge_weight(self, edge):
        pass

    @abstractmethod
    def del_node(self, node):
        pass


class Graph(IGraph):
    WEIGHT_ATTRIBUTE_NAME = "weight"
    DEFAULT_WEIGHT = 0
    LABEL_ATTRIBUTE_NAME = "label"
    DEFAULT_LABEL = ""

    def __init__(self):
        self.edge_properties = {}
        self.edge_attr = {}
        self.node_attr = {}
        self.node_neighbors = {}
    # ... rest of your methods ...
