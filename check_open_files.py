# https://stackoverflow.com/questions/6825994/check-if-a-file-is-open-in-python


def check_open(fp_csv):
    try:
        myfile = open("myfile.csv", "r+") # or "a+", whatever you                    # exit the loop
    except IOError:
        print("Could not open file! Please close Excel. Press Enter to retry.")
        # restart the loop
