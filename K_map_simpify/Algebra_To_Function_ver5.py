import sys
import numpy as np

def Var_Scan(expr):
    var=[]
    for s in expr:
        if s != '+' and s!= '-' and s!='*' and s!= '(' and s!=')'and s!=' ':      
            if s not in var:
                var.append(s)
    
    return  var

def one_bit_check(a,b):
    count=0
    try:
        for i in range(len(a)):
            count+=abs(a[i]-b[i])
        if count ==1:
            return True
        else:
            return False
    except:
        if len(a) != len(b):
            print('Error : length of a is not equal to b')

def bool_expresion_transfer(expr):

    # temp = expr
    # for s in expr:
    # if s=='+':            
    expr = expr.replace('+',' or ')
    # if s=='-':            
    expr = expr.replace('-','not ')
    expr = expr.replace('*',' and ')
    # print(expr)
    return expr

def Is_Neighbor(stack,last_stack):
    for py in [p[1] for p in stack]:
        for ly in [lp[1] for lp in last_stack]:
            if py==ly:
                return True

    return False

def kana_fill_with(expr,bit_row,bit_col,var_list):


    Kana_map=[]

    for i in range(pow(2,NumRowVar)):
        row = []
        for j in range(pow(2,NumColVar)):
            row.append(0)
        Kana_map.append(row.copy())
    
    # print(Kana_map)
    stack= []
    last_stack = []
    track=[]
    print('bool expression')
    for i, bit_r in enumerate(bit_row):        

        for j, bit_c in enumerate(bit_col):
            bit_input = bit_r + bit_c

            #initial variable value
            temp_expr = expr
            for k in range(num_var):                                     
                temp_expr = temp_expr.replace(var_list[k], str(bit_input[k])) 

            #convert string  to code
            code1 = "(" + bool_expresion_transfer(temp_expr) +") == True"        

            # compute the bool output
            b = compile(code1,'','eval')

            print("code : ",code1)
            bool_value = eval(b)
         
            print('result',bool_value)

            Kana_map[i][j] = int(bool_value) 

            # if int(bool_value) == 1:   
            #     stack.append((i,j))

        # if len(stack)!=0:
        #     if len(last_stack)!=0 and Is_Neighbor(stack,last_stack):
        #         track[-1]= last_stack.copy() + stack.copy()
        #     else:            
        #         track.append(stack.copy())            

        #     last_stack = stack.copy()
        #     stack.clear()                

    return Kana_map#,track

def RS(i,j,stack,map,dflag):
    print()
    print("pair stack: ",stack)
    print("curent map")
    for ss in range(pow(2,NumRowVar)):
        print(map[ss][0:pow(2,NumColVar)]) 
    
    bound1 = pow(2,NumRowVar)
    bound2 = pow(2,NumColVar)

    print('flag',dflag)
    if i>=0 and j>=0 and i<=pow(2,NumRowVar)-1 and j <= pow(2,NumColVar)-1:
        if map[i][j]==1:
            
            if (i,j) not in stack:
                stack.append((i,j))

            map[i][j]=-1
            
        
            s, map = RS(i%bound1,(j+1)%bound2,stack,map,dflag)
            for temp in s:
                if temp not in stack and temp!=[]:                
                    stack.append(temp)
            dflag[0]=1
                
            # if dflag[1]!=1:
            s, map = RS((i+1)%bound1,j%bound2,stack,map,dflag)
            for temp in s:
                if temp not in stack and temp!=[]:                
                    stack.append(temp)
            dflag[1]=1

            # if dflag[2]!=1:
            s, map = RS(i%bound1,(j-1)%bound2,stack,map,dflag)
            for temp in s:
                if temp not in stack and temp!=[]:                
                    stack.append(temp)
            dflag[2]=1
            
        
            s, map = RS((i-1)%bound1,j%bound2,stack,map,dflag)
            for temp in s:
                if temp not in stack and temp!=[]:                
                    stack.append(temp)
            dflag[3]=1

            
    return stack,map

