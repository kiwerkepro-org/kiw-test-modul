#!/usr/bin/env python3
"""
Autonomous Release Script - KI-WERKE
====================================
Executes the full release chain:
1. Architecture Check (Security/Standards)
2. Linter (checklist.py)
3. Version Bump (Patch)
4. Hashing (Integrity)
5. Git Operations (Tag & Push)
6. Cloud Registration

Usage:
    python .agent/scripts/release.py [--dry-run]
"""

import os
import sys
import json
import hashlib
import subprocess
import argparse
import re
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional

# --- Configuration ---
MODULE_JSON_PATH = Path("module.json")
SRC_DIR = Path("src")
CHECKLIST_SCRIPT = Path(".agent/scripts/checklist.py")
CLOUD_API_URL = "https://zentrale.kiwerke.com/api/v1/register"
ENV_FILE = Path(".env")

# --- Utils ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(text: str):
    print(f"\n{Colors.BLUE}🔄 {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def fail(message: str):
    print_error(message)
    sys.exit(1)

def run_command(cmd: List[str], cwd: Optional[Path] = None, dry_run: bool = False) -> str:
    if dry_run:
        print(f"[DRY-RUN] Executing: {' '.join(cmd)}")
        return ""
    
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        fail(f"Command failed: {' '.join(cmd)}\nError: {e.stderr}")

def load_env() -> Dict[str, str]:
    if not ENV_FILE.exists():
        fail(f".env file not found at {ENV_FILE}")
    
    env_vars = {}
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

# --- Steps ---

def step_1_architecture_check():
    print_step("1. Architecture & Security Check")
    
    forbidden_patterns = [
        (r'wp_remote_get\(', "Use KIW\\Module\\Utils\\ProxyRequest::call() instead of wp_remote_get"),
        (r'wp_remote_post\(', "Use KIW\\Module\\Utils\\ProxyRequest::call() instead of wp_remote_post"),
        (r'curl_init\(', "Direct cURL usage is forbidden"),
        (r'cdn\.jsdelivr\.net', "External CDNs are forbidden"),
        (r'googleapis\.com', "External CDNs are forbidden"),
        (r'[\'"]sk_live_[a-zA-Z0-9]+[\'"]', "Hardcoded Secret Key detected"),
    ]
    
    violations = []
    
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if not file.endswith('.php'):
                continue
                
            file_path = Path(root) / file
            
            # Skip ProxyRequest.php for network function checks
            if file == "ProxyRequest.php":
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                for pattern, msg in forbidden_patterns:
                    if re.search(pattern, content):
                        violations.append(f"{file_path}: {msg}")
            except Exception as e:
                print_error(f"Could not read {file_path}: {e}")

    if violations:
        for v in violations:
            print_error(v)
        fail("Architecture check failed.")
    else:
        print_success("Architecture Hardening passed.")

def step_2_run_linter(dry_run: bool):
    print_step("2. Running Master Checklist")
    if not CHECKLIST_SCRIPT.exists():
        fail(f"Checklist script not found at {CHECKLIST_SCRIPT}")
        
    cmd = [sys.executable, str(CHECKLIST_SCRIPT), "."]
    
    if dry_run:
        print(f"[DRY-RUN] Would run: {' '.join(cmd)}")
        return

    try:
        subprocess.run(cmd, check=True)
        print_success("Linter & Tests passed.")
    except subprocess.CalledProcessError:
        fail("Checklist failed. Fix errors before releasing.")

def step_3_bump_version(dry_run: bool) -> str:
    print_step("3. Bumping Version")
    
    if not MODULE_JSON_PATH.exists():
        fail("module.json not found")
        
    with open(MODULE_JSON_PATH, 'r') as f:
        data = json.load(f)
        
    current_version = data.get('version', '0.0.0')
    major, minor, patch = map(int, current_version.split('.'))
    new_version = f"{major}.{minor}.{patch + 1}"
    
    if dry_run:
        print(f"[DRY-RUN] Would bump version from {current_version} to {new_version}")
        return new_version

    data['version'] = new_version
    
    with open(MODULE_JSON_PATH, 'w') as f:
        json.dump(data, f, indent=4)
        
    print_success(f"Version bumped: {current_version} -> {new_version}")
    return new_version

def step_4_calculate_hash(dry_run: bool) -> str:
    print_step("4. Calculating Checksum")
    
    sha256 = hashlib.sha256()
    file_list = []
    
    # Walk src/
    for root, _, files in os.walk(SRC_DIR):
        for name in sorted(files):
            file_list.append(Path(root) / name)
            
    # Add module.json
    file_list.append(MODULE_JSON_PATH)
    
    for file_path in sorted(file_list):
        if file_path.exists():
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
                    
    final_hash = sha256.hexdigest()
    
    if dry_run:
        print(f"[DRY-RUN] Calculated hash: {final_hash}")
    else:
        print_success(f"Bundle Hash: {final_hash}")
        
    return final_hash

def step_5_git_ops(version: str, dry_run: bool):
    print_step("5. Git Operations")
    
    tag = f"v{version}"
    msg = f"Release {tag} - Autonomous Build"
    
    run_command(["git", "add", "."], dry_run=dry_run)
    run_command(["git", "commit", "-m", msg], dry_run=dry_run)
    run_command(["git", "tag", tag], dry_run=dry_run)
    
    # Check for remote
    try:
        remote_url = run_command(["git", "remote", "get-url", "origin"], dry_run=dry_run)
        if remote_url or dry_run: # If dry run, we assume remote exists or we verify checking code path
             if not remote_url and not dry_run:
                 raise subprocess.CalledProcessError(1, ["git", "remote"]) # Force exception if empty

             run_command(["git", "push", "origin", "main", "--tags"], dry_run=dry_run)
             print_success(f"Pushed to GitHub: {tag}")
    except (subprocess.CalledProcessError, Exception):
        print(f"{Colors.YELLOW}⚠️  No remote 'origin' found. Skipping Push.{Colors.ENDC}")
        print(f"{Colors.YELLOW}ℹ️  Changes committed and tagged ({tag}) locally.{Colors.ENDC}")

def step_6_cloud_registry(version: str, file_hash: str, dry_run: bool):
    print_step("6. Cloud Registration")
    
    env = load_env()
    user = env.get("KIW_CENTRAL_USER")
    password = env.get("KIW_CENTRAL_PASS")
    
    if not user or not password:
        fail("Missing KIW_CENTRAL_USER or KIW_CENTRAL_PASS in .env")
        
    with open(MODULE_JSON_PATH, 'r') as f:
        data = json.load(f)
        slug = data.get('slug', 'unknown-module')
        
    payload = {
        "module": slug,
        "version": version,
        "hash": file_hash
    }
    
    if dry_run:
        print(f"[DRY-RUN] POST {CLOUD_API_URL}")
        print(f"[DRY-RUN] Payload: {json.dumps(payload)}")
        print(f"[DRY-RUN] Auth: {user}:***")
        return

    json_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(CLOUD_API_URL, data=json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    # Basic Auth
    import base64
    auth_str = f"{user}:{password}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    req.add_header("Authorization", f"Basic {auth_b64}")
    
    try:
        with urllib.request.urlopen(req) as response:
            if 200 <= response.status < 300:
                print_success("Registered at Zentrale successfully.")
                print(response.read().decode())
            else:
                fail(f"Cloud Registry returned {response.status}")
    except urllib.error.HTTPError as e:
        # For this hypothetical scenario, we might fail if the central server doesn't exist.
        # But we must try.
        fail(f"Cloud Registry Error: {e.code} - {e.reason}")
    except Exception as e:
        fail(f"Connection Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="KI-WERKE Autonomous Release")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without changing state")
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.CYAN}🚀 KI-WERKE AUTONOMOUS RELEASE{Colors.ENDC}")
    if args.dry_run:
        print(f"{Colors.YELLOW}[DRY RUN MODE ENABLED]{Colors.ENDC}")

    # 1. Architecture
    step_1_architecture_check()
    
    # 2. Linter
    step_2_run_linter(args.dry_run)
    
    # 3. Bump
    new_version = step_3_bump_version(args.dry_run)
    
    # 4. Hash
    file_hash = step_4_calculate_hash(args.dry_run)
    
    # 5. Git
    step_5_git_ops(new_version, args.dry_run)
    
    # 6. Cloud
    step_6_cloud_registry(new_version, file_hash, args.dry_run)
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}✨ RELEASE COMPLETED SUCCESSFULLY{Colors.ENDC}")

if __name__ == "__main__":
    main()
