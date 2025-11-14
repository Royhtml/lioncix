#!/usr/bin/env python3
"""
generate_tokens.py

Generate many unique, working JWT-like tokens signed with HS256 (HMAC-SHA256)
without external libraries.

Outputs:
 - tokens.txt : one token per line
"""

import base64
import hmac
import hashlib
import json
import time
import uuid
import os
import argparse
import sys
from typing import Dict, Optional, List, Tuple, Union


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def b64url_encode(data: bytes) -> str:
    """Base64 URL-safe encoding without padding"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def b64url_decode(s: str) -> bytes:
    """Base64 URL-safe decoding with padding handling"""
    padding = '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)


def json_dumps_compact(obj: Dict) -> bytes:
    """Compact JSON serialization"""
    return json.dumps(obj, separators=(',', ':'), sort_keys=True).encode('utf-8')


def sign_hs256(msg: bytes, secret: bytes) -> bytes:
    """HMAC-SHA256 signing"""
    return hmac.new(secret, msg, hashlib.sha256).digest()


def make_jwt(payload: Dict, secret: bytes, headers: Optional[Dict] = None) -> str:
    """Create a JWT token"""
    if headers is None:
        headers = {"alg": "HS256", "typ": "JWT"}
    
    header_b = json_dumps_compact(headers)
    payload_b = json_dumps_compact(payload)
    
    seg0 = b64url_encode(header_b)
    seg1 = b64url_encode(payload_b)
    signing_input = f"{seg0}.{seg1}".encode('ascii')
    
    sig = sign_hs256(signing_input, secret)
    seg2 = b64url_encode(sig)
    
    return f"{seg0}.{seg1}.{seg2}"


def verify_jwt(token: str, secret: bytes) -> bool:
    """Verify JWT token signature"""
    try:
        segs = token.split('.')
        if len(segs) != 3:
            return False
        
        signing_input = f"{segs[0]}.{segs[1]}".encode('ascii')
        sig = b64url_decode(segs[2])
        expected = sign_hs256(signing_input, secret)
        
        return hmac.compare_digest(sig, expected)
    except Exception:
        return False


def decode_payload(token: str) -> Dict:
    """Decode JWT payload without verification"""
    segs = token.split('.')
    if len(segs) != 3:
        raise ValueError("Invalid token format")
    
    payload_b = b64url_decode(segs[1])
    return json.loads(payload_b.decode('utf-8'))


def linux_banner():
    """Display Linux-style banner"""
    print("""\033[1;32m
=============================================
  ███╗   ██╗██╗██╗     ██╗███╗   ██╗██╗   ██╗
  ████╗  ██║██║██║     ██║████╗  ██║██║   ██║
  ██╔██╗ ██║██║██║     ██║██╔██╗ ██║██║   ██║
  ██║╚██╗██║██║██║     ██║██║╚██╗██║██║   ██║
  ██║ ╚████║██║███████╗██║██║ ╚████║╚██████╔╝
  ╚═╝  ╚═══╝╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
============= HackForge V2.8.7 ===============
 Dev : Dwi Bakti N Dev
==============================================\033[0m""")


def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("\033[1;36m          TOKEN GENERATOR MENU\033[0m")
    print("="*50)
    print("\033[1;33m1.\033[0m Demo Mode (Generate 5 sample tokens)")
    print("\033[1;33m2.\033[0m Quick Generate (100 tokens)")
    print("\033[1;33m3.\033[0m Custom Generate")
    print("\033[1;33m4.\033[0m Bulk Generate (1000+ tokens)")
    print("\033[1;33m5.\033[0m Verify Existing Token")
    print("\033[1;33m6.\033[0m Download/Export Tokens")
    print("\033[1;33m7.\033[0m Settings")
    print("\033[1;33m0.\033[0m Exit")
    print("="*50)


def get_user_choice() -> str:
    """Get user menu choice"""
    while True:
        try:
            choice = input("\n\033[1;35m[\033[0m\033[1;36m*\033[0m\033[1;35m]\033[0m Enter your choice (0-7): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7']:
                return choice
            else:
                print("\033[1;31m[!] Invalid choice. Please enter 0-7.\033[0m")
        except KeyboardInterrupt:
            print("\n\n\033[1;33m[!] Operation cancelled by user.\033[0m")
            sys.exit(0)


def demo_mode():
    """Demo mode with visual output"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Demo Mode - Generating 5 sample tokens...\033[0m\n")
    
    secret = os.urandom(32)
    print(f"\033[1;33m[*] Secret Key: {secret.hex()}\033[0m\n")
    
    for i in range(5):
        payload = {
            "jti": str(uuid.uuid4()),
            "iat": int(time.time()) + i,
            "exp": int(time.time()) + 3600,
            "user": f"user-{i+1}",
            "demo": True
        }
        token = make_jwt(payload, secret)
        print(f"\033[1;32m[$] token_{i+1}:\033[0m {token}\n")
        time.sleep(0.5)
    
    print("\033[1;32m[✓] Demo tokens generated successfully!\033[0m")
    input("\nPress Enter to continue...")


def quick_generate():
    """Quick generate 100 tokens"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Quick Generate - Creating 100 tokens...\033[0m")
    
    results, secret = generate_many_tokens(count=100)
    
    filename = f"tokens_quick_{int(time.time())}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# secret_hex:{secret.hex()}\n")
        for (token,) in results:
            f.write(token + "\n")
    
    print(f"\033[1;32m[✓] Generated 100 tokens to {filename}\033[0m")
    print(f"\033[1;33m[*] Secret: {secret.hex()}\033[0m")
    
    # Show sample
    print("\n\033[1;36m[*] Sample token:\033[0m")
    print(f"{results[0][0]}\n")
    input("Press Enter to continue...")


def custom_generate():
    """Custom token generation with user input"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Custom Token Generation\033[0m")
    
    try:
        count = int(input("\n\033[1;35m[*]\033[0m Enter number of tokens to generate: "))
        ttl = int(input("\033[1;35m[*]\033[0m Enter TTL in hours (default 24): ") or "24")
        
        print("\n\033[1;35m[*]\033[0m Select secret mode:")
        print("   \033[1;33m1.\033[0m Single secret (all tokens use same key)")
        print("   \033[1;33m2.\033[0m Random secret per token")
        mode_choice = input("\033[1;35m[*]\033[0m Enter choice (1/2): ").strip()
        
        secret_mode = 'single' if mode_choice == '1' else 'random_per_token'
        
        print(f"\n\033[1;36m[*] Generating {count} tokens...\033[0m")
        results, secret = generate_many_tokens(
            count=count, 
            secret_mode=secret_mode,
            ttl_seconds=ttl * 3600
        )
        
        filename = f"tokens_custom_{int(time.time())}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            if secret_mode == "single":
                f.write(f"# secret_hex:{secret.hex()}\n")
                for (token,) in results:
                    f.write(token + "\n")
            else:
                f.write("# token\tsecret_hex\n")
                for token, secret_hex in results:
                    f.write(f"{token}\t{secret_hex}\n")
        
        print(f"\033[1;32m[✓] Generated {count} tokens to {filename}\033[0m")
        if secret_mode == 'single':
            print(f"\033[1;33m[*] Secret: {secret.hex()}\033[0m")
        
    except ValueError:
        print("\033[1;31m[!] Invalid input. Please enter numbers only.\033[0m")
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Operation cancelled.\033[0m")
        return
    
    input("\nPress Enter to continue...")


def bulk_generate():
    """Bulk generate 1000+ tokens"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Bulk Token Generation\033[0m")
    
    try:
        count = int(input("\n\033[1;35m[*]\033[0m Enter number of tokens (1000-100000): "))
        if count < 1000:
            count = 1000
        if count > 100000:
            count = 100000
            
        print(f"\n\033[1;36m[*] Generating {count} tokens (this may take a while)...\033[0m")
        
        # Show progress for large generations
        import threading
        done = False
        
        def show_progress():
            dots = 0
            while not done:
                print(f"\r\033[1;33m[*] Generating{'.' * (dots % 4)}   \033[0m", end='')
                dots += 1
                time.sleep(0.5)
        
        progress_thread = threading.Thread(target=show_progress)
        progress_thread.daemon = True
        progress_thread.start()
        
        results, secret = generate_many_tokens(count=count)
        done = True
        
        filename = f"tokens_bulk_{count}_{int(time.time())}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# secret_hex:{secret.hex()}\n")
            for (token,) in results:
                f.write(token + "\n")
        
        print(f"\r\033[1;32m[✓] Generated {count} tokens to {filename}          \033[0m")
        print(f"\033[1;33m[*] File size: {os.path.getsize(filename)} bytes\033[0m")
        
    except ValueError:
        print("\033[1;31m[!] Invalid input.\033[0m")
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Operation cancelled.\033[0m")
        return
    
    input("\nPress Enter to continue...")


def verify_token():
    """Verify an existing token"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Token Verification\033[0m")
    
    token = input("\n\033[1;35m[*]\033[0m Enter token to verify: ").strip()
    secret_hex = input("\033[1;35m[*]\033[0m Enter secret key (hex): ").strip()
    
    try:
        secret = bytes.fromhex(secret_hex)
        is_valid = verify_jwt(token, secret)
        
        if is_valid:
            print("\n\033[1;32m[✓] Token is VALID\033[0m")
            payload = decode_payload(token)
            print("\n\033[1;36m[*] Token Payload:\033[0m")
            for key, value in payload.items():
                print(f"   \033[1;33m{key}:\033[0m {value}")
        else:
            print("\n\033[1;31m[✗] Token is INVALID\033[0m")
            
    except Exception as e:
        print(f"\n\033[1;31m[!] Error: {e}\033[0m")
    
    input("\nPress Enter to continue...")


