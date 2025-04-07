from agent import Agent

def main():
    """Main entry point of the Roomba cleaning simulation."""
    agent = Agent("The Cleaner")
    print(agent)
    agent.run()

if __name__ == "__main__":
    main()
