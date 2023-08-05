#  Copyright (C)  2021 Rage Uday Kiran
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#      Copyright (C)  2021 Rage Uday Kiran

from PAMI.relativeFrequentPatterns.basic import abstract as _ab


class _Node:
    """
        A class used to represent the node of frequentPatterntree

    Attributes:
    ----------
        itemId: int
            storing item of a node
        counter: int
            To maintain the support of node
        parent: node
            To maintain the parent of every node
        child: list
            To maintain the children of node
        nodeLink : node
            Points to the node with same itemId

    Methods:
    -------

        getChild(itemName)
            returns the node with same itemName from frequentPatterntree
    """

    def __init__(self):
        self.itemId = -1
        self.counter = 1
        self.parent = None
        self.child = []
        self.nodeLink = None

    def getChild(self, itemName):
        """ Retrieving the child from the tree

            :param itemName: name of the child
            :type itemName: list
            :return: returns the node with same itemName from frequentPatternTree
            :rtype: None or Node

        """
        for i in self.child:
            if i.itemId == itemName:
                return i
        return None


class _Tree:
    """
        A class used to represent the frequentPatternGrowth tree structure

    Attributes:
    ----------
        headerList : list
            storing the list of items in tree sorted in ascending of their supports
        mapItemNodes : dictionary
            storing the nodes with same item name
        mapItemLastNodes : dictionary
            representing the map that indicates the last node for each item
        root : Node
            representing the root Node in a tree

    Methods:
    -------
        createHeaderList(items,minSup)
            takes items only which are greater than minSup and sort the items in ascending order
        addTransaction(transaction)
            creating transaction as a branch in frequentPatternTree
        fixNodeLinks(item,newNode)
            To create the link for nodes with same item
        printTree(Node)
            gives the details of node in frequentPatternGrowth tree
        addPrefixPath(prefix,port,minSup)
           It takes the items in prefix pattern whose support is >=minSup and construct a subtree
    """

    def __init__(self):
        self.headerList = []
        self.mapItemNodes = {}
        self.mapItemLastNodes = {}
        self.root = _Node()

    def addTransaction(self, transaction):
        """adding transaction into tree

        :param transaction: it represents the one transactions in database
        :type transaction: list
        """

        # This method taken a transaction as input and returns the tree
        current = self.root
        for i in transaction:
            child = current.getChild(i)
            if not child:
                newNode = _Node()
                newNode.itemId = i
                newNode.parent = current
                current.child.append(newNode)
                self.fixNodeLinks(i, newNode)
                current = newNode
            else:
                child.counter += 1
                current = child

    def fixNodeLinks(self, item, newNode):
        """Fixing node link for the newNode that inserted into frequentPatternTree

        :param item: it represents the item of newNode
        :type item: int
        :param newNode: it represents the newNode that inserted in frequentPatternTree
        :type newNode: Node

        """
        if item in self.mapItemLastNodes.keys():
            lastNode = self.mapItemLastNodes[item]
            lastNode.nodeLink = newNode
        self.mapItemLastNodes[item] = newNode
        if item not in self.mapItemNodes.keys():
            self.mapItemNodes[item] = newNode

    def printTree(self, root):
        """Print the details of Node in frequentPatternTree

        :param root: it represents the Node in frequentPatternTree
        :type root: Node

        """

        # this method is used print the details of tree
        if not root.child:
            return
        else:
            for i in root.child:
                print(i.itemId, i.counter, i.parent.itemId)
                self.printTree(i)

    def createHeaderList(self, __mapSupport, minSup):
        """To create the headerList

        :param __mapSupport: it represents the items with their supports
        :type __mapSupport: dictionary
        :param minSup: it represents the minSup
        :param minSup: float
        """
        # the frequentPatternTree always maintains the header table to start the mining from leaf nodes
        t1 = []
        for x, y in __mapSupport.items():
            if y >= minSup:
                t1.append(x)
        __itemSetBuffer = [k for k, v in sorted(__mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.headerList = [i for i in t1 if i in __itemSetBuffer]

    def addPrefixPath(self, prefix, __mapSupportBeta, minSup):
        """To construct the conditional tree with prefix paths of a node in frequentPatternTree

        :param prefix: it represents the prefix items of a Node
        :type prefix: list
        :param __mapSupportBeta: it represents the items with their supports
        :param __mapSupportBeta: dictionary
        :param minSup: to check the item meets with minSup
        :param minSup: float
        """
        # this method is used to add prefix paths in conditional trees of frequentPatternTree
        pathCount = prefix[0].counter
        current = self.root
        prefix.reverse()
        for i in range(0, len(prefix) - 1):
            pathItem = prefix[i]
            if __mapSupportBeta.get(pathItem.itemId) >= minSup:
                child = current.getChild(pathItem.itemId)
                if not child:
                    newNode = _Node()
                    newNode.itemId = pathItem.itemId
                    newNode.parent = current
                    newNode.counter = pathCount
                    current.child.append(newNode)
                    current = newNode
                    self.fixNodeLinks(pathItem.itemId, newNode)
                else:
                    child.counter += pathCount
                    current = child


class RSFPGrowth(_ab._frequentPatterns):
    """
        Algorithm to find all items with relative support from given dataset

    Reference:
    --------
        'Towards Efficient Discovery of Frequent Patterns with Relative Support' R. Uday Kiran and
               Masaru Kitsuregawa, http://comad.in/comad2012/pdf/kiran.pdf

    Attributes:
    ----------
        iFile : file
            Name of the Input file to mine complete set of frequent patterns
        oFile : file
            Name of the output file to store complete set of frequent patterns
        __memoryUSS : float
            To store the total amount of USS memory consumed by the program
        __memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        __startTime:float
            To record the start time of the mining process
        __endTime:float
            To record the completion time of the mining process
        minSup : float
            The user given minSup
        Database : list
            To store the transactions of a database in list
        __mapSupport : Dictionary
            To maintain the information of item and their frequency
        __lno : int
            it represents the total no of transactions
        tree : class
            it represents the Tree class
        __itemSetCount : int
            it represents the total no of patterns
        __finalPatterns : dict
            it represents to store the patterns
        __itemSetBuffer : list
            it represents the store the items in mining
        __maxPatternLength : int
           it represents the constraint for pattern length

    Methods:
    -------
        startMine()
            Mining process will start from here
        getFrequentPatterns()
            Complete set of patterns will be retrieved with this function
        savePatterns(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getmemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        check(line)
            To check the delimiter used in the user input file
        creatingItemSets(fileName)
            Scans the dataset or dataframes and stores in list format
        frequentOneItem()
            Extracts the one-frequent patterns from transactions
        saveAllCombination(tempBuffer,s,position,prefix,prefixLength)
            Forms all the combinations between prefix and tempBuffer lists with support(s)
        saveItemSet(pattern,support)
            Stores all the frequent patterns with their respective support
        frequentPatternGrowthGenerate(frequentPatternTree,prefix,port)
            Mining the frequent patterns by forming conditional frequentPatternTrees to particular prefix item.
            __mapSupport represents the 1-length items with their respective support

    Executing the code on terminal:
    -------
        Format:
        -------
            python3 RSFPGrowth.py <inputFile> <outputFile> <minSup> <__minRatio>

        Examples:
        ---------
            python3 RSFPGrowth.py sampleDB.txt patterns.txt 0.23 0.2  (minSup will be considered in percentage of database transactions)

            python3 RSFPGrowth.py sampleDB.txt patterns.txt 3   0.2  (minSup will be considered in support count or frequency)


    Sample run of the importing code:
    -----------
        from PAMI.frequentPatternUsingOtherMeasures import RSFPGrowth as alg

        obj = alg.RSFPGrowth(iFile, minSup, __minRatio)

        obj.startMine()

        frequentPatterns = obj.getPatterns()

        print("Total number of Frequent Patterns:", len(frequentPatterns))

        obj.savePatterns(oFile)

        Df = obj.getPatternsAsDataFrame()

        memUSS = obj.getmemoryUSS()

        print("Total Memory in USS:", memUSS)

        memRSS = obj.getMemoryRSS()

        print("Total Memory in RSS", memRSS)

        run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)

    Credits:
    -------
        The complete program was written by Sai Chitra.B  under the supervision of Professor Rage Uday Kiran.

        """

    __startTime = float()
    __endTime = float()
    _minSup = str()
    _minRatio = float()
    __finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    __memoryUSS = float()
    __memoryRSS = float()
    __Database = []
    __mapSupport = {}
    __lno = 0
    __tree = _Tree()
    __itemSetBuffer = None
    __fpNodeTempBuffer = []
    __itemSetCount = 0
    __maxPatternLength = 1000

    def __init__(self, iFile, __minSup, __minRatio, sep='\t'):
        super().__init__(iFile, __minSup, __minRatio, sep)
        self.__finalPatterns = {}

    def __creatingItemSets(self):
        """
            Storing the complete transactions of the __Database/input file in a __Database variable


            """
        self.__Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.__Database = self._iFile['Transactions'].tolist()
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def __frequentOneItem(self):
        """Generating One frequent items sets

        """
        self.__mapSupport = {}
        for i in self.__Database:
            for j in i:
                if j not in self.__mapSupport:
                    self.__mapSupport[j] = 1
                else:
                    self.__mapSupport[j] += 1

    def __saveItemSet(self, prefix, prefixLength, support, ratio):
        """To save the frequent patterns mined form frequentPatternTree

        :param prefix: the frequent pattern
        :type prefix: list
        :param prefixLength: the length of a frequent pattern
        :type prefixLength: int
        :param support: the support of a pattern
        :type support:  int
        """

        sample = []
        for i in range(prefixLength):
            sample.append(prefix[i])
        self.__itemSetCount += 1
        self.__finalPatterns[tuple(sample)] = str(support) + " : " + str(ratio)

    def __saveAllCombinations(self, tempBuffer, s, position, prefix, prefixLength):
        """Generating all the combinations for items in single branch in frequentPatternTree

        :param tempBuffer: items in a list
        :type tempBuffer: list
        :param s: support at leaf node of a branch
        :param position: the length of a tempBuffer
        :type position: int
        :param prefix: it represents the list of leaf node
        :type prefix: list
        :param prefixLength: the length of prefix
        :type prefixLength: int

        """
        max1 = 1 << position
        for i in range(1, max1):
            newPrefixLength = prefixLength
            for j in range(position):
                isSet = i & (1 << j)
                if isSet > 0:
                    prefix.insert(newPrefixLength, tempBuffer[j].itemId)
                    newPrefixLength += 1
            ratio = s / self.__mapSupport[self.__getMinItem(prefix, newPrefixLength)]
            if ratio >= self._minRatio:
                self.__saveItemSet(prefix, newPrefixLength, s, ratio)

    def __frequentPatternGrowthGenerate(self, frequentPatternTree, prefix, prefixLength, __mapSupport, minConf):
        """Mining the fp tree

        :param frequentPatternTree: it represents the frequentPatternTree
        :type frequentPatternTree: class Tree
        :param prefix: it represents a empty list and store the patterns that are mined
        :type prefix: list
        :param param prefixLength: the length of prefix
        :type prefixLength: int
        :param __mapSupport : it represents the support of item
        :type __mapSupport : dictionary
        """
        singlePath = True
        position = 0
        s = 0
        if len(frequentPatternTree.root.child) > 1:
            singlePath = False
        else:
            currentNode = frequentPatternTree.root.child[0]
            while True:
                if len(currentNode.child) > 1:
                    singlePath = False
                    break
                self.__fpNodeTempBuffer.insert(position, currentNode)
                s = currentNode.counter
                position += 1
                if len(currentNode.child) == 0:
                    break
                currentNode = currentNode.child[0]
        if singlePath is True:
            self.__saveAllCombinations(self.__fpNodeTempBuffer, s, position, prefix, prefixLength)
        else:
            for i in reversed(frequentPatternTree.headerList):
                item = i
                support = __mapSupport[i]
                CminSup = max(self._minSup, support * self._minRatio)
                betaSupport = support
                prefix.insert(prefixLength, item)
                max1 = self.__getMinItem(prefix, prefixLength)
                if self.__mapSupport[max1] > self.__mapSupport[item]:
                    max1 = item
                ratio = support / self.__mapSupport[max1]
                if ratio >= self._minRatio:
                    self.__saveItemSet(prefix, prefixLength + 1, betaSupport, ratio)
                if prefixLength + 1 < self.__maxPatternLength:
                    prefixPaths = []
                    path = frequentPatternTree.mapItemNodes.get(item)
                    __mapSupportBeta = {}
                    while path is not None:
                        if path.parent.itemId != -1:
                            prefixPath = [path]
                            pathCount = path.counter
                            parent1 = path.parent
                            if __mapSupport.get(parent1.itemId) >= CminSup:
                                while parent1.itemId != -1:
                                    mins = CminSup
                                    if __mapSupport.get(parent1.itemId) >= mins:
                                        prefixPath.append(parent1)
                                        if __mapSupportBeta.get(parent1.itemId) is None:
                                            __mapSupportBeta[parent1.itemId] = pathCount
                                        else:
                                            __mapSupportBeta[parent1.itemId] = __mapSupportBeta[
                                                                                   parent1.itemId] + pathCount
                                        parent1 = parent1.parent
                                    else:
                                        break
                                prefixPaths.append(prefixPath)
                        path = path.nodeLink
                    __treeBeta = _Tree()
                    for k in prefixPaths:
                        __treeBeta.addPrefixPath(k, __mapSupportBeta, self._minSup)
                    if len(__treeBeta.root.child) > 0:
                        __treeBeta.createHeaderList(__mapSupportBeta, self._minSup)
                        self.__frequentPatternGrowthGenerate(__treeBeta, prefix, prefixLength + 1, __mapSupportBeta,
                                                           minConf)

    def __convert(self, value):
        """
        to convert the type of user specified __minSup value
        :param value: user specified __minSup value
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self.__Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self.__Database) * value)
            else:
                value = int(value)
        return value

    def startMine(self):
        """
            main program to start the operation
        """

        self.__startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self.__creatingItemSets()
        self._minSup = self.__convert(self._minSup)
        self._minRatio = float(self._minRatio)
        self.__frequentOneItem()
        self.__finalPatterns = {}
        self.__mapSupport = {k: v for k, v in self.__mapSupport.items() if v >= self._minSup}
        print(len(self.__mapSupport), len(self.__finalPatterns), len(self.__Database))
        __itemSetBuffer = [k for k, v in sorted(self.__mapSupport.items(), key=lambda x: x[1], reverse=True)]
        for i in self.__Database:
            transaction = []
            for j in i:
                if j in __itemSetBuffer:
                    transaction.append(j)
            transaction.sort(key=lambda val: self.__mapSupport[val], reverse=True)
            self.__tree.addTransaction(transaction)
        self.__tree.createHeaderList(self.__mapSupport, self._minSup)
        if len(self.__tree.headerList) > 0:
            self.__itemSetBuffer = []
            self.__frequentPatternGrowthGenerate(self.__tree, self.__itemSetBuffer, 0, self.__mapSupport, self._minRatio)
        print("Relative support frequent patterns were generated successfully using RSFPGrowth algorithm")
        self.__endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self.__memoryRSS = float()
        self.__memoryUSS = float()
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryRSS

    def __getMinItem(self, prefix, prefixLength):
        """
            returns the minItem from prefix
        """
        minItem = prefix[0]
        for i in range(prefixLength):
            if self.__mapSupport[minItem] > self.__mapSupport[prefix[i]]:
                minItem = prefix[i]
        return minItem

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__endTime - self.__startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self.__finalPatterns.items():
            data.append([a, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def savePatterns(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self.__oFile = outFile
        writer = open(self.__oFile, 'w+')
        for x, y in self.__finalPatterns.items():
            pattern = str()
            for i in x:
                pattern = pattern + i + " "
            s1 = str(pattern) + ": " + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        res = dict()
        for x, y in self.__finalPatterns.items():
            pattern = str()
            for i in x:
                pattern = pattern + i + " "
            s1 = str(y)
            res[pattern] = s1

        return res


if __name__ == "__main__":
    ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            ap = RSFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            ap = RSFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        ap.startMine()
        Patterns = ap.getPatterns()
        print("Total number of Frequent Patterns:", len(Patterns))
        ap.savePatterns(_ab._sys.argv[2])
        memUSS = ap.getMemoryUSS()
        print("Total Memory in USS:", memUSS)
        memRSS = ap.getMemoryRSS()
        print("Total Memory in RSS", memRSS)
        run = ap.getRuntime()
        print("Total ExecutionTime in ms:", run)
    else:
        l = [0.006, 0.007, 0.008, 0.009, 0.01]
        for i in l:
            ap = RSFPGrowth(
                'https://www.u-aizu.ac.jp/~udayrage/datasets/transactionalDatabases/transactional_T10I4D100K.csv',
                0.008, 0.4)
            ap.startMine()
            correlatedPatterns = ap.getPatterns()
            print("Total number of correlated-Frequent Patterns:", len(correlatedPatterns))
            ap.savePatterns('/Users/Likhitha/Downloads/output')
            memUSS = ap.getMemoryUSS()
            print("Total Memory in USS:", memUSS)
            memRSS = ap.getMemoryRSS()
            print("Total Memory in RSS", memRSS)
            run = ap.getRuntime()
            print("Total ExecutionTime in seconds:", run)
        print("Error! The number of input parameters do not match the total number of parameters provided")
