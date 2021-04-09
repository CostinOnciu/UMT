def getMinute(time):
    """
    from a time string I get the minute int
    example: from 00:01 I get 1
    :param time: string
    :return: minute int
    """
    hour, minutes = time.split(":")
    hour = int(hour)
    minutes = int(minutes)
    return hour * 60 + minutes


def getTime(minute):
    """
    from a int minute I get the time string
    example: from 1 I get 00:01
    :param minute: int
    :return: time string
    """
    hour = minute // 60
    minutes = minute - (hour * 60)

    if hour > 9:
        hour = str(hour)
    else:
        hour = "0" + str(hour)

    if minutes > 9:
        minutes = str(minutes)
    else:
        minutes = "0" + str(minutes)

    return hour + ":" + minutes


"""
    I could have a list of 1440 elements each meaning a minute from a day
    0 is at 00:00
    1 is at 00:01
    and so on
    and for each booked I mark the whole minutes range
    after that is search for continuous sequences of more than "meeting time" minutes
    and I validate them to be in both range limits

    this would be in the worst case scenario O(1440 * 3) which I believe is okW
"""


def getFreeTime(booked1, rangeLimit1, booked2, rangeLimit2, meetingTime):
    """

    :param booked1: list
    :param rangeLimit1: list of 2 elements
    :param booked2: list
    :param rangeLimit2: list of 2 elements
    :param meetingTime: int
    :return: list
    """
    """
        Initialization of the booked minutes list
    """
    bookedMinutes = [0 for _ in range(1440)]

    """
        For every booked time table I mark the corresponding minutes in
        the booked minutes list
    """
    for times in booked1:
        startMinute = getMinute(times[0])
        endMinute = getMinute(times[1])
        for i in range(startMinute, endMinute):
            bookedMinutes[i] = 1
    for times in booked2:
        startMinute = getMinute(times[0])
        endMinute = getMinute(times[1])
        for i in range(startMinute, endMinute):
            bookedMinutes[i] = 1

    """
        Here I find all the possible solutions,
        meaning all continuous sequences of more than "meeting time" minutes
    """
    possibleSol = []
    currentLen = 0
    for minute in range(1440):
        if bookedMinutes[minute] == 0:
            if currentLen == 0:
                startMinute = minute
            currentLen += 1
        else:
            endMinute = minute
            if currentLen >= meetingTime:
                possibleSol.append((startMinute, endMinute))
            currentLen = 0
    endMinute = 1439
    if currentLen >= meetingTime:
        possibleSol.append((startMinute, endMinute))

    """
        Here I validate the possible solutions to be in the range limits 
        
        the max for the first time string
        and the min for the second time string 
        from both persons
        
        If valid I add it as a final solution
        
        Also if a sequence has one limit that is not in the range limit 
        I try to see if moving the end, or the start of the sequence, or both, to one 
        of the range points will be enough to make a valid time table for a meeting
        and if it's valid I add it as a solution
    """
    solutions = []
    for possibleSolution in possibleSol:
        if max(getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0])) <= possibleSolution[0] <= min(
                getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])):
            if min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])) >= possibleSolution[1] >= max(
                    getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0])):
                solutions.append([getTime(possibleSolution[0]), getTime(possibleSolution[1])])
            elif possibleSolution[1] > min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])):
                if min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])) - possibleSolution[0] >= meetingTime:
                    solutions.append([getTime(possibleSolution[0]),
                                      getTime(min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])))])
        elif possibleSolution[0] < max(getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0])):
            if possibleSolution[1] - max(getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0])) >= meetingTime:
                if min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])) >= possibleSolution[1] >= max(
                        getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0])):
                    solutions.append([getTime(max(getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0]))),
                                      getTime(possibleSolution[1])])
                elif possibleSolution[1] > min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])):
                    if min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])) - possibleSolution[0] >= meetingTime:
                        solutions.append([getTime(max(getMinute(rangeLimit1[0]), getMinute(rangeLimit2[0]))),
                                          getTime(min(getMinute(rangeLimit1[1]), getMinute(rangeLimit2[1])))])
    return solutions


with open("file.in", "r") as f:
    booked1Line = f.readline().split(", ")
    booked1 = []
    for time in booked1Line:
        time = time.strip().strip("['").strip("']").strip("'")
        if time != '':
            booked1.append(time.split("','"))
    # print(booked1)
    rangeLimit1Line = f.readline().split(",")
    rangeLimit1 = []
    for time in rangeLimit1Line:
        time = time.strip().strip("['").strip("']").strip("'")
        rangeLimit1.append(time)
    # print(rangeLimit1)
    booked2Line = f.readline().split(", ")
    booked2 = []
    for time in booked2Line:
        time = time.strip().strip("['").strip("']").strip("'")
        if time != '':
            booked2.append(time.split("','"))
    # print(booked2)
    rangeLimit2Line = f.readline().split(",")
    rangeLimit2 = []
    for time in rangeLimit2Line:
        time = time.strip().strip("['").strip("']").strip("'")
        rangeLimit2.append(time)
    # print(rangeLimit2)
    meetingTime = int(f.readline())
    # print(meetingTime)

    print(getFreeTime(booked1, rangeLimit1, booked2, rangeLimit2, meetingTime))
