#!/usr/bin/python3
"""Exports to-do list information for a given employee ID to JSON format."""

import sys
import requests
import json

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

def export_todo_data_to_json(employee_id, todo_data):
    file_name = f'{employee_id}.json'
    employee_todo_data = []

    for task in todo_data:
        employee_todo_data.append({
            'task': task['title'],
            'completed': task['completed'],
            'username': task['userId']
        })

    with open(file_name, 'w') as json_file:
        json.dump({employee_id: employee_todo_data}, json_file, indent=4)

    print(f'TODO list data exported to {file_name}.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    employee_data, todo_data = fetch_employee_data(employee_id)

    display_employee_todo_progress(employee_data['name'], todo_data)
    export_todo_data_to_json(employee_id, todo_data)

