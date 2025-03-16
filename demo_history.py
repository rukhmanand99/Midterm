"""
Demo script to showcase calculator history management features.
"""
from datetime import datetime, timedelta
from src.calculator import Calculator

def main():
    """Run demo of calculator history features"""
    # Create calculator instance
    calc = Calculator()

    # Perform some calculations
    calc.execute_command('add', 5, 3)
    calc.execute_command('multiply', 4, 2)
    calc.execute_command('subtract', 10, 3)
    calc.execute_command('divide', 15, 3)

    # Show full history
    print("\nFull History:")
    print(calc.get_history())

    # Filter by date range
    yesterday = datetime.now() - timedelta(days=1)
    print("\nHistory from yesterday:")
    print(calc.get_history(start_date=yesterday))

    # Filter by operation
    print("\nMultiplication operations:")
    print(calc.get_history(operation='multiply'))

    # Get history stats
    print("\nHistory Statistics:")
    stats = calc.get_history_stats()
    print(f"Total calculations: {stats['total_calculations']}")
    print(f"Most used operation: {stats['most_used_operation']}")
    print(f"Average result: {stats['average_result']:.2f}")

    # Save history
    calc.save_history('demo_history')
    print("\nHistory saved to demo_history.csv")

    # Clear history
    calc.clear_history()
    print("\nHistory cleared")

    # Load history back
    calc.load_history('demo_history')
    print("\nHistory loaded from demo_history.csv")
    print(calc.get_history())

if __name__ == "__main__":
    main()
