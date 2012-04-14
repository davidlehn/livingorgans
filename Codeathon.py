class Graph:
    def __init__(self):
        self.list = [];
    def add(self, dbt, rbt):
        self.list.append(Pair(dbt,rbt))
        
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
    def __init__(self, DBT,RBT):
        self.Donor_Type=DBT
        self.Recipient_Type=RBT
        self.otherPairs=[]
        self.visit = False
        self.value = 0
