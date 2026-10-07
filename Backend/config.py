import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# ============================================================
# ARIVORA AI - CONFIGURATION
# "Your Syllabus. Your Books. Your AI."
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

STUDENT_DIR = UPLOAD_DIR / "students"
FACULTY_DIR = UPLOAD_DIR / "faculty"

INDEX_DIR = DATA_DIR / "indexes"
VOICE_DIR = DATA_DIR / "voice_notes"
EXAM_DIR = DATA_DIR / "exams"
QUIZ_DIR = DATA_DIR / "quizzes"
TIMETABLE_DIR = DATA_DIR / "timetable"

# Ensure all directories exist
for folder in [
    DATA_DIR,
    UPLOAD_DIR,
    STUDENT_DIR,
    FACULTY_DIR,
    INDEX_DIR,
    VOICE_DIR,
    EXAM_DIR,
    QUIZ_DIR,
    TIMETABLE_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)

# Standardized Subject Names and Keywords
SUBJECT_CATALOG = {
    "computer networks": {
        "folder": "Computer_Networks",
        "name": "Computer Networks",
        "code": "CS8591",
        "units": [
            {"unit": 1, "title": "Introduction & Physical Layer", "topics": ["network edge", "network core", "delay", "loss", "throughput", "osi model", "tcp/ip suite", "physical media"]},
            {"unit": 2, "title": "Data Link Layer & LANs", "topics": ["error detection and correction", "crc", "parity", "hamming code", "framing", "multiple access protocols", "csma/cd", "csma/ca", "ethernet", "vlans", "mac addressing"]},
            {"unit": 3, "title": "Network Layer & Routing", "topics": ["ip addressing", "ipv4", "ipv6", "subnetting", "cidr", "nat", "routing algorithms", "dijkstra", "distance vector", "link state", "bgp", "ospf", "rip"]},
            {"unit": 4, "title": "Transport Layer", "topics": ["transport layer services", "multiplexing", "demultiplexing", "udp", "tcp", "reliable data transfer", "flow control", "sliding window", "congestion control", "tcp tahoe", "tcp reno"]},
            {"unit": 5, "title": "Application Layer & Security", "topics": ["dns", "domain name system", "http", "https", "ftp", "smtp", "pop3", "imap", "socket programming", "cryptography", "firewalls"]}
        ]
    },
    "dbms": {
        "folder": "DBMS",
        "name": "Database Management Systems",
        "code": "CS8492",
        "units": [
            {"unit": 1, "title": "Database Architecture & ER Model", "topics": ["database system concepts", "three tier architecture", "data independence", "data models", "entity relationship model", "er diagrams", "extended er features"]},
            {"unit": 2, "title": "Relational Model & Relational Algebra", "topics": ["relational data model", "relational algebra", "tuple relational calculus", "sql fundamentals", "ddl", "dml", "dcl", "joins", "subqueries", "views", "integrity constraints"]},
            {"unit": 3, "title": "Database Design & Normalization", "topics": ["functional dependencies", "anomalies in design", "1nf", "first normal form", "2nf", "second normal form", "3nf", "third normal form", "bcnf", "boyce codd normal form", "4nf", "lossless decomposition"]},
            {"unit": 4, "title": "Transaction Management & Concurrency", "topics": ["transaction concepts", "acid properties", "serializability", "conflict serializable", "concurrency control", "two phase locking", "2pl", "deadlock detection and prevention", "timestamp ordering"]},
            {"unit": 5, "title": "Storage, Indexing & Query Processing", "topics": ["file organization", "b tree", "b+ tree", "hashing", "query processing steps", "query optimization", "nosql databases", "mongodb", "distributed databases"]}
        ]
    },
    "operating systems": {
        "folder": "Operating_Systems",
        "name": "Operating Systems",
        "code": "CS8493",
        "units": [
            {"unit": 1, "title": "OS Overview & System Structures", "topics": ["operating system services", "system calls", "os structure", "monolithic", "microkernel", "virtual machines", "boot process"]},
            {"unit": 2, "title": "Processes & CPU Scheduling", "topics": ["process concept", "pcb", "process states", "context switching", "threads", "multithreading models", "cpu scheduling algorithms", "fcfs", "sjf", "round robin", "priority scheduling", "multilevel queue"]},
            {"unit": 3, "title": "Process Synchronization & Deadlocks", "topics": ["critical section problem", "peterson's solution", "semaphores", "monitors", "classic synchronization problems", "dining philosophers", "producer consumer", "deadlocks", "deadlock conditions", "banker's algorithm", "deadlock detection and recovery"]},
            {"unit": 4, "title": "Memory Management", "topics": ["swapping", "contiguous memory allocation", "paging", "page table", "tlb", "segmentation", "virtual memory", "demand paging", "page replacement algorithms", "fifo", "lru", "optimal", "thrashing"]},
            {"unit": 5, "title": "Storage & File Systems", "topics": ["file concepts", "access methods", "directory structure", "file system implementation", "disk scheduling algorithms", "fcfs", "sstf", "scan", "c-scan", "look", "c-look", "raid levels"]}
        ]
    },
    "data structures": {
        "folder": "Data_Structures",
        "name": "Data Structures & Algorithms",
        "code": "CS8391",
        "units": [
            {"unit": 1, "title": "Linear Data Structures - Arrays & Linked Lists", "topics": ["abstract data types", "arrays", "singly linked list", "doubly linked list", "circular linked list", "applications of linked lists", "polynomial addition"]},
            {"unit": 2, "title": "Stacks & Queues", "topics": ["stack adt", "array and linked list implementation of stack", "infix to postfix conversion", "postfix evaluation", "queue adt", "circular queue", "priority queue", "deque", "applications of queues"]},
            {"unit": 3, "title": "Non-Linear Data Structures - Trees", "topics": ["tree terminology", "binary trees", "binary tree traversals", "inorder", "preorder", "postorder", "binary search tree", "bst operations", "avl trees", "b-trees", "heaps", "priority queue"]},
            {"unit": 4, "title": "Graphs", "topics": ["graph representations", "adjacency matrix", "adjacency list", "graph traversals", "bfs", "breadth first search", "dfs", "depth first search", "topological sorting", "minimum spanning tree", "prim's algorithm", "kruskal's algorithm", "shortest path", "dijkstra's algorithm"]},
            {"unit": 5, "title": "Searching & Sorting", "topics": ["linear search", "binary search", "hashing", "hash functions", "collision resolution", "bubble sort", "insertion sort", "selection sort", "merge sort", "quick sort", "heap sort"]}
        ]
    },
    "python": {
        "folder": "Python",
        "name": "Python Programming",
        "code": "GE8151",
        "units": [
            {"unit": 1, "title": "Algorithmic Problem Solving & Python Basics", "topics": ["algorithms", "flowcharts", "pseudo code", "python data types", "variables", "operators", "expressions", "input and output"]},
            {"unit": 2, "title": "Control Flow & Functions", "topics": ["conditionals", "if elif else", "loops", "for loop", "while loop", "break continue pass", "functions", "parameters", "arguments", "recursion", "lambda functions"]},
            {"unit": 3, "title": "Compound Data - Lists, Tuples, Dictionaries", "topics": ["lists", "list operations", "slicing", "list comprehension", "tuples", "tuple assignment", "dictionaries", "dictionary operations", "sets"]},
            {"unit": 4, "title": "Strings & Files", "topics": ["string formatting", "string methods", "file handling", "reading and writing files", "file modes", "command line arguments", "modules", "packages"]},
            {"unit": 5, "title": "OOP & Exception Handling", "topics": ["classes", "objects", "methods", "inheritance", "polymorphism", "encapsulation", "exception handling", "try except finally", "custom exceptions"]}
        ]
    },
    "aptitude": {
        "folder": "Aptitude",
        "name": "Quantitative & Logical Aptitude",
        "code": "APT101",
        "units": [
            {"unit": 1, "title": "Percentages & Basic Arithmetic", "topics": ["percentages", "percentage increase decrease", "fractions to percentage", "percentage calculation", "averages", "hcf and lcm", "number system", "simplification"]},
            {"unit": 2, "title": "Time & Work and Commercial Math", "topics": ["time & work", "time and work", "work and wages", "pipes and cisterns", "efficiency", "man-days formula", "profit and loss", "simple interest", "compound interest", "ratio and proportion", "partnership"]},
            {"unit": 3, "title": "Data Interpretation", "topics": ["data interpretation", "bar charts", "pie charts", "tables", "line graphs", "caselet di", "data analysis"]},
            {"unit": 4, "title": "Logical Reasoning", "topics": ["logical reasoning", "syllogisms", "blood relations", "seating arrangement", "coding decoding", "series completion", "direction sense", "clocks and calendars"]},
            {"unit": 5, "title": "Verbal Ability & Quantitative Aptitude", "topics": ["verbal ability", "quantitative aptitude", "reading comprehension", "sentence correction", "synonyms and antonyms", "para jumbles", "time speed and distance", "trains", "boats and streams", "permutations and combinations", "probability", "mensuration"]}
        ]
    },
    "coding": {
        "folder": "Coding",
        "name": "Programming & Coding",
        "code": "CODE101",
        "units": [
            {"unit": 1, "title": "C Programming & Memory Management", "topics": ["c programming", "c language", "pointers", "dynamic memory allocation", "malloc", "calloc", "free", "structures", "unions", "file handling in c", "compilation steps"]},
            {"unit": 2, "title": "C++ & Object-Oriented Programming", "topics": ["c++", "cpp", "oops in c++", "classes and objects", "constructors", "inheritance", "polymorphism", "encapsulation", "abstraction", "virtual functions", "templates", "stl", "standard template library"]},
            {"unit": 3, "title": "Java Programming", "topics": ["java", "jvm", "jre", "jdk", "java oops", "interfaces", "abstract class", "packages", "exception handling in java", "multithreading in java", "java collections", "arraylist", "hashmap"]},
            {"unit": 4, "title": "Python Programming", "topics": ["python", "python programming", "python data types", "lists tuples dicts", "functions", "lambda", "list comprehension", "decorators", "generators", "oops in python", "file handling in python"]},
            {"unit": 5, "title": "Data Structures, Algorithms & Web Development", "topics": ["data structures", "algorithms", "arrays", "linked lists", "stacks", "queues", "binary trees", "graphs", "sorting algorithms", "searching algorithms", "time complexity", "big o", "web development", "html", "html5", "css", "css3", "javascript", "dom manipulation", "fetch api", "rest api", "responsive design", "bootstrap"]}
        ]
    },
    "multimedia and animation": {
        "folder": "MMA",
        "name": "Multimedia and Animation",
        "code": "CS8080",
        "units": [
            {"unit": 1, "title": "Introduction to Multimedia & Graphics", "topics": ["multimedia fundamentals", "graphics", "bitmap", "vector graphics", "color models", "rgb", "cmyk", "image formats", "jpeg", "png", "gif", "resolution"]},
            {"unit": 2, "title": "Principles of Animation & Motion", "topics": ["animation", "principles of animation", "traditional animation", "2d animation", "3d animation", "stop motion", "keyframing", "tweening", "morphing", "onion skinning", "frame rate", "fps", "squash and stretch", "timing and spacing"]},
            {"unit": 3, "title": "Audio & Sound Processing", "topics": ["audio digitizing", "sampling rate", "midi", "quantization", "audio compression", "mp3", "wav", "digital audio workstation", "sound effects"]},
            {"unit": 4, "title": "Video Technology & Compression", "topics": ["analog video", "digital video", "broadcast standards", "ntsc", "pal", "video compression", "mpeg", "h.264", "mp4", "video editing", "streaming"]},
            {"unit": 5, "title": "Multimedia Authoring & Web Delivery", "topics": ["multimedia authoring tools", "hypermedia", "interactive multimedia", "virtual reality", "augmented reality", "web animation", "svg animation", "blender", "adobe animate"]}
        ]
    },
    "big data analytics": {
        "folder": "Big_Data_Analysis",
        "name": "Big Data Analysis",
        "code": "23CSE18",
        "units": [
            {"unit": 1, "title": "Introduction to Big Data & Hadoop", "topics": ["big data overview", "hadoop architecture", "hdfs", "namenode", "datanode", "hadoop ecosystem", "data integrity in hadoop"]},
            {"unit": 2, "title": "Data Serialization & File Formats", "topics": ["avro", "data serialization", "sequence files", "rcfile", "parquet", "orc", "compression formats"]},
            {"unit": 3, "title": "MapReduce Architecture & Workflow", "topics": ["mapreduce workflow", "map phase", "shuffle and sort", "reduce phase", "classic mapreduce vs yarn", "yarn architecture", "resource manager", "node manager"]},
            {"unit": 4, "title": "Hadoop Operations & Job Scheduling", "topics": ["job scheduling in mapreduce", "fifo scheduler", "fair scheduler", "capacity scheduler", "data locality", "failure recovery"]},
            {"unit": 5, "title": "Big Data Frameworks - Spark & NoSQL", "topics": ["apache spark", "rdd", "spark sql", "hive", "hbase", "cassandra", "zookeeper"]}
        ]
    },
    "data warehousing": {
        "folder": "Data_Warehousing",
        "name": "Data Warehousing",
        "code": "23CSE34",
        "units": [
            {"unit": 1, "title": "Data Warehouse Architecture & Concepts", "topics": ["data warehouse fundamentals", "data mart", "three tier data warehouse architecture", "data warehouse vs dbms", "etl process", "system event manager"]},
            {"unit": 2, "title": "Dimensional Modeling & Schemas", "topics": ["dimensional modeling", "star schema", "snowflake schema", "fact constellation", "fact table", "dimensions", "conceptual hierarchies", "measures"]},
            {"unit": 3, "title": "Data Partitioning & Aggregations", "topics": ["horizontal partitioning", "vertical partitioning", "data cube", "olap operations", "roll-up", "drill-down", "slice and dice", "pivot"]},
            {"unit": 4, "title": "Data Warehouse Implementation & Metadata", "topics": ["metadata repository", "data cleaning", "data transformation", "indexing olap data", "bitmap index", "join index", "efficient computation of data cubes"]},
            {"unit": 5, "title": "OLAP Tools & Data Mining", "topics": ["molap", "rolap", "holap", "data warehouse usage for business intelligence", "decision support systems", "data mining integration"]}
        ]
    }
}