def bit_num_generate(n):

    bit_num = []

    init_bit =[0]*n

    bit_num.append(init_bit.copy())
    trace =[]

    while len(bit_num)!=pow(2,n):
        
        
        digit = n-1
        temp = bit_num[-1].copy()
        
        b=0
        for i in range(n):
            b += init_bit[i]
        
        if b!=n:
            init_bit[digit] += 1
        
        for j in range(n-1,0,-1):
            
            if init_bit[j] >=2:
                init_bit[j]=0
                init_bit[j-1]+=1

        # print('init',init_bit)
        # print('bit',bit_num)
        # print('trace',trace)
        # print()
        d=0
        for t in range(len(init_bit)):
            d+=abs(init_bit[t]-temp[t])
        # print(d)

        d1=0
        if len(trace)!=0:
            for k in range(len(trace)):
                d1=0
                for t in range(len(init_bit)):
                    d1+=abs(trace[k][t]-temp[t])
                if d1==1:
                    # print("k",k)
                    break
        # print(d1)

        if d1==1:
            # print("k",k)
            tempt = trace[k].copy()        
            trace.remove(tempt)
            trace.append(init_bit.copy())

            bit_num.append(tempt.copy())
            
        elif d==1:
            bit_num.append(init_bit.copy())
        else:        
            trace.append(init_bit.copy())
    return bit_num
    # print(bit_num_r)

def isPowOf2(a):
    print('num:',a,' ',end='')
    
    if a<2:
        if a==1:
            print('True')
            return True
        else:
            print("Error: there is no element in  line of region")
            
    else:
        while(a>=2):
            r = a % 2
            a = a/2
        
        print(a==1 and r==0)
    return (a==1 and r==0)

def divide_q(q,axis=0):#only one row / column
    num = len(q)

    # while(num!=0):
    i=0
    while(pow(2,i) <= num):
        i+=1
    max_cutsize = pow(2,i-1)

    print(q)

    q_list=[]

    temp =[]
    i = 0
    while(len(temp) < max_cutsize):      
        # print('slice:',slice)
        if q[i] not in temp:
            temp.append(q[i])
        # print(temp)

        if len(temp)>=2:
            if IsContinous(temp,x=int(not(axis))) == False:
                # print('F')
                temp.pop()
        i += 1
        i = i % len(q)

    q_list.append(temp.copy())

    temp.clear()

    i = len(q)-1
    while(len(temp) < max_cutsize):      
        # print('slice:',slice)
        if q[i] not in temp:
            temp.insert(0,q[i])

        if len(temp)>=2:
                if IsContinous(temp,x=int(not(axis))) == False:
                    # print('F')
                    del temp[0]
        i -= 1
        if i<0:
            i = len(q)


    q_list.append(temp.copy())
        

    print("divide",q_list)
    return q_list

def sort_list(sort_idx,temp_list):
    
    if type(sort_idx) != list:
        sort_idx = list(sort_idx)
    
    temp1 = []
    for i in sort_idx:
        temp1.append(temp_list[i])          

    return temp1.copy()

def sort_axis(tar_list,axis):
    
    a_list=[]
    for t in tar_list:
        a_list.append(t[axis])
    sort_idx = np.argsort(a_list)
    temp_list = sort_list(sort_idx,tar_list)
    
    return temp_list
    
def IsContinous(tar_list,x):
    
    if len(tar_list)==1:
        flag = 1
    else:
        x_list=[]
        if x==0:
            bound = pow(2,NumRowVar)
        else:
            bound = pow(2,NumColVar)

        for p in tar_list:
                x_list.append(p[x])
        
        for i in x_list:
            if (i-1) % bound in x_list or (i+1) % bound in x_list:
                flag = 1
            else:
                flag = 0
                break
      
    return bool(flag)

