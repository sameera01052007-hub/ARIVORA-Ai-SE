# ============================================================
# ARIVORA AI - CURRICULUM & SYLLABUS KNOWLEDGE REPOSITORY
# Built-in structured syllabus data for university & school standards
# ============================================================

CURRICULUM = {
    "osi layers": {
        "subject": "Computer Networks",
        "unit": 1,
        "unit_title": "Introduction & Physical Layer",
        "topic": "OSI Reference Model (Open Systems Interconnection)",
        "book": "Computer Networks - Andrew S. Tanenbaum",
        "page_ref": "Pages 28 - 36",
        "definition": "The OSI (Open Systems Interconnection) reference model is a 7-layer architectural framework developed by ISO that standardizes network communication functions regardless of underlying hardware vendor.",
        "tamil_definition": "OSI மாதிரி (Open Systems Interconnection) என்பது ISO-வினால் உருவாக்கப்பட்ட 7 அடுக்குகளைக் கொண்ட நெட்வொர்க் கட்டமைப்பு ஆகும். இது பல்வேறு சாதனங்களுக்கு இடையே தகவல் பரிமாற்றத்தை நெறிப்படுத்துகிறது.",
        "tanglish_summary": "OSI model 7 layers kondu irukku. Idhu computer network la data epdi oru device la irundhu innoru device ku poguthu nu standardize pannuthu.",
        "key_points": [
            "Layer 1: Physical Layer - Bit-level transmission across physical media (Cables, Hubs, 1s and 0s).",
            "Layer 2: Data Link Layer - Reliable node-to-node data transfer using MAC addressing & framing (Switches).",
            "Layer 3: Network Layer - Path determination, logical addressing (IPv4/IPv6) & packet routing (Routers).",
            "Layer 4: Transport Layer - End-to-end connection, segmentation, flow and error control (TCP/UDP).",
            "Layer 5: Session Layer - Establishes, manages, and terminates presentation sessions and dialogues.",
            "Layer 6: Presentation Layer - Data translation, encryption/decryption, and compression (SSL/TLS, ASCII).",
            "Layer 7: Application Layer - Direct user interface with network services (HTTP, DNS, SMTP, FTP)."
        ],
        "tamil_points": [
            "அடுக்கு 1: இயற்பியல் அடுக்கு (Physical Layer) - பிட்களை கேபிள்கள் மற்றும் ரேடியோ சிக்னல்கள் வழியாக கடத்துகிறது.",
            "அடுக்கு 2: தரவு இணைப்பு அடுக்கு (Data Link Layer) - MAC முகவரியை பயன்படுத்தி ஃபிரேம்களை (Frames) அனுப்புகிறது.",
            "அடுக்கு 3: பிணைய அடுக்கு (Network Layer) - பாக்கெட் ரூட்டிங் மற்றும் IP முகவரிகளை கையாள்கிறது.",
            "அடுக்கு 4: போக்குவரத்து அடுக்கு (Transport Layer) - TCP மற்றும் UDP நெறிமுறைகள் மூலம் இறுதி-முடிவு தகவலை கொண்டு சேர்க்கிறது.",
            "அடுக்கு 5: அமர்வு அடுக்கு (Session Layer) - இரு கணினிகளுக்கு இடையே தொடர்பை துவக்கி நிர்வகிக்கிறது.",
            "அடுக்கு 6: விளக்கக்காட்சி அடுக்கு (Presentation Layer) - தரவு மறைகுறியாக்கம் (Encryption) மற்றும் சுருக்கத்தை செய்கிறது.",
            "அடுக்கு 7: பயன்பாட்டு அடுக்கு (Application Layer) - பயனருக்கு வலைத்தளம் மற்றும் மின்னஞ்சல் சேவைகளை (HTTP, SMTP) வழங்குகிறது."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
| Layer 7: Application Layer    (HTTP, FTP, SMTP, DNS)        |
+-------------------------------------------------------------+
| Layer 6: Presentation Layer   (SSL, TLS, JPEG, Encryption)  |
+-------------------------------------------------------------+
| Layer 5: Session Layer        (RPC, NetBIOS, Sockets)       |
+-------------------------------------------------------------+
| Layer 4: Transport Layer      (TCP, UDP, Port Addressing)   |
+-------------------------------------------------------------+
| Layer 3: Network Layer        (IP, ICMP, Routers, Packets)  |
+-------------------------------------------------------------+
| Layer 2: Data Link Layer      (Ethernet, MAC, Frames)       |
+-------------------------------------------------------------+
| Layer 1: Physical Layer       (Cables, Bits, Signals)       |
+-------------------------------------------------------------+
        """,
        "advantages": [
            "Modularity: Changes in one layer do not affect other layers.",
            "Interoperability: Enables multi-vendor hardware to communicate seamlessly.",
            "Simplified troubleshooting: Errors can be isolated to a specific layer."
        ],
        "applications": "Used as the global pedagogical and engineering reference standard for internet protocols, telecom networks, and network security design."
    },

    "tcp/ip": {
        "subject": "Computer Networks",
        "unit": 1,
        "unit_title": "Introduction & Physical Layer",
        "topic": "TCP/IP Protocol Suite",
        "book": "Data Communications and Networking - Behrouz A. Forouzan",
        "page_ref": "Pages 42 - 55",
        "definition": "The TCP/IP protocol suite is a 4-layer hierarchical network architecture that forms the foundational operational protocol suite of the modern global Internet.",
        "tamil_definition": "TCP/IP என்பது இன்றைய இணையத்தின் அடிப்படை நெறிமுறை தொகுப்பாகும். இது 4 அடுக்குகளைக் கொண்டு உலகம் முழுவதும் உள்ள கணினிகளை இணைக்கிறது.",
        "tanglish_summary": "TCP/IP suite dhaan real-world internet la use aagura main 4-layer model (Application, Transport, Internet, Network Access).",
        "key_points": [
            "Application Layer: Combines OSI layers 5, 6, and 7 (HTTP, FTP, DNS).",
            "Transport Layer: End-to-end communication via TCP (Connection-oriented) or UDP (Connectionless).",
            "Internet Layer: IP protocol handles logical addressing and packet routing across networks.",
            "Network Access / Link Layer: Physical network interface handling framing and physical hardware communication."
        ],
        "tamil_points": [
            "பயன்பாட்டு அடுக்கு: வலைத்தள சேவைகள் மற்றும் நெறிமுறைகளை வழங்குகிறது.",
            "போக்குவரத்து அடுக்கு: நம்பகமான (TCP) அல்லது வேகமான (UDP) தகவல் பரிமாற்றத்தை செய்கிறது.",
            "இணைய அடுக்கு: IP முகவரி மூலம் பாக்கெட்களை சரியான இலக்குக்கு கொண்டு சேர்க்கிறது.",
            "பிணைய அணுகல் அடுக்கு: கேபிள்கள் மற்றும் வைஃபை மூலம் ஹார்ட்வேர் தொடர்பை உறுதி செய்கிறது."
        ],
        "architecture_diagram": """
+----------------------------------------------------------+
| 1. Application Layer (HTTP, HTTPS, FTP, SMTP, DNS)       |
+----------------------------------------------------------+
| 2. Transport Layer   (TCP - Reliable / UDP - Fast)       |
+----------------------------------------------------------+
| 3. Internet Layer    (IPv4, IPv6, ICMP, ARP)             |
+----------------------------------------------------------+
| 4. Network Interface (Ethernet, Wi-Fi, Physical Hardware)|
+----------------------------------------------------------+
        """,
        "advantages": ["Industry standard for the Internet", "Robust routing support", "Cross-platform compatibility"],
        "applications": "Powers the entire World Wide Web, enterprise intranets, and mobile cellular data networks."
    },

    "tcp": {
        "subject": "Computer Networks",
        "unit": 4,
        "unit_title": "Transport Layer Services & Protocols",
        "topic": "Transmission Control Protocol (TCP) Concepts",
        "book": "Computer Networks - Andrew S. Tanenbaum",
        "page_ref": "Pages 534 - 562",
        "definition": "TCP (Transmission Control Protocol) is a reliable, connection-oriented, full-duplex transport layer protocol that provides guaranteed, ordered, and error-checked delivery of a stream of octets between internet hosts.",
        "tamil_definition": "TCP (Transmission Control Protocol) என்பது இணையத்தில் இரு கணினிகளுக்கு இடையே நம்பகமான, தொடர்ச்சியான மற்றும் பிழையற்ற தகவல் பரிமாற்றத்தை உறுதி செய்யும் டிரான்ஸ்போர்ட் லேயர் நெறிமுறை ஆகும்.",
        "tanglish_summary": "TCP oru connection-oriented protocol. Data miss aagadha mathiri 3-way handshake panni, packets-a correct order la destination-ku delivery pannum.",
        "key_points": [
            "Connection-Oriented: Establishes a dedicated virtual circuit using 3-Way Handshake (SYN, SYN-ACK, ACK) before data transfer.",
            "Reliability & Error Control: Uses sequence numbers, positive acknowledgments (ACK), checksums, and timeout retransmissions.",
            "Flow Control: Implements sliding window mechanism where receiver advertises buffer window size (rwnd) to prevent overflow.",
            "Congestion Control: Dynamically adapts sender rate using slow start, congestion avoidance (AIMD), fast retransmit, and fast recovery.",
            "Full Duplex & Byte Stream: Enables simultaneous bidirectional data flow structured as continuous byte streams rather than discrete packets."
        ],
        "tamil_points": [
            "இணைப்பு சார்ந்தது (Connection-Oriented): தகவல் அனுப்பும் முன் 3-வழி ஹேண்ட்ஷேக் (SYN -> SYN-ACK -> ACK) மூலம் உறுதியான இணைப்பை உருவாக்குகிறது.",
            "நம்பகமான தரவு விநியோகம்: வரிசை எண்கள் (Sequence Numbers) மற்றும் ஒப்புகை (ACK) மூலம் பாக்கெட்டுகள் விடுபடாமல் இருப்பதை உறுதி செய்கிறது.",
            "பாய்ச்சல் கட்டுப்பாடு (Flow Control): ஸ்லைடிங் விண்டோ (Sliding Window) தொழில்நுட்பம் மூலம் ரிசீவர் பஃபர் நிரம்பி டேட்டா இழக்கப்படாமல் தடுக்கிறது.",
            "நெரிசல் கட்டுப்பாடு (Congestion Control): நெட்வொர்க் டிராஃபிக் அதிகமாகும் போது தானாகவே வேகத்தை குறைத்து சமன் செய்கிறது."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|               TCP 3-WAY HANDSHAKE CONNECTION                |
+-------------------------------------------------------------+
|  Client (Browser)                 Server (Web Host)         |
|         |                                |                  |
|         | -------- 1. SYN -------------> | (Connection Req) |
|         | <------- 2. SYN + ACK -------- | (Ack & Sync)     |
|         | -------- 3. ACK -------------> | (Connected!)     |
|         |                                |                  |
|         |<==== Established Data Stream =>| (Full Duplex)    |
+-------------------------------------------------------------+
        """,
        "advantages": [
            "Guaranteed delivery without data loss or corruption",
            "Automatic packet sequencing and flow regulation",
            "Widely standardized and supported on all computing platforms"
        ],
        "applications": "Underpins HTTP/HTTPS (Web browsing), SMTP/IMAP (Email), FTP (File transfer), and SSH (Secure remote shell)."
    },

    "tcp concepts": {
        "subject": "Computer Networks",
        "unit": 4,
        "unit_title": "Transport Layer Services & Protocols",
        "topic": "TCP Protocol Principles & Working Mechanisms",
        "book": "Computer Networks - Andrew S. Tanenbaum",
        "page_ref": "Pages 534 - 562",
        "definition": "TCP Concepts encompass connection establishment (3-Way Handshake), reliable in-order data transfer, sliding-window flow control, and end-to-end congestion control in the internet transport layer.",
        "tamil_definition": "TCP கருத்துகள் என்பது 3-வழி ஹேண்ட்ஷேக் இணைப்பு, நம்பகமான தரவு விநியோகம், ஸ்லைடிங் விண்டோ ஃப்ளோ கண்ட்ரோல் மற்றும் நெட்வொர்க் நெரிசல் கட்டுப்பாடு ஆகியவற்றை உள்ளடக்கியதாகும்.",
        "tanglish_summary": "TCP Concepts-la main-ah 3-Way Handshake, Flow Control (Sliding Window), Congestion Control, and Reliability mechanisms varum.",
        "key_points": [
            "3-Way Handshake: Synchronize and establish connection states between client and server.",
            "Sliding Window Protocol: Manages buffer capacity and eliminates bottleneck delays.",
            "Error Recovery: Retransmission timers and selective acknowledgment (SACK).",
            "Congestion Control: Avoids network collapse through Tahoe/Reno algorithms."
        ],
        "tamil_points": [
            "3-வழி ஹேண்ட்ஷேக் இணைப்பு முறை",
            "ஸ்லைடிங் விண்டோ பாய்ச்சல் கட்டுப்பாடு",
            "தானியங்கி பிழை திருத்தம் மற்றும் மறுபரிமாற்றம்"
        ],
        "advantages": ["High reliability", "Ordered byte streaming", "Flow and congestion safety"],
        "applications": "Web browsing, secure communications, database client-server links."
    },

    "acid properties": {
        "subject": "DBMS",
        "unit": 4,
        "unit_title": "Transaction Management & Concurrency",
        "topic": "ACID Properties in Transactions",
        "book": "Database System Concepts - Silberschatz, Korth, Sudarshan",
        "page_ref": "Pages 628 - 635",
        "definition": "ACID properties (Atomicity, Consistency, Isolation, Durability) are a set of four core principles that guarantee database transactions are processed reliably and maintain integrity despite system crashes or concurrency.",
        "tamil_definition": "ACID பண்புகள் (Atomicity, Consistency, Isolation, Durability) என்பது ஒரு தரவுத்தளத்தில் (Database) பரிவர்த்தனைகள் துல்லியமாகவும் பாதுகாப்பாகவும் நடைபெறுவதை உறுதி செய்யும் 4 முக்கிய விதிகளாகும்.",
        "tanglish_summary": "ACID properties dhaan database transactions la data correct-ah irukka guarantee pannum. Bank transfer example la romba mukkiyam.",
        "key_points": [
            "A - Atomicity: 'All or Nothing'. The transaction executes fully or rolls back completely (managed by Transaction Manager / Log).",
            "C - Consistency: The database must remain in a valid state satisfying all constraints before and after the transaction.",
            "I - Isolation: Concurrent transactions execute independently without interference, as if executed serially (managed by Concurrency Control / Locks).",
            "D - Durability: Once a transaction commits, its changes survive permanently even during system power failures (managed by Recovery Manager / WAL log)."
        ],
        "tamil_points": [
            "A - Atomicity (முழுமை): பரிவர்த்தனை முழுமையாக நடக்கும் அல்லது ஆரம்ப நிலைக்கு திரும்பும் (All or Nothing).",
            "C - Consistency (நிலைத்தன்மை): பரிவர்த்தனைக்கு முன்பும் பின்பும் தரவுத்தள விதிகள் சரியாக பராமரிக்கப்படும்.",
            "I - Isolation (தனிமைப்படுத்தல்): பல பயனர்கள் ஒரே நேரத்தில் பரிவர்த்தனை செய்தாலும் ஒன்றோடு ஒன்று மோதாது.",
            "D - Durability (நீடித்துழைப்பு): பரிவர்த்தனை முடிந்துவிட்டால், கணினி முடங்கினாலும் தரவு அழியாது."
        ],
        "architecture_diagram": """
[Transaction Start]
         |
         v
+-------------------+      Rollback on failure
|     ATOMICITY     | ------------------------> [Aborted State]
+-------------------+
         |
         v
+-------------------+
|    CONSISTENCY    | ----> Preserves Schema Constraints (Sum A+B constant)
+-------------------+
         |
         v
+-------------------+
|     ISOLATION     | ----> 2-Phase Locking / Serializability Isolation
+-------------------+
         |
         v
+-------------------+
|    DURABILITY     | ----> Written to Non-Volatile Disk (WAL Log)
+-------------------+
         |
         v
  [Committed State]
        """,
        "advantages": ["Prevents partial database updates", "Protects financial and mission-critical records", "Ensures zero data loss during power cuts"],
        "applications": "Banking systems, ATM withdrawals, e-commerce checkouts, airline reservation engines."
    },

    "normalization": {
        "subject": "DBMS",
        "unit": 3,
        "unit_title": "Database Design & Normalization",
        "topic": "Database Normalization (1NF, 2NF, 3NF, BCNF)",
        "book": "Fundamentals of Database Systems - Elmasri & Navathe",
        "page_ref": "Pages 485 - 510",
        "definition": "Normalization is a systematic database design technique used to decompose relational tables to minimize data redundancy, avoid insertion/update/deletion anomalies, and ensure data dependency makes logical sense.",
        "tamil_definition": "நார்மலைசேஷன் (Normalization) என்பது தரவுத்தளத்தில் தேவையற்ற தரவு நகல்களை (Data Redundancy) குறைக்கவும், பிழைகளை தவிர்க்கவும் அட்டவணைகளை ஒழுங்குபடுத்தும் முறையாகும்.",
        "tanglish_summary": "Normalization table la duplicate data-va avoid panni, tables-ah split panni proper primary key & foreign key relationship create pannum.",
        "key_points": [
            "1NF (First Normal Form): Eliminate repeating groups and multi-valued attributes; each column holds atomic (indivisible) values.",
            "2NF (Second Normal Form): Satisfies 1NF and eliminates Partial Dependency (no non-prime attribute depends on a proper subset of candidate key).",
            "3NF (Third Normal Form): Satisfies 2NF and eliminates Transitive Dependency (if X -> Y and Y -> Z, then non-key cannot determine non-key).",
            "BCNF (Boyce-Codd Normal Form): A stricter version of 3NF where for every functional dependency X -> Y, X MUST be a Super Key."
        ],
        "tamil_points": [
            "1NF: ஒவ்வொரு கட்டத்திலும் தனிப்பட்ட ஒற்றை மதிப்பு (Atomic Value) மட்டுமே இருக்க வேண்டும்.",
            "2NF: 1NF-ல் இருக்க வேண்டும் மற்றும் பகுதி சார்புநிலை (Partial Dependency) இருக்கக்கூடாது.",
            "3NF: 2NF-ல் இருக்க வேண்டும் மற்றும் இடைநிலை சார்புநிலை (Transitive Dependency) இருக்கக்கூடாது.",
            "BCNF: 3NF-ன் மேம்பட்ட நிலை; இதில் ஒவ்வொரு சார்புநிலையிலும் இடதுபுறம் சூப்பர் கீயாக (Super Key) இருக்க வேண்டும்."
        ],
        "architecture_diagram": """
[Unnormalized Table (Multivalued attributes)]
                 |
                 v   Rule: Atomic values only
+------------------------------------+
|  1NF (First Normal Form)           |
+------------------------------------+
                 |
                 v   Rule: Remove Partial Dependency
+------------------------------------+
|  2NF (Second Normal Form)          |
+------------------------------------+
                 |
                 v   Rule: Remove Transitive Dependency (X->Y->Z)
+------------------------------------+
|  3NF (Third Normal Form)           |
+------------------------------------+
                 |
                 v   Rule: For X->A, X must be a Super Key
+------------------------------------+
|  BCNF (Boyce-Codd Normal Form)     |
+------------------------------------+
        """,
        "advantages": ["Minimizes disk storage waste", "Guarantees referential integrity", "Prevents update anomalies"],
        "applications": "Enterprise ERP systems, hospital patient management, student record databases."
    },

    "process scheduling": {
        "subject": "Operating Systems",
        "unit": 2,
        "unit_title": "Processes & CPU Scheduling",
        "topic": "CPU Process Scheduling Algorithms",
        "book": "Operating System Concepts - Abraham Silberschatz, Peter Baer Galvin",
        "page_ref": "Pages 261 - 285",
        "definition": "CPU Scheduling is the process by which the OS kernel allocates CPU processing time among multiple ready processes to maximize CPU utilization, throughput, and minimize waiting time.",
        "tamil_definition": "சிபியூ திட்டமிடல் (CPU Scheduling) என்பது கணினியின் செயலியை (Processor) பல செயல்முறைகளுக்கு (Processes) திறம்பட ஒதுக்கீடு செய்யும் ஆப்பரேட்டிங் சிஸ்டத்தின் வழிமுறையாகும்.",
        "tanglish_summary": "CPU scheduling ready queue la irukura processes-ku CPU time allocate pannum. Round Robin, FCFS, SJF idhula popular algorithms.",
        "key_points": [
            "FCFS (First-Come, First-Served): Non-preemptive, simple queue order, suffers from Convoy Effect.",
            "SJF (Shortest Job First): Optimal average waiting time; requires knowing future burst times.",
            "Round Robin (RR): Preemptive scheduling using a fixed Time Quantum (ideal for time-sharing systems).",
            "Priority Scheduling: CPU allocated to highest priority process; starvation resolved using Aging.",
            "Multilevel Queue Scheduling: Partitions ready queue into foreground (interactive) and background (batch) queues."
        ],
        "tamil_points": [
            "FCFS: முதலில் வரும் செயல்முறைக்கு முதலில் முன்னுரிமை வழங்கப்படும் (வரிசை முறை).",
            "SJF: குறைந்த நேரம் எடுக்கும் பணிக்கு முதலில் CPU வழங்கப்படும் (காத்திருப்பு நேரத்தை குறைக்கும்).",
            "Round Robin: ஒவ்வொரு பணிக்கும் சமமான நேர அளவு (Time Quantum) ஒதுக்கப்படும்.",
            "Priority: அதிக முக்கியத்துவம் வாய்ந்த பணிக்கு முதலில் வாய்ப்பு தரப்படும்."
        ],
        "architecture_diagram": """
[New Process] ---> [Ready Queue] <====================+
                          |                           |
                     (Scheduler)                      | (Time Quantum expired /
                          |                           |  Preemption)
                          v                           |
                    [Running in CPU] -----------------+
                          |
             (I/O Request / Wait Event)
                          v
                    [Waiting State] ---> (I/O Complete) ---> [Ready Queue]
        """,
        "advantages": ["Prevents CPU idle time", "Ensures fair responsiveness for desktop users", "Maximizes job throughput"],
        "applications": "Windows, Linux kernel schedulers (CFS), real-time embedded OS."
    },

    "deadlocks": {
        "subject": "Operating Systems",
        "unit": 3,
        "unit_title": "Process Synchronization & Deadlocks",
        "topic": "Deadlocks & Coffman Conditions",
        "book": "Operating System Concepts - Silberschatz & Galvin",
        "page_ref": "Pages 315 - 340",
        "definition": "A deadlock is a situation where a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the set.",
        "tamil_definition": "டெட்லாக் (Deadlock) என்பது இரண்டு அல்லது அதற்கு மேற்பட்ட செயல்முறைகள் ஒன்றை ஒன்று வைத்திருக்கும் வளங்களுக்காக முடிவில்லாமல் காத்திருக்கும் முடக்க நிலையாகும்.",
        "tanglish_summary": "Deadlock na rendu processes oru resource-ah hold pannikittu mathadhu release aagura varaikkum wait panni freeze aagura condition.",
        "key_points": [
            "Mutual Exclusion: At least one resource is held in a non-shareable mode.",
            "Hold and Wait: A process holds resources while requesting additional resources.",
            "No Preemption: Resources cannot be forcibly seized; released only voluntarily.",
            "Circular Wait: A closed chain of processes exists where P[i] waits for P[i+1] and P[n] waits for P[0].",
            "Banker's Algorithm: Resource allocation and deadlock avoidance algorithm using safety checks."
        ],
        "tamil_points": [
            "Mutual Exclusion: ஒரு வளத்தை ஒரு நேரத்தில் ஒருவர் மட்டுமே பயன்படுத்த முடியும்.",
            "Hold and Wait: ஒரு வளத்தை வைத்துக்கொண்டே மற்றொன்றுக்கு காத்திருத்தல்.",
            "No Preemption: வலுக்கட்டாயமாக வளத்தை பறிக்க முடியாது.",
            "Circular Wait: செயல்முறைகள் வட்ட வடிவில் ஒன்றுக்கொன்று காத்திருத்தல்."
        ],
        "architecture_diagram": """
       Holds Resource R1 <------------ Process P1
               |                             ^
               v                             |
           Process P2 ------------> Requests Resource R1
                                           |
                                           v
                                   [CIRCULAR DEADLOCK]
        """,
        "advantages": ["Understanding deadlocks prevents application crashes", "Banker's algorithm enables safe state allocation"],
        "applications": "Multithreaded programming, database lock managers, traffic flow management."
    },

    "binary search tree": {
        "subject": "Data Structures",
        "unit": 3,
        "unit_title": "Non-Linear Data Structures - Trees",
        "topic": "Binary Search Tree (BST) Operations",
        "book": "Data Structures and Algorithm Analysis in C - Mark Allen Weiss",
        "page_ref": "Pages 110 - 135",
        "definition": "A Binary Search Tree (BST) is a node-based binary tree data structure where for every node, keys in the left subtree are strictly smaller and keys in the right subtree are strictly greater.",
        "tamil_definition": "பைனரி தேடல் மரம் (BST) என்பது ஒவ்வொரு முனையிலும், இடது துணை மரம் சிறிய மதிப்புகளையும், வலது துணை மரம் பெரிய மதிப்புகளையும் கொண்டுள்ள மர அமைப்பாகும்.",
        "tanglish_summary": "BST la left child eppovum smaller-ah irukkum, right child eppovum greater-ah irukkum. Search time complexity O(log n).",
        "key_points": [
            "Inorder Traversal of a BST always produces elements in ascending sorted order.",
            "Search, Insertion, and Deletion average time complexity is O(log n), worst-case O(n) when skewed.",
            "Deletion has 3 cases: Node has 0 children (leaf), 1 child, or 2 children (replace with inorder successor).",
            "Balanced variants like AVL Tree and Red-Black Tree prevent degradation to O(n)."
        ],
        "tamil_points": [
            "இடது துணை மரம்: மூல மதிப்பை விட குறைவான எண்கள் இருக்கும்.",
            "வலது துணை மரம்: மூல மதிப்பை விட அதிகமான எண்கள் இருக்கும்.",
            "தேடல் வேகம்: சராசரியாக O(log n) நேரத்தில் தேடலை முடிக்கும்.",
            "Inorder Traversal: எண்களை ஏறுவரிசையில் கொடுக்கும்."
        ],
        "architecture_diagram": """
                50 (Root)
               /  \\
             30    70
            /  \\   /  \\
           20  40 60   80
       Left < Root < Right
        """,
        "advantages": ["Efficient dynamic searching and sorting", "Faster lookup than linked list", "In-order gives sorted sequence"],
        "applications": "Database indexing, file system directory organization, syntax trees in compilers."
    },

    "percentage": {
        "subject": "Aptitude",
        "unit": 1,
        "unit_title": "Number System & Arithmetic",
        "topic": "Percentage Calculations and Shortcuts",
        "book": "Quantitative Aptitude for Competitive Examinations - R.S. Aggarwal",
        "page_ref": "Pages 208 - 235",
        "definition": "A percentage represents a fraction or ratio expressed with a denominator of 100, symbolized by '%'.",
        "tamil_definition": "சதவீதம் (Percentage) என்பது 100-ஐ அடிப்படையாகக் கொண்ட ஒரு கணித விகித அளவீடாகும்.",
        "tanglish_summary": "Percentage calculation aptitude exams la base topic. Formula: (Value / Total) * 100.",
        "key_points": [
            "Percentage Formula: (Part / Whole) * 100",
            "Fraction shortcuts: 1/2 = 50%, 1/3 = 33.33%, 1/4 = 25%, 1/5 = 20%, 1/6 = 16.66%, 1/8 = 12.5%",
            "Percentage Increase: (Increase / Original Value) * 100",
            "Successive Percentage change formula: [A + B + (AB / 100)] %"
        ],
        "tamil_points": [
            "சூத்திரம்: (பகுதி / மொத்தம்) * 100",
            "எளிய பின்னங்கள்: 1/4 = 25%, 1/2 = 50%, 3/4 = 75%",
            "அதிகரிப்பு சதவீதம்: (அதிகரித்த மதிப்பு / ஆரம்ப மதிப்பு) * 100"
        ],
        "architecture_diagram": """
             [Fraction: 1/4]
                    |
                    v Multiply by 100
             [Percentage: 25%]
        """,
        "advantages": ["Crucial for data interpretation and commercial math", "Quick estimation in campus placements"],
        "applications": "Campus placement tests, TNPSC, Banking exams, GATE quantitative analysis."
    },

    "data integrity in hadoop": {
        "subject": "Big Data Analysis",
        "unit": 1,
        "unit_title": "Introduction to Big Data & Hadoop",
        "topic": "Data Integrity in Hadoop & Checksum Verification",
        "book": "Hadoop: The Definitive Guide - Tom White",
        "page_ref": "Pages 85 - 94",
        "definition": "Data integrity in Hadoop ensures that data stored and processed in the Hadoop Distributed File System (HDFS) remains accurate, complete, and uncorrupted by using 32-bit CRC (Cyclic Redundancy Check) checksums verified during read and write pipelines.",
        "tamil_definition": "Hadoop-ல் தரவு ஒருமைப்பாடு (Data Integrity) என்பது HDFS-ல் சேமிக்கப்படும் தரவு பிழையின்றியும் சேதமடையாமலும் இருப்பதை உறுதி செய்யும் முறையாகும். இது CRC-32 செக்சம் (Checksum) மூலம் சரிபார்க்கப்படுகிறது.",
        "tanglish_summary": "Hadoop la data integrity na HDFS la store aagura files corrupt aagama irukka CRC checksum use panni data transfer and storage-ah verify panradhu.",
        "key_points": [
            "HDFS transparently computes a 32-bit CRC checksum for every 512 bytes of data (io.bytes.per.checksum).",
            "Clients verify checksums against separate hidden checksum files (.crc) during every block read.",
            "DataNodes run a background DataBlockScanner periodically to verify all stored blocks on disk.",
            "Corrupt blocks are immediately reported to NameNode, which initiates automatic re-replication from healthy replicas.",
            "Client can disable verification when raw speed is critical by passing false to setVerifyChecksum()."
        ],
        "tamil_points": [
            "CRC-32 செக்சம்: ஒவ்வொரு 512 பைட் டேட்டாவிற்கும் 4 பைட் செக்சம் கணக்கிடப்படுகிறது.",
            "தானியங்கி சரிபார்ப்பு: கிளையன்ட் டேட்டாவை படிக்கும் போது செக்சம் ஒப்பிட்டு பார்க்கப்படுகிறது.",
            "DataBlockScanner: ஹார்ட் டிஸ்க்கில் உள்ள பிளாக்குகளை பின்னணியில் தொடர்ந்து ஸ்கேன் செய்கிறது.",
            "சுய-பழுதுநீக்கம் (Self-Healing): பிழை கண்டறியப்பட்டால் NameNode தானாகவே மற்றொரு நகலில் இருந்து சரிசெய்கிறது."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|             HDFS DATA INTEGRITY CHECK PIPELINE              |
+-------------------------------------------------------------+
| Client (Write) ---> [512 Bytes Data + 4 Byte CRC Checksum]  |
|                               |                             |
|                               v                             |
| DataNode: Stores Data Block (.meta contains CRC checksums)  |
|                               |                             |
| DataBlockScanner (Background) -> Scans & Verifies Checksums |
|                               |                             |
| Client (Read) ---> Compares Checksum -> Mismatch Detected?  |
|                          |                                  |
|         YES: Report Corrupt Block to NameNode               |
|              -> NameNode re-replicates from replica         |
+-------------------------------------------------------------+
        """,
        "advantages": ["Prevents bit-rot and silent disk corruption", "Automated self-healing replication", "Transparent to end users and applications"],
        "applications": "Petabyte-scale distributed data warehouses, financial transaction logs, enterprise data lakes."
    },

    "avro": {
        "subject": "Big Data Analysis",
        "unit": 2,
        "unit_title": "Data Serialization & File Formats",
        "topic": "Apache Avro Serialization System",
        "book": "Hadoop: The Definitive Guide - Tom White",
        "page_ref": "Pages 105 - 128",
        "definition": "Apache Avro is a language-independent, row-oriented data serialization system that provides rich data structures, a compact binary data format, and schema evolution capabilities with schemas defined in JSON.",
        "tamil_definition": "Apache Avro என்பது மொழிகளை சாராத ஒரு தரவு வரிசைப்படுத்தல் (Data Serialization) கட்டமைப்பாகும். இது சுருக்கமான பைனரி வடிவத்திலும், JSON திட்டத்திலும் (Schema) தரவை சேமிக்கிறது.",
        "tanglish_summary": "Avro oru language-neutral serialization framework. Idhula schema JSON la irukkum, data fast binary format la store aagum.",
        "key_points": [
            "Rich schema definition written in lightweight human-readable JSON.",
            "Compact, fast binary encoding where schema is stored with the data (self-describing files).",
            "Full Schema Evolution support: reader and writer can use different schemas with default value resolution.",
            "Seamless integration with Hadoop MapReduce, Apache Spark, and Apache Kafka.",
            "No need to generate boilerplate proxy code unlike Apache Thrift or Protocol Buffers."
        ],
        "tamil_points": [
            "JSON திட்டம்: திட்ட வரையறை எளிமையான JSON அமைப்பில் செய்யப்படுகிறது.",
            "வேகமான பைனரி வடிவம்: குறைந்த சேமிப்பகத்தில் அதிவேகமாக படிக்கவும் எழுதவும் உதவுகிறது.",
            "திட்ட பரிணாமம் (Schema Evolution): பழைய மற்றும் புதிய தரவு பதிப்புகளுக்கு இடையே இணக்கத்தன்மையை தருகிறது.",
            "Kafka & Hadoop இணைப்பு: ஸ்ட்ரீமிங் மற்றும் பேட்ச் செயலாக்கத்தில் பரவலாக பயன்படுகிறது."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|                     APACHE AVRO ECOSYSTEM                   |
+-------------------------------------------------------------+
| JSON Schema (.avsc) + Data Stream                           |
|                  |                                          |
|                  v                                          |
| Avro Binary Encoder -> [Magic Bytes | Schema | Binary Rows] |
|                  |                                          |
|                  v                                          |
| Reader Schema -> Schema Resolution -> Deserialized Object   |
+-------------------------------------------------------------+
        """,
        "advantages": ["Zero code generation requirement", "Extremely compact binary storage", "Splittable file format ideal for MapReduce"],
        "applications": "Apache Kafka messaging pipeline, Hadoop data storage, cross-language RPC communication."
    },

    "mapreduce workflow": {
        "subject": "Big Data Analysis",
        "unit": 3,
        "unit_title": "MapReduce Architecture & Workflow",
        "topic": "MapReduce Computational Workflow & Execution Steps",
        "book": "Hadoop: The Definitive Guide - Tom White",
        "page_ref": "Pages 190 - 220",
        "definition": "The MapReduce workflow is a distributed computational pipeline comprising Input Splitting, Record Reading, Map execution, Combiner (optional), Shuffle and Sort, and Reduce aggregation.",
        "tamil_definition": "MapReduce ஒர்க்ஃப்ளோ (Workflow) என்பது பெரிய அளவிலான தரவை கிளஸ்டரில் பிரித்து வரைபடமாக்கி (Map), வரிசைப்படுத்தி (Shuffle & Sort), பின்னர் சுருக்கி (Reduce) முடிவை தரும் படிநிலையாகும்.",
        "tanglish_summary": "MapReduce workflow la Input Split -> Map Task -> Shuffle & Sort (Heart of MR) -> Reduce Task -> Output HDFS nu sequential stages irukku.",
        "key_points": [
            "1. InputFormat & RecordReader: Splits raw files into InputSplits (default 128MB) and yields <Key, Value> pairs.",
            "2. Map Phase: User-defined map() processes each pair and emits intermediate <K2, V2> pairs.",
            "3. Combiner (Mini-Reducer): Local in-memory pre-aggregation to reduce network traffic across nodes.",
            "4. Partitioner & Shuffle-Sort: Routes intermediate keys to assigned Reducers via hash partitioning and sorts by key.",
            "5. Reduce Phase: Reducer aggregates all values associated with each unique key and writes final result to HDFS."
        ],
        "tamil_points": [
            "படி 1: உள்ளீட்டுப் பிளவு (Input Split) - கோப்பு சம அளவிலான துண்டுகளாக பிரிக்கப்படுகிறது.",
            "படி 2: வரைபடம் (Map Task) - தரவை படித்து இடைநிலை கீ-மதிப்பு (Key-Value) இணைகளாக மாற்றுகிறது.",
            "படி 3: கலக்குதல் மற்றும் வரிசைப்படுத்துதல் (Shuffle & Sort) - ஒரே வகையான கீகளை ஒன்றாக சேர்க்கிறது.",
            "படி 4: குறைத்தல் (Reduce Task) - முடிவுகளை ஒன்றிணைத்து இறுதி அறிக்கையை HDFS-ல் எழுதுகிறது."
        ],
        "architecture_diagram": """
+----------------------------------------------------------------------+
|                      MAPREDUCE WORKFLOW PIPELINE                     |
+----------------------------------------------------------------------+
| [Input File] -> [Input Splits] -> [RecordReader]                     |
|                      |                                               |
|                      v                                               |
|               [Map Phase: map(k1, v1) -> list(k2, v2)]               |
|                      |                                               |
|                      v (Spill to Memory Buffer & Partitioner)        |
|               [Shuffle & Sort: Groups all v2 for each k2]            |
|                      |                                               |
|                      v                                               |
|               [Reduce Phase: reduce(k2, list(v2)) -> (k3, v3)]       |
|                      |                                               |
|                      v                                               |
|               [OutputFormat -> Final HDFS Part Files]                |
+----------------------------------------------------------------------+
        """,
        "advantages": ["Linear horizontal scalability", "Automatic fault tolerance through task re-execution", "High data locality reduces network bottlenecks"],
        "applications": "Large-scale log analysis, web search indexing (PageRank), batch ETL transformations, machine learning pipelines."
    },

    "classic mapreduce vs yarn": {
        "subject": "Big Data Analysis",
        "unit": 3,
        "unit_title": "MapReduce Architecture & Workflow",
        "topic": "Contrast Classic MapReduce (MRv1) and YARN (MRv2)",
        "book": "Hadoop: The Definitive Guide - Tom White",
        "page_ref": "Pages 225 - 245",
        "definition": "Classic MapReduce (MRv1) relied on a monolithic JobTracker managing both cluster resources and job execution, whereas YARN (MRv2) decouples resource management (ResourceManager) from application lifecycle management (ApplicationMaster).",
        "tamil_definition": "Classic MapReduce (MRv1) மற்றும் YARN (MRv2) இடையேயான ஒப்பீடு: MRv1-ல் JobTracker அனைத்து வேலைகளையும் ஒற்றையாக செய்தது; YARN-ல் வள மேலாண்மை (ResourceManager) மற்றும் பயன்பாட்டு கண்காணிப்பு (ApplicationMaster) தனித்தனியாக பிரிக்கப்பட்டுள்ளது.",
        "tanglish_summary": "MRv1 la JobTracker resource and execution rendaiyum paathukuchu (single point of bottleneck). YARN la ResourceManager resource mattum paakum, ApplicationMaster execution paakum.",
        "key_points": [
            "Scalability: MRv1 tops out at ~4,000 nodes due to JobTracker memory overload; YARN scales comfortably to 10,000+ nodes.",
            "Resource Governance: MRv1 uses fixed Map and Reduce slots causing wasted resources; YARN uses dynamic memory/CPU containers.",
            "Multi-Framework Support: MRv1 runs only MapReduce jobs; YARN runs Spark, Flink, Storm, HBase, and MapReduce simultaneously.",
            "Single Point of Failure (SPOF): MRv1 JobTracker failure kills all active jobs; YARN ResourceManager has high availability (Active/Standby).",
            "Job Execution: In YARN, each application gets a dedicated lightweight ApplicationMaster that negotiates with NodeManagers."
        ],
        "tamil_points": [
            "அளவிடக்கூடிய தன்மை: MRv1 4000 நோட்கள் வரை மட்டுமே இயங்கும்; YARN 10,000+ நோட்கள் வரை செயல்படும்.",
            "வள ஒதுக்கீடு: MRv1 நிலையான ஸ்லாட்டுகளை (Slots) பயன்படுத்தியது; YARN மெமரி மற்றும் CPU கண்டெய்னர்களை (Containers) தருகிறது.",
            "பல செயலாக்கங்கள்: YARN மூலம் MapReduce மட்டுமின்றி Spark மற்றும் Flink-ஐயும் இயக்க முடியும்.",
            "நம்பகத்தன்மை: YARN-ல் JobTracker முடக்கம் போன்ற தனிமுனை தோல்வி (SPOF) தடுக்கப்பட்டுள்ளது."
        ],
        "architecture_diagram": r"""
+-----------------------------------+   +------------------------------------+
|       MRv1 (CLASSIC HADOOP)       |   |            MRv2 (YARN)             |
+-----------------------------------+   +------------------------------------+
|          [JobTracker]             |   |         [ResourceManager]          |
|  (Resources + Job Coordination)   |   |        (Pure Cluster Resource)     |
|         /              \          |   |            /             \         |
|   [TaskTracker]   [TaskTracker]   |   |   [NodeManager]     [NodeManager]  |
|  (Fixed Map/Red) (Fixed Map/Red)  |   | [AppMaster+Cont]  [Containers...]  |
+-----------------------------------+   +------------------------------------+
        """,
        "advantages": ["Dynamic cluster utilization", "Native support for non-MapReduce workloads", "Eliminates JobTracker bottleneck"],
        "applications": "Modern enterprise multi-tenant compute clusters powering Spark streaming, Hive data warehousing, and deep learning."
    },

    "data mart": {
        "subject": "Data Warehousing",
        "unit": 1,
        "unit_title": "Data Warehouse Architecture & Concepts",
        "topic": "Characteristics and Architecture of Data Marts",
        "book": "Data Warehousing Fundamentals - Paulraj Ponniah",
        "page_ref": "Pages 45 - 68",
        "definition": "A Data Mart is a subset of an enterprise data warehouse focused on a specific business line, department, or functional area (e.g., Sales, Marketing, Finance).",
        "tamil_definition": "டேட்டா மார்ட் (Data Mart) என்பது நிறுவனத்தின் முக்கிய டேட்டா கிடங்கில் இருந்து ஒரு குறிப்பிட்ட துறைக்கு (எ.கா: விற்பனை, நிதி) மட்டும் தேவையான தகவல்களைக் கொண்ட சிறிய தரவுக் களஞ்சியமாகும்.",
        "tanglish_summary": "Data Mart na oru specific department (Sales or HR) ku thevayana curated data warehouse subset. Idhu enterprise DWH vida compact and fast-ah irukkum.",
        "key_points": [
            "Subject-Oriented: Focuses deeply on one single functional domain (such as inventory, marketing campaigns, or regional revenue).",
            "Department-Oriented: Tailored to serve the analytical and reporting needs of a specific user group or department.",
            "Compact and Cost-Effective: Smaller footprint, lower hardware cost, and significantly faster implementation time than enterprise DWH.",
            "Dependent vs Independent: Dependent marts draw source data directly from central DWH; independent marts ingest directly from operational OLTP.",
            "Optimized for High-Speed Querying: Employs denormalized Star or Snowflake dimensional schemas for rapid BI dashboards."
        ],
        "tamil_points": [
            "பொருள் சார்ந்த அணுகுமுறை: விற்பனை அல்லது மார்க்கெட்டிங் போன்ற ஒரு துறையை மையமாகக் கொண்டது.",
            "துறை சார்ந்த பயன்பாடு: குறிப்பிட்ட துறை மேலாளர்களின் விரைவான முடிவெடுக்கும் தேவையை பூர்த்தி செய்கிறது.",
            "குறைந்த செலவு மற்றும் வேகம்: சிறிய அளவில் இருப்பதால் எளிதில் உருவாக்கலாம், வினவல்கள் மிக விரைவாக செயல்படும்."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|                   DATA MART ARCHITECTURE                    |
+-------------------------------------------------------------+
| Operational DBs ---> [ETL Pipeline] ---> [Enterprise DWH]   |
|                                                  |          |
|                  +-------------------------------+          |
|                  |               |               |          |
|                  v               v               v          |
|             [Sales Mart]   [Finance Mart]   [HR Mart]       |
|                  |               |               |          |
|                  v               v               v          |
|             [Tableau BI]   [PowerBI Rep]    [Payroll Dash]  |
+-------------------------------------------------------------+
        """,
        "advantages": ["Easy access to frequently used departmental data", "Reduced query latency", "Accelerated business intelligence adoption"],
        "applications": "Retail regional sales analysis, clinical trial analytics, financial risk forecasting."
    },

    "horizontal partitioning": {
        "subject": "Data Warehousing",
        "unit": 3,
        "unit_title": "Data Partitioning & Aggregations",
        "topic": "Horizontal Partitioning in Data Warehouses",
        "book": "Data Warehousing: Design, Development and Best Practices - Soumendra Mohanty",
        "page_ref": "Pages 160 - 182",
        "definition": "Horizontal Partitioning divides a database table into disjoint subsets of rows (tuples) based on partition keys (such as date ranges, geographical regions, or status codes), storing each subset on distinct physical storage segments while maintaining a unified logical view.",
        "tamil_definition": "கிடைமட்ட பகிர்வு (Horizontal Partitioning) என்பது ஒரு பெரிய அட்டவணையின் வரிசைகளை (Rows) தேதி அல்லது பகுதி வாரியாக பல சிறிய தட்டுகளாக பிரித்து சேமிக்கும் தொழில்நுட்பமாகும்.",
        "tanglish_summary": "Horizontal partitioning la table rows-ah range (like year 2024, 2025) or list basis la piripom. Query execute aagum podhu partition pruning nadandhu fast response varum.",
        "key_points": [
            "Row-Level Segregation: Retains identical column schema across all partitions while distributing row records.",
            "Partition Pruning: Query optimizer eliminates irrelevant partitions before execution, dramatically accelerating query response.",
            "Partitioning Strategies: Range (by timestamps/dates), Hash (uniform distribution via hash key), List (discrete categories like states), and Composite.",
            "Maintenance Lifecycle: Enables rapid rolling-window data archival by dropping or detaching ancient partitions instantly.",
            "High Concurrency: Parallel query engines scan individual partitions simultaneously across separate disk spindles."
        ],
        "tamil_points": [
            "வரிசை வாரியான பிரிப்பு: ஒரே மாதிரியான நெடுவரிசைகளுடன் வரிசைகள் மட்டும் பிரிக்கப்படுகின்றன.",
            "Partition Pruning: தேவையில்லாத பகுதிகளை தவிர்க்கும் நுட்பம் வினவல் வேகத்தை பல மடங்கு கூட்டுகிறது.",
            "பராமரிப்பு எளிமை: பழைய ஆண்டு தரவுகளை எளிதாக காப்பகப்படுத்தலாம் (Archive/Drop).",
            "இணை செயலாக்கம் (Parallel Processing): ஒரே நேரத்தில் பல பகிர்வுகளில் தேடல் நடக்கும்."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|              HORIZONTAL PARTITIONING ARCHITECTURE           |
+-------------------------------------------------------------+
|                  [Logical Orders Table]                     |
|                               |                             |
|               +---------------+---------------+             |
|               | Partition Key = Order_Date    |             |
|               v                               v             |
|   [Partition 1: Year 2023]         [Partition 2: Year 2024] |
|   (Rows 1 to 5,000,000)            (Rows 5,000,001+)        |
|               |                               |             |
|          [Disk Vol A]                    [Disk Vol B]       |
+-------------------------------------------------------------+
        """,
        "advantages": ["Sub-second query response via partition elimination", "Simplified index maintenance", "Zero-downtime historical data purging"],
        "applications": "Telecom call detail records (CDR), e-commerce historical orders, bank transaction history."
    },

    "data cube": {
        "subject": "Data Warehousing",
        "unit": 3,
        "unit_title": "Data Partitioning & Aggregations",
        "topic": "Data Cube and Multidimensional Data Model",
        "book": "Data Mining: Concepts and Techniques - Jiawei Han & Micheline Kamber",
        "page_ref": "Pages 125 - 150",
        "definition": "A Data Cube is a multidimensional data structure used in OLAP systems that models and aggregates numerical measures across multiple analytical dimensions (e.g., Time, Item, Location).",
        "tamil_definition": "டேட்டா க்யூப் (Data Cube) என்பது பல பரிமாணங்களில் (பொருள், காலம், இடம்) கணக்கிடப்பட்ட புள்ளிவிவரங்களை வேகமான பகுப்பாய்விற்காக முப்பரிமாண அல்லது பலபரிமாண அமைப்பில் சேமிக்கும் மாடல் ஆகும்.",
        "tanglish_summary": "Data Cube oru multi-dimensional structure. Time, Location, Item dimensions-la sales measure-ah pre-compute panni roll-up, drill-down panna use aagum.",
        "key_points": [
            "Dimensions & Measures: Dimensions provide contextual viewpoints (Who, When, Where); Measures are quantitative metrics (Sales, Profit).",
            "Cuboid Lattice: An n-dimensional cube contains 2^n cuboids ranging from 0-D apex cuboid (grand total) to n-D base cuboid.",
            "Core OLAP Operations: Roll-up (drill-up/aggregation), Drill-down (increasing granularity), Slice (selecting one dimension value), Dice (subcube selection), and Pivot (rotation).",
            "Storage Implementations: MOLAP (dense/sparse multidimensional arrays), ROLAP (relational star schema tables), and HOLAP (hybrid).",
            "Pre-computation trade-off: Materializing all cuboids accelerates queries but exponentially expands storage requirements."
        ],
        "tamil_points": [
            "பரிமாணங்கள் மற்றும் அளவீடுகள்: நேரம், இருப்பிடம் போன்ற பரிமாணங்களுடன் விற்பனை தொகை போன்ற அளவீடுகள் இணைகின்றன.",
            "OLAP செயல்பாடுகள்: Roll-up (சுருக்கம்), Drill-down (ஆழமான பார்வை), Slice (ஒரு பகுதியை மட்டும் வெட்டுதல்), Pivot (சுழற்றுதல்).",
            "முன்கூட்டியே கணக்கிடுதல்: வினவல்கள் கேட்டவுடன் விடை கிடைக்க முன்கூட்டியே கூட்டல் கணக்குகள் சேமிக்கப்படுகின்றன."
        ],
        "architecture_diagram": """
+-------------------------------------------------------------+
|                   3D DATA CUBE (OLAP MODEL)                 |
+-------------------------------------------------------------+
|                       [Dimensions]                          |
|             Time (Q1, Q2, Q3, Q4)                           |
|             Item (Mobile, Laptop, Tablet)                   |
|             Location (Chennai, Bangalore, Mumbai)           |
|                                                             |
|                       +-------------+                       |
|                      /             /|                       |
|                     +-------------+ |                       |
|                     | Total Sales | |                       |
|                     | $450,000    | +                       |
|                     |             |/                        |
|                     +-------------+                         |
|                     [Cell Value = SUM(Sales Amount)]        |
+-------------------------------------------------------------+
        """,
        "advantages": ["Instantaneous analytical computation", "Intuitive multi-angle business exploration", "Supports complex predictive modeling"],
        "applications": "Executive decision support systems (DSS), global supply chain forecasting, financial trend analytics."
    },

    "fact table": {
        "subject": "Data Warehousing",
        "unit": 2,
        "unit_title": "Dimensional Modeling & Schemas",
        "topic": "Fact Table Design, Keys, and Additive Measures",
        "book": "The Data Warehouse Toolkit - Ralph Kimball",
        "page_ref": "Pages 35 - 55",
        "definition": "A Fact Table is the central table in a dimensional star or snowflake schema containing quantitative numerical business measurements (facts) and foreign keys referencing connected dimension tables.",
        "tamil_definition": "உண்மை அட்டவணை (Fact Table) என்பது ஸ்டார் ஸ்கீமாவின் நடுவில் அமைந்துள்ள முக்கிய அட்டவணையாகும். இதில் எண்களாலான அளவீடுகளும் (விற்பனை, லாபம்) மற்றும் பிற பரிமாண அட்டவணைகளின் ஃபாரின் கீகளும் (Foreign Keys) இடம்பெறும்.",
        "tanglish_summary": "Fact table star schema ku center la irukkum. Idhula business metrics (sales amount, quantity) and foreign keys to dimension tables irukkum.",
        "key_points": [
            "Grain of the Fact Table: Represents the fundamental atomic level of measurement (e.g., individual line item on a retail sales receipt).",
            "Composite Primary Key: Formed by the union of all foreign keys pointing to dimension tables.",
            "Measure Types: Fully Additive (can be summed across all dimensions like sales dollars), Semi-Additive (summed across some dimensions like bank balances), and Non-Additive (ratios/percentages).",
            "Factless Fact Tables: Record events or occurrences without numerical measures (e.g., student class attendance logs).",
            "Massive Volumetrics: Fact tables typically comprise 90%+ of total data warehouse storage capacity."
        ],
        "tamil_points": [
            "மைய இடம்: ஸ்டார் அமைப்பின் நடுவில் அமைந்து அனைத்து பரிமாண அட்டவணைகளுடன் இணைகிறது.",
            "அளவீடுகள்: விற்பனை எண்ணிக்கை, தொகை போன்ற கூட்டக்கூடிய எண்கள் இருக்கும்.",
            "ஃபாரின் கீகள்: Date_ID, Store_ID, Product_ID போன்ற பரிமாண இணைப்புகள் இருக்கும்.",
            "தானியங்கி வளர்ச்சி: நிறுவனத்தின் ஒவ்வொரு பரிவர்த்தனையிலும் இந்த அட்டவணை பெரிதாகிக்கொண்டே செல்லும்."
        ],
        "architecture_diagram": r"""
+-------------------------------------------------------------+
|             STAR SCHEMA WITH CENTRAL FACT TABLE             |
+-------------------------------------------------------------+
|  [Dim_Date]      [Dim_Product]      [Dim_Store]   [Dim_User]|
|      \                 |                 |           /      |
|       \                |                 |          /       |
|        v               v                 v         v        |
|    +----------------------------------------------------+   |
|    |               FACT_SALES TABLE                     |   |
|    +----------------------------------------------------+   |
|    | * Date_Key (FK)                                    |   |
|    | * Product_Key (FK)                                 |   |
|    | * Store_Key (FK)                                   |   |
|    | * Customer_Key (FK)                                |   |
|    | -------------------------------------------------- |   |
|    | Units_Sold       (Additive Metric)                 |   |
|    | Total_Revenue    (Additive Metric)                 |   |
|    | Discount_Amount  (Additive Metric)                 |   |
|    +----------------------------------------------------+   |
+-------------------------------------------------------------+
        """,
        "advantages": ["Highly denormalized for lightning-fast join queries", "Intuitive schema design for business analysts", "Scales seamlessly to billions of rows"],
        "applications": "POS retail billing analytics, airline ticket bookings, hospital patient admission tracking."
    }
}
