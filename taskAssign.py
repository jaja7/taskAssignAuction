'''
使用市场拍卖算法实现任务分配
Luo L. Distributed Algorithm Design for Constrained Multi-robot Task Assignment[J]. 2014.
'''
def getCostMat():
    return [[10, 19, 8, 15], [10, 18, 7, 17], [13, 16, 9, 14], [12, 19, 8, 18]]


class Task:
    def __init__(self, idx):
        self.id = idx
        self.worker = None  # 是否被分配
        self.costChange = 0  # 易标代价


class Worker:
    def __init__(self, idx, rawCostList):
        self.id = idx
        self.loaded = None  # 是否选中某个task
        self.rawCostList = rawCostList
        self.priceList = []
        self.assignFailed = False

    def getBestTask(self, taskList, maxCost):
        '''
        todo ...任务少的时候会出现死循环
        '''
        self.priceList = []
        for idx, task in enumerate(taskList):
            self.priceList.append(self.rawCostList[idx] + task.costChange)

        tmp_list = sorted(self.priceList)
        # 最低代价值，及其序号
        minPrice = tmp_list[0]
        minIdx = self.priceList.index(minPrice)
        secPrice = tmp_list[1]  # 次低代价值
        costDiff = secPrice - minPrice

        if minPrice > maxCost: # 如果代价矩阵
            return [None, None]
        else:
            return [taskList[minIdx], costDiff]


class WorkerGroup:
    def __init__(self, workerList):
        self.workerList = workerList
        self.numWork = len(workerList)
        self.pointer = 0

    def getWorker(self):
        '''
        找到一个对当前分配不满意的worker，不满意需要满足两个条件：当前闲置，且有空闲任务
        '''
        for worker in self.workerList:
            if worker.loaded is not None or worker.assignFailed is True:
                continue
            else:
                return worker

    def showAssign(self):
        for worker in self.workerList:
            print("worker[%d] --> task[%d]" % (worker.id, worker.loaded.id))

def assign(costMat, maxCost):
    numWorker = len(costMat)
    numTask = len(costMat[0])
    workerList = []
    taskList = []
    for i in range(numWorker):
        costList = costMat[i]
        objWorker = Worker(i+1, costList)
        workerList.append(objWorker)
    for i in range(numTask):
        objTask = Task(i+1)
        taskList.append(objTask)

    workerGroup = WorkerGroup(workerList)

    worker = workerGroup.getWorker()
    while worker is not None:
        print('get new worder:', worker.id)
        bestTask, costDiff = worker.getBestTask(taskList, maxCost)
        if bestTask is None:
            worker.assignFailed = True
        else:
            print('\t find best task:', bestTask.id)
            if bestTask.worker is not None:
                # 先解除原来的分配
                bestTask.worker.loaded = None

            # 建立新的配对
            bestTask.worker = worker
            bestTask.costChange += (costDiff + 0.1)  #需要增加一个小数，防止某些情况下的死循环
            worker.loaded = bestTask

        worker = workerGroup.getWorker()  # 更新worker

    workerGroup.showAssign()


if __name__ == '__main__':
    costMat = getCostMat()

    # 获取代价矩阵中的最大值
    maxRowList = []
    for costList in costMat:
        maxRowList.append(max(costList))
    maxCost = max(maxRowList)

    assign(costMat, maxCost)
