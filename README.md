# Snake-Deep-Q-Learning

# To run this repository, you will need some installations:

1. Download Python: https://www.python.org/
2. Open Command Prompt, switch to your directory where you installed the repository.
3. Run: `python -m pip install requirement.txt`

# To start training:
1. In Command Prompt, run: `python train.py` (The model is saved every 10 games)
2. After training, close the program.
3. The model is saved in `model.pth`
4. To play with the trained model, run: `python play.py`

# Optional settings:
- In `settings.py`, you can change some parameters.
    - `BLOCK_SIZE (default = 30)` : make sure that 600/BLOCK_SIZE equals an even number
    - `SPEED (default = 60)` : change the tick speed of the game
    - `Color` : change the colors of the game