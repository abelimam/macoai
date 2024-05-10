from joblib import Parallel, delayed
from pathlib import Path
import os

def play_game(game_conf: str):
    os.system("python play_n_games.py " + game_conf)

if __name__ == "__main__":
    conf_files = *map(str, Path("conf").rglob("*.json")),
    Parallel(n_jobs=6, backend='multiprocessing')(delayed(play_game)(i) for i in conf_files if 'asmacag' not in i)