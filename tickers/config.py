# ~ Configuration file, all constants in one place :)

TICKERS_COUNT = 100
TICKERS_WINDOW = 5

HORIZONTAL_MARGIN = 10
VERTICAL_MARGIN = 5

PTS_RADIUS_PERCENT = 1

FONT_ENLARGEMENT = 1.5
FONT_NAME = "Arial"
FONT_MOD = "bold"

COLOR_BACKGROUND = "white"
COLOR_OBJECT = "darkblue"

DB_USER = "postgres" 
DB_PASS = "1"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"


TICKERS_DIGITS = 10 ** (len(str(TICKERS_COUNT)) - 1)




if __name__ == '__main__':
	exit()
