import Application
import AshKetchum
import Agent
from MapGeneration import LEGAL_MOVES

wrestle = True
sumo = True
model = None
width = 20
height = 20
steppies = 100000
if sumo and not wrestle:
    model = Agent.MakeModel(width, height)
    model.load_weights(f"Nets/{width}X{height}-{steppies}.h5f")
    model.compile(optimizer="Adam", loss=['mse'])
app = Application.GameLoop()
if wrestle:
    AshKetchum.Train(app, width, height, LEGAL_MOVES, steppies)
elif not wrestle:
    app.Run(sumo, model)