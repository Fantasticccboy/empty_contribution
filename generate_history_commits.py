import subprocess
import random
from datetime import datetime, timedelta

def generate_random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_days)
    
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    
    return random_date.replace(hour=random_hours, minute=random_minutes, second=random_seconds)

def create_empty_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'Created at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    print(f'✓ Created file: {filename}')

def git_add_and_commit(filename, commit_date, commit_message):
    try:
        subprocess.run(['git', 'add', filename], check=True, capture_output=True)
        
        date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
        subprocess.run(['git', 'commit', '-m', commit_message, '--date', date_str], 
                     check=True, capture_output=True)
        
        print(f'✓ Committed: {commit_message}')
        print(f'  Date: {date_str}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'✗ Git operation failed: {e}')
        return False

def push_to_remote():
    try:
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print('✓ Pushed to remote repository')
        return True
    except subprocess.CalledProcessError as e:
        print(f'✗ Push failed: {e}')
        return False

def main():
    NUM_COMMITS = 365
    START_DATE = datetime(2024, 1, 1)
    END_DATE = datetime(2025, 1, 9)
    
    print(f'Generating {NUM_COMMITS} historical commits...')
    print(f'Date range: {START_DATE.strftime("%Y-%m-%d")} to {END_DATE.strftime("%Y-%m-%d")}')
    print(f'Press Ctrl+C to stop\n')
    
    dates = []
    for _ in range(NUM_COMMITS):
        date = generate_random_date(START_DATE, END_DATE)
        dates.append(date)
    
    dates.sort()
    
    for i, commit_date in enumerate(dates, 1):
        try:
            filename = f'history_{i:03d}.txt'
            commit_message = f'Historical commit #{i} - {commit_date.strftime("%Y-%m-%d")}'
            
            print(f'\n[{i}/{NUM_COMMITS}] Creating commit...')
            
            create_empty_file(filename)
            
            if git_add_and_commit(filename, commit_date, commit_message):
                print(f'  Progress: {i}/{NUM_COMMITS} ({i/NUM_COMMITS*100:.1f}%)')
            
        except KeyboardInterrupt:
            print(f'\n\nStopped by user. Created {i-1} commits.')
            break
        except Exception as e:
            print(f'✗ Error: {e}')
            continue
    
    print(f'\n✓ Completed! Total commits created: {len(dates)}')
    print('\nDo you want to push all commits to remote? (y/n): ', end='')
    
    try:
        choice = input().strip().lower()
        if choice == 'y':
            print('\nPushing to remote repository...')
            if push_to_remote():
                print('✓ All commits pushed successfully!')
            else:
                print('✗ Push failed. Please check your git configuration.')
        else:
            print('Skipped pushing to remote.')
    except KeyboardInterrupt:
        print('\nSkipped pushing to remote.')

if __name__ == '__main__':
    main()
