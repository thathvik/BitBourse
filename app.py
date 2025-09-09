from src.logger import get_logger, setup_logging

# Set's up logging structure for the program before any logger calls 
# (by this point, all the loggers will have been defined in respective modules but not called)
setup_logging()

logger = get_logger(__name__)

def main():
    try:
        # Function or class to help pick between stocks and crypto
        # Help pick the symbol before going forward

        # make API call

        # Turn the price for the symbol
        print(f"Placeholder.")

    except Exception as global_exception:
        logger.error(f"main(): Unable to show the requested information. Global Exception Occured: {global_exception}")

    
if __name__ == "__main__":
    main()
