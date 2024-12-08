#imports
from tkinter.filedialog import askopenfilename
import pandas as pd

# load CpG
## DUSP example and random bi-modal site example
CpGs = ["cg01171360","cg10157098"]

#load CpG list - in the future allow to load number of CpGs
#file_path3 = askopenfilename(title="Select CpG list file", filetypes=[("txt\cpg files", "*.txt *.cpg")])
#CpGs = open(f"{file_path3}","r").read().splitlines()

# graph each person on x axis
# graph each methylation level on y axis (graph the difference between max time point to min time point)

# load methylation array - in the future allow for csv files
file_path = askopenfilename(title="Select methylation array TP1", filetypes=[("pickle files", "*.pkl, *.pickle")])
df1 = pd.read_pickle(file_path)
file_path = askopenfilename(title="Select methylation array TP2", filetypes=[("pickle files", "*.pkl, *.pickle")])
df2 = pd.read_pickle(file_path)
file_path = askopenfilename(title="Select methylation array TP3", filetypes=[("pickle files", "*.pkl, *.pickle")])
df3 = pd.read_pickle(file_path)
file_path = askopenfilename(title="Select methylation array TP4", filetypes=[("pickle files", "*.pkl, *.pickle")])
df4 = pd.read_pickle(file_path)

dfs = [df1, df2, df3, df4]

def prepare_dfs(cpg,dfs):
    dfs_CpGs = []
    for df in dfs:
        dfs_CpGs.append(df.loc[cpg])

    gsms = []
    for df in dfs_CpGs:
        gsms.append([index.split('_')[0] for index in df.index])

    new_df = pd.DataFrame({'methylation_TP1': [None] * 45, 'methylation_TP2': [None] * 45, 'methylation_TP3': [None] * 45, 'methylation_TP4': [None] * 45})
    return new_df,gsms,dfs_CpGs

def order_data(new_df,gsms,dfs_CpGs,cpg):
    def extract_methylation_values(new_df,dfs_CpGs,gsms,TP):
        matching_rows = []
        for g in gsms[0]:
            for index in dfs_CpGs.index:
                if str(index).startswith(str(g)):
                    matching_rows.append(index)
        if (matching_rows):
            values_add = dfs_CpGs.loc[matching_rows].values
            i = 0
            for value in values_add:
                new_df[TP].iloc[i] = value
                i += 1

    extract_methylation_values(new_df,dfs_CpGs[0],gsms[0],'methylation_TP1')
    extract_methylation_values(new_df,dfs_CpGs[1],gsms[1],'methylation_TP2')
    extract_methylation_values(new_df,dfs_CpGs[2],gsms[2],'methylation_TP3')
    extract_methylation_values(new_df,dfs_CpGs[3],gsms[3],'methylation_TP4')

    def calc_max_diff(new_df):
        differences = []
        for gsm in new_df.index:
            difference = new_df.iloc[gsm].max() - new_df.iloc[gsm].min()
            differences.append(difference)

        result_df = pd.DataFrame(differences, columns=["Max_Min_Difference"])
        return result_df

    clean_df = new_df[:34]
    diff_df = calc_max_diff(clean_df)

    def plot_results(diff_df,cpg=cpg):
        import matplotlib.pyplot as plt
        from tkinter import filedialog

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(diff_df.index, diff_df.values, marker='o', linestyle='-', color='b')

        # Add labels and title
        plt.xlabel("GSM Index Number")
        plt.ylabel("Methylation Number")
        plt.title(f"Methylation Levels mix(TP)-Max(TP) by GSM Index for {cpg}")

        # Set ticks to match GSM indices
        plt.xticks(ticks=range(len(diff_df.index)), labels=diff_df.index, rotation=45)

        # Set y-axis range
        plt.ylim(0, 1)

        # Show the plot
        plt.tight_layout()
        folder_path = filedialog.askdirectory(title="Select a Folder to save plot")
        plt.savefig(f"{folder_path}/{cpg}.png")

    plot_results(diff_df)

for cpg in CpGs:
    new_df,gsms,dfs_CpGs = prepare_dfs(cpg=cpg,dfs=dfs)
    order_data(new_df,gsms,dfs_CpGs,cpg=cpg)