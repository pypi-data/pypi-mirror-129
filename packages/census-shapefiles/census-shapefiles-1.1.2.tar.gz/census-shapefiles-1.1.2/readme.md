## Census Shapefiles

Library to pull shapefiles from the Census

### Installation
```
pip install census-shapefiles
```

### Usage
```python
from census_shapefiles import CensusShapefiles

sfs = CensusShapeFiles()
for shapefile in sfs.city.get_shapefiles():
    # Do something with the temp file
```