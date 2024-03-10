from __future__ import annotations

from api import API, TreeNode
from geocoders.geocoder import Geocoder


# Перебор дерева
class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def __dfs(self, area_id, data, sp):
        for node in data:
            areas = node.areas

            if node.id == str(area_id):
                sp.append(node.name)
                return sp, node
            elif areas:
                if self.__dfs(area_id, areas, sp):
                    sp.append(node.name)
                    return sp, node

        return sp

    def _apply_geocoding(self, area_id: str) -> str:
        """
            TODO:
            - Сделать перебор дерева для каждого area_id
            - В ходе перебора возвращать массив элементов, состоящих из TreeNode необходимой ветки
            - Из массива TreeNode составить полный адрес
        """
        path = f'{area_id},"{", ".join(self.__dfs(area_id, data=self.__data, sp=[])[0])}"'

        return path
