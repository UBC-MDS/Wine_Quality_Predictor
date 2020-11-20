# setup
library(tidyverse)
library(lubridate)

# data import
df <- read_csv('data/raw/Global_Mobility_Report.csv')

procases_sum <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/11-18-2020.csv')

cases_time_series <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

# Countries are chosen by population scale and number of confirmed cases
country_lst <- c('US','Canada','Brazil', 'Argentina','Colombia',
                 'France','Russia','Spain', 'UK','Italy',
                 'India', 'South Africa')





# data wrangling

chosen_country <- 'Canada'

# cases
can_time <- cases_time_series %>% 
     filter(`Country/Region` == chosen_country) %>%
     select(-Lat, -Long, -`Province/State`) %>% 
     pivot_longer(!`Country/Region`, names_to = 'date', values_to = "cases") %>%
     mutate(date = mdy(date) ) %>% 
     group_by(date) %>% 
     summarize(cum_cases = sum(cases)) %>% 
     mutate(inc_cases = cum_cases - data.table::shift(cum_cases, 1L, type='lag', fill=0))


can_cases <- can_time %>% 
     ggplot(aes(x = date, 
                y = inc_cases)) + 
     geom_line() +
     scale_y_continuous(trans = 'log')+
     scale_x_date(date_labels = "%Y %b")

can_cases

# mobility (Google is banned in China)

# Ploting mobility rate for all Canada
# TBD: facet by country
can_df <- df %>% 
     filter(country_region == chosen_country) %>% 
     filter(is.na(sub_region_1)) %>% 
     select(-country_region_code, -sub_region_2, -metro_area, -iso_3166_2_code, -census_fips_code) %>% 
     pivot_longer(!c(country_region, sub_region_1, date), 
                  names_to = 'places', values_to = "percentages_change") %>% 
     mutate(places = case_when(places == "grocery_and_pharmacy_percent_change_from_baseline" ~ "grocery_and_pharmacy",
                               places == "parks_percent_change_from_baseline" ~ "parks",
                               places == "residential_percent_change_from_baseline" ~ "residential",
                               places == "retail_and_recreation_percent_change_from_baseline" ~ "retail_and_recreation",
                               places == "transit_stations_percent_change_from_baseline" ~ "transit_stations",
                               places == "workplaces_percent_change_from_baseline" ~ "workplaces"))

can_mobil <- can_df %>% 
     ggplot(aes(x = date,
                y = percentages_change,
                colour = places)) +
     geom_line() +
     scale_x_date(date_labels = "%Y %b")
can_mobil

can_combo <- left_join(can_df, can_time)


