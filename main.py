from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Import necessary libraries
from flask import request, jsonify

# ... Your existing code ...

# Flask route to handle window control
@app.route('/control', methods=['POST'])
def control_window():
    direction = request.form.get('direction')

    if direction == 'open':
        look_around2()  # Call your existing function for opening the window
    elif direction == 'close':
        look_around()   # Call your existing function for closing the window

    return jsonify({'status': 'success'})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



# ... Your existing code ...

# MQTT message handling
def message_arrived(topic, msg):
    print("[INFO] {}{}".format(topic, msg))
    if topic == b'udemedellin/dexteram':
        if msg == b'1':
            print("[INFO] ad dextram")
            look_around2()  # Open the window
    elif topic == b'udemedellin/sinistram':
        if msg == b'1':
            print("[INFO] ad sinistram")
            look_around()   # Close the window
    elif topic == b'udemedellin/declinemus':
        if msg == b'1':
            print("[INFO] ut declinemus")
            apagado()
    # Add more conditions as needed

# ... Your existing code ...



if __name__ == '__main__':
    app.run(debug=True)