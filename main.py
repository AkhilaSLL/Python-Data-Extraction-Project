"""
Title: CITS 1401 - Project 1
Author: Akhila Liyanage (23729213)
"""


def main(csvfile, adultID, Option):
    # Read and analyse csv file with the following headers:
    # ID[0], Expression[1], Distance[2], Gdis[3], Ldis[4]
    headerIdxs = []  # holds header indices to match with data

    with open(csvfile, "r") as file:
        headerIdxs = getHeaderIdxs(file.readline())

    # calculate stats if Option is stats, else calculate FR
    if Option.lower() == "stats":
        expData = [
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
        ]  # holds all expression data
        lineCount = 1  # to keep track of read lines

        # open the csv file as read-only
        with open(csvfile, "r") as file:
            for line in file:
                currLine = line.split(",")
                # ignore headers and other adultIDs
                if currLine[headerIdxs[0]].lower() != adultID.lower():
                    continue
                # extract data by following the header indices
                else:
                    currLine[headerIdxs[2]] = int(currLine[headerIdxs[2]])  # Distance
                    currLine[headerIdxs[3]] = float(currLine[headerIdxs[3]])  # GDi
                    currLine[headerIdxs[4]] = float(
                        currLine[headerIdxs[4]].strip("\n")
                    )  # LDi

                    # use Distance column as an index for sorting
                    if currLine[headerIdxs[1]].lower() == "neutral":
                        expData[0][currLine[headerIdxs[2]] - 1] = fixData(
                            currLine, headerIdxs, Option
                        )
                    elif currLine[headerIdxs[1]].lower() == "angry":
                        expData[1][currLine[headerIdxs[2]] - 1] = fixData(
                            currLine, headerIdxs, Option
                        )
                    elif currLine[headerIdxs[1]].lower() == "disgust":
                        expData[2][currLine[headerIdxs[2]] - 1] = fixData(
                            currLine, headerIdxs, Option
                        )
                    else:  # happy
                        expData[3][currLine[headerIdxs[2]] - 1] = fixData(
                            currLine, headerIdxs, Option
                        )
                    lineCount += 1
                # all required data is extracted so exit the loop
                if lineCount == 33:
                    break

        # OP1: get max and min values of GDi and LDi across each expression
        OP1 = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        minGDi, maxGDi, minLDi, maxLDi, = (
            1000000,
            0,
            1000000,
            0,
        )

        for i in range(8):
            for j in range(4):
                # find minGDi
                if expData[j][i][1] < minGDi:
                    minGDi = expData[j][i][1]
                # find maxGDi
                if expData[j][i][1] > maxGDi:
                    maxGDi = expData[j][i][1]
                # find minLDi
                if expData[j][i][2] < minLDi:
                    minLDi = expData[j][i][2]
                # find maxLDi
                if expData[j][i][2] > maxLDi:
                    maxLDi = expData[j][i][2]
            OP1[i][0] = round(minGDi, 4)
            OP1[i][1] = round(maxGDi, 4)
            OP1[i][2] = round(minLDi, 4)
            OP1[i][3] = round(maxLDi, 4)
            minGDi, maxGDi, minLDi, maxLDi, = (
                1000000,
                0,
                1000000,
                0,
            )

        # OP2: get difference of GDi and LDi for each expression
        OP2 = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        for i in range(4):
            for j in range(8):
                OP2[i][j] = round(expData[i][j][1] - expData[i][j][2], 4)

        # OP3: get average of GDi across the expressions
        OP3 = [0] * 8

        for i in range(8):
            OP3[i] = round(
                (
                    expData[0][i][1]
                    + expData[1][i][1]
                    + expData[2][i][1]
                    + expData[3][i][1]
                )
                / 4,
                4,
            )

        # OP4: get standard deviation of LDi across the expressions
        OP4 = [0] * 8
        dist_avg = [0] * 8
        numerator = 0

        for i in range(8):
            # get mean for each distance
            dist_avg[i] = (
                expData[0][i][2]
                + expData[1][i][2]
                + expData[2][i][2]
                + expData[3][i][2]
            ) / 4
            # numerator = sum of the square of each LDi - mean
            for j in range(4):
                numerator += (expData[j][i][2] - dist_avg[i]) ** 2
            # get the square root of the numerator divided by 4
            OP4[i] = round((numerator / 4) ** 0.5, 4)
            numerator = 0

        return OP1, OP2, OP3, OP4

    else:  # calculate FR
        maxCossim = 0  # will hold maximum cosine similarity
        adultIDGDi_N = []  # adultID GDI Neutral
        adultIDGDi_O = []  # adultID GDI other expressions
        othersGDI_N = []  # all other ID GDI Neutral

        # get adultID GDi values
        with open(csvfile, "r") as file:
            for line in file:
                currLine = line.split(",")

                # ignore headers
                if currLine[headerIdxs[0]].lower() == "id":
                    continue

                currLine[headerIdxs[2]] = int(currLine[headerIdxs[2]])  # Distance
                currLine[headerIdxs[3]] = float(currLine[headerIdxs[3]])  # GDi

                # extract data from other IDs
                if currLine[headerIdxs[0]].lower() != adultID.lower():
                    if currLine[headerIdxs[1]].lower() == "neutral":
                        othersGDI_N.append(fixData(currLine, headerIdxs, Option))
                # extract data from adultID
                else:
                    if currLine[headerIdxs[1]].lower() == "neutral":
                        adultIDGDi_N.append(fixData(currLine, headerIdxs, Option))
                    elif currLine[headerIdxs[1]].lower() == "angry":
                        adultIDGDi_O.append(fixData(currLine, headerIdxs, Option))
                    elif currLine[headerIdxs[1]].lower() == "disgust":
                        adultIDGDi_O.append(fixData(currLine, headerIdxs, Option))
                    else:  # happy
                        adultIDGDi_O.append(fixData(currLine, headerIdxs, Option))

            # sort both lists according to ID first then by Distance
            adultIDGDi_N = sorted(adultIDGDi_N, key=lambda x: x[1])
            othersGDI_N = sorted(
                sorted(othersGDI_N, key=lambda x: x[1]), key=lambda x: x[0]
            )

            # iterate and compare with other expressions to find max cossim
            i = 0
            while i < len(adultIDGDi_O):
                cossim = calCosSim(adultIDGDi_N, adultIDGDi_O[i : i + 8])
                if cossim > maxCossim:
                    ID = adultIDGDi_O[i][0]
                    maxCossim = cossim
                i += 8

            # iterate and compare with all other IDs to find max cossim
            i = 0
            while i < len(othersGDI_N):
                cossim = calCosSim(adultIDGDi_N, othersGDI_N[i : i + 8])
                if cossim > maxCossim:
                    ID = othersGDI_N[i][0]
                    maxCossim = cossim
                i += 8
        return ID, round(maxCossim, 4)


