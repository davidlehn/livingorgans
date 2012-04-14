class Graph:
    def __init__(self):
        self.list = [];

    def add(self, id, dbt, rbt):
        pair = Pair(id, dbt,rbt)
        self.list.append(pair)
        return pair
        
    def findEdges(self):
        for thing in self.list:
            thing.otherPairs = []
        for Potential_Donor in self.list:
            for Potential_Recipient in self.list:
                if (Potential_Donor != Potential_Recipient):
                        
                    if Potential_Donor.Donor_Type == "A" and (Potential_Recipient.Recipient_Type == "A" or Potential_Recipient.Recipient_Type == "B"):
                        Potential_Donor.otherPairs.append(Potential_Recipient)

                    elif Potential_Donor.Donor_Type == "AB" and Potential_Recipient.Recipient_Type == "AB":
                        Potential_Donor.otherPairs.append(Potential_Recipient)
                        
                    elif Potential_Donor.Donor_Type == "O":
                        Potential_Donor.otherPairs.append(Potential_Recipient)
                    elif Potential_Donor.Donor_Type == "B" and (Potential_Recipient.Recipient_Type == "AB" or Potential_Recipient.Recipient_Type == "B"):
                        Potential_Donor.otherPairs.append(Potential_Recipient)

    def findCycle(self, start):
        for node in self.list:
            node.visit = False
            node.value = 0
        return self.startdfs(start,start)
    
    def startdfs (self, node,start):
        ans = []
        if node.Donor_Type == node.Recipient_Type:
            return [[node]]
        for firstEdge in node.otherPairs:
            for SecondEdge in firstEdge.otherPairs:  
                if SecondEdge == start:
                    ans.append([node,firstEdge])
                for ThirdEdge in SecondEdge.otherPairs:
                    if ThirdEdge ==start:
                        ans.append([node,firstEdge,SecondEdge])
        return ans

    def findAllCycles(self):
        for node in self.list:
            node.visit = False
            node.value = 0
        ans = []
        for node in self.list:
               temp = self.startalldfs(node,node)
               for a in temp:
                   ans.append(a)
        return ans
        
    def startalldfs (self, node,start):
        ans = []
        node.visit = True
        if node.Donor_Type == node.Recipient_Type:
            return [[node]]
        for firstEdge in node.otherPairs:
            if firstEdge.visit == True:
                continue
            for SecondEdge in firstEdge.otherPairs:
                if SecondEdge == start:
                    ans.append([node,firstEdge])
                if SecondEdge.visit == True:
                    continue
                for ThirdEdge in SecondEdge.otherPairs:
                    if ThirdEdge ==start:
                        ans.append([node,firstEdge,SecondEdge])
        return ans

            

    

#        max = []
#        for next  in node.otherPairs:
#            for backToStart in next.otherPairs:
#                if backToStart == start: 
#                    max.append([node,next])
#                    break
#                for reallyBackToStart in backToStart.otherPairs:
#                    if reallyBackToStart == start:
#                        max.append([node,next,backToStart])
#                        break
#        return max

class Pair:
    def __init__(self, id, DBT,RBT):
        self.Id=id
        self.Donor_Type=DBT
        self.Recipient_Type=RBT
        self.otherPairs=[]
        self.visit = False
        self.value = 0



def main():
    x = Graph()
    x.add('1','A','AB')
    x.add('2','A','O')
    x.add('3','AB','B')
    x.add('4','B','A')
    x.add('5','AB','A')
    x.add('6','B','O')
    x.add('7','B','B')
    x.add('8','O','O')
    x.findEdges()
    
    ans =x.findCycle(x.list[0])
    for a in ans:
      for b in a:
        print b.Donor_Type +"  "+b.Recipient_Type
      print ""
    print
    print
    ans = x.findAllCycles()
    for a in ans:
      for b in a:
        print b.Donor_Type +"  "+b.Recipient_Type
      print ""
    print
    print

if __name__ == "__main__":
    main()

