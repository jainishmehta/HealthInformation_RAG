import os
def test_app_running():
    script_name = os.environ.get("RAG_MAIN_SCRIPT", "rag_main.py")