import pandas as pd
import numpy as np
import os.path

def load_ascs(
        dirname                :str=None,
        filepath               :str=None,
        noreturn_unknown_data  :bool=True,
        sep="\t"
    ):
    """
        Read asc files, and classify sample to 3 DataFrame.
        
        Parameters
        ----------
        dirname  :
        filepath : fullpath

        Return
        ----------
        cell_df,background_df,(unknown_df)
    """
    if(dirname is not None):
        basenames = os.listdir(dirname)
        full_paths_dict = {dirname:[basename for basename in basenames if basename.endswith(".asc")]}
    elif(filepath is not None):
        basename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        full_paths_dict = {dirname:basename}
    else:
        print("No dirname and no filepath")
        exit(-1)

    cell_df,background_df,unknown_df = load_ascs_from_dict_(full_paths_dict)
    if(noreturn_unknown_data):
        return cell_df,background_df
    return cell_df,background_df,unknown_df

def load_ascs_from_dict_(files:dict,sep="\t"):
    """
        Read asc files, and classify sample to 3 DataFrame.
        
        Parameters
        ----------
        files: Ex.{"datas/220601":['u_266_7.asc', 'u_266_water.asc']}

        Return
        ----------
        raw_data_df,background_df,unknown_df
    """

    is_first_loop= True

    for parent_dir , basenames in files.items():
        cell_df     = pd.DataFrame()
        background_df  = pd.DataFrame()
        unknown_df  = pd.DataFrame()
        for basename in basenames:
            filename = os.path.join(parent_dir,basename)
            cell_name = os.path.splitext(basename)[0]
            raw_data = pd.read_csv(filename,sep="\t",header=None) 
            cell_data = raw_data.iloc[:,1] 

            if(is_first_loop):
                is_first_loop = False
                raman_shift = ["Raman_"+str(a)[:9] for a in raw_data.iloc[:,0]]

            if cell_name.split("_")[-1].isdecimal():
                cell_df[cell_name]   = cell_data
            elif(("water" in cell_name) or ("quartz" in cell_name)):
                background_df[cell_name] = cell_data
            else :
                #No match「*_digit.asc」,「*quartz*.asc」,「*qater*.asc」
                unknown_df[cell_name]    = cell_data
                unknown_df.index         = raman_shift
                            
        
        cell_df.index = raman_shift
        background_df.index = raman_shift

    return cell_df,background_df,unknown_df

if __name__ == "__main__":

    # import time
    # time_sta = time.time()
    # files = {"/Users/FujisawaNoritaka/Documents/M1/codes/datas/220601":['u_266_7.asc', 'u_266_water.asc', 'u_266_10.asc', 'delta_47_1.asc', 'u_266_6.asc', 'u_266_4.asc', 'delta_47_3.asc', 'delta_47_2.asc', 'u_266_5.asc', 'u_266_1.asc', 'delta_47_6.asc', 'delta_47_7.asc', 'u_266_2.asc', 'delta_47_5.asc', 'delta_47_4.asc', 'sio2.asc', 'u_266_3.asc', 'delta_47_10.asc', 'delta_47_9.asc', 'delta_47_8.asc', 'u_266_8.asc', 'delta_46_quartz.asc', 'u_266_9.asc', 'u_266_quartz.asc', 'delta_46_water.asc']}
    # load_ascs(files)

    # time_end = time.time()
    # # 経過時間（秒）
    # tim = time_end- time_sta

    # print(tim)
    cell_data,background_data =load_ascs("/Users/FujisawaNoritaka/Documents/M1/codes/datas/220601")

        