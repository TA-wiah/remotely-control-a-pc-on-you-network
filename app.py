from smbprotocol.connection import Connection
from smbprotocol.exceptions import SMBAuthenticationError, SMBTimeout
import os

def list_files_in_folder(conn, folder_path):
    with conn.connect_share("Users") as share:
        with share.create_directory_context(folder_path) as ctx:
            for item in ctx.list():
                print(item.filename)

def download_file(conn, remote_path, local_path):
    with conn.connect_share("Users") as share:
        with share.open_file(remote_path, "rb") as remote_file:
            with open(local_path, "wb") as local_file:
                data = remote_file.read(65536)
                while data:
                    local_file.write(data)
                    data = remote_file.read(65536)

def delete_file(conn, file_path):
    with conn.connect_share("Users") as share:
        share.delete_file(file_path)

def main():
    print("Welcome to Cyber Hatcher Do the Bad By Jeffrey")
    print("For educational purpose")
    remote_pc_ip = input("Enter remote PC IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        conn = Connection(remote_pc_ip, username=username, password=password)

        while True:
            print("\nOptions:")
            print("1. List files in folder")
            print("2. Download file")
            print("3. Delete file")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                folder_path = input("Enter folder path (e.g., 'Documents' or 'Downloads'): ")
                list_files_in_folder(conn, folder_path)
            elif choice == "2":
                remote_path = input("Enter remote file path: ")
                local_path = os.path.join(os.path.expanduser("~"), "Desktop", "Cyber Hatch", os.path.basename(remote_path))
                download_file(conn, remote_path, local_path)
                print(f"File downloaded to: {local_path}")
            elif choice == "3":
                file_path = input("Enter file path: ")
                delete_file(conn, file_path)
                print("File deleted successfully.")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    except SMBAuthenticationError:
        print("Authentication failed. Please check your credentials.")
    except SMBTimeout:
        print("Connection timed out. Please check the remote PC's availability.")
    except Exception as e:
        print("Error:", str(e))
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Redirect standard output and error streams to /dev/null (Unix-like systems)
    # or NUL (Windows)
    if os.name == 'posix':
        os.system("python script.py > /dev/null 2>&1")
    elif os.name == 'nt':
        os.system("python script.py > NUL 2>&1")
