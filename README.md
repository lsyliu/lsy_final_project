# Shuying_Liu_SI507_final_project
"final project.py" is the main program code. 
For this final project, I built a program to help users to select cars through choosing their preferences. Users can run the program and interact with the program through inputing commands as directed by the program. At the end, users can choose bar charts, box plots or maps to be presented. 
A "data_cleaned.csv" database file is needed for this program to run successfully. The data are retreived through web scraping from 6 Ebay websites and a city coordinate data file downloaded from simplemaps website.
The following Python packages are needed for the program to run: requests, numpy, pandas, time, matplotlib.pyplot, seaborn, plotly.graph_objects.
The following are functions created for this program:
•	car_info_detail1: generate information and graphs using data from the database for one specific used car as the user chooses
•	car_info_detail20: generate information and graphs using data from the database for more than one used car after filtering through users preferences
•	car_info_get: create interactions with users to filtering the data as users choose their preferences step by step
•	create_us_graph: generate a choropleth map which shows locations with the number of cars at the locations using location data

