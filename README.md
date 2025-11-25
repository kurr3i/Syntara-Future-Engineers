Project Overview:

The Future Engineers Syntara project is a student-led initiative that integrates robotics, computer vision, and event-driven programming to create a fully autonomous robotic car. The system is designed to navigate indoor environments while performing three main tasks: detecting obstacles, reacting appropriately to them, and tracking objects using AI vision.
The Syntara robot can identify and avoid obstacles of different types. Green obstacles are bypassed to the left, while red obstacles are avoided to the right. This behavior is based on real-time sensor input and intelligent decision-making. The combination of Arduino-controlled actuation and Raspberry Pi-based high-level processing enables a modular, scalable, and responsive robotic system.
This project also serves as a practical demonstration of Event-Driven Architecture (EDA) in embedded robotics, emphasizing clean separation between sensing, processing, and actuation layers.

System Architecture:

The Syntara robotic system consists of two primary layers:

Arduino Microcontroller Layer
The Arduino handles low-level motor and servo control. It receives high-level movement commands from the Raspberry Pi via USB-Serial communication and executes them in real time. A physical push-button triggers system startup, allowing the Arduino to notify the Raspberry Pi that it is ready to begin operations. This layer ensures precise actuation and real-time responsiveness.

Raspberry Pi High-Level Layer
The Raspberry Pi runs a modular Python software stack divided into core modules. It handles sensor reading, decision-making, and communication with the Arduino. The system employs an Event-Driven Architecture (EDA), where events such as incoming serial data or HuskyLens object detections are dispatched to registered handlers via an Event Bus. This design promotes decoupling, scalability, and maintainability.

Key components include:

Serial Communication Module: Handles all reading and writing to the Arduino.

HuskyLens Reader Module: Interfaces with the AI vision camera, detecting and stabilizing object recognition events.

Handlers Module: Defines high-level reactions to events, translating sensor input into movement commands.

Event Bus: Facilitates modular communication between components without direct dependencies.

The system runs multiple threads: one for serial listening, another for AI vision processing, and the main thread managing event subscriptions. This enables simultaneous data acquisition, decision-making, and command dispatching.

Core Modules Description

Arduino Module — Microcontroller_commands.ino
This module implements the low-level motor and servo control logic of the Syntara prototype. The Arduino acts as an embedded controller responsible for executing simple, time-sensitive motion commands triggered by the Raspberry Pi through a USB-Serial connection.
The program manages a DC motor (via IN1/IN2 pins) and a servo motor, both orchestrated through a minimal command protocol. A physical push-button connected to the board sends an initialization signal ('q') to the Raspberry Pi, allowing the high-level system to detect when the user manually activates the robot. Once the Pi sends a 'w' command, the Arduino unlocks movement and begins forward motion.
Special commands ('e', 'v', 'u') allow the Raspberry Pi to request predefined action sequences involving motor stops, servo adjustments, or complex maneuvers. When each sequence finishes, the microcontroller automatically returns to the forward-movement state. Debounce handling, safety stops, and continuous serial polling ensure stable real-time operation.

Raspberry Core Module — event_bus.py
This module implements the central Event Bus used across the Raspberry Pi subsystem. It provides a lightweight, extensible Event-Driven Architecture (EDA) that allows different components—such as serial readers, HuskyLens modules, and high-level logic handlers—to communicate through strongly typed events instead of direct function calls.
The EventBus class maintains an internal registry of event types mapped to their corresponding handler functions. Components can subscribe to specific event classes, enabling clean decoupling and modular growth. When an event is published, the bus automatically dispatches it to every registered handler, printing diagnostic messages to support debugging during development.
This architecture enables the project to scale while maintaining clear boundaries between sensing, processing, and actuation layers.

