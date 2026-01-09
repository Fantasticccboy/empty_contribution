from github import Github, Auth
from datetime import datetime
import time
import random

def create_github_issue(token, repo_name, title, body=None):
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        
        issue = repo.create_issue(
            title=title,
            body=body
        )
        
        print(f'✓ Issue created successfully!')
        print(f'  Issue URL: {issue.html_url}')
        print(f'  Issue Number: {issue.number}')
        return issue
    except Exception as e:
        print(f'✗ Failed to create issue: {e}')
        return None

def main():
    GITHUB_TOKEN = 'a'
    REPO_NAME = 'Fantasticccboy/empty_contribution'
    
    TOTAL_ISSUES = 150
    BASE_INTERVAL = 30
    RANDOM_DELAY_MAX = 10
    
    print(f'Starting to create {TOTAL_ISSUES} issues...')
    print(f'Base interval: {BASE_INTERVAL} seconds + random delay (0-{RANDOM_DELAY_MAX} seconds)')
    print(f'Press Ctrl+C to stop\n')
    
    for i in range(1, TOTAL_ISSUES + 1):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = f'Auto Issue {i}/{TOTAL_ISSUES} - {timestamp}'
            body = f'This is automatically created issue #{i}\n\nCreated at: {timestamp}\n\nRandom string: {"".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))}'
            
            print(f'\n[{i}/{TOTAL_ISSUES}] Creating issue...')
            issue = create_github_issue(GITHUB_TOKEN, REPO_NAME, title, body)
            
            if issue:
                print(f'  Progress: {i}/{TOTAL_ISSUES} ({i/TOTAL_ISSUES*100:.1f}%)')
            
            if i < TOTAL_ISSUES:
                random_delay = random.uniform(0, RANDOM_DELAY_MAX)
                total_delay = BASE_INTERVAL + random_delay
                print(f'  Waiting {total_delay:.1f} seconds before next issue...')
                time.sleep(total_delay)
                
        except KeyboardInterrupt:
            print(f'\n\nStopped by user. Created {i-1} issues.')
            break
        except Exception as e:
            print(f'✗ Error: {e}')
            print(f'  Waiting 10 seconds before retry...')
            time.sleep(10)
    
    print(f'\n✓ Completed! Total issues created: {min(i, TOTAL_ISSUES)}')

if __name__ == '__main__':
    main()
