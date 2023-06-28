import os


def check_file_exists(full_file_name):
    print(f"in check_file_exists  file_name = {full_file_name}")
    try:
        if os.path.isfile(full_file_name):
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred:", e)
        return False



file_name = "db/chroma-collections.parquet"
exists = check_file_exists(file_name)
print(exists)