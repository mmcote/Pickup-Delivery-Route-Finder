class MinHeap:
   def __init__(self):
      '''Nodes are key-value pairs, stored in an array.
      The first element of the pair is the key,
      the second is the value.
      '''
      self._array = []
      
   def add(self,key,value):
      self._array.append((key,value))
      self.fix_heap_up(len(self._array)-1)
      
   def fix_heap_up(self,i):
      if self.isroot(i):
         return
      j = self.parent(i)
      if self._array[i][0]<self._array[j][0]:
         self.swap(i,j)
         self.fix_heap_up(j)
         
   def isroot(self,i):
      return i==0
      
   def parent(self,i):
      return (i-1)//2
      
   def swap(self,i,j):
      self._array[i],self._array[j] = self._array[j],self._array[i]
      
   def pop_min(self):
      r = self._array[0]
      l = self._array[-1]
      del self._array[-1]
      if len(self._array)>0:
         self._array[0] = l
         self.fix_heap_down(0)
      return r
         
   def fix_heap_down(self,i):
      if self.isleaf(i):
         return
      j = self.index_of_min_child(i)
      if self._array[i][0]>self._array[j][0]:
         self.swap(i,j)
         self.fix_heap_down(j)
      
   def index_of_min_child(self,i):
      l = self.lchild(i)
      r = self.rchild(i)
      if r<len(self._array):
         if self._array[l][0]<self._array[r][0]:
            return l
         else:
            return r
      return l
   
   def lchild(self,i):
      return 2*i+1
      
   def rchild(self,i):
      return 2*i+2
      
   def isleaf(self,i):
      return self.lchild(i)>=len(self._array)
   
   def isempty(self):
       return len(self._array)==0
      
