from flask import Flask, request
from ouimeaux.environment import Environment

app = Flask(__name__)
env = Environment()

def turn_lights_on(room):
    # get light
    light.set_state(state=1)

def turn_lights_off(room):
    # get light
    light.set_state(state=0)

def dim_lights(level, room):
    # get light
    light.set_state(dim=int(level))
    
@app.route('/lights/<action>')
def light_control(action):
    method = None

    if action == 'turn_on':
        method = turn_lights_on
    elif action == 'turn_off':
        method = turn_lights_off
    elif action == 'dim':
        method = dim_lights

    if method is not None:
        method(**request.args)
    else:
        return "Invalid action."


if __name__ == '__main__':
    env.start()
    env.discover()
    bridge = env.get_bridge('WeMo Link')
    app.run()