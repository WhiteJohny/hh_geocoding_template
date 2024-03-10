from __future__ import annotations

import time

from api import API
from geocoders.geocoder import Geocoder
from geocoders.memorized_tree_geocoder import MemorizedTreeGeocoder
from geocoders.simple_query_geocoder import SimpleQueryGeocoder
from geocoders.simple_tree_geocoder import SimpleTreeGeocoder


def format_time(start_ns: int, end_ns: int) -> str:
    diff = end_ns - start_ns

    diff_ms = diff / 10**6
    if diff_ms > 1000:
        seconds = round(diff_ms / 1000, 2)
        return f"{seconds} s"
    else:
        mills = round(diff_ms, 2)
        return f"{mills} ms"


def main():
    areas_data = API.get_areas()

    geocoder_list: list[Geocoder] = [
        SimpleQueryGeocoder(samples=10),
        SimpleTreeGeocoder(samples=10, data=areas_data),
        MemorizedTreeGeocoder(samples=10, data=areas_data),
        SimpleTreeGeocoder(samples=1000, data=areas_data),
        MemorizedTreeGeocoder(samples=1000, data=areas_data),
        SimpleTreeGeocoder(samples=10000, data=areas_data),
        # SimpleTreeGeocoder(data=areas_data),
        MemorizedTreeGeocoder(samples=10000, data=areas_data),
        MemorizedTreeGeocoder(data=areas_data),
    ]

    for geocoder in geocoder_list:
        class_name = geocoder.__class__.__name__
        samples_num = geocoder.__dict__["_samples"]

        start_time_ms = time.time_ns()
        geocoder.geocode()
        end_time_ms = time.time_ns()

        time_formatted = format_time(start_time_ms, end_time_ms)

        print(f"{class_name} [{samples_num}]: {time_formatted}")


if __name__ == "__main__":
    main()
