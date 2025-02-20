import json
from collections import OrderedDict

# ---------------------------- LRU Cache Implementation ---------------------------- #
class LRUCache:
    def __init__(self, capacity: int):
        """Initialize LRU Cache with a given capacity."""
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str):
        """Retrieve an item from the cache. If found, move it to the end to mark it as recently used."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key: str, value):
        """Insert an item into the cache. If full, remove the least recently used item."""
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Remove the LRU item
        self.cache[key] = value

# ---------------------------- AI Agent with Context Awareness ---------------------------- #
class AIAgent:
    def __init__(self, data_file="Intership-data.json", cache_size=3):
        """Initialize AI agent with caching, context tracking, and load the dataset."""
        self.cache = LRUCache(cache_size)
        self.data = self.load_data(data_file)
        self.context = []  # Store past queries to maintain continuity

    def load_data(self, file_path):
        """Load JSON data from the given file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Data file not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")
            return None

    def get_client_reports(self):
        """Extract and return account balances for each client."""
        if not self.data:
            return "Error: No data loaded."

        reports = {}
        for client in self.data["clients"]:
            reports[client["client_name"]] = {
                year: client[year]["account_balance"]
                for year in client if year.isdigit() 
            }
        return reports

    def get_avg_transaction(self):
        """Calculate and return the average transaction amount per transaction type."""
        if not self.data:
            return "Error: No data loaded."

        transaction_sums = {}
        transaction_counts = {}

        for client in self.data["clients"]:
            for year in client:
                if year.isdigit():
                    for tx in client[year]["transactions"]:
                        desc = tx["description"]
                        transaction_sums[desc] = transaction_sums.get(desc, 0) + tx["amount"]
                        transaction_counts[desc] = transaction_counts.get(desc, 0) + 1

        return {k: round(transaction_sums[k] / transaction_counts[k], 2) for k in transaction_sums}

    def process_query(self, query: str):
        """Process a natural language query and return appropriate data."""
        query = query.lower().strip()

        if len(self.context) > 5:
            self.context.pop(0)
        self.context.append(query)

        if "client reports" in query:
            return self.get_client_reports()

        elif "average transaction" in query:
            return self.get_avg_transaction()

        elif "summary" in query:
            summary = {}
            for past_query in self.context[:-1]:
                if "client reports" in past_query:
                    summary["Client Reports"] = self.get_client_reports()
                elif "average transaction" in past_query:
                    summary["Transaction Insights"] = self.get_avg_transaction()

            return summary if summary else "No past queries to summarize. Try asking about client reports or transactions first."

        else:
            return "Unknown query. Try asking about 'client reports' or 'average transaction amounts'."

    def handle_query(self, query: str):
        """Check cache before processing a query to improve response speed."""
        cached_result = self.cache.get(query)
        if cached_result:
            print(f"[CACHE HIT] Returning cached result for: '{query}'")
            return cached_result
        
        print(f"[CACHE MISS] Processing query: '{query}'")
        response = self.process_query(query)
        self.cache.put(query, response)
        return response

# ---------------------------- Running the AI Agent ---------------------------- #
if __name__ == "__main__":
    agent = AIAgent(cache_size=3)

    queries = [
        "What are the client reports for health data?",
        "Give the average transaction amount for different types of transactions.",
        "What are the client reports for health data?",
        "Fetch user analytics summary.",
    ]

    for q in queries:
        print("\nQuery:", q)
        print("Response:", agent.handle_query(q))

