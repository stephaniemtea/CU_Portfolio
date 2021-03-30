import time
import random

#CPU Scheduler
runQueue = []
onDeck = []
numOfTasks = 0
simTime = 0
sumCompleteTimes = 0
waitTimes = 0
tasks = ["Sleep", "Eating", "Homework", "Break", "Catnap", "Snack", "Reading", "Shower", "Cleaning", "Watching TV", "Calling People", "Running"] #store different types of process categories

print("Processes are in progress: \n")

#Process class
class Process:
  def __init__(self, e, c):
    self.pid = random.randint(1,10000)
    self.execTime = e
    self.programCounter = 0
    self.category = c

  def run(self):
    global simTime, numOfTasks, sumCompleteTimes, waitTimes
    self.programCounter += 1 #while each process is running, add a counter until it reaches the execution time
    simTime += 1 #add one to to the simulation time
    #Runs when the task is COMPLETED
    if self.programCounter == self.execTime: #if the program counter reaches the execution time
      print(self.category, f"Finished ({self.execTime})")
      numOfTasks += 1 #add task to task list
      sumCompleteTimes += simTime #add simulation time or the time it takes for the task to complete
      for x in range(len(runQueue)): #run loop for length of task queue
        waitTimes = 0 #set wait time to zero because the first task starts at zero time
        waitTimes += sumCompleteTimes  #add total time to the wait time 
    time.sleep(1)

  def debug(self):
    print(f"PID: {self.pid}, Exec Time: {self.execTime}, Counter: {self.programCounter}, Category: {self.category}")
  
  def showStats(self):
    print("\nAll Processes have finished")
    print(f"Total Simulation Time: {simTime}")
    print(f"Tasks Executed: {numOfTasks}\n")
    # Throughput
    throughput = round(numOfTasks/simTime, 3)
    print(f"Throughout: {throughput} (tasks/sec)")

    #Avg Completion Time
    avgCompletionTime = round(sumCompleteTimes /numOfTasks, 3)
    print(f"Avg. Completion Time: {avgCompletionTime} sec")

    #Avg Wait Time
    avgWaitTimes = round(waitTimes/numOfTasks, 3)
    print(f"Avg. Wait Time: {avgWaitTimes} sec")

#Create processes
runQueue.insert(0, Process(4, "Sleep")) 
runQueue.insert(0, Process(3, "Classes"))
runQueue.insert(0, Process(1, "Lunch"))
runQueue.insert(0, Process(2, "CatNap"))
runQueue.insert(0, Process(1, "Snack"))
runQueue.insert(0, Process(3, "Homework"))
runQueue.insert(0, Process(2, "Surfing the Web"))

for x in range(20):
  onDeck.append(Process(random.randint(1,5), random.choice(tasks)))

for x in range(random.randint(5, 10)):
  runQueue.insert(random.randint(0, len(runQueue)-1), onDeck[random.randint(0, len(onDeck))-1]) #add process with random category and exec time
  runQueue.sort(key=lambda x: x.execTime,reverse=True)
  #sort the runQueue list after processes are added


#Run each process in order
#Until the list is empty
while len(runQueue) > 0:  
  #POP the next process object off list
  #cP = currentProgram
  cP = runQueue.pop()
  #Keep running process for execTime
  while cP.programCounter < cP.execTime:
    cP.run()
cP.showStats()





