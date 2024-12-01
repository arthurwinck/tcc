import subprocess
import sys
import os


def run_mypy():
    result = subprocess.run(["poetry", "run", "mypy", "."], check=False)
    return result.returncode


def run_scrapy():
    subprocess.run(["scrapy", "crawl", "conecta-api", "-O", "json/links-stable.json"])


def run_fastapi():
    subprocess.run(["fastapi", "dev", "app.py"])


def run_streamlit():
    subprocess.run(["streamlit", "run " "app.py"])


def run_mypy_then_process(fn):
    if run_mypy() == 0:
        fn()
    else:
        print("Type checking failed. Please fix the errors.")
        sys.exit(1)


def scraper():
    os.chdir("tcc/scraper")
    run_mypy_then_process(run_scrapy)


def api():
    os.chdir("tcc/api")
    run_mypy_then_process(run_fastapi)


def front():
    os.chdir("tcc/frontend")
    run_mypy_then_process(run_streamlit)
