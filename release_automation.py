import os
import json
import hashlib
import re
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime

# --- CONFIG ---
MODULE_JSON_PATH = "module.json"
RELEASE_MD_PATH = "release.md"
SRC_DIR = "src"

# --- LINTER ---
def run_linter():
    print("--- 1. Pre-Flight Check (Linter) ---")
    violations = []
    
    # Simple regex patterns
    cdn_pattern = re.compile(r'https?://(cdn|unpkg|fonts\.googleapis|ajax\.googleapis)', re.IGNORECASE)
    # Echo without escaping (very basic heuristic, can have false positives/negatives)
    echo_pattern = re.compile(r'echo\s+\$[a-zA-Z_]', re.IGNORECASE) 
    esc_pattern = re.compile(r'(esc_html|esc_attr|esc_url|wp_kses|json_encode)', re.IGNORECASE)
    
    # Superglobals
    superglobal_pattern = re.compile(r'\$_(POST|GET|REQUEST)', re.IGNORECASE)
    sanit_pattern = re.compile(r'(sanitize_|filter_input|wp_verify_nonce|check_admin_referer)', re.IGNORECASE)

    # Walk src directory
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".php"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        ln = i + 1
                        # CDN Check
                        if cdn_pattern.search(line):
                            violations.append(f"[CDN] {path}:{ln} - External asset detected.")
                        
                        # Echo Check (heuristic)
                        if echo_pattern.search(line) and not esc_pattern.search(line):
                             # Ignore if comments
                            if not re.search(r'//|#|\*', line):
                                violations.append(f"[ESCAPING] {path}:{ln} - Potential unescaped output.")
                        
                        # Superglobal Check
                        if superglobal_pattern.search(line) and not sanit_pattern.search(line):
                             if not re.search(r'//|#|\*', line):
                                violations.append(f"[SANITIZATION] {path}:{ln} - Direct superglobal access without visible sanitization.")

    if violations:
        print("❌ LINTER FAILED:")
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("✅ Linter passed.")

# --- VERSIONING & HASH ---
def update_version_and_hash():
    print("--- 2. Versioning & Hashing ---")
    
    if not os.path.exists(MODULE_JSON_PATH):
        print("❌ module.json not found!")
        sys.exit(1)
        
    with open(MODULE_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    old_version = data.get('version', '1.0.0')
    parts = old_version.split('.')
    if len(parts) == 3:
        parts[2] = str(int(parts[2]) + 1)
        new_version = ".".join(parts)
    else:
        new_version = old_version + ".1"
        
    data['version'] = new_version
    # Ensure architecture is updated to match the commit message standard if older
    if 'system' in data:
         data['system']['architecture'] = "v1.1.2"
    
    print(f"Bumping version: {old_version} -> {new_version}")
    
    # Update module.json FIRST to include it in hash calculation with new version? 
    # Usually hash represents the state of the release. So yes.
    with open(MODULE_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    # Calculate Hash
    sha256 = hashlib.sha256()
    files_to_hash = []
    
    # Add module.json
    files_to_hash.append(MODULE_JSON_PATH)
    
    # Add src files
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            files_to_hash.append(os.path.join(root, file))
            
    files_to_hash.sort()
    
    for fw in files_to_hash:
        try:
            with open(fw, 'rb') as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    sha256.update(chunk)
        except Exception as e:
            print(f"Error checking file {fw}: {e}")
            
    final_hash = sha256.hexdigest()
    print(f"Hash calculated: {final_hash}")
    
    # Update release.md
    release_content = f"""# Release Metadata

- **Version:** {new_version}
- **Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Build Hash (SHA-256):** {final_hash}
- **Architecture:** v1.1.2
- **CMS:** WordPress

## Integrity
The SHA-256 hash above is calculated over:
- `module.json`
- `src/**/*`

## Changelog
- **[UPDATE]** Version bump to {new_version}.
"""
    with open(RELEASE_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(release_content)
        
    return new_version, final_hash, data.get('slug', 'unknown')

# --- GIT ---
def run_git_steps(version):
    print("--- 3. GitHub Automation ---")
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = f"Release v{version} - Architecture v1.1.2"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "tag", f"v{version}"], check=True)
        
        print("Pushing to remote... (This might take a moment)")
        # subprocess.run(["git", "push", "origin", "--tags"], check=True)
        # subprocess.run(["git", "push", "origin", "main"], check=True) 
        # Using a single push command for branch and tags usually works best: git push origin HEAD --tags
        subprocess.run(["git", "push", "origin", "HEAD", "--tags"], check=True)
        
        print("✅ Git operations successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

# --- CLOUD REGISTRATION ---
def register_cloud(slug, version, hash_val):
    print("--- 4. Cloud Registration ---")
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v
    
    user = env_vars.get('KIW_CENTRAL_USER')
    password = env_vars.get('KIW_CENTRAL_PASS')
    
    if not user or not password:
        print("⚠️ Credentials missing in .env. Skipping cloud registration.")
        return False
        
    url = "https://zentrale.kiwerke.com/api/v1/register"
    payload = {
        "module": slug,
        "version": version,
        "hash": hash_val
    }
    data = json.dumps(payload).encode('utf-8')
    
    # Mock request for now as the URL might not be real or reachable in this context,
    # AND I don't want to leak credentials if the environment captures stderr/out loosely.
    # But the user asked for "Vollautomatisch".
    # I will attempt it.
    
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        # Basic Auth needed? Prompt implies loading user/pass but not how to use them.
        # Assuming Basic Auth or Bearer? Or just fields? 
        # Usually user/pass implies Basic Auth.
        # Let's try adding Basic Auth header.
        import base64
        auth_str = f"{user}:{password}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        req.add_header("Authorization", f"Basic {b64_auth}")
        
        # User prompt check: "Sende POST... JSON Payload: {...}". 
        # Doesn't explicitly say how to authenticate other than "Load USER/PASS".
        # I'll assume usage in payload OR headers. Standard is usually headers.
        
        # For safety in this simulation environment, I will PRINT the intent but fail gracefully if URL is unreachable.
        print(f"Sending POST to {url}...")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"Response: {response.getcode()}")
            print(response.read().decode())
            print("✅ Cloud registration successful.")
            return True
            
    except Exception as e:
        print(f"❌ Cloud registration failed: {e}")
        return False

# --- MAIN ---
if __name__ == "__main__":
    run_linter()
    new_ver, f_hash, f_slug = update_version_and_hash()
    
    if run_git_steps(new_ver):
        register_cloud(f_slug, new_ver, f_hash)
        
    print("\n--- 5. Abschlussbericht ---")
    print(f"Module: {f_slug}")
    print(f"Version: {new_ver}")
    print(f"Hash: {f_hash}")
    print("Done.")
