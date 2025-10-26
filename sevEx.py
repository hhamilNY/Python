
def read_file(path: str) -> str | None:
    try:
        with open(path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {path}, please try with a valid file path.")
        return None
    except Exception as e:
        print(f"Error reading file: {path}, Error: {repr(e)}")
        return None
    
def main() -> None:
    file_path: str = "example.txt"
    content: str | None = read_file(file_path)
    if content is not None:
        print(content)

if __name__ == "__main__":
    main()  

