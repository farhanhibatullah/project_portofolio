from zipfile import ZipFile

def unzip_file_from_path(filepath: str, targetpath: str):
    filepath = "/".join(filepath.split("\\"))
    targetpath = "/".join(targetpath.split("\\"))
    print(filepath, targetpath)
    with ZipFile(filepath) as file:
        try:
            file.extractall(targetpath)
            print("extract successfully!")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    target_path = "D:\\Belajar Full Stack Data Scientist\\Project\\Data Science\\Project 1 - Customer Behaviour Dashboard\\dataset"
    file_path = "D:\\Belajar Full Stack Data Scientist\\Project\\Data Science\\Project 1 - Customer Behaviour Dashboard\\online+retail.zip"
    unzip_file_from_path(targetpath=target_path, filepath=file_path)