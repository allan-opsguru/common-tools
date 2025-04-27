import pika
import os
import sys
import ssl

# Get connection parameters from environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST')
rabbitmq_port = os.environ.get('RABBITMQ_PORT', 5671) # Default AMQPS port
rabbitmq_user = os.environ.get('RABBITMQ_USER')
rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
rabbitmq_vhost = os.environ.get('RABBITMQ_VHOST', '/') # Default vhost

# Validate that required environment variables are set
if not all([rabbitmq_host, rabbitmq_user, rabbitmq_password]):
    print("Error: Please set the RABBITMQ_HOST, RABBITMQ_USER, and RABBITMQ_PASSWORD environment variables.")
    sys.exit(1)

print(f"Attempting to connect to RabbitMQ broker at {rabbitmq_host}:{rabbitmq_port}...")

try:
    # Define credentials
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

    # Define connection parameters
    # Ensure SSL is used for Amazon MQ (port 5671)
    ssl_options = None
    if int(rabbitmq_port) == 5671:
        # Create a default SSL context
        context = ssl.create_default_context()
        # You might need to adjust context settings depending on your MQ broker's specific requirements,
        # e.g., loading specific CA certificates if using self-signed or private CAs.
        # context.load_verify_locations(cafile="/path/to/your/ca.pem") # Example
        ssl_options = pika.SSLOptions(context)

    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=int(rabbitmq_port),
        virtual_host=rabbitmq_vhost,
        credentials=credentials,
        ssl_options=ssl_options  # Enable SSL for secure connection
    )

    # Establish connection
    connection = pika.BlockingConnection(parameters)
    print("Successfully connected to RabbitMQ broker!")

    # Close the connection
    connection.close()
    print("Connection closed.")
    sys.exit(0)

except pika.exceptions.AMQPConnectionError as e:
    print(f"Error connecting to RabbitMQ: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
