from __future__ import annotations

from api import TreeNode, API
from geocoders.geocoder import Geocoder


class StackNode:
    def __init__(self, areas: list[TreeNode], next: StackNode | None = None):
        self.areas = areas
        self.next = next


class CustomStack:
    def __init__(self):
        self.__head = None
        self.__length = 0

    def peek(self):
        if self.__head is None:
            return None
        else:
            return self.__head.areas

    def append(self, areas: list[TreeNode]):
        if self.__head is None:
            self.__head = StackNode(areas)
        else:
            new_elem = StackNode(areas=areas, next=self.__head)
            self.__head = new_elem
        self.__length += 1

    def pop(self):
        if self.__head is None:
            return None
        else:
            areas = self.__head.areas
            next = self.__head.next
            self.__head.next = None
            self.__head = next
            self.__length -= 1
            return areas

    def __len__(self):
        return self.__length

    def __repr__(self):
        return self.__head.__repr__()


# Инверсия дерева
class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

        self.__dictionary = self.__dfs()
    """
        TODO:
        Сделать функцию перебора дерева:
        - Для каждого узла сохранять в словарь адресов
    """
    def __dfs(self) -> dict:
        paths = {}
        stack = CustomStack()

        stack.append(self.__data)

        while len(stack) > 0:
            current_areas = stack.pop()

            if current_areas:
                for area in current_areas:
                    stack.append(area.areas)

                    parent_path = paths.get(area.parent_id) or ''
                    paths[area.id] = parent_path + ', ' + area.name

        return paths

    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Возвращать данные из словаря с адресами
        """
        path = f'{area_id},"{self.__dictionary.get(str(area_id))[2:]}"'

        return path
