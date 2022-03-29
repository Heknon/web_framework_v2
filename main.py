import logging

from web_framework_v2 import framework

app: framework.Framework = framework.Framework(
    static_folder="",
    static_url_path="",
    host="localhost",
    port=80,
    log_level=logging.INFO
)


def main():
    app.start()


if __name__ == '__main__':
    main()
