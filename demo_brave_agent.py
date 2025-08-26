"""Demo script to showcase the Brave API agent capabilities."""
import os
import sys
from dotenv import load_dotenv

# Demo script for Brave Agent

load_dotenv()

def demo_brave_agent():
    """Run a demonstration of the Brave agent with various queries."""
    from brave_agent import ResearchAgent
    
    print("🎯 BRAVE AGENT DEMONSTRATION")
    print("=" * 60)
    
    # Initialize agent
    try:
        agent = ResearchAgent()
        print("✅ Agent initialized successfully!\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Demo queries that showcase different capabilities
    demo_queries = [
        "What are the latest developments in quantum computing in 2024?",
        "Calculate the compound interest on $10000 at 5% for 10 years using the formula A = P(1 + r)^t",
        "What is the current state of AI research in natural language processing?",
        "Find recent research papers about machine learning interpretability",
        "What are the environmental impacts of cryptocurrency mining?"
    ]
    
    print("🔬 Running demonstration queries...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'='*80}")
        print(f"DEMO QUERY {i}: {query}")
        print(f"{'='*80}")
        
        try:
            response = agent.chat(query)
            print(response)
            
            # Add separator between queries
            print(f"\n{'─'*80}")
            input("Press Enter to continue to next demo query...")
            
        except Exception as e:
            print(f"❌ Error during query {i}: {e}")
    
    print(f"\n{'='*80}")
    print("🎉 Demo completed! You can now use the agent interactively.")
    print("Run: python brave_agent.py")
    print(f"{'='*80}")

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 ENVIRONMENT CHECK")
    print("=" * 40)
    
    required_vars = [
        ("GOOGLE_API_KEY", "Google API key for Gemini LLM"),
        ("BRAVE_API_KEY", "Brave Search API key"),
    ]
    
    optional_vars = [
        ("GEMINI_MODEL", "Gemini model name (defaults to gemini-2.5-flash)"),
    ]
    
    all_good = True
    
    print("Required environment variables:")
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        status = "✅ Set" if value else "❌ Not set"
        print(f"  {var_name}: {status} - {description}")
        if not value:
            all_good = False
    
    print("\nOptional environment variables:")
    for var_name, description in optional_vars:
        value = os.getenv(var_name, "default")
        status = f"✅ {value}" if os.getenv(var_name) else "⚠️ Using default"
        print(f"  {var_name}: {status} - {description}")
    
    print("=" * 40)
    
    if all_good:
        print("✅ Environment is properly configured!")
        return True
    else:
        print("❌ Please set the missing environment variables in your .env file")
        return False

if __name__ == "__main__":
    print("🚀 BRAVE AGENT DEMO LAUNCHER")
    print("=" * 50)
    
    # Check environment first
    if not check_environment():
        print("\n📝 To set up environment variables:")
        print("1. Create a .env file in the project root")
        print("2. Add the following lines:")
        print("   GOOGLE_API_KEY=your_google_api_key_here")
        print("   BRAVE_API_KEY=your_brave_api_key_here")
        print("   GEMINI_MODEL=gemini-2.5-flash  # optional")
        sys.exit(1)
    
    print("\n🎯 Choose an option:")
    print("1. Run full demonstration")
    print("2. Test Brave API only")
    print("3. Start interactive agent")
    print("4. Exit")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            demo_brave_agent()
        elif choice == "2":
            print("\n🧪 Running Brave API tests...")
            os.system("python test_brave_api.py")
        elif choice == "3":
            print("\n🤖 Starting interactive agent...")
            os.system("python brave_agent.py")
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice. Please run the script again.")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
