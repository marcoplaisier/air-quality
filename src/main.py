import json

import paho.mqtt.client as mqtt


def publish_cb(client: mqtt.Client, topic):
    def publish(msg):
        client.publish(topic, json.dumps(msg))

    return publish


# on_connect(): called when the CONNACK from the broker is received. The call could be for a refused connection,
# check the reason_code to see if the connection is successful or rejected.

# on_connect_fail(): called by loop_forever() and loop_start() when the TCP connection failed to establish. This
# callback is not called when using connect() or reconnect() directly. It’s only called following an automatic (
# re)connection made by loop_start() and loop_forever()

# on_disconnect(): called when the connection is closed.

# on_message(): called when a MQTT message is received from the broker.

# on_publish(): called when an MQTT message was sent to the broker. Depending on QoS level the callback is called at
# different moment:

# on_subscribe(): called when the SUBACK is received from the broker

# on_unsubscribe(): called when the UNSUBACK is received from the broker

def on_subscribe(client: mqtt.Client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client: mqtt.Client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def on_connect(client: mqtt.Client, userdata, flags, reason_code, properties):
    client.subscribe("#")
    print(f"connected, {reason_code}")
    device = {
        "name": "Living Room Sensor Hub",
        "identifiers": [
            "rpico co2"
        ]}
    msg = {
        "name": None,
        "device_class": "carbon_dioxide",
        "unit_of_measurement": "ppm",
        "state_topic": "homeassistant/sensor/living-room/state",
        "unique_id": "co2lr",
        "value_template": "{{ value_json.co2 | round(0) }}",
        "expire_after": 120,
        "suggested_area": "Woonkamer",
        "suggested_display_precision": 0,
        " state_class": "measurement",
        "device": device
    }
    client.publish("homeassistant/sensor/co2lr/config", json.dumps(msg))
    msg = {
        "name": None,
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_topic": "homeassistant/sensor/living-room/state",
        "unique_id": "templr",
        "value_template": "{{ value_json.temperature | round(1) }}",
        "expire_after": 120,
        "suggested_area": "Woonkamer",
        "suggested_display_precision": 1,
        " state_class": "measurement",
        "device": device
    }
    client.publish("homeassistant/sensor/templr/config", json.dumps(msg))
    msg = {
        "name": None,
        "device_class": "humidity",
        "unit_of_measurement": "%",
        "unique_id": "humlr",
        "value_template": "{{ value_json.humidity | round(1) }}",
        "suggested_display_precision": 1,
        "state_topic": "homeassistant/sensor/living-room/state",
        "expire_after": 120,
        "suggested_area": "Woonkamer",
        "state_class": "measurement",
        "device": device
    }
    client.publish("homeassistant/sensor/humlr/config", json.dumps(msg))
    publish_state = publish_cb(client, "homeassistant/sensor/living-room/state")
    publish_state({'temperature': 22.4, 'humidity': 66, 'co2': 1101})


def on_message(client: mqtt.Client, userdata, msg):
    pass


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe

client.username_pw_set("mqtt-user", "pFpSlFBpcW{dz,MAQ3Ams}&ad")
client.connect("homeassistant.local", 1883, 60)
client.loop_forever()