def rectangle_search4(s,axis):
    indx_list=[]
    element_count=[]
    line_set = []

    for p in s: 
                
        if p[axis] not in indx_list:
            indx_list.append(p[axis])
            element_count.append(1)

            line_set.append([p])
        else:
            idx = indx_list.index(p[axis])
            element_count[idx] += 1
            line_set[idx].append(p)

    #sort the indx list and element count list
    sort_idx=np.argsort(indx_list)

    indx_list = sort_list(sort_idx, indx_list)
    element_count = sort_list(sort_idx, element_count)
    line_set = sort_list(sort_idx, line_set)
    
    for i,l_set in enumerate( line_set):
        line_set[i] = sort_axis(l_set, axis = int (not (axis) )).copy()


    q_extend=[]
    q_list=[]
    q=[]
    c_trace=[]
    if len(indx_list)==1:

        if (isPowOf2(element_count[0])) == False:
            q_list = divide_q(line_set[0].copy(),axis)
            
            for qi in q_list:
                q_extend.append(qi.copy())
        else:
            q_extend.append(line_set[0].copy())       
    else:

        for i,count in enumerate(element_count):
    
            if count not in c_trace:
                c_trace.append(count)
                print(count)            
                                
                for j,set_l in enumerate(line_set):
                    
                    if element_count[j] >= count:
                        x = int(not(axis))
                        
                        if element_count[j] > count:
                            id_list = []
                            b_list = []
                            
                            cur_ini_idx = set_l[0][x]
                            for k,p in enumerate( line_set[i]):
                                id_list.append(p[x])

                                if len(b_list)<1:
                                    b_list.append(cur_ini_idx - id_list[0])
                                else:
                                    b_list.append( cur_ini_idx - id_list[-2]- id_list[-1] )

                            for k,id in enumerate(id_list):                            
                                temp_list.append(set_l[id+b_list[k]])
                        
                        elif element_count[j] == count:                        
                            sid = 0
                            eid = count
                            temp_list = set_l[sid:eid].copy()

                        
                        
                        flag = int( IsContinous( temp_list,x) ) 

                        print('flag:',flag)

                        if flag == 1:

                            if isPowOf2(count) ==False:
                                if q_list!=[]:
                                    temp_q_list = divide_q(temp_list.copy() ,axis)
                                    for t,temp_q in enumerate( temp_q_list ):
                                        q_list[t]+= temp_q.copy()
                                else:
                                    q_list = divide_q( temp_list.copy(),axis)
                            else:
                                q += temp_list.copy()

                        elif flag == 0 and q != [] or q_list!=[]:

                            if isPowOf2(count) ==False:
                                q_extend += q_list.copy()
                                q_list.clear()
                            else:
                                q_extend.append(q.copy())
                                q.clear()  

                    elif q != [] or q_list!=[]:
                            if isPowOf2(count) ==False:
                                q_extend += q_list.copy()
                                q_list.clear()
                            else:
                                q_extend.append(q.copy())
                                q.clear()   

                if q !=[] or q_list!=[]:
                    if isPowOf2(count) ==False:
                        q_extend += q_list.copy()
                        q_list.clear()
                    else:
                        q_extend.append(q.copy())
                        q.clear()   
                print(q_extend)
        
        #search each row / column 
        final_q_extend =[]
        for r,q_rect in enumerate(q_extend):

            if isPowOf2( len(q_rect) )== False:
                if axis==1:
                    ns=0
                else:
                    ns=1

                print("Recursive:")
                split_rects = rectangle_search4(q_rect.copy(),ns)
                
                for sr in split_rects:
                    if sr not in q_extend:
                        final_q_extend.append(sr.copy())
            else:
                final_q_extend.append(q_rect.copy())
        q_extend = final_q_extend.copy()

    return q_extend
     
