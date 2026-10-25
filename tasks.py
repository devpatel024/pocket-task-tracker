"""Task tracker. Usage: python3 tasks.py {add TITLE,list,done ID}.
Data is saved to ~/.pocket-tasks.json. Use --file PATH to override.
"""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=Path, default=Path.home() / '.pocket-tasks.json')
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add')
    add.add_argument('title')
    commands.add_parser('list')
    done = commands.add_parser('done')
    done.add_argument('id', type=int)
    args = parser.parse_args()
    try:
        tasks = json.loads(args.file.read_text()) if args.file.exists() else []
        if not isinstance(tasks, list) or any(
            not isinstance(t, dict) or not isinstance(t.get('id'), int)
            or not isinstance(t.get('title'), str) or not isinstance(t.get('done'), bool)
            for t in tasks
        ):
            raise ValueError('Invalid task database')
        if args.command == 'list':
            for task in tasks:
                print(f"{task['id']}: [{'x' if task['done'] else ' '}] {task['title']}")
            if not tasks:
                print('No tasks yet.')
            return
        if args.command == 'add':
            title = args.title.strip()
            if not title:
                parser.error('Task title cannot be empty')
            tasks.append(dict(id=max((t['id'] for t in tasks), default=0) + 1,
                              title=title, done=False))
        else:
            task = next((t for t in tasks if t['id'] == args.id), None)
            if task is None:
                parser.error(f'Task {args.id} does not exist')
            task['done'] = True
        temporary = args.file.with_suffix(args.file.suffix + '.tmp')
        temporary.write_text(json.dumps(tasks, indent=2) + '\n')
        os.replace(temporary, args.file)
        print('Saved.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