def download_tokens():
    """Download/export tokens with options"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Download/Export Tokens\033[0m")
    
    # Find token files
    token_files = [f for f in os.listdir('.') if f.startswith('tokens_') and f.endswith('.txt')]
    
    if not token_files:
        print("\n\033[1;31m[!] No token files found.\033[0m")
        input("Press Enter to continue...")
        return
    
    print("\n\033[1;33mAvailable token files:\033[0m")
    for i, filename in enumerate(token_files, 1):
        size = os.path.getsize(filename)
        print(f"   \033[1;33m{i}.\033[0m {filename} ({size} bytes)")
    
    try:
        choice = int(input(f"\n\033[1;35m[*]\033[0m Select file (1-{len(token_files)}): "))
        if 1 <= choice <= len(token_files):
            selected_file = token_files[choice-1]
            
            print(f"\n\033[1;36m[*] Selected: {selected_file}\033[0m")
            print("\n\033[1;35m[*]\033[0m Export options:")
            print("   \033[1;33m1.\033[0m Copy to downloads folder")
            print("   \033[1;33m2.\033[0m Show file content")
            print("   \033[1;33m3.\033[0m Get file info")
            
            export_choice = input("\033[1;35m[*]\033[0m Enter choice (1-3): ").strip()
            
            if export_choice == '1':
                # Copy to downloads (simulated)
                import shutil
                downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads', selected_file)
                shutil.copy2(selected_file, downloads_path)
                print(f"\033[1;32m[✓] Copied to: {downloads_path}\033[0m")
                
            elif export_choice == '2':
                # Show first few lines
                with open(selected_file, 'r') as f:
                    lines = f.readlines()[:10]
                print(f"\n\033[1;36m[*] First 10 lines of {selected_file}:\033[0m")
                for line in lines:
                    print(f"   {line.strip()}")
                if len(lines) == 10:
                    print("   \033[1;33m... (more content truncated)\033[0m")
                    
            elif export_choice == '3':
                # File info
                size = os.path.getsize(selected_file)
                with open(selected_file, 'r') as f:
                    line_count = sum(1 for _ in f)
                print(f"\n\033[1;36m[*] File Info:\033[0m")
                print(f"   \033[1;33mName:\033[0m {selected_file}")
                print(f"   \033[1;33mSize:\033[0m {size} bytes")
                print(f"   \033[1;33mLines:\033[0m {line_count}")
                print(f"   \033[1;33mCreated:\033[0m {time.ctime(os.path.getctime(selected_file))}")
        
    except (ValueError, IndexError):
        print("\033[1;31m[!] Invalid selection.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
    
    input("\nPress Enter to continue...")


def settings_menu():
    """Settings menu"""
    clear_screen()
    linux_banner()
    print("\n\033[1;36m[*] Settings\033[0m")
    
    print("\n\033[1;33mAvailable settings:\033[0m")
    print("   \033[1;33m1.\033[0m Change default output directory")
    print("   \033[1;33m2.\033[0m Set default token count")
    print("   \033[1;33m3.\033[0m Configure token claims")
    print("   \033[1;33m4.\033[0m About")
    
    choice = input("\n\033[1;35m[*]\033[0m Enter choice (1-4): ").strip()
    
    if choice == '4':
        print("\n\033[1;36m[*] About Token Generator:\033[0m")
        print("   \033[1;33mVersion:\033[0m 2.8.7")
        print("   \033[1;33mAuthor:\033[0m Dwi Bakti N Dev")
        print("   \033[1;33mDescription:\033[0m JWT Token Generator with HS256")
        print("   \033[1;33mFeatures:\033[0m")
        print("     - Multiple generation modes")
        print("     - Bulk token creation")
        print("     - Token verification")
        print("     - Export capabilities")
    
    input("\nPress Enter to continue...")


def generate_many_tokens(
    count: int = 1000,
    secret_mode: str = 'single',
    base_secret: Optional[bytes] = None,
    ttl_seconds: int = 60 * 60 * 24
) -> Tuple[List[Tuple[Union[str, Tuple[str, str]]]], Optional[bytes]]:
    """
    Generates `count` tokens.
    """
    out = []
    now = int(time.time())
    
    if secret_mode == 'single' and base_secret is None:
        base_secret = os.urandom(32)

    for i in range(count):
        jti = str(uuid.uuid4())
        iat = now + i
        exp = iat + ttl_seconds
        
        payload = {
            "jti": jti,
            "iat": iat,
            "exp": exp,
            "sub": f"user-{i+1}",
            "role": "user" if (i % 5) else "admin",
            "seq": i + 1
        }

        if secret_mode == 'single':
            token = make_jwt(payload, base_secret)
            out.append((token,))
        else:
            secret = os.urandom(32)
            token = make_jwt(payload, secret)
            out.append((token, secret.hex()))
    
    return out, base_secret


def main():
    """Main function with interactive menu"""
    clear_screen()
    
    while True:
        clear_screen()
        linux_banner()
        show_menu()
        choice = get_user_choice()
        
        if choice == '0':
            print("\n\033[1;32m[✓] Thank you for using Token Generator!\033[0m")
            print("\033[1;36m[*] Goodbye!\033[0m\n")
            break
        elif choice == '1':
            demo_mode()
        elif choice == '2':
            quick_generate()
        elif choice == '3':
            custom_generate()
        elif choice == '4':
            bulk_generate()
        elif choice == '5':
            verify_token()
        elif choice == '6':
            download_tokens()
        elif choice == '7':
            settings_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Program interrupted by user.\033[0m")
        sys.exit(0)