def Algebra_Simplfy(bool_expr):
    # bool_expr ='-X+Y'      
        
    print('Expression:',bool_expr)

    # sys.exit()
    var_list=Var_Scan(bool_expr)
    # var_list =Var_Scan_Node_Ver(bool_tr)
    print('variable:',var_list)


    global num_var
    num_var = len(var_list)
    NumOfCompos = 2^num_var # total element of karna map

    global NumRowVar,NumColVar
    NumRowVar = int(num_var/2)
    NumColVar = num_var - NumRowVar

    row_var = var_list[0:NumRowVar]
    col_var = var_list[NumRowVar:num_var]

    #initial the bit combination of each variable on row / column
    '''For row variable'''
    bit_num_r=bit_num_generate(NumRowVar)
    print(row_var,':\t',bit_num_r,'\t')
    
    '''For column variable'''
    bit_num_c=bit_num_generate(NumColVar)
    print(col_var,':\t',bit_num_c,'\t')
   
    #fil with the kana table
    kana_map = kana_fill_with(bool_expr,bit_num_r,bit_num_c,var_list)
    # kana_map,track = kana_fill_with(bool_expr,bit_num_r,bit_num_c,var_list)
    print("kana map:")
    print(row_var,"\\",col_var)

    for i in range(len(kana_map)):
        print(kana_map[i])
   
    #specify the location of simplfication
    stack = []
    track = []

    for i in range(pow(2,NumRowVar)):
        for j in range(pow(2,NumColVar)):
            if kana_map[i][j] ==1:
                direct_flag = [0]*4
                print("Region search: ")
                print("start point({},{})".format(i,j))
                stack,map = RS(i,j,stack,kana_map,direct_flag)
                kana_map = map
                if stack!=[]:
                    track.append(stack.copy())
                    stack.clear()

    print("Track of region:",track)
    print()

    #find the rectangle region
    RT=[]
    for s in track:       
        
        #count  rectangle of the region
        rect_set1 = rectangle_search4(s,axis=0)
        rect_set2 = rectangle_search4(s,axis=1)
        rect_set = rect_set1.copy() + rect_set2.copy()
        
        print('before')
        for r in rect_set:
            print(r)
        print('=========================')

        #elimate the same rectangle
        s_trace = []
        for i, rs in enumerate( rect_set ):
            if set(rs) not in s_trace:
                s_trace.append(set(rs).copy())

        print('after')
        rect_set = [list(st) for st in s_trace]
        for r in rect_set:
            print(r)
        print('=========================')
  

        rect_count=[]
        for rs in rect_set:
            rect_count.append( len(rs) )
        
        #sort the list of rectangle
        sort_idx = np.argsort(rect_count)
        
        sort_idx = list(sort_idx)

        temp=[]
        for id in sort_idx:
            temp.append(rect_set[id])
        rect_set = temp.copy()        
        del temp
        
        #find the top few of max rectangles
        R = [] # max rectangles of region
        p_trace=[]
        #R_set_trace = set(rect_set)

        while(len(p_trace) != len(s)):
                        
            print('-'*len(rect_set),len(rect_set),end='')
            temp_r = rect_set.pop()

            if (set(temp_r) & set(p_trace)) != set(temp_r):            
                
                print(temp_r)
                R.append(temp_r)

                for p in R[-1]:
                    if p not in p_trace:
                        p_trace.append(p)
            else:
                print('[duplicate]')

        print('=========================')
        print('Rectgles in region:',R)

        # if R not in RT:
        RT.append(R)
    print('Track of Rectangle Set:\n',RT)  

    print("kana map:")
    for i in range(len(kana_map)):
        print([abs(x) for x in kana_map[i]])  

    
    #simplfication kana map 
    print('\nSimplfy the Kana map:')
    final=''
    for iter,R in enumerate(RT):
        
        count=0
        for s in R:
            
            flag = []
            for ff in range(num_var):
                flag.append(0)  

            count+=1
            print('rect',count)
            print(s)

            #initial the first check value of rectangle
            pair = s.pop()
            print(" pair: ",pair,end='')
            i = pair[0]
            j = pair[1]

            temp1 = bit_num_r[i] + bit_num_c[j]
            print(" bit num",temp1)
            
            #check each value of kana map
            #determine which element to be eliminated
            while(len(s)!=0):
                pair = s.pop()
                print(" pair: ",pair,end='')

                i = pair[0]
                j = pair[1]
                temp2 = bit_num_r[i] + bit_num_c[j]
                print(" bit num",temp2)

                for k in range(len(temp2)):
                    tempb=abs(temp1[k]-temp2[k])
                    if tempb!=0:
                        flag[k]  = tempb#abs(temp1[k]-temp2[k])
                print(" flag",flag)
            
            #control the output string of single rectangle
            output=''
            for t in range(len(flag)):
                if flag[t]==0:
                    if temp1[t]==1:
                        output+=str(var_list[t])
                    else:
                        output+=str(var_list[t])+ "'"

            if (iter!=0 or sum(flag)!=len(flag)): 
                # print(sum(flag))
                final += output + ' + '
            # print(final)

    final = final[:-3]  #delete final +
    return final

if __name__ == '__main__':
    
    bool_expr =  '(-X+Y*Z)+B*D'
    #'-((a+c)*(d+a*b))'
    #' a+b * c '
    #'(a+b)*c*(a+b)'
    #'(a + b)*b*c ' 
    #'a*b+c'
    # #'-((a+c)*(d+a*b))'
    #'(x * y)+(-(a*z))'
    #'(a+b)*c*(a+b)' 
    #'(-X+Y*Z)+B*D'
        
    #'(c+(b*(-a)))'
    #'(a + b) + (c*c)'
    
    # 'a + b + c'
    # '(a*b+c)'
    # ' a+b * c '
    # 'a + b * c'    
    
    final=Algebra_Simplfy(bool_expr)
        
    print('simple:',final)
''' notice if the number of variable over 5 
    need to modify the rectanle_search() 
    to avoid stack overflow'''
