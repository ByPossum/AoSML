from WrestleWithGymmie import WrestleWithGymmie
import Agent
import numpy

def Train(app, width, height, legalMove, steppies):
    gymmie = WrestleWithGymmie(app, width, height, legalMove)

    worldState = gymmie.observe.shape
    actions = gymmie.actions.shape[0]
    model = Agent.MakeModel(width, height)
    agent = Agent.MakeAgent(model, actions, width*height)
    agent.compile(optimizer="Adam", metrics=['mse'])
    agent.fit(gymmie, nb_steps=steppies, visualize=False, verbose=1)

    agent.save_weights(f"Nets/{width}X{height}-{steppies}.h5f", overwrite=True)