"""
Function to calculate the cosine similarity score
"""


def calCosSim(l1, l2):
    numerator, A_sqr, B_sqr = 0, 0, 0

    # get sums of all components
    for i in range(8):
        numerator += l1[i][2] * l2[i][2]
        A_sqr += l1[i][2] * l1[i][2]
        B_sqr += l2[i][2] * l2[i][2]

    # return calculated cossim
    return numerator / (A_sqr**0.5 * B_sqr**0.5)


"""
Function to fix 0 or negative GDis and LDis, and return relevant data
"""


def fixData(currLine, headerIdxs, Option):
    if currLine[headerIdxs[3]] <= 0:
        currLine[headerIdxs[3]] = 50.0
    if Option.lower() == "stats":
        if currLine[headerIdxs[4]] <= 0:
            currLine[headerIdxs[4]] = 50.0
        # return Distance, GDi, LDi
        return [
            currLine[headerIdxs[2]],
            currLine[headerIdxs[3]],
            currLine[headerIdxs[4]],
        ]
    else:  # FR
        # return ID, Distance, GDi
        return [
            currLine[headerIdxs[0]],
            currLine[headerIdxs[2]],
            currLine[headerIdxs[3]],
        ]


"""
Function to get the indices of the headers
"""


def getHeaderIdxs(line):
    checkHeaders = ["ID", "Expression", "Distance", "Gdis", "Ldis"]
    headerIdxs = []

    headerLine = line.split(",")
    headerLine[4] = headerLine[4].strip("\n")

    for i in range(5):
        idx = headerLine.index(checkHeaders[i])
        headerIdxs.append(idx)

    return headerIdxs


# OP1, OP2, OP3, OP4 = main("ExpData_Sample.csv", "E001", "stats")
# print(OP1, "\n\n", OP2, "\n\n", OP3, "\n\n", OP4)
# ID, cossim = main("ExpData_Sample.csv", "E001", "FR")
# print(ID, cossim)
