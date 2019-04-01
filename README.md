# `thatkiy` - Fast geodesic distances in Python

This is a **personal project** centered around geodesic distances.
Its goal is to be able to quickly compute, for every coordinate in a list:

- Distances to a given point (e.g. distances from each point to NYC)
- Nearest neighbors: distances to the closest point in another list (e.g. distances from each point to a city), and the identity of such point
- Number of neighbors: number of points of another list within a certain distance or buffer.

## Usage

From Python:

```python
import thatkiy
...
```

From the command line:

```
...
```

## Dependencies:

- [`rtree`](http://toblerity.org/rtree/) (wrapper around [`libspatialindex`](https://libspatialindex.org/)). Windows binaries [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)
- [`pyproj`](https://github.com/pyproj4/pyproj) (wrapper around [`proj4`](https://proj4.org/))


## Why "thatkiy"?

Thatkiy was one of the Inca measures of distance, equivalent to about 130 cm.
I would have preferred to use "topo", but it's already a quite popular name on Github, and has other meanings.

![Gordon McEwan, "The Incas: New Perspectives", p.179](incas_new_perspective_mcewan_p179.png)
[Gordon McEwan, "The Incas: New Perspectives", p.179](https://books.google.com/books?id=J3WZuTINl2QC&pg=PA179)


## Why not geopandas, etc.?

Earlier tests deemed them too slow/complicated, but there might be workarounds. EG:

https://stackoverflow.com/questions/54804073/how-can-i-accelerate-a-geopandas-spatial-join/54804074#54804074


## Limitations

- Not parallelized, although that should be trivial
- Not Cython, although most of the heavy load is already in C.
- Only deals with points, not with lines/polygons
