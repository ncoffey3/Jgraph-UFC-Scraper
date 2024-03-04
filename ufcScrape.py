# ufcScrape.py
# Nolan Coffey
# 3-3-24
# This program scrapes the record of two UFC fighters and plots a graph of their record with wins broken into three categories. 
# These are their method of winning (Knockout, Submission, or Decision)

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re
import math
import sys

async def scrape_ufc(fighter1, fighter2, filename):
    df = pd.DataFrame(columns=["name", "wins", "losses"])

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = False)
        page1 = await browser.new_page()
        page2 = await browser.new_page()

        # Open the fighter pages
        await page1.goto("https://www.ufc.com/athlete/" + fighter1)
        await page2.goto("https://www.ufc.com/athlete/" + fighter2)

        pages = [page1, page2]
        fighters = []

        # Scrape relevant statistics for both fighters
        for page in pages:

            content = await page.content()

            content = BeautifulSoup(content, "html.parser")

            name = content.find("h1", class_="hero-profile__name").text.strip()
            record = content.find("p", class_="hero-profile__division-body").text.strip()
            winByMethod = content.find_all("div", class_="c-stat-3bar c-stat-3bar--no-chart")[1]
            winByMethod = winByMethod.find_all("div", class_="c-stat-3bar__value")
            winByKO = winByMethod[0]
            winByDec = winByMethod[1]
            winBySub = winByMethod[2]

            winByKO = winByKO.text.strip()
            winBySub = winBySub.text.strip()
            winByDec = winByDec.text.strip()

            winByKO = re.match(r'(\d+)', winByKO)
            winByKO = winByKO.group(0)

            winBySub = re.match(r'(\d+)', winBySub)
            winBySub = winBySub.group(0)

            winByDec = re.match(r'(\d+)', winByDec)
            winByDec = winByDec.group(0)

            record = re.match(r'(\d+)-(\d+)', record)

            if record:
                wins, losses = record.groups()
            #print(name)
            #print(record)
            #print(wins)
            #print(losses)
            #print(winByKO)
            #print(winBySub)
            #print(winByDec)

            fighters.append({'Name': name, 'Wins': int(wins), 'KO' : int(winByKO), 'Sub': int(winBySub), 'Dec': int(winByDec), 'Losses': int(losses)})
        generate_jgraph(fighters, filename)
        print(f"Output: {filename}")

def generate_jgraph(fighters, filename="fighters.jgr"):
    lines = ["newgraph\n"]

    # Calculate the fighter with the most wins and round up to the nearest multiple of 5
    x_max = max(fighters[0]['Wins'], fighters[1]['Wins']) 
    x_max = math.ceil(x_max / 5) * 5

    # Do the same with losses to find the minimum x value
    x_min = max(fighters[0]['Losses'], fighters[1]['Losses'])
    x_min = (math.ceil(x_min / 5) * 5) * -1

    lines.append(f"xaxis\n min {x_min} max {x_max}\n mhash 9\n hash_labels font Times-Italic\n label : Wins by Method\n\n")
    lines.append("yaxis\n size 1.5 min 0 max 3\n nodraw\ncopygraph yaxis draw_at 0\n\n")
    
    # First fighter
    lines.append(f"(* {fighters[0]['Name']} *)\n")
    # 3 bars are layered, Decisions will be the last bar so we draw it first, drawn at total number of fighter's wins
    if fighters[0]['Dec'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 0 0 1 (* blue for dec *)\npts {fighters[0]['Wins']} 1\n")
    if fighters[0]['Sub'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 0 .5 0 (* green for sub *)\npts {fighters[0]['Wins']-fighters[0]['Dec']} 1\n")
    if fighters[0]['KO'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 1 0 0 (* red for KO *)\npts {fighters[0]['Wins']-fighters[0]['Dec']-fighters[0]['Sub']} 1\n")
    if fighters[0]['Losses'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill .4 .4 .4 (* grey for losses *)\npts {fighters[0]['Losses'] * -1} 1\n\n")

    # Second fighter
    lines.append(f"(* {fighters[1]['Name']} *)\n")
    if fighters[1]['Dec'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 0 0 1 (* blue for dec *)\npts {fighters[1]['Wins']} 2\n")
    if fighters[1]['Sub'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 0 .5 0 (* green for sub *)\npts {fighters[1]['Wins']-fighters[1]['Dec']} 2\n")
    if fighters[1]['KO'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill 1 0 0 (* red for KO *)\npts {fighters[1]['Wins']-fighters[1]['Dec']-fighters[1]['Sub']} 2\n")
    if fighters[1]['Losses'] > 0:
        lines.append(f"newcurve marktype ybar marksize 0 .5 cfill .4 .4 .4 (* grey for losses *)\npts {fighters[1]['Losses'] * -1} 2\n\n")

    lines.append(f"newstring\n hjl vjc\n fontsize 9\n font Helvetica-Narrow\n(* {fighters[0]['Name']} total wins *)\n x {fighters[0]['Wins']+.5} y 1 : {fighters[0]['Wins']}\n")
    lines.append(f"(* {fighters[1]['Name']} total wins *)\n copystring x {fighters[1]['Wins']+.5} y 2 : {fighters[1]['Wins']}\n")
    lines.append(f"copystring x 5 y 1.5 : {fighters[0]['Name']}\ncopystring x 5 y 2.5 : {fighters[1]['Name']}\n")
    lines.append(f"(* total losses *)\ncopystring x {fighters[0]['Losses'] * -1} y 1.4 : {fighters[0]['Losses']}\n")
    lines.append(f"(* total losses *)\ncopystring x {fighters[1]['Losses'] * -1} y 2.4 : {fighters[1]['Losses']}\n")


    # Add Legend
    lines.append("legend top\nnewcurve marktype ybar cfill 1 0 0 marksize 5 .2\n label : Knockout\n")
    lines.append("newcurve marktype ybar cfill 0 .5 0 marksize 5 .2\n label : Submission\n")
    lines.append("newcurve marktype ybar cfill 0 0 1 marksize 5 .2\n label : Decision\n")
    lines.append("newcurve marktype ybar cfill .4 .4 .4 marksize 5 .2\n label : Losses\n")


    # Write to .jgr file
    with open(filename, 'w') as f:
        f.writelines(lines)



if __name__ == "__main__":
    if len(sys.argv) == 4:  

        firstFighter = sys.argv[1]
        secondFighter = sys.argv[2]
        filename = sys.argv[3]
        
        asyncio.run(scrape_ufc(firstFighter, secondFighter, filename))
    else:
        print("Usage: python ufcScrape.py <firstFighter> <secondFighter> <outputFile.jgr>")



                      
    
