"""
Title: CITS 1401 - Project 1
Author: Akhila Liyanage (23729213)
"""


def main(csvfile, adultID, Option):
    # Read and analyse csv file with the following headers:
    # ID[0], Expression[1], Distance[2], Gdis[3], Ldis[4]
    with open(csvfile, "r") as file:
        header_idxs = get_header_idxs(file.readline())  # holds header indices to match with data

    # calculate stats if Option is stats, else calculate FR
    if Option.lower() == "stats":
        exp_data = [
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
            [[0, 0, 0]] * 8,
        ]  # holds all expression data
        line_count = 1  # to keep track of read lines

        # open the csv file as read-only
        with open(csvfile, "r") as file:
            for line in file:
                curr_line = line.split(",")
                # ignore headers and other adultIDs
                if curr_line[header_idxs[0]].lower() != adultID.lower():
                    continue
                # extract data by following the header indices
                else:
                    curr_line[header_idxs[2]] = int(curr_line[header_idxs[2]])  # Distance
                    curr_line[header_idxs[3]] = float(curr_line[header_idxs[3]])  # GDi
                    curr_line[header_idxs[4]] = float(curr_line[header_idxs[4]].strip("\n"))  # LDi

                    # use Distance column as an index for sorting
                    if curr_line[header_idxs[1]].lower() == "neutral":
                        exp_data[0][curr_line[header_idxs[2]] - 1] = fix_data(curr_line, header_idxs, Option)
                    elif curr_line[header_idxs[1]].lower() == "angry":
                        exp_data[1][curr_line[header_idxs[2]] - 1] = fix_data(curr_line, header_idxs, Option)
                    elif curr_line[header_idxs[1]].lower() == "disgust":
                        exp_data[2][curr_line[header_idxs[2]] - 1] = fix_data(curr_line, header_idxs, Option)
                    else:  # happy
                        exp_data[3][curr_line[header_idxs[2]] - 1] = fix_data(curr_line, header_idxs, Option)
                    line_count += 1
                # all required data is extracted so exit the loop
                if line_count == 33:
                    break

        # OP1: get max and min values of GDi and LDi across each expression
        op1 = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        min_gdi, max_gdi, min_ldi, max_ldi = 1000000, 0, 1000000, 0

        for i in range(8):
            for j in range(4):
                # find min_gdi
                if exp_data[j][i][1] < min_gdi:
                    min_gdi = exp_data[j][i][1]
                # find max_gdi
                if exp_data[j][i][1] > max_gdi:
                    max_gdi = exp_data[j][i][1]
                # find min_ldi
                if exp_data[j][i][2] < min_ldi:
                    min_ldi = exp_data[j][i][2]
                # find max_ldi
                if exp_data[j][i][2] > max_ldi:
                    max_ldi = exp_data[j][i][2]
            op1[i][0] = round(min_gdi, 4)
            op1[i][1] = round(max_gdi, 4)
            op1[i][2] = round(min_ldi, 4)
            op1[i][3] = round(max_ldi, 4)
            min_gdi, max_gdi, min_ldi, max_ldi = 1000000, 0, 1000000, 0

        # OP2: get difference of GDi and LDi for each expression
        op2 = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        for i in range(4):
            for j in range(8):
                op2[i][j] = round(exp_data[i][j][1] - exp_data[i][j][2], 4)

        # OP3: get average of GDi across the expressions
        op3 = [0] * 8

        for i in range(8):
            op3[i] = round((exp_data[0][i][1] + exp_data[1][i][1] + exp_data[2][i][1] + exp_data[3][i][1]) / 4, 4)

        # OP4: get standard deviation of LDi across the expressions
        op4 = [0] * 8
        dist_avg = [0] * 8
        numerator = 0

        for i in range(8):
            # get mean for each distance
            dist_avg[i] = (exp_data[0][i][2] + exp_data[1][i][2] + exp_data[2][i][2] + exp_data[3][i][2]) / 4
            # numerator = sum of the square of each LDi - mean
            for j in range(4):
                numerator += (exp_data[j][i][2] - dist_avg[i]) ** 2
            # get the square root of the numerator divided by 4
            op4[i] = round((numerator / 4) ** 0.5, 4)
            numerator = 0

        return op1, op2, op3, op4

    else:  # calculate FR
        max_cossim = 0  # will hold maximum cosine similarity
        adult_id_gdi_n = []  # adultID GDI Neutral
        adult_id_gdi_o = []  # adultID GDI other expressions
        others_gdi_n = []  # all other ID GDI Neutral

        # get adultID GDi values
        with open(csvfile, "r") as file:
            for line in file:
                curr_line = line.split(",")

                # ignore headers
                if curr_line[header_idxs[0]].lower() == "id":
                    continue

                curr_line[header_idxs[2]] = int(curr_line[header_idxs[2]])  # Distance
                curr_line[header_idxs[3]] = float(curr_line[header_idxs[3]])  # GDi

                # extract data from other IDs
                if curr_line[header_idxs[0]].lower() != adultID.lower():
                    if curr_line[header_idxs[1]].lower() == "neutral":
                        others_gdi_n.append(fix_data(curr_line, header_idxs, Option))
                # extract data from adultID
                else:
                    if curr_line[header_idxs[1]].lower() == "neutral":
                        adult_id_gdi_n.append(fix_data(curr_line, header_idxs, Option))
                    elif curr_line[header_idxs[1]].lower() == "angry":
                        adult_id_gdi_o.append(fix_data(curr_line, header_idxs, Option))
                    elif curr_line[header_idxs[1]].lower() == "disgust":
                        adult_id_gdi_o.append(fix_data(curr_line, header_idxs, Option))
                    else:  # happy
                        adult_id_gdi_o.append(fix_data(curr_line, header_idxs, Option))

            # sort both lists according to ID first then by Distance
            adult_id_gdi_n = sorted(adult_id_gdi_n, key=lambda x: x[1])
            others_gdi_n = sorted(sorted(others_gdi_n, key=lambda x: x[1]), key=lambda x: x[0])

            # iterate and compare with other expressions to find max cossim
            i = 0
            while i < len(adult_id_gdi_o):
                cos_sim = cal_cos_sim(adult_id_gdi_n, adult_id_gdi_o[i: i + 8])
                if cos_sim > max_cossim:
                    match_id = adult_id_gdi_o[i][0]
                    max_cossim = cos_sim
                i += 8

            # iterate and compare with all other IDs to find max cossim
            i = 0
            while i < len(others_gdi_n):
                cos_sim = cal_cos_sim(adult_id_gdi_n, others_gdi_n[i: i + 8])
                if cos_sim > max_cossim:
                    match_id = others_gdi_n[i][0]
                    max_cossim = cos_sim
                i += 8
        return match_id, round(max_cossim, 4)


