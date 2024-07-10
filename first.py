import json
import requests
from kafka import KafkaProducer, KafkaConsumer

# Fetch data from the Random User Generator API
url = "https://randomuser.me/api/"
data = requests.get(url).json()

# Extract the results from the data
results = data["results"]

# Sort the results by a specific criterion, let's say by first name
sorted_results = sorted(results, key=lambda x: x["name"]["first"])

# Print the sorted results
# print("Sorted Results:")
# print(sorted_results)



# Extracted information
for result in sorted_results:
    extracted_info = {
        "Name": f"{result['name']['title']} {result['name']['first']} {result['name']['last']}",
        "Gender": result['gender'].capitalize(),
        "Email": result['email'],
        "Username": result['login']['username'],
        "Phone": result['phone'],
        "Cell": result['cell'],
        "ID (TFN)": result['id']['value'],
        "Nationality": result['nat'],
        "Picture": result['picture']['large']
    }

    # Printing the extracted information
    for key, value in extracted_info.items():
        print(f"{key}: {value}")

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Serialize sorted results to JSON
# message = json.dumps(sorted_results).encode()  # Serialize message to bytes



message = json.dumps(extracted_info).encode()




# Send serialized message to Kafka topic
topic = 'my_topic'
producer.send(topic, message)

# Create a Kafka consumer
consumer = KafkaConsumer('my_topic', bootstrap_servers='localhost:9092', group_id='my_consumer_group')

# Consume messages from Kafka topic
for message in consumer:
    # Decode consumed message from bytes to JSON
    consumed_message = json.loads(message.value.decode())
    print("Consumed Message:", consumed_message)
    # Add break condition to exit loop after consuming one message
    break

# Close Kafka producer and consumer
producer.close()
consumer.close()
