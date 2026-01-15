from server import create_app
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    create_app().run()
