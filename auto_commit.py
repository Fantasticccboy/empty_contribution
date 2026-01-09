import random
import string
import time
import subprocess
from datetime import datetime

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def append_to_readme(content):
    with open('README.md', 'a', encoding='utf-8') as f:
        f.write(f'\n{content}')

def git_commit_and_push():
    try:
        subprocess.run(['git', 'add', 'README.md'], check=True, capture_output=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f'Auto commit: {timestamp}'
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print(f'✓ Git commit and push successful at {timestamp}')
    except subprocess.CalledProcessError as e:
        print(f'✗ Git operation failed: {e}')

def main():
    print('Starting auto commit script...')
    print('Press Ctrl+C to stop')
    
    while True:
        try:
            random_str = generate_random_string()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = f'[{timestamp}] Random string: {random_str}'
            
            append_to_readme(content)
            print(f'✓ Added to README.md: {content}')
            
            git_commit_and_push()
            
            time.sleep(5)
        except KeyboardInterrupt:
            print('\nStopping script...')
            break
        except Exception as e:
            print(f'✗ Error: {e}')
            time.sleep(5)

if __name__ == '__main__':
    main()
