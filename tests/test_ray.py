import pytest

from geomdl import ray
from geomdl.ray import Ray, RayIntersection

def test_ray_intersect():
    r2 = Ray((5.0, 181.34), (13.659999999999997, 176.34))
    r3 = Ray((19.999779996773235, 189.9998729810778), (19.999652977851035, 180.00009298430456))
    t0, t1, res = ray.intersect(r2, r3)
    assert res != RayIntersection.SKEW

