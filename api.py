from __future__ import annotations

import dataclasses

from requests import get


@dataclasses.dataclass
class TreeNode:
    id: str
    name: str
    parent_id: str | None
    areas: list[TreeNode]


class API:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_areas() -> list[TreeNode]:
        def deserialize_tree(raw_tree: dict) -> dict:
            areas = list(
                map(
                    lambda inner_tree: TreeNode(**deserialize_tree(inner_tree)),
                    raw_tree["areas"]
                )
            )

            return dict({
                **raw_tree,
                "areas": areas,
            })

        return list(
            map(
                lambda raw_tree: TreeNode(**deserialize_tree(raw_tree)),
                get(f"{API.BASE_URL}/areas").json()
            )
        )

    @staticmethod
    def get_area(area_id) -> TreeNode:
        return TreeNode(**get(f"{API.BASE_URL}/areas/{area_id}").json())
