import os
import pdb
import copy


if os.path.exists("output.txt"):
  os.remove("output.txt")


f2=open("output.txt","a+")
def main():
    MinimaxSPLA()
class MinimaxSPLA:

    def validate(self):
        self.lahsa_valid={}
        self.spla_valid={}
        self.lahsa_valid_list=[]
        self.spla_valid_list=[]
        self.lahsa_spla_common={}
        self.chosen_moves=[]
        for x in self.T3_final:
            if (x[5]=='F'):
                if (int(x[6:9])>17):
                    if(x[9]=='N'):
                        key=x[:5]
                        self.lahsa_valid[key]=self.ud_val[key]#WILL IT REFER TO SAME ObjECT??
                        self.lahsa_valid_list.append(x[:5])
        for x in self.T3_final:                   #2 loops ineff
            if(x[10:13]=='NYY'):
                key=x[:5]

                self.spla_valid[key]=self.ud_val[key]
                self.spla_valid_list.append(x[:5])#list of valid keys

       
        spla_valid_set=set(self.spla_valid)
        lahsa_valid_set=set(self.lahsa_valid)
        for key in spla_valid_set.intersection(lahsa_valid_set):
            self.lahsa_spla_common[key]=self.spla_valid[key]
        # self.lahsa_spla_common=list(set(self.lahsa_valid) & set(self.spla_valid))#common between both lists
       
        return

    def calculate_capacity(self,line,total_capacity):

        cap=line[13:]#.count('1')
        i=1
        new_cap={}

        for x in cap:
            # print total_capacity[i]
            if x=='1':
                new_cap[i]=total_capacity[i]-1
            else:
                new_cap[i]=total_capacity[i]
            i=i+1
        

        return new_cap


    def __init__(self):
        #print "FINAL"
        self.lahsa=[]
        self.spla=[]
        total=[]
        T1=[]
        T2=[]
        self.T3=[]
        days=[]
        uid=[]
        self.ud_dict={}
        self.ud_val={}
        self.lahsa_spla_cap={}
        self.lahsa_score=0
        self.T3_final=[]#list of inputs with lahsa and spla previous choices removed

        with open("input.txt","r") as f1:
            line=f1.readline()
            line=line.rstrip()
            b=int(line)
            print "b=",b#lahsa beds

            line=next(f1)
            line=line.rstrip()
            p=int(line)
            print "p=",p#spla spots

            line=next(f1)
            line=line.rstrip()
            L=int(line)
            print "L=",L

            cnt=0
            while(cnt!=L):
                line=next(f1)
                line=line.rstrip()
                T1.append(line)
                # self.calculate_capacity(line)
                cnt+=1
            # lahsa = [map(int, x) for x in T1]
            print T1

            line=next(f1)
            line=line.rstrip()
            S=int(line)
            print "S=",S

            cnt=0
            while(cnt!=S):
                line=next(f1)
                line=line.rstrip()
                T2.append(line)
                # self.calculate_capacity(line)
                cnt+=1
            # lahsa = [map(int, x) for x in T1]
           

            line=next(f1)
            line=line.rstrip()
            T=int(line)
           

            cnt=0
            while(cnt!=T):
                line=next(f1)
                line=line.rstrip()
                self.T3.append(line)
                cnt+=1
            # lahsa = [map(int, x) for x in T1]
           
        self.lahsa = map(int,T1)
        self.spla = map(int,T2)
        # total = [map(int, x) for x in T3]

        lahsa_cap_dict={}
        spla_cap_dict={}
        i=1

        while i<8:
            lahsa_cap_dict[i]=b
            spla_cap_dict[i]=p
            i=i+1

        

        for x in self.T3:#spliting the string to get the days schedule
            d=x[13:]
            days.append(d)

        for x in self.T3:#spliting the string to get the days schedule
            d=x[:5]
            uid.append(d)

            if (d in T1):

                lahsa_cap_dict=self.calculate_capacity(x,lahsa_cap_dict)
            if (d in T2):
                spla_cap_dict=self.calculate_capacity(x,spla_cap_dict)

        # print ("!!CAPACITIES UPDATED:lahsa,spla",lahsa_cap_dict,spla_cap_dict)

        uid_T1=[item for item in uid if item not in T1 ]#removing items already chosen
        uid_final=[item for item in uid_T1 if item not in T2]#elements remaining in list
        #remains=[item for item in T3 if item not in list2]]]

        # T3_final=[item for item in uid_final if item]
        for x in uid_final:
            for y in self.T3:
                if x==y[:5]:
                    self.T3_final.append(y)


        self.ud_dict=dict(zip(uid,days))
        if (len(T1) or len(T2)) >0:
            print "hey"
            #del_occurred()

        for key, freq in self.ud_dict.iteritems():#1100 into nos. ie 2
            for x in uid_final:
                if x!=key:
                    self.ud_val[key]=freq.count('1')

        # ud_val = {k: v for k, v in ud_dict.iteritems() if k not in uid_final}

        #validate the input into spla_valid and lahsa_valid/common to both
        self.validate()
        if(len(self.spla_valid)==0):
            f2.write('0')

        # l_s_uid=[]
        # for x in self.lahsa_spla_common:#spliting the string to get the uid
        #     d=x[:5]
        #     l_s_uid.append(d)
        #
        # for key, freq in self.ud_val.iteritems():#getting the capacities of common lahsa and spla
        #     for x in l_s_uid:
        #         if x==key:
        #             self.lahsa_spla_cap[key]=self.ud_val[key]





        dup_spla=self.spla
        sup_lahsa=self.lahsa
       
        self.length_common=len(self.lahsa_spla_cap)
        
        spla_valid_remain=copy.deepcopy(self.spla_valid)
        lahsa_valid_remain=copy.deepcopy(self.lahsa_valid)

        self.path={}

        answer=self.Minimax(spla_valid_remain,lahsa_valid_remain,lahsa_cap_dict,spla_cap_dict)
        print "A=",answer

        
        f2.write(answer)
        self.spla_count=0
        print "---end---"

    def update_cap(self,lahsa_cap,spla_cap,current, state):#state=spla, salse for lahsa

        curr_cap=self.ud_dict[current]
        new_lahsa_cap=copy.deepcopy(lahsa_cap)
        new_spla_cap=copy.deepcopy(spla_cap)
        if(state=='spla'):
            i=1
            for letter in curr_cap:
                new_spla_cap[i]=new_spla_cap[i]-int(letter)#for 1 or 0 it subtracts from current capacity.
                i=i+1
            # new_lahsa_cap=lahsa_cap
        else:
            i=1
            for letter in curr_cap:
                new_lahsa_cap[i]=new_lahsa_cap[i]-int(letter)#for 1 or 0 it subtracts from current capacity.
                i=i+1

            # new_spla_cap=spla_cap

        return new_lahsa_cap,new_spla_cap

    def valid_check(self,valid_remain,cap):
        valid_cap_list=copy.deepcopy(valid_remain)

        for x in valid_remain.keys():
            i=1

            for letter in self.ud_dict[x]:
                if letter=='1':
                    cap_check=cap[i]-1

                    if (cap_check<0):
                        del valid_cap_list[x]
                        break
                i=i+1                           

        return valid_cap_list




    def Minimax(self,spla_valid_remain,lahsa_valid_remain,b,p):

           # base case : targetDepth reached ie common ones are done. or is the base case that all applicants are chosen
          
           lahsa_cap=copy.deepcopy(b)
           spla_cap=copy.deepcopy(p)

           best_score=float('-inf')
           print "Minimax"
           
           spla_valid_remain_copy=copy.deepcopy(spla_valid_remain)
           lahsa_valid_remain_copy=copy.deepcopy(lahsa_valid_remain)

           spla_cap_valid={}
           spla_cap_valid=self.valid_check(spla_valid_remain,spla_cap)
           # pdb.set_trace()#debug
           
           spla_key = spla_valid_remain.keys()
           for key in spla_key:#going over all elements in spla remains
               
               self.spla_count=0
               splacopy = copy.deepcopy(spla_valid_remain)
               lahsacopy = copy.deepcopy(lahsa_valid_remain)
               

               new_lahsa_cap,new_spla_cap=self.update_cap(lahsa_cap,spla_cap,key,'spla')

               # if (new_spla_cap<0):
               #     continue

               print ("chosen, lahsa and spla_cap:",key,new_lahsa_cap,new_spla_cap)
               print("*************************************************")
               t_score=self.minplay(key,splacopy,lahsacopy,new_lahsa_cap,new_spla_cap,'lahsa')
               

               score=t_score+self.ud_val[key]
               print "score_now=",score
               if(score==best_score):#same score, choose smaller one
                   if (key<best_move):
                       best_move=key
               if (score>best_score):
                   best_move=key
                   best_score=score
               print("*************************************************")

               print "chosen_score=",score
           print "chosen_max_val=", best_score
           self.path['chosen']=best_move
         

           return best_move


    def minplay(self,current,spla_valid_remain,lahsa_valid_remain,lahsa_cap,spla_cap,state):
        
        spla_count=0


        lahsa_valid_remain=self.valid_check(lahsa_valid_remain,lahsa_cap)
        

        if(current in lahsa_valid_remain.keys()):
            del lahsa_valid_remain[current]

        if(current in spla_valid_remain.keys()):
            del spla_valid_remain[current]    

        

        if (len(lahsa_valid_remain)==0):

            if(len(spla_valid_remain)==0):#all applicants over
                
                score=0
                return score
            
            #base case for when spla ones are remaining
            else:
                for k in spla_valid_remain.keys():
                     
                         spla_count=spla_count+self.spla_valid[k]
                         new_lahsa_cap,new_spla_cap=self.update_cap(lahsa_cap,spla_cap,k,'spla')
                         spla_valid_remain=self.valid_check(spla_valid_remain,spla_cap)
                         if(len(spla_valid_remain)==0):
                             break
                         self.path[current]=k
               

                return spla_count
        best_score= float('inf')

        children={}
        

        for x,freq in lahsa_valid_remain.iteritems():
            
            lhr_local=copy.deepcopy(lahsa_valid_remain)
            spla_local=copy.deepcopy(spla_valid_remain)

            new_lahsa_cap,new_spla_cap=self.update_cap(lahsa_cap,spla_cap,x,state)

            

            score=self.maxplay(x,spla_local,children,new_lahsa_cap,new_spla_cap,'spla')
           

            if(score==best_score):#same score, choose smaller one
                if (x<best_move):
                    best_move=x

            if (score<best_score):
                best_move=x
                best_score=score
            

        self.path[current]=best_move
        return best_score

    def maxplay(self,current,spla_valid_remain,lahsa_valid_remain,lahsa_cap,spla_cap,state):
        
        spla_count=0

    
        spla_valid_remain=self.valid_check(spla_valid_remain,spla_cap)
        
        #none of the remaining fit the capacity
        if(len(spla_valid_remain)==0):#all applicants over
           
            score=0
            return score

        if(current in lahsa_valid_remain.keys()):
            del lahsa_valid_remain[current]#delete the current element if in lahsa's list
        if(current in spla_valid_remain.keys()):
            del spla_valid_remain[current]

        if (len(lahsa_valid_remain)==0):#if nothing remains in lahsa to pick

            if(len(spla_valid_remain)==0):#all applicants over

                
                score=0
                return score
            
            #base case for when spla ones are remaining
            else:
                count = 0
                for k in spla_valid_remain.keys():

                     # if (k not in lahsa_valid_remain.keys()):
                         #spla_count=spla_count+self.spla_valid[k]

                         count += self.spla_valid[k]

                         self.path[current]=k
             

                return count
        best_score= float('-inf')
        children={}
        
        lhr={}
        

        for x,freq in spla_valid_remain.iteritems():

            lhr_local=copy.deepcopy(lahsa_valid_remain)
            spla_local=copy.deepcopy(spla_valid_remain)

            new_lahsa_cap,new_spla_cap=self.update_cap(lahsa_cap,spla_cap,x,state)

            t_score=self.minplay(x,spla_local,lhr_local,new_lahsa_cap,new_spla_cap,'lahsa')

            score=t_score+freq#check this problematic

            #score=score+scoresofar but only spla\
            # tscore=score+self.ud_val[x]
            if(score==best_score):#same sacore, choose smaller one
                if (x<best_move):
                    best_move=x

            if (score>best_score):
                best_move=x
                best_score=score
            

        self.path[current]=best_move
        return best_score






main()

# f1.close()
f2.close()
