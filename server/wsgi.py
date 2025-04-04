from server import create_app
from server.extensions import logger

app = create_app()

if __name__ == "__main__":
    try:
        logger.info("App Succesfully Created....")
        app.run(debug=True)
    except BaseException as e:
        logger.error(e)
