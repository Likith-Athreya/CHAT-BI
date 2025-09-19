import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent))

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bi_agent.log')
        ]
    )

def check_environment():
    """Check if all required environment variables are set."""
    load_dotenv()
    
    required_vars = ['GROQ_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("See env_example.txt for reference.")
        return False
    
    return True

def create_sample_database():
    """Create sample database if it doesn't exist."""
    from sample_data import SampleDataGenerator
    from config import Config
    
    db_url = Config.DATABASE_URL
    print("📊 Creating sample database...")
    generator = SampleDataGenerator(db_url)
    try:
        generator.create_sample_database()
        print("✅ Sample database created successfully!")
    finally:
        generator.close()

def main():
    """Main function to start the BI Agent."""
    print("🚀 Starting Business Intelligence Agent...")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if not check_environment():
        sys.exit(1)
    
    if os.getenv("SEED_SAMPLE_DATA", "False").lower() == "true":
        create_sample_database()
    
    try:
        import streamlit.web.cli as stcli
        
        os.environ['STREAMLIT_SERVER_PORT'] = '8501'
        os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        
        print("🌐 Starting web interface...")
        print("📱 Open your browser and go to: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the server")
        
        target_app = os.getenv("BI_APP", "app.py")
        if not os.path.exists(target_app):
            target_app = "main.py"
        sys.argv = ["streamlit", "run", target_app]
        stcli.main()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down BI Agent...")
        logger.info("Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        logger.error(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
