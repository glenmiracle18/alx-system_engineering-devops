#!/usr/bin/python3
"""Accessing a REST API for todo lists of employees"""

import sys
import requests

def fetch_employee_data(employee_id):
    base_url = 'https://jsonplaceholder.typicode.com'
    employee_url = f'{base_url}/users/{employee_id}'
    todo_url = f'{base_url}/todos?userId={employee_id}'

    try:
        employee_response = requests.get(employee_url)
        todo_response = requests.get(todo_url)

        employee_response.raise_for_status()
        todo_response.raise_for_status()

        employee_data = employee_response.json()
        todo_data = todo_response.json()

        return employee_data, todo_data
    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {e}')
        sys.exit(1)

def display_employee_todo_progress(employee_name, todo_data):
    total_tasks = len(todo_data)
    done_tasks = [task for task in todo_data if task['completed']]
    num_done_tasks = len(done_tasks)

    print(f"Employee {employee_name} is done with tasks({num_done_tasks}/{total_tasks}):")

    for task in done_tasks:
        print(f"\t{task['title']}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    employee_data, todo_data = fetch_employee_data(employee_id)

    display_employee_todo_progress(employee_data['name'], todo_data)

