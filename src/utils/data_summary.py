def summarize(df):

    print("="*50)

    print("Rows :", len(df))

    print("Columns :", len(df.columns))

    print("Start :", df["date"].min())

    print("End :", df["date"].max())

    print("="*50)