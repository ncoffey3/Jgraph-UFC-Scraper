# Jgraph UFC Scraper
by Nolan Coffey

This program scrapes the UFC website for the record of two MMA fighters. Then generates a jgraph file that plots the fighters wins by their method (Knockout, Submission, or Decision). The fighters' losses are also plotted in the opposite direction.
## Sample graph:
<img src ="https://github.com/ncoffey3/Jgraph-UFC-Scraper/assets/123964103/2d5f34a5-b893-401d-b6e8-6299a0333a59" width = "500" height = "500"> 

## Instructions for Running the Program:
The program can be executed from the command line as follows:
* python ufcScrape.py fighter1 fighter2 output.jgr
* * Fighter names should contain a '-' between first and last. Example: jon-jones
  * The outputfile should end with .jgr. Example: test.jgr
 * Example usage:
 * python ufcScrape.py brandon-moreno alexandre-pantoja moreno_pantoja.jgr

# Generating a PDF or JPG:
* The program outputs a .jgr file, which then can be converted to a pdf using the following command:
* * jgraph < example.jgr | ps2pdf -dEPSCrop - example.pdf
* PDF to JPG
* * convert -density 300 -trim example.pdf -quality 100 example.jpg
   
## Dependencies
* In order to webscrape, Playwright is required. Which requires NodeJS and NPM for the installation.
* This video contains further instructions for the installation process: https://www.youtube.com/watch?v=IB2P1FBXjcQ&list=PLhW3qG5bs-L9sJKoT1LC5grGT77sfW0Z8&index=2



## More Example Graphs:

* The breakdown of win methods allows for an interesting visualization of a fighter's style. Derrick Lewis is a knockout artist compared to Jim Miller who is known for his submissions. 
<img src="https://github.com/ncoffey3/Jgraph-UFC-Scraper/assets/123964103/44719aed-4c19-4d9a-806b-ec5c7fcce54d" width="500" height="500">
<img src="https://github.com/ncoffey3/Jgraph-UFC-Scraper/assets/123964103/4e1e6e96-16d5-418c-9fd2-fa0593a46848" width="500" height="500">
<img src="https://github.com/ncoffey3/Jgraph-UFC-Scraper/assets/123964103/2ff25874-7d26-430f-8500-6b64cecb85fd" width="500" height="500">

### Kickboxing rivals style reflected
<img src="https://github.com/ncoffey3/Jgraph-UFC-Scraper/assets/123964103/5cd2c8aa-2071-4166-a1f9-8df633ccb56d" width="500" height="500">



