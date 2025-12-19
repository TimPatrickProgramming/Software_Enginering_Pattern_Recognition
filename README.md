# Software Engineering Pattern Recognition Project

## Purpose of this Project

This project implements a Python-based computer vision application for real-time pattern and color recognition. The system can identify geometric shapes (circles, rectangles, squares, and triangles) and their associated colors (red, green, blue, yellow and violet) from visual input.

### Key Features

- **Dual Input Modes**: Process images from a live camera feed or from a folder of static images
- **Shape Detection**: Recognizes circles, rectangles, squares, and triangles using contour approximation
- **Color Recognition**: Identifies five base colors (red, green, blue, yellow and violet) through HSV color space filtering
- **Visual Feedback**: Highlights detected patterns directly on the processed images
- **Automated Logging**: Records all detections with their shape type and color to a CSV file
- **Configurable Settings**: Customize color ranges and detection parameters via an external configuration file

## Project Setup

For the project setup, a virtual environment needs to be created. Follow the steps below to set up the venv and execute the script.

1. Navigate to your project directory in your terminal of choice.
    - VS Code is the simplest solution for this, as the terminal already opens in your project directory
2. Create your virtual environment and name it accordingly, e.g., 'virtualbox'
    - `python -m venv virtualbox`
3. Activate the virtual environment. Make sure to remain in the project directory
    - `virtualbox\Scripts\activate` (Windows)
4. Install the required libraries from requirements.txt
    - `pip install -r requirements.txt`
5. Now you are ready to start the project by executing main.py
    - `python main.py`
    - **Note for VS Code users**: Ensure you select the correct Python interpreter for your virtual environment
        - Press `Ctrl + Shift + P` and type `Python: Select Interpreter`
        - Select the Python version associated with your virtual environment (e.g., the one inside `virtualbox`)
6. To deactivate the venv, enter the following command in the terminal
    - `deactivate`

## Project Structure

The project follows a modular structure with clear separation of concerns:

```
Software_Enginering_Pattern_Recognition/
│
├── Python/                      # Main source code directory
│   ├── main.py                  # Application entry point - handles mode selection and initialization
│   ├── ShapeDetectorApp.py      # PyQt6 GUI application class
│   ├── Image_Loader.py          # Handles image acquisition from camera or folder
│   ├── Image_Processing.py      # Core vision processing - HSV conversion, contour detection, shape classification
│   ├── Shape.py                 # Shape data model hierarchy (Triangle, Rectangle, Square, Circle)
│   ├── Visualisation.py         # Rendering utilities for drawing contours and labels
│   ├── Logger.py                # CSV logging functionality for detection results
│   └── config.ini               # Configuration file for color ranges and system settings
│
├── Documents/                   # Project documentation and reports
├── Pictures/                    # Sample images for testing and demonstration
│
├── requirements.txt             # Python dependencies specification
├── README.md                    # Project documentation (this file)
└── .gitignore                   # Git ignore rules
```

### Key Files Description

- **[main.py](Python/main.py)**: Orchestrates application startup, reads configuration, and delegates to either GUI or console mode
- **[config.ini](Python/config.ini)**: Defines HSV color ranges for detection and system parameters (camera index, log path, default modes)
- **[requirements.txt](requirements.txt)**: Lists all Python package dependencies with version specifications


## Architecture

The architecture of this pattern recognition system follows object-oriented design principles with clear separation of concerns. The application is structured into distinct layers: data acquisition (Image_Loader), processing logic (Image_Processing, Visualisation), data models (Shape hierarchy), persistence (Logger), and presentation (ShapeDetectorApp for GUI, main.py for console mode).

This modular architecture enables flexibility in input sources (camera or folder), processing pipelines, and output modes (GUI or console), while maintaining a clean dependency structure where each component has a well-defined responsibility.

### Static View - Class Diagram

```mermaid
classDiagram
    class Shape {
        <<abstract>>
        +approx: ApproxType
        +color_name: str
        +__init__(approx, color_name)
    }
    
    class Triangle {
        +__init__(approx, color_name)
    }
    
    class Rectangle {
        +__init__(approx, color_name)
    }
    
    class Square {
        +__init__(approx, color_name)
    }
    
    class Circle {
        +__init__(approx, color_name)
    }
    
    class Image_Loader {
        -image_path: str
        -cam: VideoCapture
        +__init__(image_path, select_camera)
        +load_folder_images() List~ndarray~
        +load_camera_image() ndarray
        +release_camera()
    }
    
    class Image_Processing {
        -colors: Dict
        -ranges: Dict
        +__init__(colors, ranges)
        +process_image(image) Tuple~ndarray, List~Shape~~
    }
    
    class Logger {
        -log_path: str
        +__init__(log_path)
        +log_detection(shapes)
    }
    
    class Visualisation {
        +draw_contours(imageFrame, shapes)$ ndarray
    }
    
    class ShapeDetectorApp {
        -image_loader: Image_Loader
        -image_processor: Image_Processing
        -logger: Logger
        -timer: QTimer
        -current_mode: str
        -image_files: List~ndarray~
        -current_image_index: int
        +__init__(image_loader, image_processor, logger)
        +setup_ui()
        +select_folder()
        +check_mode_change()
        +switch_mode(mode)
        +start_camera_mode()
        +start_image_mode()
        +load_current_image()
        +load_next_image()
        +update_camera_frame()
        +process_and_display(image)
        +closeEvent(event)
    }
    
    Shape <|-- Triangle
    Shape <|-- Rectangle
    Shape <|-- Square
    Shape <|-- Circle
    
    Image_Processing --> Shape : creates
    Image_Processing --> Visualisation : uses
    ShapeDetectorApp --> Image_Loader : uses
    ShapeDetectorApp --> Image_Processing : uses
    ShapeDetectorApp --> Logger : uses
    Logger --> Shape : logs
```

