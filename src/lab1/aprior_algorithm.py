import pandas as pd


def init(df):
  clist=[]
  for i in range(len(df.columns)):
    if i >=2:
      clist.append(df.columns[i])

  dfnk=df.drop(clist,axis=1)
  return dfnk

def maxage_of_df(df):
  lar=0
  index=0
  for i in range(len(df)):
    if df[df.columns[0]][i]>lar:
      lar=df[df.columns[0]][i]
      index=i
  return index

def generate_data(max,min,df):
  datalistk=[] # 初始datalist
  for i in range(max):
    datalistk.append([])
  for i in range(len(df)):
    datalistk[df[df.columns[0]][i]-min].append(df[df.columns[1]][i])
  return datalistk

def check_data(list):
  zlist=[]
  plist=[]
  for i in range(len(list)):
    if len(list[i])==0:
      zlist.append(i)
  for i in range(len(zlist)):
    plist.append(zlist.pop())
  for i in plist:
    del list[i]
  return list

def data_num(df):
  return len(df)

def set_data(list):
  datalistk_set=[]
  for i in range(len(list)):
    datalistk_set.append(set(list[i]))
  return datalistk_set

def set_init(index):
  item_list=[[]]
  for i in range(len(index)):
    item_list[0].append(set([index[i]]))
  return item_list

def get_num(list):
  return len(list)

def creat_support_df(datalistk_set,item_list,num,min_support=0.5,max_length=4):

  item_sup=[]      #符合sup
  sup_list=[]
  item_nsup=[]     #不符合sup
  nsup_list=[]
  bad_sup=[]       #紀錄後面被篩選掉的set

  #  algo.
  for i in range(max_length):

    item_sup.append([])
    sup_list.append([])
    item_nsup.append([])
    nsup_list.append([])
    bad_sup.append([])

    #判斷符合min sup的item 加入item sup
    for j in range(len(item_list[i])):
      num_s=0

      #判斷item_list[i][j]出現次數
      for k in range(len(datalistk_set)):
        st=item_list[i][j].intersection(datalistk_set[k])
        if st==item_list[i][j]:
          num_s += 1

      #將篩選過的item加入先的list row
      sup=num_s/num

      if sup>=min_support :
        sup_list[i].append(sup)
        item_sup[i].append(item_list[i][j])
      if sup<min_support :
        nsup_list[i].append(sup)
        item_nsup[i].append(item_list[i][j])

    item_list.append([])

    # 更新item_list 作為下一輪運算用
    for j in range(len(item_sup[i])-1):
      for k in range(j+1,len(item_sup[i]),1):
        st=item_sup[i][j].union(item_sup[i][k])
        if len(st)==i+2:
          stu=0
          for l in range(len(item_list[i+1])):
            if st == item_list[i+1][l]:
              stu=1
          if stu==0:
            item_list[i+1].append(st)

    #找出不滿min sup 元素的超集
    for j in range(len(item_list[i+1])):
      for k in range(len(item_nsup[i])):
        st=item_list[i+1][j].intersection(item_nsup[i][k])
        if st== item_nsup[i][k]:
          stu=0
          for l in range(len(bad_sup[i])):
            if item_list[i+1][j] == bad_sup[i][l]:
              stu=1
          if stu==0:
            bad_sup[i].append(item_list[i+1][j])

    #刪除不滿min sup 元素的超集
    for j in range(len(bad_sup[i])):
      item_list[i+1].remove(bad_sup[i][j])

  df=pd.DataFrame()
  tem_list1=[]
  for i in range(len(sup_list)):
    for j in range(len(sup_list[i])):
      tem_list1.append(sup_list[i][j])
  tem_list2=[]
  for i in range(len(item_sup)):
    for j in range(len(item_sup[i])):
      tem_list2.append(item_sup[i][j])
  df['item_name']=tem_list2
  df['support']=tem_list1

  tem3_list=[]
  tem4_list=[]
  for i in range(len(df)):
    tem3_list.append(len(df['item_name'][i]))
    tem4_list.append(pow(2,len(df['item_name'][i])))
  df['item_len']=tem3_list
  df['subset_num']=tem4_list

  tem5_list=[]
  for i in range(len(df)):
    tem5_list.append(3*i)
  df['conf_index']=tem5_list
  tem6_list=[]
  for i in range(len(df)):
    tem6_list.append(3*i+1)
  df['conf_n_index']=tem6_list
  tem7_list=[]
  for i in range(len(df)):
    tem7_list.append(3*i+2)
  df['conf_t_index']=tem7_list
  return df

