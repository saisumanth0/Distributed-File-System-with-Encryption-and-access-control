import argparse
import shutil
import os
from file_operations import encrypt_file, load_encryption_key,replicate_file_to_other_nodes # Import upload_file from file_operations


# Function to upload a file with encryption
def upload_file_with_encryption(args):
    print(f"Uploading file: {args.file} as {args.role} to storage node {args.storage_node}")

    # Check if the file exists
    if not os.path.isfile(args.file):
        print(f"Error: The file {args.file} does not exist.")
        return

    # Load encryption key
    key = load_encryption_key()

    # Encrypt the file and get the encrypted file path
    encrypted_file_path = encrypt_file(args.file, key)  # Calls encrypt_file from file_operations.py

    # Create the storage directory if it doesn't exist
    storage_dir = f"storage_node_{args.storage_node}"
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)  # Create the directory if it doesn't exist

    # Now call upload_file from file_operations.py to upload the encrypted file
    # Define the destination path for the encrypted file (correct path)
    destination_path = os.path.join(storage_dir, os.path.basename(encrypted_file_path))  # Correct destination path

    try:
        shutil.move(encrypted_file_path, destination_path)  # Move the encrypted file
        print(f"File uploaded successfully to {destination_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

    destination_storage_nodes = [1, 2, 3, 4]
    unavailable_nodes = [1, 2, 3]
    replicate_file_to_other_nodes(destination_path,args.storage_node, destination_storage_nodes, unavailable_nodes)
    print("replicated to other nodes")

# Placeholder function to view files (could be expanded later)
def view_files(args):
    print(f"Viewing files as {args.role}")
    # Add logic to view files here

# Placeholder function to view file content
def view_file_content(filename, role, key):
    print(f"Viewing content of {filename} as {role} using key: {key}")
    # Add logic here to decrypt and view file content

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Distributed File System CLI")
    subparsers = parser.add_subparsers()

    # Subparser for 'view' command (view metadata of files)
    view_parser = subparsers.add_parser('view', help="View files in the system")
    view_parser.add_argument('--role', choices=['admin', 'viewer'], required=True, help="Role of the user (admin/viewer)")
    view_parser.set_defaults(func=view_files)  # This will call the view_files function

    # Subparser for 'view_content' command (view content of a file)
    content_parser = subparsers.add_parser('view_content', help="View content of a file")
    content_parser.add_argument('--role', choices=['admin', 'viewer'], required=True, help="Role of the user (admin/viewer)")
    content_parser.add_argument('--filename', type=str, required=True, help="Filename to view content")
    content_parser.add_argument('--key', required=True, help="Decryption key")  # Key argument, no IV required
    content_parser.set_defaults(func=view_file_content)  # This will call the view_file_content function

    # Subparser for 'upload' command (upload a file)
    upload_parser = subparsers.add_parser('upload', help="Upload a file to the system")
    upload_parser.add_argument('--role', choices=['admin', 'viewer'], required=True, help="Role of the user (admin/viewer)")
    upload_parser.add_argument('--file', type=str, required=True, help="Path to the file to upload")
    upload_parser.add_argument('--storage_node', type=int, required=True, help="Storage node to upload to")
    upload_parser.set_defaults(func=upload_file_with_encryption)  # This will call the upload_file_with_encryption function

    # Parse arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the parsed arguments
    if hasattr(args, 'func'):
        # If it's the view_content function, we need to pass the key parameter only
        if 'filename' in args and 'key' in args:
            # Convert the key from the command-line argument (if it is passed as a string)
            key = bytes(args.key, 'utf-8')  # Adjust based on your key format
            # Call the view_file_content function with the correct parameters
            args.func(args.filename, args.role, key)
        else:
            args.func(args)
    else:
        parser.print_help()  # Print help if no valid command was given

if __name__ == "__main__":
    main()
