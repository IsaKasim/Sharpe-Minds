#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import math

nInst=100
currentPos = np.zeros(nInst)
POSITION_LIMIT = 10000

histArbPortfolio = []
for x in range(6):
    histArbPortfolio.append([])


def exp_ma(prices, days, smoothing):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    Y = np.array([56, 69, 80, 57, 84, 63])
    X = np.array([98, 79, 66, 71, 91, 51])
    beta = np.array([6.2389, 4.0588, 1.2982, 0.5628, 0.1989, 1.8436])
    thresh = np.array([0.447, 0.752, 0.328, 0.420, 0.0747, 0.868])

    arbPortfolio = []
    for i in range(len(Y)):
        arbPortfolio.append(prcSoFar[Y[i]][nt - 1] - prcSoFar[X[i]][nt - 1] * beta[i])

    rpos = np.zeros(nInst)
    for j in range(len(Y)):
        histArbPortfolio[j].append(arbPortfolio[j])
        bias = exp_ma(histArbPortfolio[j], 20, 1)[-1] if len(histArbPortfolio[j]) >= 20 else 0

        if currentPos[Y[j]] == 0:
            highestValue = max(prcSoFar[Y[j]][nt - 1], beta[j] * prcSoFar[X[j]][nt - 1])
            numToBuy = math.floor(POSITION_LIMIT / highestValue)
            if arbPortfolio[j] < -thresh[j] + bias:
                # BUY
                rpos[Y[j]] = numToBuy
                rpos[X[j]] = round(-numToBuy*beta[j])
            elif arbPortfolio[j] > thresh[j] + bias:
                # SELL
                rpos[Y[j]] = -numToBuy
                rpos[X[j]] = round(numToBuy * beta[j])
        elif currentPos[Y[j]] > 0:
            if arbPortfolio[j] > 0 + bias:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]
        elif currentPos[Y[j]] < 0:
            if arbPortfolio[j] < 0 + bias:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]

    currentPos += rpos
    return currentPos
