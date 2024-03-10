from geocoders.geocoder import Geocoder
from api import API, TreeNode


# Алгоритм "в лоб"
class SimpleQueryGeocoder(Geocoder):
    def _apply_geocoding(self, area_id: str) -> str:
        node = API.get_area(area_id)
        path = node.name + '"'

        while node.parent_id is not None:
            node = API.get_area(node.parent_id)
            path = node.name + ', ' + path

        path = str(area_id) + ',"' + path

        return path
