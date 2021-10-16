# this is an R script uses Nomis API to download UK census input
# from more info https://docs.evanodell.com/nomisr/articles/introduction.html

library(nomisr)

x <- nomis_data_info()
# search datasets for Religion information
search_A <- nomis_search(name = "*Religion*")
tibble::glimpse(search_A)

# check available measures
search_A_measures <- nomis_get_metadata("NM_529_1", "measures")
search_A_measures

# check available geography types
search_A_geography <- nomis_get_metadata("NM_529_1", "geography", "TYPE")
search_A_geography

# extract input at district / unitary level
nomis_religion <- nomis_get_data(id = "NM_529_1",
                                 time = "latest", 
                                 geography = "TYPE464", # local authorities: district / unitary 
                                 measures=c(20301), 
                                 rural_urban = 0,
                                 select = c("DATE", 
                                            "GEOGRAPHY_CODE",
                                            "GEOGRAPHY_NAME",
                                            "RURAL_URBAN_NAME",
                                            "C_RELPUK11_NAME",
                                            "MEASURES_NAME",
                                            "OBS_VALUE"))

# extract input at county / unitary  level
nomis_religion2 <- nomis_get_data(id = "NM_529_1",
                                 time = "latest", 
                                 geography = "TYPE463", # local authorities: county / unitary 
                                 measures=c(20301), 
                                 rural_urban = 0,
                                 select = c("DATE", 
                                            "GEOGRAPHY_CODE",
                                            "GEOGRAPHY_NAME",
                                            "RURAL_URBAN_NAME",
                                            "C_RELPUK11_NAME",
                                            "MEASURES_NAME",
                                            "OBS_VALUE"))

#  save the files
write.csv(nomis_religion,
          "./input/nomis_religion.csv",
          row.names = FALSE)

write.csv(nomis_religion2,
          "./input_religion2.csv",
          row.names = FALSE)
