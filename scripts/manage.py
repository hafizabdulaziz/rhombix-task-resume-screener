import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Rhombix ResumeScreener Pro Management CLI")
    parser.add_argument("command", choices=["setup", "run", "test", "seed"], help="Command to execute")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        print("Setting up Rhombix ResumeScreener Pro environment...")
        subprocess.run(".venv\\Scripts\\python -m pip install -e .", shell=True)
        print("Setup completed successfully.")
    elif args.command == "run":
        print("Starting Uvicorn server...")
        subprocess.run(".venv\\Scripts\\uvicorn src.main:app --reload", shell=True)
    elif args.command == "test":
        print("Running test suite...")
        subprocess.run(".venv\\Scripts\\pytest", shell=True)
    elif args.command == "seed":
        print("Seeding initial data...")
        subprocess.run(".venv\\Scripts\\python scripts/seed_data.py", shell=True)

if __name__ == "__main__":
    main()
