import requests
from bs4 import BeautifulSoup

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


def sudoku():
    page = requests.get("https://www.menneske.no/sudoku/eng/random.html?diff=8")
    soup = BeautifulSoup(page.content, "html.parser")
    puzzle = soup.select("div.grid td")
    sudoku = []
    for i in range(9):
        row = []
        for j in range(9):
            sq = puzzle[i * 9 + j].text
            if sq == "\xa0":
                sq = 0

            row.append(int(sq))
        sudoku.append(row)

    return sudoku
