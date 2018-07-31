from .base_chart import BaseChart


class Node:
    """
    Node is the class of basic unit of tree node.
    It has the capability to find the node and make
    the node return the dictionary type.

    """

    id = 0

    def __init__(self, name, parent):
        self.id = Node.id + 1
        Node.id += 1
        self.name = name
        self.parent = parent
        self.value = 0
        self.children = []
        self.real_value = 0

    @staticmethod
    def find_nodes(name, root):
        if name == root.name:
            return root
        elif root.children:
            for node in root.children:
                return Node.find_nodes(name, node)
        else:
            return None

    def to_dict(self):

        dic = {}
        dic['id'] = self.id
        dic['name'] = self.name
        if self.parent:
            dic['parent'] = self.parent.id
        if len(self.children) == 0:
            dic['value'] = self.value
            dic['real_value'] = self.real_value

        return dic


class TreemapChart(BaseChart):
    """
    TreemapChart is the class of having ability to build a tree and return the forest tree
    as dictionary type

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'treemap'
        self.__description__ = 'treemap chart'
        self.__levels__ = 1
        self.__highlight__ = {}
        self._forest = []


    def _available_types(self):
        self.available_types = ['treemap', 'table']

    def _construct_tree(self, data, xAxis, y_label, sum_values):
        root = None
        parent = None
        for index, row in data.iterrows():
            if index:
                for x in xAxis:
                    search_result = Node.find_nodes(row[x], root)
                    if not search_result:
                        node = Node(row[x], parent)
                        parent.children.append(node)
                        parent = node
                    else:
                        parent = search_result

                parent.value = round(abs(float(row[y_label])) / sum_values * 100000)
                parent.real_value = float(row[y_label])

            else:
                root = Node(row[y_label], None)
                parent = root

        return root

    def _tree_to_dict(self, node, results = []):
        if node:
            results.append(node.to_dict())
            if node.children:
                for child in node.children:
                    self._tree_to_dict(child, results)

        return results

    def _forest_to_dict(self):
        results = []
        for tree in self._forest:
            tree_dict = []
            results.extend(self._tree_to_dict(tree,tree_dict))

        return results

    def transformation(self, raw_data):
        
        print('treemap')
        df = raw_data['data']
        xAxis, yAxis = self._parse_header(df)
        for y_label in yAxis:
            sum_values = sum(abs(float(value)) for value in df[y_label][1:].values)
            print(sum_values)
            self._forest.append(self._construct_tree(df, xAxis, y_label, sum_values))

        self.__series__ = [{'data':self._forest_to_dict()}]
        self.__levels__ = len(xAxis) + 1
        self._set_common_properties(raw_data)







