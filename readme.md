# Python Tornado client serving as middleware between an ESP32 and a ROS Package

The ESP32 hosts a websocket server. Its IP address is hardcoded into this program, and it can then communicate over the websocket to the ESP32. `roslibpy` is then used to establish 2-way communication over websockets between the ESP32 and ROS. 

# To run

- Rust compiler needed to build roslibpy
- Install Tornado (venv preferred): `python3 -m pip install tornado`
- Install Roslibpy: `pip install roslibpy`
