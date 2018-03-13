from models.place import Place
from models.state import State
from mcts import UCT

class BusTripPlanner(object):

    def plan(self, departure_point, departure_time, terminal_time, num_iters, top_k=1, min_similarity=0.2):
        origin = Place(None, departure_point)
        is_terminal = lambda s: True if s.time > terminal_time or s.had_food else False
        initial_state = State(origin, departure_time)
        utc = UCT(initial_state, is_terminal)
        history = []

        for iter in range(num_iters):
            reward, leaf, simulated_actions = utc.search()
            history.append((reward, leaf, simulated_actions))

        history.sort(reverse=True, key=lambda x: x[0])
        journeys = []
        visiting_places = []
        for reward, leaf, simulated_actions in history:
            actions = leaf.get_actions_from_root() + simulated_actions
            places = [action.target.id for action in actions]
            similarity = sum([float(p in visiting_places) for p in places]) / len(places)
            if similarity >= min_similarity:
                continue
            visiting_places += places
            itinerary = [action.to_dict() for action in actions]
            journeys.append((reward, itinerary))
            print(leaf, reward)
            if len(journeys) == top_k:
                break

        return journeys

