# Appends a Pandas dataframe to the specified Markdown file
def append_df_to_markdown(path, df, title=None):
    with open(path, "a") as f:
        if title is not None:
            f.write("## "+title+"\n\n")
        f.write(df.to_markdown(index=False, floatfmt=".2f")+'\n\n')