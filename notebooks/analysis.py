import pandas as pd

file_path = "data/Superstore/Sample - Superstore.csv"
# Try different encodings
for encoding in ["utf-8", "latin1", "cp1252", "ISO-8859-1"]:
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"✅ Successfully loaded using encoding: {encoding}")
        print(df.head())
        print(df.info())
        break
    except Exception as e:
        print(f"❌ Failed with {encoding}: {e}")