import numpy as np
import matplotlib.pyplot as plt


def pickup_surroundGrids(centerGrid, dataList):

  data = [[elem[0], elem[1]] for elem in dataList]

  # get 4 surround grids
  surroundGrid = []
  if centerGrid[0] != 0:
    surroundGrid.append([centerGrid[0]-1, centerGrid[1]])
  if centerGrid[1] != 0:
    surroundGrid.append([centerGrid[0], centerGrid[1]-1])
  surroundGrid.append([centerGrid[0]+1, centerGrid[1]])
  surroundGrid.append([centerGrid[0], centerGrid[1]+1])

  # pickup existing grid in data
  existSurroundGrid = []
  for i_surroundGrid in surroundGrid:
    if i_surroundGrid in data:
      idx = data.index(i_surroundGrid)
      existSurroundGrid.append(dataList[idx])

  return existSurroundGrid



def create_polylineFig(data):

  dataList = data.tolist()
  dataList = [[i_data[0], i_data[1], idx] for idx, i_data in enumerate(dataList)]
  # dataNp = np.insert(data, 2, np.linspace(0, data.shape[0]-1, data.shape[0]), axis=1) # idx

  traceList = [[] for i in range(len(dataList))]

  currentTrace = 0
  for idx, i_data in enumerate(dataList):

    # first grid
    if idx == 0:
      traceList[idx].append(currentTrace)
      continue

    # center grid
    grid = i_data[0:2]

    # surrounding grid
    surroundGrid = pickup_surroundGrids(grid, dataList)

    # get grid to check the trace
    idxToCheck = 0
    for i_surroundGrid in surroundGrid:
      if i_surroundGrid[2] < idx:
        idxToCheck = max([idxToCheck, i_surroundGrid[2]])

    # judge continuity
    gridToCheck = dataList[idxToCheck][0:2]
    surroundGrid2 = pickup_surroundGrids(gridToCheck, dataList)
    checkTrace = max(traceList[idxToCheck])

    countTrace = 0
    for i_surroundGrid in surroundGrid2:
      idxToCheck2 = dataList.index(i_surroundGrid)
      if checkTrace in traceList[idxToCheck2]:
        countTrace = countTrace + 1

    if countTrace >= 2:
      branchFlg = True
    else:
      branchFlg = False

    # branching
    if branchFlg:
      currentTrace = currentTrace + 1
      previousTrace = np.min(traceList[idxToCheck])

      for idxToAddTrace in range(idxToCheck+1):
        if previousTrace in traceList[idxToAddTrace]:
          traceList[idxToAddTrace].append(currentTrace)

    traceList[idx].append(currentTrace)

  # plotDict = {}
  # for idx in range(currentTrace):



  # create figure
  fig, ax = plt.subplots(figsize=(16, 9))
  for ii in range(len(plotDict)):
    dataNp = np.array(plotDict[ii])
    ax.plot(dataNp[:,0], dataNp[:,1], color="white", alpha=1/currentTrace)

  ax.set_aspect("equal")
  ax.set_facecolor("black")
  plt.show()




if __name__ == "__main__":

  data = np.load(r"../res/data.npy")

  create_polylineFig(data)
