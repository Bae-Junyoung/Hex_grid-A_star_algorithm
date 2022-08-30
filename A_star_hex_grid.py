import collections
from shapely.geometry import Point, Polygon
import make_hex_grid
import numpy as np
import pickle


road_union = Polygon([[2,0], [3,0], [3,2], [5,2], [5,3], [3,3], [3,5], [2,5], [2,3], [0,3], [0,2], [2,2], [2,0]])
road_union_buffer10 = road_union.buffer(10)

hex_grid = make_hex_grid.hex_grid

hex_grid_on_road = hex_grid[hex_grid.geometry.centroid.progress_apply(lambda x: x.within(road_union_buffer10[0]))]
hex_grid_on_road.reset_index(drop=True,inplace=True)

hex_grid_on_road['cube_q'] = hex_grid_on_road.cube.apply(lambda x: x.q)
hex_grid_on_road['cube_r'] = hex_grid_on_road.cube.apply(lambda x: x.r)
hex_grid_on_road['cube_s'] = hex_grid_on_road.cube.apply(lambda x: x.s)

# file_path = './hex_grid10_on_road.json'
# dfdf = hex_grid_on_road.to_json()
#
# with open(file_path,'w') as outfile:
#     json.dump(dfdf,outfile, indent=4)

hex_adjacent_index = collections.defaultdict(list)
hex_grid_on_road_buffer1 = hex_grid_on_road.buffer(1)

for i in range(hex_grid_on_road.shape[0]):
    idx = hex_grid_on_road.index[hex_grid_on_road_buffer1.intersects(hex_grid_on_road.geometry[i])].tolist()
    idx.remove(i)
    hex_adjacent_index[i] = idx

# # save data
# with open('./hex_adjacent_index.pickle', 'wb') as fw:
#     pickle.dump(hex_adjacent_index, fw)

# Time Complexity는 H에 따라 다르다.
# O(b^d), where d = depth, b = 각 노드의 하위 요소 수
# heapque를 이용하면 길을 출력할 때 reverse를 안해도 됨

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def aStar(start, end):
    # startNode와 endNode 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    # openList, closedList 초기화
    openList = []
    closedList = []

    # openList에 시작 노드 추가
    openList.append(startNode)

    # endNode를 찾을 때까지 실행
    while openList:

        # 현재 노드 지정
        currentNode = openList[0]
        currentIdx = 0

        # 이미 같은 노드가 openList에 있고, f 값이 더 크면
        # currentNode를 openList안에 있는 값으로 교체
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIdx = index

        # openList에서 제거하고 closedList에 추가
        openList.pop(currentIdx)
        closedList.append(currentNode)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                # maze 길을 표시하려면 주석 해제
                # x, y = current.position
                # maze[x][y] = 7
                path.append(current.position)
                current = current.parent

            return path[::-1]  # reverse

        children = []
        # 인접한 xy좌표 전부
        for newPosition in hex_adjacent_index[currentNode.position]:

            # 노드 위치 업데이트
            nodePosition = newPosition

            new_node = Node(currentNode, nodePosition)
            children.append(new_node)

        # 자식들 모두 loop
        for child in children:

            # 자식이 closedList에 있으면 continue
            if child in closedList:
                continue

            # f, g, h값 업데이트
            child.g = currentNode.g + 10*np.sqrt(3)
#             child.h = hex_distance(hex_grid_on_road.loc[child.position,'cube'], hex_grid_on_road.loc[endNode.position,'cube'])
            child.h = hex_grid_on_road.geometry[child.position].distance(hex_grid_on_road.geometry[endNode.position])

            child.f = child.g + child.h

            # 자식이 openList에 있으고, g값이 더 크면 continue
            if len([openNode for openNode in openList
                    if child == openNode and child.g >= openNode.g]) > 0:
                continue

            openList.append(child)


