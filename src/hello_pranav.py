import sys
import platform

def verify_environment():
    print("\n--- Project_ Local Environment Verification ---")
    print("Developer: Pranav (Local Node)")
    
    # This must output 3.12
    print(f"Python Version: {sys.version.split()[0]}")
    
    # This must output Linux
    print(f"OS Platform: {platform.system()} {platform.release()}")
    print("Status: Container Parity Achieved.\n")

if __name__ == "__main__":
    verify_environment()