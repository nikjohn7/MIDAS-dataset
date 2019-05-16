import os,csv
directory = 'C:/Data/FakeNews/fakeNewsDatasets/fakeNewsDataset/legit'
f=open("C:/Data/FakeNews/fakeNewsDatasets/data.csv",'r+')
w=csv.writer(f)
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        st=''
        f1 = open(os.path.join(directory,filename),'r+')
        line = [x.strip() for x in f1.readlines()[1:]]
        st=st.join(line)
        #print(st)
        w.writerow([line])
        f1.close()
        continue
    else:
       continue