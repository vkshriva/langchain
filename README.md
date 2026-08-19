# Dockerized Python dev environment

How to build and start:

```bash
docker compose up --build
```

This starts the default Streamlit app, `travelplanner_5/main.py`, at http://localhost:8501.

To run a plain Python example with `docker compose up`, set `APP_MODE=python` and provide the file path with `APP_TARGET`:

```bash
APP_MODE=python APP_TARGET=ex_6/main.py docker compose up --build --abort-on-container-exit
```

The container prints the example output and exits when the script finishes. Use `docker compose up` without `APP_MODE=python` for Streamlit apps.

For the interactive chat app, run the container in attached mode so your keyboard input reaches the Python process:

```bash
APP_MODE=python APP_TARGET=ex_2/main.py docker compose run --rm -it app
```

How to run after editing code without rebuilding:

```bash
docker compose up
```

Run a specific Python file from a subfolder:

```bash
APP_MODE=python APP_TARGET=services/foo/main.py docker compose up --build --abort-on-container-exit
```

For a Streamlit file in any nested folder inside `app/`, change the path and leave the default mode:

```bash
APP_TARGET=tasks/bar/main.py docker compose up
```

Rebuild only when `requirements.txt` changes:

If you change `requirements.txt`, rebuild the image so dependencies are reinstalled:

```bash
docker compose up --build
```

Notes:

- You can add more `.py` files inside the `app/` folder, including nested subfolders.
- Because the entire `app/` folder is mounted as a volume, new files you create on the host will be immediately available inside the container without changing the Dockerfile or compose file.
