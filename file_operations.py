import sqlite3
import os
from decryption import decrypt_file
from encryption_utils import generate_key
from cryptography.fernet import Fernet
import argparse


def is_node_available(storage_node, unavailable_nodes):
    # Simulate the availability of nodes (nodes 2 and 4 are down in this example)
    if storage_node in unavailable_nodes:
        return False
    return True

def file_exists_on_node(file_name, storage_node):
    file_path = f"storage_node_{storage_node}/{file_name}"
    return os.path.isfile(file_path)

def retrieve_file_with_fault_tolerance(file_name, primary_node, all_nodes, unavailable_nodes):
    print(f"Retrieving file: {file_name} from node {primary_node} with fault tolerance.")

    # Case 1: Check if the primary node is available
    if not is_node_available(primary_node, unavailable_nodes):
        print(f"Node {primary_node} is unavailable. Checking other nodes...")
        # Attempt to retrieve the file from other nodes
        for node in all_nodes:
            if is_node_available(node, unavailable_nodes):
                # Try to fetch the file from the available node
                if file_exists_on_node(file_name, node):
                    print(f"File found on Node {node}. File successfully retrieved.")
                    return f"storage_node_{node}/{file_name}"
                else:
                    print(f"File {file_name} not found on Node {node}.")
        print("Error: File not found on any available nodes.")
        return None

    # Case 2: Primary node is available, but file is not found
    if file_exists_on_node(file_name, primary_node):
        print(f"File found on Node {primary_node}. File successfully retrieved.")
        return f"storage_node_{primary_node}/{file_name}"

    # If the file was not found on the primary node, check other nodes
    print(f"File not found on Node {primary_node}. Checking other nodes...")
    for node in all_nodes:
        if node != primary_node and is_node_available(node):
            # Try to fetch the file from other available nodes
            if file_exists_on_node(file_name, node):
                print(f"File found on Node {node}. File successfully retrieved.")
                return f"storage_node_{node}/{file_name}"

    print(f"Error: File {file_name} not found on any available nodes.")
    return None

def generate_and_save_key():
    """Generates an encryption key and saves it to the 'metadata' folder."""
    key = generate_key()  # Generate the encryption key
    metadata_dir = "metadata"
    os.makedirs(metadata_dir, exist_ok=True)  # Ensure 'metadata' directory exists

    key_path = os.path.join(metadata_dir, "encryption_key.key")
    try:
        with open(key_path, "wb") as key_file:
            key_file.write(key)  # Write the key to the file
        print(f"Encryption key generated and saved to {key_path}")
    except Exception as e:
        print(f"Error saving the encryption key: {e}")

