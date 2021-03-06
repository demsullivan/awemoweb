from flask import Flask, request
from ouimeaux.environment import Environment

app = Flask(__name__)
env = Environment()
bridge = None

def target_and_method_for(target_name):
    groups = bridge.bridge_get_groups()
    target, method = None, None
    if target_name in groups.keys():
        target = groups[target_name]
        state_get = bridge.group_get_state
        state_set = bridge.group_set_state
    else:
        lights = bridge.bridge_get_lights()
        if target_name in lights.keys():
            target = lights[target_name]
            state_get = bridge.light_get_state
            state_set = bridge.light_set_state

    return (target, state_get, state_set)

def turn_lights_on(room=None, light=None):
    target_name = room or light
    (target, state_get, state_set) = target_and_method_for(target_name[0])
    method(target, state=1)

def turn_lights_off(room=None, light=None):
    target_name = room or light
    (target, state_get, state_set) = target_and_method_for(target_name[0])
    method(target, state=0)

def dim_lights(level, room=None, light=None):
    target_name = room or light
    (target, state_get, state_set) = target_and_method_for(target_name[0])
    method(target, dim=int(level))
    
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
        return "OK"
    else:
        return "Invalid action."


if __name__ == '__main__':
    env.start()
    env.discover()
    bridge = env.get_bridge('WeMo Link')
    app.run(host='0.0.0.0')