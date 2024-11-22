Distributed File System with Fault Tolerance and Encryption

## Description
A scalable and secure distributed file system that ensures reliable storage through fault tolerance, role-based access control, and data encryption. I have done this project as part of my masters project for Distributed Systems.
This Project is just a basic DFS with minimum features, this can be developed further.

## Features
- Fault tolerance through data replication.
- Secure encryption for file storage and retrieval.
- Role-based access control for user security.
- Scalable architecture suitable for distributed environments.

## steps to follow

- Firstly, run the metadata_manager.py. This creates a new metadata folder and metadata database under the folder.
- Then Run encryption_utils.py which generates the encryption key and saves inside metadata folder.
  
To upload file: run dfs.py in CLI  with the command "python dfs.py upload --role <admin/viewer> --file filepath.txt --storage_node <1/2/3>"

To view or edit file  "python file_operations.py "<textfile>.enc" "<admin/viewer>" <node> "
