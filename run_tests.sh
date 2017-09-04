source env/bin/activate
pytest -v tests/p1_tests.py
pytest -v tests/p2_tests.py
pytest -v tests/p3_tests.py
pytest -v tests/p4_tests.py
pytest -v tests/state_tests.py
pytest -v tests/tm_tests.py
pytest -v tests/transition_tests.py
deactivate
