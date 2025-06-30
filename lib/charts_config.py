import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme()


def plot_woe_iv(df, cls, rotation_X=0):
    x = np.array(df["Bin_Range"])
    y = df["woe"]
    plt.figure(figsize=(20, 10))
    plt.plot(x, y, marker="o", linestyle="--", color="k")
    plt.xlabel(df.columns[0], rotation=rotation_X)
    plt.ylabel("WOE")
    plt.title(str(f"Weight of Evidence (WOE) - {cls}"))
    plt.xticks(rotation=rotation_X)
