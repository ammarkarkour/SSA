#import datetime
from datetime import datetime
import nltk
import re
import string
from pattern.en import suggest
from word2number import w2n
stopword = nltk.corpus.stopwords.words('english')

##########################################################################
                         #####interface######

#This function uses nltk library and pattern.en library to 
def spelling_correction(text):
    pass
#requires text to be string



#This function takes a text and parse it to get what you should search for
def parse_to_search(text):
    pass
#requires text to be string



#This function read the deadline from the text that user gives it 
#and then returns the deadline in terms of datetime
def get_deadline(text):
    pass
# requires text to be a string



#This function reads the data (time of task)
#from the text that user gives it, and then returns the data as float
#use it to get duration
def get_duration(text):
    pass
# requires text to be a string



#This function returns how many perscentage you will lose if you don't do this task
#we use the output of this task to calculate the score of the task
#we get the inputs from the function get data 
def get_taskGrade(taskGrade, courseGrade):
    pass
# requires both of taskGrade and courseGrade to be a ints or floats



#This function returns the diff between the time you have and how long the task 
#will need to be done 
#we use the output of this task to calculate the score of the task 
#we get the input duration from the function get_duration
#we get the input deadline from the function get_deadline
def get_taskTime(duration, deadLine):
    pass
# requires duration to be a int or float
# requires deadline to be datetime



#This function gives you the score for each task
#we get duration from get_duration or the user manually
#we get taskTime from the function get_taskTime
#we get taskGrade from the function get_taskGrade
def get_taskScore( duration, taskTime, taskGrade):
    pass
#requires all of them to be ints or floats



#This function reads word number and return it as number
#use this function to get gradetask and coursegrade   
def get_grade(text):
    pass
#requires text to be a string 



#get the name of the task
def get_taskName(text):
    pass
# requires text to be a string



#it adds the new task and reorder the list, then rewrite the file with 
#the updated list, then returns a dict with the list
#we get the task name from the function get_taskName
#we get the score from the function give_score which uses get_taskTime
#and get_taskGrade which use get_duration to read the text from the user
def add_task(taskName, taskScore, deadline):
    pass
# requires task to be a string
# requires score to be an int or a float 



#This function delete the given task from the list and return a dict that contains the new list of tasks
def delete_task(taskName):
    pass
#requires taskName to be a string
   

   
#This function edit a task's details and update the tasks file
def edit_task(taskName, taskScore, deadline, duration, taskGrade, courseGrade):
        pass



#This task updates the list of tasks based on the deadline only 
#puts the missed tasks on the lat of the list 
#it returns a dict that cntains the tasks 
def update_list():
    pass


#returns a list of the tasks
def get_tasks():
    pass

##########################################################################

                            #####implementation######


def spelling_correction(text):
    pattern = re.compile(r"(.)\1{2,}")
    text = (pattern.sub(r"\1\1", text)).split()
    text = [suggest(word)[0][0] for word in text ]
    return " ".join(text)



#This function takes a text and parse it to get what you should search for
def parse_to_search(text):

    #text = "".join([char for char in text if char not in string.punctuation])
    text = spelling_correction(text)
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word not in stopword]
    return " ".join(text)



