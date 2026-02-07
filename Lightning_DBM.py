import numpy as np
import matplotlib.pyplot as plt


def selectNewSite(candidateSite, eta):

    # calculate probability
    candidateSiteNp = np.array(candidateSite)
    phiMin = np.min(candidateSiteNp[:,2])
    phiMax = np.max(candidateSiteNp[:,2])
    if phiMin == phiMax:
        PhiList = np.ones([np.size(candidateSiteNp, axis=0)])
    else:
        PhiList = (candidateSiteNp[:,2] - phiMin) / (phiMax - phiMin)
    sumPhi = np.sum(np.power(PhiList, eta), axis=0)
    probList = (np.power(PhiList, eta) / sumPhi).tolist()

    # select one site
    selectedIdx = np.random.choice(a=np.arange(0, len(candidateSite), 1), size=1, p=probList)

    return candidateSite[selectedIdx[0]][0:2]


def calcElecPotential(candidateSite, growthSite, endSite):

    endSite = np.array(endSite)

    # calculate each potential
    for idx, candidate_i in enumerate(candidateSite):

        # calculation parameters
        R1 = 1/2
        R2 = np.max([np.min(np.sqrt((endSite[:,0] - candidate_i[0])**2 + (endSite[:,1] - candidate_i[1])**2)),0.6])
        c1 = -(R1/R2 - 1)**(-1)
        c2 = (1/R2 - 1/R1)**(-1)

        # newly added candidate point
        if candidate_i[2] == 0:

            phi = 0
            for growthSite_i in growthSite:
                r = np.sqrt((candidate_i[0]-growthSite_i[0])**2 + (candidate_i[1]-growthSite_i[1])**2)
                phi = phi + (c1 + c2/r)

        # update of the potential
        else:
            # latest added point
            addedSite = growthSite[-1]

            r = np.sqrt((candidate_i[0] - addedSite[0])**2 + (candidate_i[1] - addedSite[1])**2)
            phi = candidate_i[2] + (c1 + c2/r)

        # save the calculated result
        candidateSite[idx][2] = phi

    return candidateSite


def addCandidateSite(candidateSite, growthSite, gridSize):

    addedPnt = growthSite[-1]
    candidateSite_new = list(filter(lambda elem: (not elem[0] == addedPnt[0]) or (not elem[1] == addedPnt[1]), candidateSite))

    # added point
    newPnt = growthSite[-1]

    # candidate of candidate point
    newCandidate = [
        [newPnt[0] - 1, newPnt[1]],
        [newPnt[0], newPnt[1] - 1],
        [newPnt[0], newPnt[1] + 1],
        [newPnt[0] + 1, newPnt[1]]
    ]

    # loop for each candidate
    for newCandidate_i in newCandidate:

        # if it includes gridSize
        if newCandidate_i[0] >= 0 \
            and newCandidate_i[0] < gridSize[0] \
            and newCandidate_i[1] >= 0 \
            and newCandidate_i[1] < gridSize[1]:

            if (not newCandidate_i in growthSite) \
                and (not newCandidate_i in candidateSite):

                newCandidate_i.append(0)
                candidateSite_new.append(newCandidate_i)

    return candidateSite_new


def initialize(gridSize, originPnt, endCond):

    # field matrix, (0,0) at bottom left grid
    fieldMat = np.zeros(gridSize)

    # list of growth site
    growthSite = []

    # list of candidate site
    candidateSite = []

    # initial point
    if originPnt == "TopCenter":
        addPnt = [int((gridSize[0]-1)/2), gridSize[1]-1]
    elif originPnt == "Center":
        addPnt = [int((gridSize[0]-1)/2), int((gridSize[1]-1)/2)]
    elif originPnt == "BottomCenter":
        addPnt = [int((gridSize[0]-1)/2, 0)]

    endSite = calcEndSiteList(gridSize, endCond)


    return fieldMat, growthSite, candidateSite, endSite, addPnt


def calcEndSiteList(gridSize, endCond):

    if endCond == "BottomEdge":
        rowIdx = np.zeros([1, gridSize[0]])
        columnIdx = np.arange(0, gridSize[0], 1).reshape([1, -1])
    elif endCond == "TopEdge":
        rowIdx = np.zeros([1, gridSize[0]]) + gridSize[0] - 1
        columnIdx = np.arange(0, gridSize[0], 1).reshape([1, -1])
    elif endCond == "LeftEdge":
        rowIdx = np.arrange(0, gridSize[1], 1).reshape([1, -1])
        columnIdx = np.zeros([1, gridSize[1]])
    elif endCond == "RightEdge":
        rowIdx = np.arrange(0, gridSize[1], 1).reshape([1, -1])
        columnIdx = np.zeros([1, gridSize[1]]) + gridSize[1] - 1
    elif endCond == "BottomCenter":
        if np.mod(gridSize[0],2) == 0:
            rowIdx = [0, 0]
            columnIdx = [gridSize[0]/2 - 1, gridSize[0]/2]
        else:
            rowIdx = [0]
            columnIdx = [(gridSize[0]-1)/2]

    endSite = np.vstack([columnIdx, rowIdx]).T.tolist()

    return endSite


def mainLoop(gridSize, originPnt, endCond, eta):

    # define matrix and list for data container
    fieldMat, growthSite, candidateSite, endSite, addPnt = initialize(gridSize, originPnt, endCond)

    endFlg = False

    while(not endFlg):

        # calculate add site
        if len(growthSite) < 1:
            addSite = addPnt
        else:
            # probability calc
            addSite = selectNewSite(candidateSite, eta)

        growthSite.append(addSite)
        fieldMat[addSite[0],addSite[1]] = 1

        # calculate candidate site
        candidateSite = addCandidateSite(candidateSite, growthSite, gridSize)

        # calculate electric potential
        candidateSite = calcElecPotential(candidateSite, growthSite, endSite)

        # create a figure


        # update loop flag
        if addSite in endSite:
            endFlg = True

    return growthSite




if __name__ == "__main__":

    # User Input
    scale = 6
    gridSize = [16*10*scale, 9*10*scale]
    originPnt = "TopCenter" # "TopCenter", "Center" or "BottomCenter"
    endCond = "BottomCenter" # "BottomEdge", "LeftEdge", "RightEdge", "TopEdge" or "BottomCenter"
    eta = 10 # User parameter

    # Calculation
    growthSite = mainLoop(gridSize, originPnt, endCond, eta)

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 4.5))
    data = np.array(growthSite).T
    ax.scatter(data[0,:], data[1,:], color="white", marker="o", alpha=0.1/scale**(1/2), edgecolors="none", s=500/(scale**2))
    ax.scatter(data[0,:], data[1,:], color="white", marker="s", alpha=0.5, edgecolors="none", s=10/(scale**2))
    ax.set(xlim=(0, gridSize[0]), ylim=(0, gridSize[1]), xticks=[], yticks=[])
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    plt.show()

