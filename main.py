from ai2thor.controller import Controller
import time
import torch
import util
import lifelonglearning as ll
from tqdm import tqdm

# Some global variables
Buffer = []
BufferStream = []

# Learning threshold
threshold = 0.05

# Training the interactive agent in the ai2thor environments
def train(controller, environments):
    for environment in tqdm(environments, desc="Training the model on the environments"):
        # Init this environment's buffer memory to empty
        M = []
        # Reset the controller to the new environment
        # controller.reset(scene=environment)
        event = controller.step("MoveAhead")
        
        # Initial state
        state = util.State(controller.last_event.metadata)
        with open("ExampleState.json", "w+") as f:
            f.write(repr(state))
        
        return

        # Run this environment actions for 100 seconds
        startTime = time.perf_counter()
        while(time.perf_counter() - startTime < 100):
            # Determine action
            action = ll.InitialPolicy(state)
            transition = util.Transition(state, action)

            # Execute action
            event = controller.step(action.actionType)
            if (not event.metadata["lastActionSuccess"]):
                # Handle an unsuccessful action
                pass
            
            BufferStream.append(transition)

            # Select s_p and a_p from BufferStream
            if (ll.D(transition) < ll.threshold):
                newTransition = ll.A_correct(state, BufferStream)
                M.append(newTransition)

            newState = util.State(event.metadata)
            state = newState
        
        # Lifelong Learning Componenet
        theta_k = ll.A_cl()
        
# Let's test the agent in the ai2thor environments
def test():
    successRate = 0
    return successRate

def main():
    controller = Controller(
        agentMode = "locobot",
        visibilityDistance=1.5,
        scene="FloorPlan1",
        gridSize=0.25,
        movementGaussianSigma = 0,
        rotateStepDegress=90,
        rotateGaussianSigma = 0,
        fieldOfView = 90
    )
    # Add all iThor scenes
    kitchens = [f"FloorPlan{i}" for i in range(1, 31)]
    living_rooms = [f"FloorPlan{200 + i}" for i in range(1, 31)]
    bedrooms = [f"FloorPlan{300 + i}" for i in range(1, 31)]
    bathrooms = [f"FloorPlan{400 + i}" for i in range(1, 31)]

    environments = kitchens + living_rooms + bedrooms + bathrooms
    train(controller, environments)
    test()

    return

if __name__ == '__main__':
    main()