def load_encryption_key():
    """Loads the encryption key from the 'metadata' folder."""
    print("Loading encryption key is called")
    metadata_dir = "metadata"
    key_path = os.path.join(metadata_dir, "encryption_key.key")

    try:
        with open(key_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: Encryption key file not found at {key_path}. Please generate the key first.")
        return None

def decrypt_file(encrypted_file_path, key):
    """
    Decrypts a file using the Fernet key and saves it as a new file.
    """
    fernet = Fernet(key)
    print(f"Decryption Key Used: {key}")

    try:
        # Open the encrypted file
        with open(encrypted_file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)

        decoded_content = decrypted_data.decode('utf-8')  # Try decoding as UTF-8

        # Clean up the content to normalize line breaks
        cleaned_content = decoded_content.replace('\r\n', '\n').replace('\r', '\n')

        print(f"\nDecrypted Content (Text):\n{cleaned_content}")


        # Save the decrypted data to a new file
        #decrypted_file_path = encrypted_file_path.replace('.enc', '_decrypted.txt')
        #with open(decrypted_file_path, 'wb') as dec_file:
        #    dec_file.write(decrypted_data)

        #print(f"File decrypted successfully: {decrypted_file_path}")
        #return decrypted_file_path  # Return the path of the decrypted file

    except Exception as e:
        print(f"Error while decrypting file: {e}")
        return None
        #print(f"\nDecrypted Content:\n{decrypted_data.decode("utf-8")}")  # Display decrypted content directly


def view_file_content(filename, role, key, storage_node, all_nodes, unavailable_nodes):
    print(f"Viewing content of {filename} with role {role}")

    if not filename.endswith('.enc'):
        filename += '.enc'

    #file_path = os.path.join(f"storage_node_{storage_node}", filename)

    file_path=retrieve_file_with_fault_tolerance(filename, storage_node, all_nodes, unavailable_nodes)


    try:
        # Read the encrypted content
        with open(file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        # Decrypt the data
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)


        decrypted_text = decrypted_data.decode("utf-8")
        #print(f"Decrypted file content saved to {decrypted_file_path}")
        print(f"Decrypted file content:\n{decrypted_text}")

    except Exception as e:
        print(f"Error while decrypting file: {e}")

def encrypt_file(file_path, key):
    print(f"Encryption Key Used: {key}")
    print("This encryption function is called")
    encrypted_file_path = file_path + ".enc"

    # Check if already encrypted
    if file_path.endswith(".enc"):
        print(f"File {file_path} is already encrypted.")
        return encrypted_file_path

    try:
        with open(file_path, "rb") as file:
            original_data = file.read()
        print(f"Original Data (before encryption): {original_data[:50]}")

        # Encrypt the data
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(original_data)
        print(f"Encrypted Data (after encryption): {encrypted_data[:50]}")

        # Save encrypted data
        with open(encrypted_file_path, "wb") as enc_file:
            enc_file.write(encrypted_data)

        print(f"Encrypted file saved as: {encrypted_file_path}")
        return encrypted_file_path

    except Exception as e:
        print(f"Error encrypting file: {e}")
        return None


def replicate_file_to_other_nodes(file_path, source_storage_node, destination_storage_nodes, unavailable_nodes):
    """Replicates the file to other storage nodes."""
    print("Replicate function is called")
    try:
        # Read the file from the source storage node
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Replicate the file to all the destination nodes
        for node in destination_storage_nodes:
            if node in unavailable_nodes:
                pass
            else:
                dest_path = f"storage_node_{node}/{os.path.basename(file_path)}"
                with open(dest_path, 'wb') as dest_file:
                    dest_file.write(file_data)

                print(f"File replicated successfully to storage node {node}")

    except Exception as e:
        print(f"Error during file replication: {e}")


def edit_file_content(filename, role, key, storage_node, all_nodes, unavailable_nodes):
    """Edit file content for admins."""
    if role.lower() != "admin":
        print("Error: Only users with the 'admin' role can edit files.")
        return

    print(f"Editing content of {filename} with role {role}")

    if not filename.endswith('.enc'):
        filename += '.enc'

    #file_path = os.path.join(f"storage_node_{storage_node}", filename)

    file_path = retrieve_file_with_fault_tolerance(filename, storage_node, all_nodes, unavailable_nodes)

    try:
        with open(file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)
        current_content = decrypted_data.decode("utf-8")

        print(f"\nCurrent content of the file:\n{current_content}")


        new_content = input("Enter the content to append:\n")
        updated_content = current_content + "\n" + new_content
        updated_encrypted_data = cipher.encrypt(updated_content.encode("utf-8"))

        print(f"\nYou entered:\n{new_content}")
        confirmation = input("Save changes? (y/n): ").strip().lower()

        if confirmation == 'y':
            new_encrypted_data = cipher.encrypt(new_content.encode("utf-8"))

            with open(file_path, 'wb') as enc_file:
                enc_file.write(updated_encrypted_data)

            print(f"File {filename} encrypted and updated successfully.")

            destination_storage_nodes = [1, 2, 3, 4]  # Example: replicate to storage nodes 2, 3, and 4
            replicate_file_to_other_nodes(file_path, storage_node, destination_storage_nodes, unavailable_nodes)
        else:
            print("Edit operation cancelled.")

    except Exception as e:
        print(f"Error while editing file: {e}")

def main():
    # Set up argparse to take command line arguments
    parser = argparse.ArgumentParser(description="Encrypt and decrypt files using Fernet encryption.")
    parser.add_argument('file_path', help="Path to the encrypted file")
    parser.add_argument('role', choices=['admin', 'viewer'], help="Role of the user (admin/viewer)")
    parser.add_argument('storage_node', type=int, help="Storage node number")
    parser.add_argument('--edit', action='store_true', help="Edit file content (admin only)")
    args = parser.parse_args()

    # Load the encryption key
    key = load_encryption_key()

    if key is None:
        print("Encryption key not found. Please generate the key first.")
        return

    all_nodes = [1, 2, 3, 4]
    unavailable_nodes = [1, 2, 3]  # Nodes that are down

    operation = input("Enter operation (view/edit): ").strip().lower()
    if operation == "view":
        view_file_content(args.file_path, args.role, key, args.storage_node, all_nodes, unavailable_nodes)
    elif operation == "edit":
        edit_file_content(args.file_path, args.role, key, args.storage_node, all_nodes, unavailable_nodes)
    else:
        print("Invalid operation entered. Only 'view' and 'edit' are supported.")

    # Example usage of view_file_content
    #encrypted_file_path = args.file_path  # File path passed from CLI
    #role = args.role  # Role passed from CLI
    #storage_node = args.storage_node  # Storage node passed from CLI

    # Call the function to view the content of the encrypted file (decrypted)
    #view_file_content(encrypted_file_path, role, key, storage_node)

if __name__ == "__main__":
    main()