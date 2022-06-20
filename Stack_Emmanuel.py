class LinkedList:
  head=None

class Node:
  value=None
  nextNode=None

def push(S,element):
  NodeN=Node()
  NodeN.value=element
  NodeN.nextNode=S.head
  S.head=NodeN

def pop(S):
  CurrentNode=S.head
  PoppedValue=CurrentNode.value
  CurrentNode=CurrentNode.nextNode
  S.head=CurrentNode
  return(PoppedValue)
