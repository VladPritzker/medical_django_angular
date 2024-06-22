import os
from datetime import datetime

def backup_mysql_db():
    db_name = 'myproject'
    db_user = 'pritzker'
    db_password = 'Test11!!'
    db_host = 'localhost'
    db_port = '3306'

    now = datetime.now()
    backup_dir = "/Users/vladbuzhor/Library/Mobile Documents/com~apple~CloudDocs/Vlad/Study/Study/Django_Angular_React_finance /angular_django"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{now.strftime('%Y%m%d_%H%M%S')}.sql")

    command = f"mysqldump -u {db_user} -p{db_password} -h {db_host} -P {db_port} {db_name} > {backup_file}"
    os.system(command)
    print(f"Backup completed: {backup_file}")

if __name__ == '__main__':
    backup_mysql_db()