def creat_conf_list(df):
  # 找出所有subset
  conf_list=[]
  for i in range(len(df)):
    conf_list.append([])
    conf_list.append([])
    conf_list.append([])
    for j in df['item_name'][i]:
      conf_list[df['conf_index'][i]].append(set([j]))
  for i in range(len(df)):
    item_len=df['item_len'][i]
    for m in range(item_len-1):
      for j in range(len(conf_list[3*i])-1):
        for k in range(j+1,len(conf_list[3*i]),1):
          st=conf_list[3*i][j].union(conf_list[3*i][k])
          if len(st)==m+2:
            stu=0
            for l in range(len(conf_list[3*i])):
              if st == conf_list[3*i][l]:
                stu=1
            if stu==0:
              conf_list[3*i].append(st)
  # 計算出所有的confidence
  for i in range(len(df)):
    for j in range(len(conf_list[3*i])):
      for k in range(len(df)):
        item=df['item_name'][k]
        if conf_list[3*i][j]==item:
          conf_list[3*i+1].append(df['support'][k])
  for i in range(len(df)):
    for j in range(len(conf_list[3*i])-1):
      conf=conf_list[3*i+1][-1]/conf_list[3*i+1][j]
      conf_list[3*i+2].append(conf)
  return conf_list

def creat_result(conf_list,min_confidence=0.3):
  tem8_list=[[],[],[],[],[]]
  for i in range(len(df)):
    for j in range(len(conf_list[3*i+2])):
      if conf_list[3*i+2][j]>=min_confidence:
    #    print('')
    #    print("Rule: " + str(conf_list[3*i][j]) + " -> " + str(conf_list[3*i][-1]-conf_list[3*i][j]))
    #    print("Support: " + str(conf_list[3*i+1][-1]))
    #    print("Confidence: " + str(conf_list[3*i+2][j]))
    #    print('')
    #    print("=====================================>")
        tem8_list[0].append(conf_list[3*i][j])
        tem8_list[1].append(' --> ')
        tem8_list[2].append(conf_list[3*i][-1]-conf_list[3*i][j])
        tem8_list[3].append(conf_list[3*i+1][-1])
        tem8_list[4].append(conf_list[3*i+2][j])
  df_res=pd.DataFrame()
  df_res['Body']=tem8_list[0]
  df_res['Implies']=tem8_list[1]
  df_res['Head']=tem8_list[2]
  df_res['Support']=tem8_list[3]
  df_res['Confidence']=tem8_list[4]
  return df_res
if __name__=='__main__':
  ## kaggle UCI Data
  dfk=pd.read_csv('./input_data/Kaggle_UCI_Data.csv')
  print('kaggle done')

  dfnk=init(dfk)
  x=maxage_of_df(dfnk)
  mini=min(dfnk[dfnk.columns[0]])
  datalistk=generate_data(x,mini,dfnk)
  datalistk=check_data(list=datalistk)
  index=dfnk.groupby([dfnk.columns[1]]).count().index
  datalistk_set= set_data(list = datalistk)
  item_list = set_init(index=index)
  num= get_num(list =datalistk_set)
  df=creat_support_df(datalistk_set,item_list,num)
  conf_list=creat_conf_list(df)
  res_kaggle=creat_result(conf_list)
  res_kaggle.to_csv('./output_data_aprior_algorithm/Kaggle_result.csv',index=False,header=True)
  print('kaggle Success')

  ## IBM UCI Data
  dfk=pd.read_csv('./input_data/IBM_Generator_Data.csv')
  print('IBM done')
  dfk=dfk.drop(columns=[dfk.columns[1]])
  dfnk=init(dfk)
  x=maxage_of_df(dfnk)
  mini=min(dfnk[dfnk.columns[0]])
  datalistk=generate_data(x,mini,dfnk)
  datalistk=check_data(list=datalistk)
  index=dfnk.groupby([dfnk.columns[1]]).count().index
  datalistk_set= set_data(list = datalistk)
  item_list = set_init(index=index)
  num= get_num(list =datalistk_set)
  df=creat_support_df(datalistk_set,item_list,num,min_support=0.1,max_length=3)
  conf_list=creat_conf_list(df)
  res_IBM=creat_result(conf_list,0.32)
  res_IBM.to_csv('./output_data_aprior_algorithm/IBM_Generator_Data_result.csv',index=False,header=True)
  print('IBM Success')
