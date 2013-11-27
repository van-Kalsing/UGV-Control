from surface.polygon import Polygon, Point
from surface.surface import Surface



polygon1 = Polygon([(0.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.0, 0.0)])
polygon2 = Polygon([(0.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.0, 0.0)])
polygon3 = Polygon([(0.5, 0.3, 0.0), (1.0, 1.1, 0.0), (1.0, 0.0, 0.2)])

print("Тестирование сопоставления полигонов")
print(Polygon.match_polygons(polygon1, polygon2, 0.0))
print(Polygon.match_polygons(polygon1, polygon3, 0.0))
print(Polygon.match_polygons(polygon1, polygon2, 0.7))
print(Polygon.match_polygons(polygon1, polygon3, 0.7))

point1 = Point(polygon1, [(1, 1.0)])
point2 = Point(polygon1, [(1, 0.5), (2, 0.5)])
point3 = Point(polygon1, [(2, 1.0)])

print("Тестирование вычисление координат точек")
print(point1.coordinates)
print(point2.coordinates)
print(point3.coordinates)

point4 = Point(polygon1, [(1, 1.2)])

print("Тестирование сопоставления точек")
print(Point.match_points(point1, point4, 0.0))
print(Point.match_points(point1, point4, 0.25))
print(Point.match_points(point1, point3, 0.25))
print(Point.match_points(point1, point3, 1.0))
