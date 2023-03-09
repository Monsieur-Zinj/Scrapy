import re
import pandas as pd
from utils import get_func_calls
# open and read file ex_py, put it in variable code
with open("ex_py", "r") as f:
    code = f.read()

import ast
# get function calls
tree = ast.parse(code)
func_call=get_func_calls(tree)

# get module 
# case 1 : looking for pattern like "import xyz"
case_1=re.findall("^import ([^ ]*)$",code, re.MULTILINE)
print(case_1)

# case 2 : looking for pattern like "import xyz as"
case_2=re.findall("(?:^| {2,})import ([^ ]*) as (.*)$",code, re.MULTILINE)
print(case_2)



# case 3 : looking for pattern like "from xyz import" without "as"
case_3=re.findall("from (.*?) import ((?:(?! as ).)*)$",code, re.MULTILINE)
print(case_3)

# case 4 : looking for pattern like "from xyz import as"
case_4=re.findall("from (.*) import (.*) as (.*)$",code, re.MULTILINE)
print(case_4)




# print all cases
print("case 1 :",case_1,"\ncase 2 :",case_2,"\ncase 3 :",case_3,"\ncase 4 :",case_4)
# make a df with case_1
df_1 = pd.DataFrame(case_1, columns=["module"])
# add a column "alias", with same values as "module"
df_1["alias"]=df_1["module"]

# make a df with case_2
df_2 = pd.DataFrame(case_2, columns=["module","alias"])



# make a df with case_4
# the first column, "module", is the first element + "." + the second element
# the last is the "alias"
df_4 = pd.DataFrame(case_4, columns=["module","mod2","alias"])
df_4["module"]=df_4["module"]+"."+df_4["mod2"]
df_4["func"]
df_4

# concat df_1 and df_2 and df_4
df_mod_alias=pd.concat([df_1,df_2, df_4])

# for each tuple in case_3, split the string in the second element of the tuple
# and add each element to a dataframe with the first element of the tuple as module
df_3 = pd.DataFrame(columns=["module","func"])
for i in case_3:
    f=i[1].split(",")
    mod=[i[0]]*len(f)
    print(mod)
    print(f)
    # concat mod and f to df_3
    df_3=pd.concat([df_3,pd.DataFrame(list(zip(mod,f)),columns=["module","func"])])



# make a df with func_call
df_func_call = pd.DataFrame(func_call, columns=["func"])

# join df_func_call and df_3 on "func"
df_func_mod=pd.merge(df_func_call,df_3,how="left",on="func")

# subset with row where "module" is NaN
df_func_alias=df_func_mod[df_func_mod["module"].isna()]
# keep row where "func" contains "."
df_func_alias=df_func_alias[df_func_alias["func"].str.contains("\.")]
# the first element of the split is the module
df_func_alias["module"]=df_func_alias["func"].str.split("\.").str[0]
# remove the first element of the split of "func"
df_func_alias["func"]=df_func_alias["func"].str.split("\.",n=1).str[1]
df_func_alias


# join df_mod_alias and df_func_alias on "alias" and "module"
df_func_mod_2=pd.merge(df_mod_alias,df_func_alias,how="left",left_on="alias",right_on="module")
# keep only "module_x" and "func" columns, rename "module_x" to "module"
df_func_mod_2=df_func_mod_2[["module_x","func"]].rename(columns={"module_x":"module"})
df_func_mod_2

# remove NaN values from df_func_mod
df_func_mod=df_func_mod[~df_func_mod["module"].isna()]
# permute columns
df_func_mod=df_func_mod[["module","func"]]
df_func_mod

# concat df_func_mod and df_func_mod_2
df_func_mod_final=pd.concat([df_func_mod,df_func_mod_2])

# index of row where "module" contains "."
index=df_func_mod_final["module"].str.contains("\.")
# for the rows concerned, split on "." and keep the first element
# the last element is added to "func"
df_func_mod_final.loc[index,"module2"]=df_func_mod_final.loc[index,"module"].str.split("\.").str[0]
df_func_mod_final.loc[index,"func"]=+"."+df_func_mod_final.loc[index,"module"].str.split("\.",n=1).str[1]
df_func_mod_final



# in df_1 replace all Nan with ""










# # make a df with case_1
# df_1 = pd.DataFrame(case_1, columns=["module"])
# # add a column "alias" with missing values
# df_1["alias"]=None
# # make a df with case_2
# df_2 = pd.DataFrame(case_2, columns=["module","alias"])

# # for each tuple in case_3, split the string in the second element of the tuple
# # and add each element to a dataframe with the first element of the tuple as module
# df_3 = pd.DataFrame(columns=["module","func"])
# for i in case_3:
#     f=i[1].split(",")
#     mod=[i[0]]*len(f)
#     print(mod)
#     print(f)
#     # append mod and f to df_3
#     df_3=df_3.append(pd.DataFrame(list(zip(mod,f)),columns=["module","func"]))

# print(df_3)





# # make 2 list : one with string containing "." and other with the rest
# func_call_dot=[]
# func_call_no_dot=[]
# for i in func_call:
#     if "." in i:
#         func_call_dot.append(i)
#     else:
#         func_call_no_dot.append(i)

# # in func_call_dot, split the string at the first "." and add the 2 elements to a dataframe
# df_dot = pd.DataFrame(columns=["module","func"])
# for i in func_call_dot:
#     f=i.split(".",1)
#     df_dot=df_dot.append(pd.DataFrame([f],columns=["module","func"]))


# # make a df with func_call_no_dot with missing values for module
# df_no_dot = pd.DataFrame(func_call_no_dot, columns=["func"])
# df_no_dot["module"]=None

# # print all df with their name
# print("case 1")
# print(df_1)
# print("case 2")
# print(df_2)
# print("case 3")
# print(df_3)
# print("func_call_dot")
# print(df_dot)
# print("func_call_no_dot")
# print(df_no_dot)


