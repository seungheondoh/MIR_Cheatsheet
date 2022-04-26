import pandas as pd
from collections import Counter

def df_to_histogram(df, column):
    target = df[column]
    most_common = Counter(target[target != 0]).most_common()
    df = pd.DataFrame(most_common, columns=['category','freq']).set_index("category")
    df.plot.bar(color="b")
    
def df_to_group_histogram(df, column, _min, _max, interval):
    target = df[column]
    out = pd.cut(target, bins=[int(i) for i in range(_min, _max, interval)], include_lowest=False)
    out.value_counts(sort=False).plot.bar(rot=60, color="b")