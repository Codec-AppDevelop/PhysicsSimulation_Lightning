import numpy as np
import matplotlib.pyplot as plt


def create_polylineFig(data):

  dataNp = np.insert(data, 2, np.linspace(0, data.shape[0]-1, data.shape[0]), axis=1) # idx
  dataNp = np.insert(dataNp, 3, 0, axis=1) # trace

  for idx, i_data in enumerate(dataNp):

    # center grid
    grid = i_data[0:1]

    # surrounding grid
    surroundGrid = []
    if grid[0] != 0:
      surroundGrid.append([i_data[0]-1, i_data[1]])




if __name__ == "__main__":

  data = np.load(r"../res/data.npy")

  create_polylineFig(data)
