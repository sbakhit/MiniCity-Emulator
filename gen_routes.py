import random
import json

def generate_routes(num_objects, num_points, height, width):
    routes = []
    for i in range(num_objects):
        routes.append({
            "id": str(i), 
            "starting_location": {"x": random.randrange(0, height), "y": random.randrange(0, width)}, 
            "route": []
        })
        x = routes[-1]["starting_location"]["x"]
        y = routes[-1]["starting_location"]["y"]
        for n in range(num_points):
            r = random.randrange(0, 2)
            routes[-1]["route"].append({"x": x + (1 - r), "y": y + r})
            x = routes[-1]["route"][-1]["x"]
            y = routes[-1]["route"][-1]["y"]
    return routes

if __name__ == "__main__":
    routes = generate_routes(10, 5, 1024, 1024)
    routes_json = json.dumps(routes)
    print(routes_json)
