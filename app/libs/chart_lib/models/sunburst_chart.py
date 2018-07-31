from .base_chart import BaseChart

class SunburstChart(BaseChart):
    """
    SunburstChart is the class of showing the sunburst chart.

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'sunburst2'
        self.__description__ = 'SunburstChart chart'

    def _available_types(self):
        self.available_types = ['line', 'column', 'bar', 'pie', 'table']


    def transformation(self, raw_data):
        tree = PieTree()
        df = raw_data['data']
        xAxis, yAxis = self._parse_header(df)

        for index, row in df.iterrows():
            if index == 0:
                continue
            arrow_list =[]
            for x in xAxis:
                arrow_list.append(Node(str(row[x])))
            tree.buildTree(arrow_list)

        mydic = {'name':'root','children':[]}
        
        self.__series__ = [{'data':tree.traverse(mydic, tree.current_node)}]
       
        self._set_common_properties(raw_data)





class Node:
    """
    Node class
    """
    def __init__(self, data):
        self.children = []
        self.data = data
        self.parent = None


class PieTree:
    """
    PieTree class
    """
    def __init__(self):
        self.dic_list = []
        self.root = Node("root")
        self.current_node = self.root
        self.output_tree = {}
        self.current_dic = {}
       

    def createNode(self, data):
        return Node(data)
    
    def find_node(self, node, root):
        if node.data == root.data:
            return root
        else:
            for child in root.children:
                if self.find_node(node, child):
                    return self.find_node(node, child)
         

    def buildTree(self, target_list):
        
        result = self.find_node(target_list[0], self.current_node)
        old_node = target_list[0]
       
        if result:
#                 print("YES !")
            del target_list[0]
            for target in target_list:
                result = self.find_node(target_list[0], self.current_node)
                if result:
                    self.current_node = result
                    continue
#                 if target_list:
                self.current_node = self.insert_node(target, self.current_node)
        else:
#                 print("NO!")
            old_node.parent = self.current_node
            self.current_node.children.append(old_node)
            last_child = len(self.current_node.children)
            self.current_node = self.current_node.children[last_child-1]
            del target_list[0]
        if len(target_list)> 0:  
            self.buildTree(target_list)  
        else:
            self.current_node = self.root
                    
                
    def insert_node(self, insert_node, current_node):
        insert_node.parent = self.current_node
        self.current_node.children.append(insert_node)
        current_len = len(self.current_node.children)
        return current_node.children[current_len-1]


    def traverse(self, current_dic, child):
        self.current_node = child
        self.current_dic = current_dic

        if self.current_node.children:
            current_dic['name'] =  self.current_node.data
            current_dic['children']= []

            for child in self.current_node.children:
                t_dic = {}
                if child.children:
                    t_dic['name'] = child.data
                    current_dic['children'].append(self.traverse(t_dic, child)) 
                else:
                    current_dic['children'].append({'name':'CTR','size':child.data}) 
    
        return current_dic
            



