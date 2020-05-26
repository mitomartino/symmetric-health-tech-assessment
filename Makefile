backend/.venv: backend/requirements.txt
	rm -rf backend/.venv
	bash -c "virtualenv -p python3 ./backend/.venv && source ./backend/.venv/bin/activate && pip install -r ./backend/requirements.txt"

frontend/node_modules: frontend/package.json
	cd frontend && yarn install

develop: backend frontend backend/.venv frontend/node_modules
	bash -c "source ./backend/.venv/bin/activate && ./develop.sh"

