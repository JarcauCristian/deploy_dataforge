import argparse
from neo4j import GraphDatabase

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--addr", type=str, help="Address for deploymnets db!", required=True)
parser.add_argument("-p", "--password", type=str, help="Password for neo4j database!", required=True)
parser.add_argument("-u", "--username", type=str, help="Username for neo4j database!", required=True)

args = parser.parse_args()

class GraphDatabaseManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_graph(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_link_nodes)

    @staticmethod
    def _create_and_link_nodes(tx):
        tx.run("MERGE (b:MainNode {name: 'Base'})")

        categories = ['medicine', 'energy', 'tourism', 'plants', 'technology']
        for category in categories:
            tx.run(
                "MATCH (b:MainNode {name: 'Base'}) "
                "MERGE (c:Category {name: $category}) "
                "MERGE (c)-[:BELONGS_TO]->(b)",
                category=category
            )


graph_db_manager = GraphDatabaseManager(f'bolt://{args.addr}:7687', args.username, args.password)
graph_db_manager.create_graph()
graph_db_manager.close()
