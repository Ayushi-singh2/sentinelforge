from app.mcp.tools import inspect_repository
from app.mcp.schemas import RepositoryRequest


def main():
    # Change "." to any repository path you want to inspect
    request = RepositoryRequest(path=".")

    try:
        result = inspect_repository(request)

        print("=" * 50)
        print("Repository Inspection Result")
        print("=" * 50)

        print(f"Total Files      : {result.total_files}")
        print(f"Languages        : {', '.join(result.languages)}")

        print("\nImportant Files:")
        if result.important_files:
            for file in result.important_files:
                print(f"  - {file}")
        else:
            print("  None")

        print("\nFiles:")
        for file in result.files:
            print(f"  - {file}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()