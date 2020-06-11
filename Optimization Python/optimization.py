import time
import random
import bisect


class Log:
    def __init__(self, arrivaltime, user, session, event, usrfield):
        self.arrivaltime = arrivaltime
        self.user = user
        self.session = session
        self.event = event
        self.usrfield = usrfield

    def getArrivaltime(self):
        return self.arrivaltime

    def getUser(self):
        return self.user

    def getSession(self):
        return self.session

    def getEvent(self):
        return self.event

    def getUsrfield(self):
        return self.usrfield

    def __str__(self):
        return "(arrivaltime:%s, user:%s, session:%d, event:%s, usrfield:%d)" % (time.ctime(self.arrivaltime),
                                                                                 self.user,
                                                                                 self.session,
                                                                                 self.event,
                                                                                 self.usrfield)

    def __repr__(self):
        return "(arrivaltime:%s, user:%s, session:%d, event:%s, usrfield:%d)" % (time.ctime(self.arrivaltime),
                                                                                 self.user,
                                                                                 self.session,
                                                                                 self.event,
                                                                                 self.usrfield)


def randomLogs(n):
    stringmaxlen = 3
    sessionmax = 1000
    events = ['eventA', 'eventB', 'eventC', 'eventD', 'eventE']
    arrivalmin = int(time.mktime(time.strptime('Mon Jan 1 12:00:00 2020')))
    arrivalmax = int(time.mktime(time.strptime('Mon Mar 1 12:00:00 2020')))
    usrfieldmax = 10000
    chars = 'abcdefghijklmnprstuvyz'
    logs = []

    for i in range(1, n + 1):
        arrival = random.randint(arrivalmin, arrivalmax)
        user = ''
        for x in range(0, stringmaxlen):
            user += random.choice(chars)
        session = random.randint(0, sessionmax)
        event = random.choice(events)
        usrfield = random.randint(0, usrfieldmax)
        log = Log(arrival, user, session, event, usrfield)
        logs.append(log)
    return logs


def registerEqualQuery(logs, field):
    def query(val1):
        res = []
        for (index, log) in enumerate(logs):
            if getattr(log, field)() == val1:
                res.append(log)
        return res

    if field not in ['getArrivaltime', 'getUser', 'getSession', 'getEvent', 'getUsrfield']:
        raise Exception('field name not found')
    return query


def registerRangeQuery(logs, field):
    def query(p1,p2):
        res=[]
        if field in ['getSession']:
            for (index, log) in enumerate(logs):
                if int(log.getSession()) >= (p1) and int(log.getSession()) <= int(p2):
                    res.append(log)
            return res
        else:
            for (index, log) in enumerate(logs):
                if compareDate(log.getArrivaltime(),p1,p2):
                    res.append(log)
            return res


    if field not in ['getArrivaltime','getSession']:
        raise Exception('field name not found')
    return query

def registerOptimizedRangeQuery(logs, field):
    dictionary = {}

    def OptimizedQuery(p1,p2):
        #Optimizedlist = []
        # iterate through dictionary items to find required value
        return list({key:value for key, value in dictionary.items() if p1 <= value <= p2}.keys())

    if field not in ['getArrivaltime', 'getSession']:
        raise Exception('field name not found')
    for (index, log) in enumerate(logs):
        temp = getattr(log, field)()
        dictionary[log] = eval(temp) if isinstance(temp, str) else temp
        # if field == 'getArrivaltime':
        #     dictionary[log] = log.getArrivaltime()
        # else:
        #     dictionary[log] = log.getSession()
    return OptimizedQuery


def registerOptimizedEqualQuery(logs, field):
    dictionary = {}

    def OptimizedQuery(attribute):
        Optimizedlist = []
        # iterate through dictionary items to find required value
     
        for key, value in dictionary.items():
            if value == attribute:
                Optimizedlist.append(key)
        return Optimizedlist

    if field not in ['getArrivaltime', 'getUser', 'getSession', 'getEvent', 'getUsrfield']:
        raise Exception('field name not found')
    for (index, log) in enumerate(logs):
        dictionary[log] = getattr(log, field)()
    return OptimizedQuery
def compareDate(actualDate, startDate, endDate):
    return actualDate > startDate and actualDate < endDate
import test


def main():
    case = input("Enter test item: ")
    casefun = getattr(test, case)
    casefun()


if __name__ == '__main__':
    main()
