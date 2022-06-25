"""
    To read asc file and create DataFrame
    * load_ascs
"""

import pandas as pd
import os.path

def load_ascs(
        dirname                :str=None,
        filepath               :str=None,
        noreturn_unknown_data  :bool=True,
        sep="\t"
    ):
    """
        Read asc files from dirname or filepath, and classify sample to 3 DataFrame.
        
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

    cell_df,background_df,unknown_df = _load_ascs_from_dict(full_paths_dict)
    if(noreturn_unknown_data):
        return cell_df,background_df
    return cell_df,background_df,unknown_df

def _load_ascs_from_dict(files:dict,sep="\t"):
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
        if(len(basenames)):
            continue
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

            if(("water" in cell_name) or ("quartz" in cell_name)):
                background_df[cell_name] = cell_data
            elif cell_name.split("_")[-1].isdecimal():
                cell_df[cell_name]   = cell_data
            else :
                #No match「*_digit.asc」,「*quartz*.asc」,「*qater*.asc」
                unknown_df[cell_name]    = cell_data
                unknown_df.index         = raman_shift
                            
        if(cell_df.empty):
            print(f"No asc files. In {os.path.join(parent_dir)}.")
            exit(-1)

        cell_df.index = raman_shift
        background_df.index = raman_shift

    return cell_df,background_df,unknown_df

if __name__ == "__main__":
    path = "./"
    cell_data,background_data =load_ascs(path)
    print(cell_data)
    print(background_data)

        