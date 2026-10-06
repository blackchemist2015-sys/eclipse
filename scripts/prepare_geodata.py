"""Download Natural Earth (public domain) layers and cut them to the eclipse region.

Usage: python scripts/prepare_geodata.py [cache_dir]
Writes compact GeoJSON files into data/.
"""
import os
import sys
import urllib.request

import geopandas as gpd
from shapely.geometry import box

BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
LAYERS = ["ne_10m_admin_0_countries", "ne_10m_admin_1_states_provinces",
          "ne_10m_lakes", "ne_50m_admin_0_countries"]
REGION = box(-35, -25, 80, 60)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")


def fetch(name, cache):
    path = os.path.join(cache, name + ".geojson")
    if not os.path.exists(path):
        print("downloading", name)
        urllib.request.urlretrieve(BASE + name + ".geojson", path)
    return gpd.read_file(path)


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", ".cache")
    os.makedirs(cache, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    c10 = fetch("ne_10m_admin_0_countries", cache)
    c10 = c10[c10.intersects(REGION)][["ADMIN", "NAME", "NAME_AR", "ADM0_A3", "geometry"]]
    c10["geometry"] = c10.geometry.simplify(0.01, preserve_topology=True)
    c10.to_file(os.path.join(OUT, "countries_region.geojson"), driver="GeoJSON")

    c50 = fetch("ne_50m_admin_0_countries", cache)[["ADMIN", "NAME", "NAME_AR", "ADM0_A3", "geometry"]]
    c50["geometry"] = c50.geometry.simplify(0.05, preserve_topology=True)
    c50.to_file(os.path.join(OUT, "countries_world.geojson"), driver="GeoJSON")

    a1 = fetch("ne_10m_admin_1_states_provinces", cache)
    a1 = a1[a1.intersects(REGION)][["name", "name_en", "name_ar", "adm0_a3", "geometry"]]
    a1["geometry"] = a1.geometry.simplify(0.005, preserve_topology=True)
    a1.to_file(os.path.join(OUT, "admin1_region.geojson"), driver="GeoJSON")

    lakes = fetch("ne_10m_lakes", cache)
    lakes = lakes[lakes.intersects(REGION)][["name", "geometry"]]
    lakes.to_file(os.path.join(OUT, "lakes_region.geojson"), driver="GeoJSON")
    print("done")


if __name__ == "__main__":
    main()
