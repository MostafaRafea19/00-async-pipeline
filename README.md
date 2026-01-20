A high-performance asynchronous task processing system. This microservice architecture decouples long-running operations (like video processing or email sending) from the main HTTP request/response cycle using **Flask**, **Celery**, and **Redis**.

## **🚀 Features**

* **Non-Blocking API:** Returns 202 Accepted immediately, ensuring the UI never hangs.  
* **Distributed Task Queue:** Uses Redis to broker messages between the API and Workers.  
* **Background Workers:** Dedicated Celery processes handle heavy lifting independently.  
* **State Management:** API endpoints to poll for task status (PENDING vs SUCCESS) and retrieve results.

## **⚙️ Architecture**

1. **Producer (Flask):** Receives the request $\\rightarrow$ Pushes job to Redis $\\rightarrow$ Returns ID.  
2. **Broker (Redis):** Holds the queue of pending jobs.  
3. **Consumer (Celery):** Picks up jobs from Redis $\\rightarrow$ Executes logic $\\rightarrow$ Saves result.

## **🛠️ Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/YOUR\_USERNAME/00-async-pipeline.git\](https://github.com/YOUR\_USERNAME/00-async-pipeline.git)  
   cd 00-async-pipeline

2. **Set up the Virtual Environment:**  
   python3 \-m venv .venv  
   source .venv/bin/activate

3. **Install Dependencies:**  
   pip install \-r requirements.txt

4. ⚠️ Prerequisite: Redis  
   You must have a Redis server running locally.  
   * **Mac (Homebrew):** brew services start redis  
   * **Docker:** docker run \-d \-p 6379:6379 redis

## **🏃‍♂️ Usage (The Two-Terminal Setup)**

Since this is a distributed system, you need **two** terminal windows running simultaneously.

### **Terminal 1: The Background Worker**

This process listens to the queue and executes the heavy tasks.

celery \-A tasks.celery\_app worker \--loglevel=info

### **Terminal 2: The API Server**

This process handles incoming HTTP requests.

flask run

## **🔌 API Endpoints**

### **1\. Trigger a Job**

POST /start-task  
Simulate a heavy task by defining how long it should "sleep".  
**Request:**

{  
  "duration": 10  
}

**Response (Immediate):**

{  
  "message": "Job received. Processing in background.",  
  "task\_id": "c8455d39-6500-4820-9923-281515945100"  
}

### **2\. Check Status**

**GET** /result/\<task\_id\>

**Response (While Processing):**

{  
  "state": "PENDING",  
  "status": "Job is still processing..."  
}

**Response (When Complete):**

{  
  "state": "SUCCESS",  
  "result": "Processed for 10 seconds."  
}

## **📚 Technical Stack**

* **Python 3.x**  
* **Flask:** REST API  
* **Celery:** Distributed Task Queue  
* **Redis:** In-memory Data Structure Store (Broker & Backend)