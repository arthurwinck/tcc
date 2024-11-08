import subprocess
import sys
import os


def run_mypy():
    result = subprocess.run(
        ["poetry", "run", "mypy", "tcc/api", "tcc/scraper"], check=False
    )
    return result.returncode


def run_scrapy():
    os.chdir("tcc/scraper")
    subprocess.run(["scrapy", "crawl", "conecta-api", "-O", "json/links.json"])


def run_fastapi():
    subprocess.run(["fastapi", "dev", "tcc/api/app.py"])


def run_mypy_then_process(fn):
    if run_mypy() == 0:
        fn()
    else:
        print("Type checking failed. Please fix the errors.")
        sys.exit(1)


def scraper():
    run_scrapy()
    # run_mypy_then_process(run_scrapy)


def api():
    run_mypy_then_process(run_fastapi)