"""
Function to calculate the cosine similarity score
"""


def cal_cos_sim(l1, l2):
    numerator, a_sqr, b_sqr = 0, 0, 0

    # get sums of all components
    for i in range(8):
        numerator += l1[i][2] * l2[i][2]
        a_sqr += l1[i][2] * l1[i][2]
        b_sqr += l2[i][2] * l2[i][2]

    # return calculated cossim
    return numerator / (a_sqr ** 0.5 * b_sqr ** 0.5)


"""
Function to fix 0 or negative GDis and LDis, and return relevant data
"""


def fix_data(curr_line, header_idxs, option):
    if curr_line[header_idxs[3]] <= 0:
        curr_line[header_idxs[3]] = 50.0
    if option.lower() == "stats":
        if curr_line[header_idxs[4]] <= 0:
            curr_line[header_idxs[4]] = 50.0
        # return Distance, GDi, LDi
        return curr_line[header_idxs[2]], curr_line[header_idxs[3]], curr_line[header_idxs[4]]
    else:  # FR
        # return ID, Distance, GDi
        return curr_line[header_idxs[0]], curr_line[header_idxs[2]], curr_line[header_idxs[3]]


"""
Function to get the indices of the headers
"""


def get_header_idxs(line):
    check_headers = ["ID", "Expression", "Distance", "Gdis", "Ldis"]
    header_idxs = []

    header_line = line.split(",")
    header_line[4] = header_line[4].strip("\n")

    for i in range(5):
        idx = header_line.index(check_headers[i])
        header_idxs.append(idx)

    return header_idxs

# OP1, OP2, OP3, OP4 = main("ExpData_Sample.csv", "E001", "stats")
# print(OP1, "\n\n", OP2, "\n\n", OP3, "\n\n", OP4)
# ID, cossim = main("ExpData_Sample.csv", "E001", "FR")
# print(ID, cossim)
