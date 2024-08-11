### GitHub Repository Description

**Truck IoT Data Streaming with Spark, Kafka, and Docker**

This project simulates IoT data for a truck traveling between two locations, showcasing real-time data processing using Apache Kafka and Apache Spark Streaming. The entire environment is containerized using Docker, ensuring easy setup and deployment.

![image](https://github.com/user-attachments/assets/82f2f228-9074-4bc4-a8b4-84513fa26ab3)


**Key Features:**
- **IoT Data Simulation:** Generates realistic IoT data representing a truck's journey between two specific locations, including metrics such as location, speed, and fuel consumption.
- **Apache Kafka Integration:** Streams the simulated data in real-time to Apache Kafka topics, providing reliable and scalable data transmission.
- **Apache Spark Streaming:** Processes the data from Kafka using PySpark, applying transformations and aggregations to extract meaningful insights.
- **AWS S3 Storage:** Streams the processed data from Spark to AWS S3 for long-term storage and further analysis.
- **Dockerized Environment:** Utilizes Docker to containerize Kafka and PySpark, ensuring a consistent and reproducible environment across different setups.

**Technologies Used:**
- Docker
- Apache Kafka
- Apache Spark Streaming (PySpark)
- AWS S3
- Python

**Getting Started:**
The repository includes Docker Compose files and detailed instructions for setting up and running the Kafka and PySpark environment. Follow the provided steps to simulate the IoT data and run the complete data pipeline.

_First install all the package inside ther requirements.txt and type your AWS_ACCESS_KEY and AWS_SECRET_KEY inside a file called config.py which you need to create in /jobs folder:_
```
pip install -r requirements.txt
```
_Then run the docker compose file:_
```
docker compose up -d
```
_Next run the simulation code in jobs/main.py:_
```
python3 jobs/main.py
```
_Now submit spark job from to the spark master inside the docker container:_
```
docker exec -it sc-spark-master-1 spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 jobs/spark-city.py
```
_After the a few minutes you will see the data that you produce in main.py file will get streamed to your AWS S3 storage._

---

This project is an excellent resource for learning and demonstrating real-time data streaming, processing, and cloud storage using Docker, open-source tools, and cloud services.
