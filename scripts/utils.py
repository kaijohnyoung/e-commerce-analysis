# Appends a Pandas dataframe to the specified Markdown file
def append_df_to_markdown(path, df, title=None):
    with open(path, "a") as f:
        if title is not None:
            f.write("## "+title+"\n\n")
        f.write(df.to_markdown(index=False, floatfmt=".2f")+'\n\n')

# Appends an image at some specified path to a specified Markdown file
def append_image_to_markdown(md_path, image_path, title):
    with open(md_path, "a") as f:
        f.write("## "+title+"\n\n")
        f.write(f'![{title}]({image_path})\n\n')