# mtalive
Propagates if a specified executable is currently running or not.
The server will listen on `ADDRESS:PORT/mtalive`

### Preinstalled dependencies
You must have the following packets installed:
- `python3` (tested w/ 3.10.x)
- `git` (update script)

### Install/run/update
To install mtalive, clone the repo and run `update.sh`.
To update mtalive, simply run `update.sh` again.

The script installs/updates the requiered dependencies in a virtual environment.

### Run
Params:
1. `luanti_path` (required)
2. `listening_address` (optional, defaults to `127.0.0.1`)
3. `listening_port` (optional, defaults to `3000`)
(The order of params is important)

```bash
./env/bin/python3 mtalive.py /home/user/luanti/bin/luantiserver 127.0.0.1 3000
```

Fields for a SystemD Unit
```bash
[Service]
WorkingDirectory=/home/user/mtalive
ExecStart=/home/user/mtalive/env/bin/python3 mtalive.py /home/user/luanti/bin/luantiserver 127.0.0.1 3000
```
