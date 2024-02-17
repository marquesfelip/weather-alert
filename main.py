from src.app import App


def main():

    App().fetch_and_publish_weather(zip_code="14150-000", country_code="BR")


if __name__ == "__main__":
    main()
