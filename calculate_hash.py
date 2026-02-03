
import hashlib
import os

def calculate_hash(directory, files_to_include):
    sha256_hash = hashlib.sha256()
    
    paths = []
    
    # Walk directory
    for root, dirs, files in os.walk(directory):
        for names in files:
            paths.append(os.path.join(root, names))
            
    # Add specific files
    for f in files_to_include:
        if os.path.exists(f):
            paths.append(os.path.abspath(f))
            
    paths.sort() # Ensure deterministic order
    
    for path in paths:
        if os.path.isfile(path):
            try:
                with open(path, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
            except Exception as e:
                print(f"Error reading {path}: {e}")
                
    return sha256_hash.hexdigest()

print(calculate_hash("src", ["module.json"]))
