# Student Schedule Viewer

A static web app for looking up student revision sessions and exam schedules by Pupil ID.

## Features

- Search by Pupil ID from the browser
- View revision sessions, exam schedule, or all events in one table
- Export the current tab to Excel or PDF
- Load data directly from local JSON files

## Project Files

- `index.html`: main application UI and browser logic
- `student_schedule_data.json`: student revision and exam data used by the app
- `room_schedule_data.json`: supporting room schedule dataset
- `student_schedule_viewer.html`: alternate viewer file kept in the repository

## Run Locally

Because the app uses `fetch()` to load JSON files, run it through a local web server instead of opening the HTML file directly.

### Option 1: Python

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

### Option 2: VS Code Live Server

If you use the Live Server extension, start it from this folder and open the generated local URL.

## Deploy on GitHub Pages

This project is compatible with GitHub Pages because it is a static site.

1. Push this repository to GitHub.
2. In the GitHub repository, open **Settings** > **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the `main` branch and the `/ (root)` folder.
5. Save the settings and wait for GitHub Pages to publish.

Your site will then be available from the GitHub Pages URL shown in the repository settings.

## Notes

- Keep `index.html` and `student_schedule_data.json` in the same folder.
- Large JSON files may make the first page load slower depending on browser and network conditions.
