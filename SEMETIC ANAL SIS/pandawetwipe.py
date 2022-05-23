
import pandas as pd

class wetWiper:
    
    @staticmethod
    def WipeTheThing():
        loadeddata=pd.read_csv('poempandas.csv',index_col=0)
        print(loadeddata.size)
        loadeddata=loadeddata.dropna()
        print(loadeddata.size)
        loadeddata.reset_index(drop=True, inplace=True)
        loadeddata.to_csv('test.csv', encoding='utf-8-sig')
        print(str(loadeddata['String'][159]))
        count=0
        todelete=[]
        for i in range(len(loadeddata)):
            print(i)
            print(loadeddata['String'][i])
            if'المزيد عن' in loadeddata['String'][i]:
                count=count+1
                print(loadeddata['String'][i])
                todelete.append(i)
            
            elif 'أضف معلومة او شرح' in loadeddata['String'][i]:
                count=count+1
                print(loadeddata['String'][i])
                todelete.append(i)
        
        loadeddata = loadeddata.drop(labels=todelete, axis=0)
        print(count)
        print(loadeddata)
        loadeddata.reset_index(drop=True, inplace=True)
        loadeddata.to_csv('poempandas.csv', encoding='utf-8-sig')
        #np.savetxt("poemsentimentpos.txt", cleanlist,fmt='%s',delimiter=',',encoding="utf-16")