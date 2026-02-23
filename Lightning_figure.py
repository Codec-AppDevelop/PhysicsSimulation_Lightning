import numpy as np
import matplotlib.pyplot as plt


def create_polylineFig(data):

  dataList = data.tolist()
  dataList = [[i_data[0], i_data[1], idx, []] for idx, i_data in enumerate(dataList)]
  # dataNp = np.insert(data, 2, np.linspace(0, data.shape[0]-1, data.shape[0]), axis=1) # idx

  currentTrace = 0
  for idx, i_data in enumerate(dataList):

    # center grid
    grid = i_data[0:1]
    currentIdx = dataList[2]

    # surrounding grid
    surroundGrid = []
    if grid[0] != 0:
      surroundGrid.append([i_data[0]-1, i_data[1]])
    if grid[0] != 0:
      surroundGrid.append([i_data[0], i_data[1]-1])
    surroundGrid.append([i_data[0]+1, i_data[1]])
    surroundGrid.append([i_data[0], i_data[1]+1])

    # judge
    # continuous if maximum index within grids whose order is less than the grid
    contFlg = False

    idxList = []
    maxTraceIdx = 0
    for i_surroundGrid in surroundGrid:
      if i_surroundGrid in dataList:
        idxTmp = dataList.index(i_surroundGrid)
        idxList.append(idxTmp)

        if idxTmp == currentIdx - 1:
          contFlg = True
        elif idxTmp < currentIdx:
          maxTraceIdx = np.max([maxTraceIdx, idxTmp])

    # process
    if contFlg == True:
      dataList[idx][3].append(currentTrace)
    else:
      currentTrace = currentTrace + 1
      dataList[idx][3].append(currentTrace)



if __name__ == "__main__":

  data = np.load(r"../res/data.npy")

  create_polylineFig(data)