#### Class Responsibilities

**Data Models:**
- **Shape (Abstract)**: Base class for all geometric shapes, storing contour approximation and color information
- **Triangle, Rectangle, Square, Circle**: Concrete shape implementations inheriting from Shape

**Core Processing:**
- **Image_Loader**: Manages image acquisition from both camera streams and folder-based image collections
- **Image_Processing**: Core vision processing - converts images to HSV color space, applies color masks, detects contours, and classifies shapes
- **Visualisation**: Renders detected shapes and their labels onto processed images

**Application Layer:**
- **ShapeDetectorApp**: PyQt6-based GUI providing interactive mode switching, folder selection, and real-time visualization
- **Logger**: Persists detection results to CSV files for analysis and record-keeping

**Dependencies:**
The architecture maintains a unidirectional dependency flow: ShapeDetectorApp orchestrates Image_Loader, Image_Processing, and Logger; Image_Processing creates Shape instances and utilizes Visualisation for rendering; Logger references Shape objects for persistence.

### Dynamic View - Sequence Diagram

The sequence diagram illustrates the runtime behavior of the application in both GUI and console modes. The flow begins with initialization where the main module reads configuration settings and instantiates the core components (Image_Loader, Image_Processing, Logger).

In **GUI mode**, the ShapeDetectorApp orchestrates continuous processing loops that acquire images (from camera or folder), pass them through the image processing pipeline, and display results. The Image_Processing component performs the core computer vision workflow: HSV conversion, color-based masking, contour detection, polygon approximation, and shape classification. For each detected shape meeting the area threshold, appropriate Shape objects are instantiated. The Visualisation utility then annotates the image with bounding contours and labels before display.

In **console mode**, the main module directly manages the processing loop and uses OpenCV windows for display instead of a GUI framework.

Both modes follow the same core processing pipeline and log all detections to CSV through the Logger component, ensuring consistent behavior regardless of interface choice.

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant App as ShapeDetectorApp
    participant Loader as Image_Loader
    participant Processor as Image_Processing
    participant Vis as Visualisation
    participant Log as Logger
    participant Shape

    User->>Main: Start Application
    Main->>Main: Read config.ini
    Main->>Loader: Create Image_Loader
    Main->>Processor: Create Image_Processing
    Main->>Log: Create Logger
    
    alt GUI Mode
        Main->>App: Create ShapeDetectorApp
        App->>App: setup_ui()
        
        loop Camera/Image Mode Active
            alt Camera Mode
                App->>Loader: load_camera_image()
                Loader-->>App: return frame
            else Image Mode
                App->>Loader: load_folder_images()
                Loader-->>App: return images[]
            end
            
            App->>Processor: process_image(image)
            Processor->>Processor: Convert to HSV
            
            loop For each color range
                Processor->>Processor: Create color mask
                Processor->>Processor: Find contours
                
                loop For each contour
                    Processor->>Processor: Approximate polygon
                    Processor->>Processor: Calculate area
                    
                    alt area > 300
                        alt 3 vertices
                            Processor->>Shape: Create Triangle
                        else 4 vertices
                            Processor->>Processor: Check if square
                            alt Square
                                Processor->>Shape: Create Square
                            else Rectangle
                                Processor->>Shape: Create Rectangle
                            end
                        else > 6 vertices
                            Processor->>Shape: Create Circle
                        end
                    end
                end
            end
            
            Processor->>Vis: draw_contours(image, shapes)
            Vis-->>Processor: return annotated_image
            Processor-->>App: return (image, shapes)
            
            App->>Log: log_detection(shapes)
            Log->>Log: Write to CSV
            
            App->>User: Display processed image
        end
        
    else Console Mode
        loop Until Quit
            alt Camera Mode
                Main->>Loader: load_camera_image()
                Loader-->>Main: return frame
            else Image Mode
                Main->>Loader: load_folder_images()
                Loader-->>Main: return images[]
            end
            
            Main->>Processor: process_image(image)
            Processor-->>Main: return (image, shapes)
            Main->>Log: log_detection(shapes)
            Main->>User: Display with OpenCV
        end
    end
```
