import pandas as pd

def comp(phama_tuple):
    file1=phama_tuple[0]
    file2=phama_tuple[1]
    key1=phama_tuple[2]
    key2=phama_tuple[3]
    cont1 = pd.read_csv(file1)
    cont2 = pd.read_csv(file2)
    res=pd.merge(cont1,cont2 ,on=[key1,key2],how='inner')
    res.to_csv('out5.csv')
    return 



if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    print("The start time is: " + str(start))
    parmas_list = ('fingerprint_10000.csv','all-dec_ref.csv','target','compounds')
    comp(parmas_list)
    end = datetime.datetime.now()
    print ("The end time is: " + str(end))
    print("The function run time is : "+str(end - start))