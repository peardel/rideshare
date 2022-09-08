import math

EARTH_RADIUS = 6371 # in km
def lat_lon_euclidean_dist(lat1: float, lon1: float, lat2: float, lon2: float, use_radians:bool=False) -> float:
    """
        d = acos( sin φ1 ⋅ sin φ2 + cos φ1 ⋅ cos φ2 ⋅ cos Δλ ) ⋅ R 
        lat/longs should be in degrees,
        distance will be given in km
    """
    if not use_radians:
        lat1, lon1, lat2, lon2 = (math.radians(x) for x in (lat1, lon1, lat2, lon2))
    return math.acos( math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1) ) * EARTH_RADIUS