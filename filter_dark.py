# The following program subtracts one folder from another if both folder has  same number
# of files(csv in this case), and all the files in both folder are of same number of rows and columns
import pandas as pd
import glob
from numpy import genfromtxt



def subtract(path1, data2, folder_save):
    # Path for 2 folders
    path1 = path1
    data2 = pd.read_csv(data2, header=None)
    counter = 0
    # Using zip, we can run multiple loops in parallel
    # In our case we must sort the files while reading with glob
    for fname1 in sorted(glob.glob(path1)):
        # Read files in both folder with pandas and put them in 2 dataframe
        data1 = pd.read_csv(fname1, header=None)
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        # As our filename contains unix timestamp, we can extract the timestamp slicing the filename
        # Change the ranges depending on file path path manually
        #    print(fname1)
        timestamp = str(fname1.split('.')[0].split('_')[3])
        print(timestamp)

        # Subtract one dataframe from another, as sorted they should match the sequence
        # Fill empty cell with 0 to avoid "NAN"
        df = df1.subtract(df2, fill_value=0)
        # Round to one decimal place
        df = df.round(1)
        # Set all the negatives to zero
        df[df < 0] = 0
        counter = counter + 1
        print(df)
        # Save each file(dataframe) including the timestamp extracted
        df.to_csv("/home/pi/PycharmProjects/LED_Test_all/output/"+folder_save+"/filteredSpec_"+timestamp+".csv",
                  header=False, index=False)

    print(counter, "files processed and saved")


subtract(r"/home/pi/PycharmProjects/LED_Test_all/output/LED1/*.csv",
         "/home/pi/PycharmProjects/LED_Test_all/output/Dark/LED1_dark.csv",
         "LED1_filtered")