#this function converts words numbers to int number
def text2int (textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand","million", "billion", "trillion"]
        scales2 = ["hundreds", "thousands","millions", "billions", "trillions"]


        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
        for idx, word in enumerate(scales2): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else: 
                scale, increment = numwords[word]

                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            


    if onnumber:
        curstring += repr(result + current)  

    return curstring



#This function read the deadline from the text that user
# gives it and then returns the deadline in terms of datetime
def get_deadline(text):


    if re.search("\d+/\d+/\d+",text):
        date = text
        return (datetime.strptime(date, '%d/%m/%Y'))

    text1 = text2int(parse_to_search(text))
    newText = text1.split()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    months = [ "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    currentTime = datetime.now()
    final = ["", "" , str(currentTime.year)]
    for i in range(len(newText)):
        if newText[i].lower() in months:
            month = months.index(newText[i].lower()) + 1
            final[1] = str(month)

        if not newText[i].isalpha() and newText[i] != " " and final[1] != "" and int(newText[i]) > int(final[1])  :
            final[2] = str(newText[i])

        if not newText[i].isalpha() and newText[i] != " " and final[1] == "":
            final[0] = newText[0]

    harshCode = text.split()
    hardCode = {"eleven":11, "twelve":12, "thirteen":13, "fourteen":14, "fifteen":15,
        "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19}

    for i in range(1,len(harshCode)):
        if harshCode[i-1] == "twenty" and harshCode[i] in hardCode and hardCode[harshCode[i]] > 10 and hardCode[harshCode[i]] < 20:
            final[2] = str(20*100 + hardCode[harshCode[i]])


    date = "/".join(final)
    return (datetime.strptime(date, '%d/%m/%Y'))


 
#This function read the data (time of task)
#from the text that user gives it, and then returns the data as float
#use it to get duration
def get_duration(text):

    try: 

        return float(text)

    except:

        text = text2int(text).split()
        result = ""
        #print(text)
        for i in range(1 , len(text)):
            if not text[i - 1].isalpha() and text[i - 1] != " ":

                 result = float(text[i - 1]) 

            if not text[i].isalpha() and text[i - 1] != " ":
                result = float(text[i])

            if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "minutes" or text[i] == "minute" ):

                return float(text[i - 1]) / 60

            if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "days" or text[i] == "day" ):

                return float(text[i - 1]) * 24

            if not text[i - 1].isalpha() and text[i - 1] != " " and  ( text[i] == "hours" or text[i] == "hour" ):
            
                return float(text[i - 1])

        return result

 

#This function reads word number and return it as number
#use this function to get gradetask and coursegrade   
def get_grade(text):

    try:
        return w2n.word_to_num(parse_to_search(text))

    except:

        try:
            return float(text)

        except:

            try:

                return float((text.split(" "))[0])

            except:
                return "can you  enter the number in a different way"


#get the name of the task
def get_taskName(text):

    text = parse_to_search(spelling_correction(text))
    text = text.split()
    j = 0;
    for i in text:
        if i == "add":
            #print(" ".join(text[text.index("add") + 1:]))
            return " ".join(text[text.index("add") + 1:])



#this function returns the diff between the time you have and how long the task will need to be done
def get_taskTime(duration, deadLine):

    currentTime = datetime.now()

    deff = (8765.81277 *(deadLine.year - currentTime.year) + 730.484398 *(deadLine.month - currentTime.month) + 24*(deadLine.day - currentTime.day) +(deadLine.hour - currentTime.hour) )+24    #print(deff)
    
    if deff <=  0:

        return "missed"

    deff2 = deff - float(duration)

    return deff2



#this task returns how many perscentage you have until you drop to lower grade
def get_taskGrade(taskGrade, courseGrade):

    howMuch = float(courseGrade) % 10 
    return   howMuch - (float(courseGrade) - (float(courseGrade) - float(taskGrade)))



#This function gives you the score for each task
def get_taskScore( duration, taskTime = 80, taskGrade = 5):

    if  taskTime == "missed" or taskTime >= 168 :

        return 0

    elif taskTime == 0 or ((- 1 * taskTime) / duration)*100 >= 80 :

        taskTime = 400

    elif 0 < taskTime and taskTime < 24:

        taskTime = 350

    elif 24 <= taskTime and taskTime < 48:

        taskTime = 300

    elif 48 <= taskTime and taskTime < 72:

        taskTime =250

    elif 72 <= taskTime and taskTime < 96:

        taskTime = 200

    elif 96 <= taskTime and taskTime < 120:

        taskTime = 150

    elif 120 <= taskTime and taskTime < 144:

        taskTime = 100

    elif 144 <= taskTime and taskTime < 168:

        taskTime = 50

    

    else:

        taskTime == 200


    if taskGrade < 0 :

        taskGrade = 500

    elif 9 <= taskGrade :

        taskGrade = 50

    elif  8 <= taskGrade and taskGrade < 9:

        taskGrade = 100

    elif 7 <= taskGrade and taskGrade < 8:

        taskGrade = 150

    elif 6 <= taskGrade and taskGrade < 7:

        taskGrade = 200

    elif 5 <= taskGrade and taskGrade < 6:

        taskGrade = 250

    elif 4 <= taskGrade and taskGrade < 5 :

        taskGrade = 300

    elif 3 <= taskGrade and taskGrade < 4:

        taskGrade = 350

    elif 2 <= taskGrade and taskGrade < 3:

        taskGrade = 400

    elif 1 <= taskGrade and taskGrade < 2:

        taskGrade = 450

    else:

        taskGrade == 250

    #print(taskGrade + taskTime)
    return taskGrade + taskTime
    


# it adds the new task and reorder the list, then rewrite the file with the updated list
#then returns a dict with the list
def add_task(taskName, taskScore, deadline, duration, taskGrade, courseGrade):

    dataBase = open("tasks.txt", "r+")
    line = dataBase.readline()
    while line == "\n":

        line = dataBase.readline()

    tasks = {}
    while line:
        
        while line == "\n":
            line = dataBase.readline()

        line = line.split("@")
        
        tasks[line[0]] = [line[1],float(line[2]),float(line[3]),float(line[4]), float(line[5].strip())]
        line = dataBase.readline()

    if taskName in tasks:
        tasks[taskName] = [deadline,taskScore, duration, taskGrade, courseGrade]

    else:
        tasks[taskName] = [deadline,taskScore, duration, taskGrade, courseGrade]  

    tasks = [(k, tasks[k]) for k in sorted(tasks, key=lambda x : tasks.get(x)[1], reverse=True)]

    dataBase = open("tasks.txt" , "w+")
    for key , value in tasks:
        dataBase.seek(0,2)
        dataBase.write(key + "@" +str(value[0]) +"@" +str(value[1]) + "@" +str(value[2])  + "@" +str(value[3])  + "@" +str(value[4])  +"\n" )

    dataBase.close()
    return tasks



#This function delete the given task from the list and return a dict that contains the new list of tasks
def delete_task(taskName):

    with open("tasks.txt", "r+") as f:
        lines = f.readlines()
    with open("tasks.txt", "w+") as f:
        for line in lines:
            line_list = line.split("@")
            if line_list[0] != taskName:
                f.write(line)
    tasks = {}

    with open("tasks.txt", "r+") as f:
        line = f.readline()
        while line == "\n":
            line = f.readline()
        while line:
            line_list2 = line.split("@")
            tasks[line_list2[0]] = [line_list2[1],float(line_list2[2]),float(line_list2[3]),float(line_list2[4]), float(line_list2[5].strip())]
            line = f.readline()

    return tasks



#This function edit a task's details and update the tasks file
def edit_task(taskName, taskScore, deadline, duration, taskGrade, courseGrade):

    with open("tasks.txt", "r+") as f:
        lines = f.readlines()
    with open("tasks.txt", "w+") as f:
        for line in lines:
            line_list = line.split("@")
            if line_list[0] != taskName:
                f.write(line)
            else: 
                f.write(taskName + "@" +str(deadline) +"@" +str(taskScore) + "@" +str(duration)  + "@" +str(taskGrade)  + "@" +str(courseGrade)  +"\n" )
    update_list()



#This task updates the list of tasks based on the deadline only 
#puts the missed tasks on the lat of the list 
#it returns a dict that cntains the tasks 
def update_list():

    currentTime =datetime.now()
    with open("tasks.txt", "r+") as f:
        lines = f.readlines()
    with open("tasks.txt", "w+") as f:
        for line in lines:
            line_list = line.split("@")
            date = line_list[1]
            date = date.split(" ")
            date = date[0]
            date = datetime.strptime(date, '%Y-%m-%d')
            line_list[2] =str(get_taskScore( float(line_list[3]), get_taskTime(float(line_list[3]),date) , 
                            get_taskGrade(float(line_list[4]), float(line_list[5]))))
            
            line = "@".join(line_list)
            f.write(line)   

    tasks = {}

    with open("tasks.txt", "r") as f:
        line = f.readline()
        while line == "\n":
            line = f.readline()
        while line:
            line_list2 = line.split("@")
            tasks[line_list2[0]] = [line_list2[1],float(line_list2[2]),float(line_list2[3]),float(line_list2[4]), float(line_list2[5].strip())]
            line = f.readline()

    tasks = [(k, tasks[k]) for k in sorted(tasks, key=lambda x : tasks.get(x)[1], reverse=True)]


    dataBase = open("tasks.txt" , "w+")
    for key , value in tasks:
        dataBase.seek(0,2)
        dataBase.write(key + "@" +str(value[0]) +"@" +str(value[1]) + "@" +str(value[2])  + "@" +str(value[3])  + "@" +str(value[4])  +"\n" )

    dataBase.close()

    return tasks


#returns a list of the tasks
def get_tasks():

    with open("tasks.txt", "r+") as f:
        lines = f.readlines()

    lines2 = []
    for line in lines:
        lines2.append((line.strip()).split("@"))
        
    return lines2


# print(add_task(get_taskName("add english homework"), get_taskScore(get_duration("five hours"),get_taskTime(get_duration("five hours")
#     ,get_deadline("twenty first of june")),get_taskGrade(get_grade("one point five percent"),get_grade("ninety five percent"))), get_deadline("twenty first of june")))
