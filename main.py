import subprocess

def main():
    # Run the URL processing script
    subprocess.run(['python', 'process_url.py'])

    # Run the additional data script
    subprocess.run(['python', 'additional_task.py'])

if __name__ == '__main__':
    main()
