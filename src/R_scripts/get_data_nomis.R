# R script for Nomis API to download UK census data sets
# More info https://docs.evanodell.com/nomisr/articles/introduction.html

library(nomisr)

# Function to extract data for a given geography type
extract_nomis_data <- function(geography_type) {
  nomis_get_data(
    id = "NM_529_1",
    time = "latest",
    geography = geography_type,
    measures = c(20301),
    rural_urban = 0,
    select = c(
      "DATE",
      "GEOGRAPHY_CODE",
      "GEOGRAPHY_NAME",
      "RURAL_URBAN_NAME",
      "C_RELPUK11_NAME",
      "MEASURES_NAME",
      "OBS_VALUE"
    )
  )
}

# Get all available sets info
all_sets_info <- nomis_data_info()

# Search datasets for Religion information
search_results <- nomis_search(name = "*Religion*")
tibble::glimpse(search_results)

# Check available measures and geography types for a specific dataset
search_A_measures <- nomis_get_metadata("NM_529_1", "measures")
print(search_A_measures)

search_A_geography <- nomis_get_metadata("NM_529_1", "geography", "TYPE")
print(search_A_geography)

# Extract input at district / unitary level
nomis_religion <- extract_nomis_data("TYPE464")

# Extract input at county / unitary level
nomis_religion2 <- extract_nomis_data("TYPE463")

# Save files at the data repository
write.csv(nomis_religion, "./input/nomis_religion.csv", row.names = FALSE)
write.csv(nomis_religion2, "./input/nomis_religion2.csv", row.names = FALSE)

