# debug_state.py - run this separately
import base64
from Agent.Nodes import *
from Agent.Graph import *

graph = CivicIssueAgent()

with open(r"C:\Users\fatim\Downloads\road_pothole.jpg", "rb") as img:
    encoded = base64.b64encode(img.read()).decode()
def run():
    # Load image as base64
    with open(r"C:\Users\fatim\Downloads\road_pothole.jpg", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    image_base64 = f"data:image/jpeg;base64,{encoded}"

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    initial_input = {
        "issueimage": image_base64,
        "userEmail": "diya@gmail.com",
        "location": "Sector 15 Chandigarh",
    }

    print("\n--- Starting Agent ---\n")

    # Stream execution from the graph
    for event in graph.stream(initial_input, config=config, stream_mode="updates"):
        node_name = list(event.keys())[0]
        output = event[node_name]
        print(f"🔵 NODE: {node_name}")
        print("OUTPUT:", output, "\n")

    # Loop until the agent finishes
    while True:
        state = graph.get_state(config)

        # If graph is waiting at a human-in-the-loop node (like HumanConfirm)
        if state.next and any("Human" in n for n in state.next):
            # The node itself will handle input and update state
            print(f"⚠️ Waiting for Human Input at: {state.next}")
            
            # Resume streaming to let HumanConfirm node ask for input
            for event in graph.stream(None, config=config, stream_mode="updates"):
                node_name = list(event.keys())[0]
                output = event[node_name]
                print(f"🔵 NODE: {node_name}")
                print("OUTPUT:", output, "\n")

        # If no next nodes, execution is finished
        elif not state.next:
            print("\n✅ Agent completed.")
            print("Email Sent:", state.values.get("emailSend"))
            print("Issue Saved:", state.values.get("issueSaved"))
            break
        else:
            print("⚠️ Waiting at:", state.next)
            break

if __name__ == "__main__":
    run()