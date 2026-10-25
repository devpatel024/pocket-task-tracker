# Pocket Task Tracker

A calm task board for your browser, plus a dependency-free Python command-line companion.

## Browser app

Open `index.html` in a modern browser. No installation, account, API keys, tracking scripts, or external services are needed.

- Organize tasks into To do, In progress, and Completed.
- Add notes, priorities, and due dates; search or filter the board.
- View task counts and completion progress.
- Switch between light and dark themes.
- Export a JSON backup and import it later. Import replaces the board after confirmation.
- Use the responsive layout on desktop or mobile.

Three clearly labeled sample tasks appear on first use. Edit or delete them to make the board your own. Browser tasks are stored locally in that browser and are separate from CLI task data. Clearing browser data can remove them, so export backups. Browser storage behavior for files opened directly can vary; if saving is unavailable, serve the folder with `python3 -m http.server 8000` and open `http://localhost:8000`.

The app does not connect to GitHub, handle credentials, process payments, or promise profile achievements or income.

## CLI quick start

Requires Python 3.10 or newer. No packages or account registration needed.

```sh
git clone https://github.com/devpatel024/pocket-task-tracker.git
cd pocket-task-tracker
python3 tasks.py add "Ship my first project"
python3 tasks.py add "Write documentation"
python3 tasks.py list
python3 tasks.py done 1
python3 tasks.py list
```

On Windows, use `py` instead of `python3` if needed.

Example output after completing task 1:

```text
1: [x] Ship my first project
2: [ ] Write documentation
```

## Data storage

The default database is `~/.pocket-tasks.json`. For a separate task list, place `--file` before the command:

```sh
python3 tasks.py --file work-tasks.json add "Review the release"
python3 tasks.py --file work-tasks.json list
```

The parent directory must already exist. Task IDs stay stable. Empty titles and unknown IDs are rejected. Malformed databases produce an error instead of being overwritten.

Keep personal task databases out of Git. The app is intended for one local user; simultaneous writes are not supported. Back up important task data.

## Run tests

```sh
python3 -m unittest -v
```

Tests use temporary databases and cover persistence across processes, Unicode titles, completion, invalid commands, malformed database preservation, and empty lists.

## Contributing

Open an issue describing the behavior you want to improve, or propose a focused pull request. Include a reproduction or example and run the tests before submitting. Useful next features include due dates, filtering completed tasks, and export.
