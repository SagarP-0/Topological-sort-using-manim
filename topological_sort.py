from manim import *
import networkx as nx
from collections import defaultdict, deque

config.frame_width = 16
config.frame_height = 9

class TopologicalSortVisualization(Scene):
    def construct(self):
        scale_factor = 1.5
        
        nodes = {
            'shirt': ('Shirt', UP * 2.5 * scale_factor + LEFT * 3 * scale_factor),
            'hoodie': ('Hoodie', UP * 2.5 * scale_factor),
            'inners': ('Inners', LEFT * 3 * scale_factor),
            'pants': ('Pants', ORIGIN),
            'belt': ('Belt', RIGHT * 3 * scale_factor),
            'socks': ('Socks', DOWN * 2.5 * scale_factor + LEFT * 3 * scale_factor),
            'shoes': ('Shoes', DOWN * 2.5 * scale_factor),
            'school': ('School', RIGHT * 5 * scale_factor)
        }
        
        edges = [
            ('shirt', 'hoodie'),
            ('hoodie', 'school'),
            ('inners', 'pants'),
            ('pants', 'belt'),
            ('belt', 'school'),
            ('socks', 'shoes'),
            ('shoes', 'school')
        ]

        vertex_radius = 0.5
        vertices = {}
        for node, (label, pos) in nodes.items():
            circle = Circle(radius=vertex_radius, color=GREEN)
            text = Text(label, font_size=32)
            text.scale(0.6)
            vertex = VGroup(circle, text)
            vertex.move_to(pos)
            vertices[node] = vertex

        edges_objects = []
        for start, end in edges:
            start_pos = vertices[start].get_center()
            end_pos = vertices[end].get_center()
            direction = (end_pos - start_pos) / np.linalg.norm(end_pos - start_pos)
            arrow = Arrow(
                start_pos + direction * vertex_radius,
                end_pos - direction * vertex_radius,
                buff=0,
                color=GREEN,
                max_tip_length_to_length_ratio=0.15,
                stroke_width=3
            )
            edges_objects.append(arrow)

        edges_group = VGroup(*edges_objects)
        vertices_group = VGroup(*vertices.values())
        graph_vis = VGroup(edges_group, vertices_group)

        # initial dag
        self.play(Create(edges_group), run_time=2)
        self.play(Create(vertices_group), run_time=2)
        self.wait(1)

        # definition for topological sort
        def all_topological_sorts(graph, nodes_set):
            in_degree = {node: 0 for node in nodes_set}
            for node in graph:
                for neighbor in graph[node]:
                    in_degree[neighbor] += 1
            
            def backtrack(path, in_degree):
                if len(path) == len(nodes_set):
                    return [path[:]]
                
                result = []
                for node in nodes_set:
                    if in_degree[node] == 0 and node not in path:
                        for neighbor in graph.get(node, []):
                            in_degree[neighbor] -= 1
                        path.append(node)
                        result.extend(backtrack(path, in_degree))
                        path.pop()
                        for neighbor in graph.get(node, []):
                            in_degree[neighbor] += 1
                return result

            return backtrack([], in_degree)

        # get all nodes
        graph_dict = defaultdict(list)
        all_nodes = set()
        
        for u, v in edges:
            graph_dict[u].append(v)
            all_nodes.add(u)
            all_nodes.add(v)

        # topologiical sorot result
        all_topological_sorts_result = all_topological_sorts(graph_dict, all_nodes)
        #print(len(all_topological_sorts_result))
        # solutions
        spacing_y = 1.0 * scale_factor
        spacing_x = 1.0 * scale_factor
        start_y = 0
        node_scale = 1.1
        
        self.play(
            graph_vis.animate.scale(0.9).shift(UP * 8), #shift DAG
            run_time=2
        )
        self.wait(1)

        solutions_group = VGroup()
        for i, solution in enumerate(all_topological_sorts_result[:5]): # varying outputs. 
            solution_group = VGroup()
            current_y = start_y - (i * spacing_y) + 3
            solution_nodes = []
            
            for j, node in enumerate(solution):
                node_copy = vertices[node].copy().scale(node_scale)
                target_x = (j - len(solution)/2) * spacing_x
                node_copy.move_to([target_x, current_y, 0])
                solution_nodes.append(node_copy)
                solution_group.add(node_copy)
            
            for j in range(1, len(solution_nodes)):
                prev_node = solution_nodes[j-1]
                curr_node = solution_nodes[j]
                
                start_pos = prev_node.get_center()
                end_pos = curr_node.get_center()
                
                direction = (end_pos - start_pos) / np.linalg.norm(end_pos - start_pos)
                buffer = vertex_radius * node_scale
                
                arrow = Arrow(
                    start=start_pos + direction * buffer,
                    end=end_pos - direction * buffer,
                    buff=0,
                    color=GREEN,
                    max_tip_length_to_length_ratio=0.15,
                    stroke_width=3
                )
                solution_group.add(arrow)
            
            solutions_group.add(solution_group)
            self.play(Create(solution_group), run_time=1)
            self.wait(1)

        self.wait(4)
        print("all possible solutions for the graph would be :",len(all_topological_sorts_result))