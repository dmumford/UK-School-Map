# UK-School-Map
A Map of *almost* all Educational Schools, Colleges, and Universities in the UK. The map clusters Schools that are in close proximity, relative to the map zoom level.

## Background
This is one of the files from a larger project I made. The project involved scraping School, College, and University
information from the interwebs (Names, addresses, URLs, etc..), and storing them in an SQL database. This resulted in a table with over 40,000 records.

The scraped data wasn't perfect so I had to clean it up by trimming trailing whitespaces, removing unknown characters, validating data, etc..

The next step involved making calls to various Geo-location APIs to retrieve longitude and latitude values from partial address queries.

Finally, I loop through the database and plot the longitude and latitude coordinates onto a map of the UK, and output the map to a .html file


## Usage
You will need to change the MySQL credentials (lines 45-49). You will also need to change the table name in the SQL query (line 63). For the script to work, your MySQL table will need to have the following columns:

1. school (the name of the School/college/university)
2. addr1 (first line of the address)
3. addr2 (second line of the address)
4. town
5. county
6. postcode (aka Zip code)
7. country
8. id (unique row id)

![Map.html](https://github.com/dmumford/UK-School-Map/raw/main/example+output.png?raw=true)