Raspberry Core Module — events.py
This module defines the full set of event types used throughout the Syntara system. Each class represents a structured message that encapsulates information flowing between components such as the serial interface, HuskyLens readers, and high-level decision logic. The module uses Python’s dataclass pattern to provide lightweight, immutable containers for event data.
StartEvent and SerialDataReceivedEvent support the interaction between the Raspberry Pi and the Arduino, signaling startup triggers and incoming serial commands. The set of HuskyLens-related events (e.g., HuskyLensObjectDetectedEvent) provide bounding-box information for tracked objects, which higher-level modules use to determine reactive behavior. Additional proximity-based events like RightCloseEvent, LeftFarEvent, or FrontCloseEvent allow sensor data to be translated into abstract, direction-specific system actions.
This event taxonomy forms the backbone of the project’s event-driven architecture.

Raspberry Core Module — handlers.py
This module contains the system’s high-level event handlers, responsible for translating raw sensor data and serial messages into concrete robot actions. It forms the “decision layer” of the Raspberry Pi subsystem.
The handle_serial_data function processes single-character signals received from the Arduino—representing proximity states detected by ultrasonic sensors—and applies a stability-counter mechanism to reduce noise. Once a condition becomes stable (e.g., repeated 'f', 'r', 'l' inputs), the handler triggers the appropriate motor sequence by sending structured commands back to the Arduino. Priority rules ensure that critical events, such as front-close obstacles, override all other actions.
Additional helper functions (execute_left_far_sequence, execute_front_close_sequence, etc.) define reusable behavior templates. The module also includes handle_huskylens_detection, which forwards object-tracking data from the HuskyLens camera to the Arduino using an encoded string format. This enables coordinated visual-based behaviors in the robot.

Raspberry Core Module — serial_communication.py
This module manages all low-level serial communication between the Raspberry Pi and the Arduino. It abstracts the USB-Serial link into a clean communication layer that supports initialization, data transmission, continuous listening, and safe shutdown.
The initialize_serial_connection function configures the serial port, resets the input buffer, and ensures stable communication at 115200 baud. Outgoing messages are handled through send_command, which sends ASCII-encoded control characters back to the microcontroller. Incoming data is processed by read_serial_data, which performs non-blocking reads, removes null bytes, and returns sanitized payloads.
The serial_listen_loop runs as a continuous event-emission routine that converts every piece of incoming data into a SerialDataReceivedEvent and publishes it through the Event Bus. This design allows asynchronous integration with the rest of the system. Safe shutdown is handled by close_serial_connection.

Raspberry Core Module — huskylens_reader.py
This module implements the vision-processing layer of the system by interfacing directly with the HuskyLens AI camera through I2C. It continuously retrieves detected objects, applies temporal filtering for stability, and publishes high-level detection events to the Event Bus.
The huskylens_loop routine polls the camera for detected objects, tracking IDs 1 and 2. A stability mechanism ensures that only consistently detected objects trigger events, reducing false positives. Each detection emits a HuskyLensObjectDetectedEvent containing position and size information, which downstream handlers use to make movement decisions. The module also manages disconnections or I2C errors gracefully.

Raspberry Main Module — main.py
This is the entry point for the Raspberry Pi subsystem, responsible for initializing the event-driven architecture and starting concurrent tasks. It orchestrates the integration of vision, serial communication, and high-level decision handlers.
The program launches huskylens_loop and serial_listen_loop in dedicated daemon threads, while the main thread subscribes handlers to the Event Bus. This setup enables simultaneous object detection, serial monitoring, and command dispatching. The main thread maintains execution while background threads handle sensing and actuation. KeyboardInterrupt is gracefully handled to allow safe shutdown.
This modular threading design creates a fully asynchronous, event-driven robot control architecture.

Future Work and Conclusion
The Syntara project demonstrates a successful integration of embedded hardware, AI vision, and event-driven software in a small autonomous robot. Future improvements may include more sophisticated obstacle classification, path planning algorithms, and multi-object tracking. The modular EDA architecture ensures that new sensors or behaviors can be added without disrupting existing functionality.
This project serves as a hands-on learning experience in robotics, AI vision, and software engineering for aspiring engineers, combining hardware control, real-time communication, and scalable software architecture.