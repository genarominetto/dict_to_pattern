from src.scaffolder import Scaffolder

# Example usage
if __name__ == "__main__":
    file1 = "main.py"
    file2 = "main.py"

    scaffolder = Scaffolder(file1, file2)
    if scaffolder.is_equivalent():
        print("The files are logically equivalent.")
    else:
        print("The files are not logically equivalent. Here is the diff:")
        print(scaffolder.get_diff())