# Alias lookup for subjects
SUBJECT_ALIASES = {
    "cn": "computer networks",
    "networks": "computer networks",
    "network": "computer networks",
    "computer network": "computer networks",
    "computer networks": "computer networks",

    "dbms": "dbms",
    "database": "dbms",
    "database management": "dbms",
    "database management systems": "dbms",
    "sql": "dbms",

    "os": "operating systems",
    "operating system": "operating systems",
    "operating systems": "operating systems",

    "ds": "data structures",
    "dsa": "data structures",
    "data structures": "data structures",
    "data structure": "data structures",
    "algorithms": "data structures",

    "python": "python",
    "python programming": "python",

    "aptitude": "aptitude",
    "quant": "aptitude",
    "quantitative aptitude": "aptitude",
    "percentages": "aptitude",
    "percentage": "aptitude",
    "time and work": "aptitude",
    "time & work": "aptitude",
    "data interpretation": "aptitude",
    "logical reasoning": "aptitude",
    "verbal ability": "aptitude",

    "coding": "coding",
    "programming": "coding",
    "code": "coding",
    "c programming": "coding",
    "c++": "coding",
    "cpp": "coding",
    "java": "coding",
    "web development": "coding",
    "web dev": "coding",

    "mma": "multimedia and animation",
    "animation": "multimedia and animation",
    "animations": "multimedia and animation",
    "multimedia": "multimedia and animation",
    "multimedia and animation": "multimedia and animation",
    "multimedia applications": "multimedia and animation",

    "bda": "big data analytics",
    "big data": "big data analytics",
    "big data analysis": "big data analytics",
    "big data analytics": "big data analytics",
    "hadoop": "big data analytics",

    "dw": "data warehousing",
    "data warehouse": "data warehousing",
    "data warehousing": "data warehousing",
    "data mart": "data warehousing"
}

# Supported Educational Boards
BOARDS = [
    "Anna University",
    "CBSE Class 10",
    "CBSE Class 12",
    "Tamil Nadu State Board",
    "Matriculation",
    "Autonomous College",
    "Government Exams (TNPSC/UPSC)"
]

# Supported Languages
LANGUAGES = [
    "English",
    "Tamil",
    "Thanglish",
    "Hindi",
    "Malayalam",
    "Telugu",
    "Kannada"
]
