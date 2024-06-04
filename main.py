from src.scaffolder import Scaffolder


# Example usage
if __name__ == "__main__":
    dir1 = "targets"
    dir2 = "src"

    diff = Scaffolder()
    differences = diff.compare_directories(dir1, dir2)
    if differences:
        for file1, file2, diff in differences:
            print(f"Difference between {file1} and {file2}:")
            print(diff)
    else:
        print("The directories are logically equivalent.")
