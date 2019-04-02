clear all
cls

global project "C:\Dropbox\Projects\PopulationCensus"
adopath + "$project/aliases/code"

use "C:\Dropbox\Projects\PopulationCensus\merged\data\everything"
generate_canonical_city city_name, gen(x) state(state_abbrev)
kosi state_id x || state_abbrev state_name county_name county_id city_name feature_id fips founded type pop1850-pop1910
tempfile everything
save "`everything'"

insheet using reserve_cities.tsv, clear
rename city x
merge 1:1 state_id x using "`everything'", keep(master match) assert(match)

* .. ? incomplete due to system crash
