if hash python3 2>/dev/null; then
	PYTHONPATH=$(pwd) python3 application/app.py
    else
        PYTHONPATH=$(pwd) python application/app.py
    fi
