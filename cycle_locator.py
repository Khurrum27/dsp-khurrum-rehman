from operator import attrgetter

Cycle_arr = [{ "id":1,
 "arrondisment":1,
 "cycle_type":"Mountain",
 "comfort_level":9,
 "status":"available"}, 
 { "id":2,
 "arrondisment":18,
 "cycle_type":"Hybrid",
 "comfort_level":7,
 "status":"available"},
 { "id":3,
 "arrondisment":13,
 "cycle_type":"Road",
 "comfort_level":6,
 "status":"available"},
 { "id":4,
 "arrondisment":3,
 "cycle_type":"Mountain",
 "comfort_level":7,
 "status":"available"},
 { "id":5,
 "arrondisment":4,
 "cycle_type":"Electric",
 "comfort_level":9, 
 "status":"available"},
 { "id":6,
 "arrondisment":5,
 "cycle_type":"Road",
 "comfort_level":5, 
 "status":"booked"}
]

class Cycle:
    """Class to represent a Cycle object."""
    def __init__(self, id, location, type, comfort, status):
        self.id = id
        self.location = location
        self.type = type
        self.comfort = comfort
        self.available = status

    def __str__(self):
        result = "available" if self.available else "booked"
        return f"ID: {self.id}, Location: {self.location}, Type: {self.type}, Comfort: {self.comfort}, Status: {result}"


class LinkedListNode:
    """Node for the linked list to store cycle bookings."""
    def __init__(self, data):
        self.data = data
        self.next = None


class CycleManager:
    def __init__(self):
        self.cycles = Cycle_arr
        self.booking_queue = []  
        self.booking_stack = []  
        self.head = None

    # ------------------------- Display Function ------------------------- #
    def display_cycles(self, cycle_list=None):
        """Display all cycles."""
        if cycle_list is None:
            cycle_list = self.cycles
        print("\nCycles:")
        for cycle in cycle_list:
            print(cycle)

    # ------------------------- Add Cycle ------------------------- #
    def add_cycle(self):
        """Add a new cycle to the list."""
        try:
            cycle_id = int(input("Enter new Cycle ID: "))
            location = int(input("Enter arrondisment (1-20): "))
            cycle_type = input("Enter cycle type (Mountain, Road, Hybrid, Electric): ")
            comfort = int(input("Enter comfort level (1-10): "))
            new_status = input("Enter Cycle Availablity (booked or available): ")

            for cycle in self.cycles:
                if cycle["id"] == cycle_id:
                    print("Error: Cycle ID already exists. Please choose another ID.")
                    return

            new_cycle = {"id": cycle_id, "arrondisment": location, "cycle_type": cycle_type, "comfort_level": comfort , "status": new_status}
            self.cycles.append(new_cycle)
            print("New cycle added successfully!")
        except ValueError:
            print("Invalid input. Please enter the correct data types.")

    
    def delete_cycle(self):
        try:
            cycle_id = int(input("Enter the ID of the cycle to delete: "))

            cycles_copy = self.cycles.copy()
            for cycle in cycles_copy:
                if cycle["id"] == cycle_id:
                    self.cycles.remove(cycle)
                    print(f"Cycle with ID {cycle_id} has been deleted.")
                    return

            print(f"No cycle found with ID {cycle_id}.")
        except ValueError:
            print("Invalid input. Please enter a numeric Cycle ID.")


    def display_cycles(self):
        """Display all cycles."""
        print("\nCycles in the system 2:")
        for cycle in self.cycles:
            print(f"ID: {cycle['id']}, Location: {cycle['arrondisment']}, Type: {cycle['cycle_type']}, Comfort: {cycle['comfort_level']}, Status: {cycle['status']}")

    # ------------------------- Booking Management ------------------------- #
    
    def book_cycle(self):
        try:
            cycle_id = int(input("Enter the ID of the cycle to book: "))
            for cycle in self.cycles:
                if cycle["id"] == cycle_id and cycle["status"] == "available":
                    cycle["status"] = "booked"  
                    self.booking_queue.append(cycle)
                    self.booking_stack.append(cycle)
                    print(f"Cycle {cycle_id} has been successfully booked.")
                    return 
            print(f"Cycle {cycle_id} is not available for booking.")
        except ValueError:
            print("Invalid input. Please enter a numeric Cycle ID.")

    def cancel_last_booking(self):
        """Cancel the last booking (LIFO)."""
        if self.booking_stack:
            cycle = self.booking_stack.pop()
            cycle["status"] = "available"
            self.booking_queue.remove(cycle)
            print(f"Last Booking for Cycle has been cancelled.")
        else:
            print("No bookings to cancel.")
   


    # ------------------------- Search Cycle By Location and Type ------------------------- #
    def search_cycle(self):
        """Search cycles based on location and cycle type."""
        try:
            location = int(input("Enter the location (arrondisment) to search: "))
            cycle_type = input("Enter the cycle type (Mountain, Road, Hybrid, Electric): ").capitalize()

            # Filter cycles that match both condition
            results = []
            for cycle in self.cycles:
                if(cycle["arrondisment"]== location and cycle_type == cycle["cycle_type"]):
                    results.append(cycle)
            if results:
                for result in results:
                    print(f"\nCycles matching Location: {result['arrondisment']} and Type: {result['cycle_type']}")
            else:
                print(f"No cycles found for Location {location} and Type {cycle_type}.")
        except ValueError:
            print("Invalid input. Location must be a number.")

    def sort_by_location(self):
        self.cycles.sort(key=lambda cycle: cycle['arrondisment']) 
        self.display_cycles() 
               

    # ------------------------- Main Menu Methods ------------------------- #
    def main_menu(self):
        """Main menu to manage cycle operations."""
        while True:
            print("\n--- Cycle Management Menu ---")
            print("1. Display all cycles")
            print("2. Add a cycle")
            print("3. Delete a cycle")
            print("4. Search a cycle (by Location & Type)")
            print("5. Book a cycle")
            print("6. Cancel last booking")
            print("7. sort by location")
            print("8. Exit")

            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    self.display_cycles()
                case "2":
                    self.add_cycle()
                case "3":
                    self.delete_cycle()
                case "4":
                    self.search_cycle()
                case "5":
                    self.book_cycle()
                case "6":
                    self.cancel_last_booking()
                case "7":
                    self.sort_by_location()
                case "8":
                    print("Exiting... Goodbye!")
                    break
                case _:
                    print("Invalid choice, try again.")


# ------------------------- Run Application ------------------------- #
if __name__ == "__main__":
    manager = CycleManager()
    manager.main_menu()