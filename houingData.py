import csv
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

class Property:
    def __init__(self, id, latestPrice, numOfBedrooms, city, latest_saleyear):
        self.id = id
        self.latestPrice = float(latestPrice)
        self.numOfBedrooms = int(numOfBedrooms)
        self.city = city
        self.latest_saleyear = datetime.strptime(latest_saleyear, '%Y')

class BSTNode:
    def __init__(self, property):
        self.property = property
        self.left = None
        self.right = None

class RealEstateAnalyzer:
    def __init__(self):
        self.properties = []
        self.price_bst_root = None

    def load_data(self, filename):
        """Load property data from CSV file"""
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                prop = Property(
                    row['zpid'], 
                    row['latestPrice'], 
                    row['numOfBedrooms'], 
                    row['city'], 
                    row['latest_saleyear']
                )
                self.properties.append(prop)
        print(f"Loaded {len(self.properties)} properties")

    def insert_bst(self, node, property):
        """Recursive function to insert a property into the BST"""
        if node is None:
            return BSTNode(property)
        
        if property.latestPrice < node.property.latestPrice:
            node.left = self.insert_bst(node.left, property)
        else:
            node.right = self.insert_bst(node.right, property)
        
        return node

    def build_price_bst(self):
        """Build a binary search tree based on property prices"""
        self.price_bst_root = None
        for property in self.properties:
            self.price_bst_root = self.insert_bst(self.price_bst_root, property)
        print("Binary Search Tree built successfully")

    def search_by_price_range(self, root, min_price, max_price, results):
        """Recursive function to search for properties in a given price range"""
        if root is None:
            return
        
        if min_price <= root.property.latestPrice <= max_price:
            results.append(root.property)
        
        if min_price < root.property.latestPrice:
            self.search_by_price_range(root.left, min_price, max_price, results)
        
        if max_price > root.property.latestPrice:
            self.search_by_price_range(root.right, min_price, max_price, results)

    def find_properties_in_price_range(self, min_price, max_price):
        """Search for properties in a given price range using BST"""
        results = []
        self.search_by_price_range(self.price_bst_root, min_price, max_price, results)
        return results

    def calculate_average_price_by_location(self):
        """Calculate average prices by location using a dictionary"""
        location_prices = defaultdict(list)
        for prop in self.properties:
            location_prices[prop.city].append(prop.latestPrice)
        avg_prices = {loc: sum(prices) / len(prices) for loc, prices in location_prices.items()}
        return avg_prices

    def find_trends(self):
        """Analyze trends in property values over time"""
        yearly_location_prices = defaultdict(lambda: defaultdict(list))
        for prop in self.properties:
            year = prop.latest_saleyear.year
            yearly_location_prices[year][prop.city].append(prop.latestPrice)
        trends = {}
        for year, locations in yearly_location_prices.items():
            trends[year] = {loc: sum(prices) / len(prices) for loc, prices in locations.items()}
        return trends

    def visualize_data(self):
        """Create visualizations using matplotlib"""
        avg_prices = self.calculate_average_price_by_location()
        plt.figure(figsize=(10, 6))
        plt.bar(avg_prices.keys(), avg_prices.values())
        plt.title('Average Property Prices by Location')
        plt.xlabel('Location')
        plt.ylabel('Average Price ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('avg_prices_by_location.png')
        plt.close()

        trends = self.find_trends()
        plt.figure(figsize=(10, 6))
        for location in set(prop.city for prop in self.properties):
            yearly_prices = [trends[year].get(location, 0) for year in sorted(trends.keys())]
            plt.plot(sorted(trends.keys()), yearly_prices, label=location)
        plt.title('Property Price Trends by Location')
        plt.xlabel('Year')
        plt.ylabel('Average Price ($)')
        plt.legend()
        plt.tight_layout()
        plt.savefig('price_trends.png')
        plt.close()

        print("Visualizations saved: avg_prices_by_location.png and price_trends.png")

def main():
    analyzer = RealEstateAnalyzer()
    analyzer.load_data('/Users/brandonshin/CSE 313E/Project2/austinHousingData.csv')
    analyzer.build_price_bst()

    # Perform analysis
    avg_prices = analyzer.calculate_average_price_by_location()
    trends = analyzer.find_trends()

    # Prompt user for price range
    while True:
        try:
            min_price = float(input("Enter the minimum price: $"))
            max_price = float(input("Enter the maximum price: $"))
            if min_price < 0 or max_price < 0 or min_price > max_price:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter valid positive numbers with max price greater than min price.")

    # Search for properties in the specified price range
    results = analyzer.find_properties_in_price_range(min_price, max_price)

    # Write results to a text file
    with open('property_search_results.txt', 'w') as f:
        f.write(f"Properties between ${min_price:,.2f} and ${max_price:,.2f}:\n\n")
        if results:
            for prop in results:
                f.write(f"ID: {prop.id}, Price: ${prop.latestPrice:,.2f}, Bedrooms: {prop.numOfBedrooms}, Location: {prop.city}, Date Listed: {prop.latest_saleyear.strftime('%Y')}\n")
        else:
            f.write("No properties found in the specified price range.\n")

    print(f"Search results have been written to 'property_search_results.txt'")

    # Generate visualizations
    analyzer.visualize_data()

# Main execution
if __name__ == "__main__":
    main()