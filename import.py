import pandas as pd
import requests
import zipfile
import io

dfs = []
FILE_DOWNLOAD_URL = "http://cicresearch.ca/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/CSVs/GeneratedLabelledFlows.zip"
response = requests.get(FILE_DOWNLOAD_URL)
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
  # List all files in the ZIP
  print("Files in ZIP:", z.namelist())

  for file in z.namelist()[1:]:
  # Extract and read the desired CSV file
    with z.open(file) as f:
      dfs.append(pd.read_csv(f, encoding='cp1252'))

df = pd.concat(dfs, ignore_index=True)

print(df.head())
