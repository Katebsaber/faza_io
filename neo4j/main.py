import redis
from redis.client import Redis
import json
import pickle
import requests
from bs4 import BeautifulSoup
from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "faza"))
graph.delete_all()
graph.schema.create_uniqueness_constraint("Product", 'name')

r = redis.Redis(host='localhost', port=6379, db=0)


def get_all_records(r: Redis):
    list_of_products = []
    for key in r.scan_iter("*"):
        list_of_products.append(key.decode("utf-8"))
    return list_of_products


def dk_code_extractor(link: str):
    return link.split('/')[4]


list_of_products = get_all_records(r)

print(len(list_of_products))
# print(list_of_products[0])
# print(json.loads(r.get(list_of_products[0])))

i=1
for each_product in list_of_products:
    try:

        print(i/len(list_of_products))
        parent = json.loads(r.get(each_product))
        parent_link = each_product
        parent_code = dk_code_extractor(parent_link)
        parent_name = parent[0]
        p1 = Node("Product", name=parent_code, alias=parent_name, link=parent_link)
        graph.merge(p1, "Product", "name") 
        for each_similar in parent[1]:
            similar_link = each_similar
            similar_code = dk_code_extractor(similar_link)
            p2 = Node("Product", name=similar_code, link=similar_link)
            graph.merge(p2, "Product", "name") 
            relation = Relationship(p1, "IS_SIMILAR_TO", p2)
            graph.create(relation)
        i+=1
    except Exception as e:
        print(e)
        pass

    # break


# graph.delete_all()

# alice = Node("Person", name="Alice")
# bob = Node("Person", name="Bob")
# alice_knows_bob = Relationship(alice, "KNOWS", bob)
# graph.create(alice_knows_bob)