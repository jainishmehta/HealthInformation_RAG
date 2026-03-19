import runpy
import pytest
import time
import requests
import threading


@pytest.mark.parametrize('script', ['rag_main.py'])
def test_script_execution(script):
    threading.Thread(target=runpy.run_path, args=(script,), daemon=True).start()

    url = "http://127.0.0.1:7860"
    start = time.time()
    while time.time() - start < 30:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)
    else:
        pytest.fail(f"Gradio did not respond at {url} within 30 seconds")

    assert response.status_code == 200