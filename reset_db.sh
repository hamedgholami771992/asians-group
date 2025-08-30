#!/bin/bash

echo -e "\033[36mStarting full Django database reset...\033[0m"

# 1. Remove database file
if [ -f "db.sqlite3" ]; then
    rm -f db.sqlite3
    echo -e "\033[32mRemoved db.sqlite3\033[0m"
else
    echo -e "\033[33mdb.sqlite3 not found, skipping...\033[0m"
fi

# 2. Remove old migration files except __init__.py
dirs=("subscriptions/migrations" "accounts/migrations")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        find "$dir" -type f \( -name "*.py" -o -name "*.pyc" \) ! -name "__init__.py" -exec rm -f {} +
        echo -e "\033[32mCleaned migrations from $dir\033[0m"
    else
        echo -e "\033[33mMigration folder not found: $dir - skipping...\033[0m"
    fi
done

# 3. Recreate migrations
echo -e "\033[36mCreating new migrations...\033[0m"
python manage.py makemigrations accounts
python manage.py makemigrations subscriptions

# 4. Apply migrations
echo -e "\033[36mApplying migrations...\033[0m"
python manage.py migrate

# 5. Suggest superuser creation
echo ""
echo -e "\033[32mReset completed successfully!\033[0m"
echo -e "\033[33m(You may now run: python manage.py createsuperuser)\033[0m"
