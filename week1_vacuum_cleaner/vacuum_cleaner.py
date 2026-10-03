def reflex_agent(location, status):
    """Returns the action the vacuum cleaner should take based on location and status."""
    if status.lower() == "dirty":
        return "Suck (Clean the dust)"
    elif location.upper() == "A":
        return "Move Right to Location B"
    elif location.upper() == "B":
        return "Move Left to Location A"
    else:
        return "Unknown location or status"

def run_vacuum_simulation():
    print("=== Two-Location Vacuum Cleaner Simulation ===")
    
    # Get user input for Location A and B status
    locations = ['A', 'B']
    environment = {}
    
    for loc in locations:
        environment[loc] = input(f"Enter status for Location {loc} (Dirty/Clean): ").strip()
        
    # Start simulation at Location A
    current_location = 'A'
    print(f"\nVacuum starts at Location {current_location}")
    
    # Process Location A
    status_a = environment[current_location]
    action_a = reflex_agent(current_location, status_a)
    print(f"Location A is {status_a} -> Action: {action_a}")
    
    if status_a.lower() == "dirty":
        environment['A'] = "Clean"
        print("Loca'
    print(f"\nVacuum moves to Location {current_location}")
    status_b = environment[current_location]
    action_b = reflex_agent(current_location, status_b)
    print(f"Location B is {status_b} -> Action: {action_b}")
    
    if status_b.lower() == "dirty":
        environment['B'] = "Clean"
        print("Location B is now Clean.")
        
    print("\n=== Cleaning Complete: Both locations A and B are clean! ===")

# Run the program
if __name__ == "__main__":
    run_vacuum_simulation()tion A is now Clean.")
        
    # Move to Location B
    current_location = 'B
