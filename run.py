from app import create_app
from config import get_config
from dotenv import load_dotenv

load_dotenv()
app = create_app(get_config())

if __name__ == '__main__':
    app.run(debug=True)
