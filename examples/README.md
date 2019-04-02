Feature-complete example:

```
cls && tupu some_cities.csv?id=uid
	--output=augmented.tsv
		--distance=dist_ny,40.7143,-74.0060
		--distance=dist_dc,38.9072,-77.0369
		--neighbor dist_reserve,id_reserve,reserve_cities.tsv?id=feature_id
		-n dist_city,id_city
		--verbose --timeit
```
