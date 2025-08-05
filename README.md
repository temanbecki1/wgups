# WGUPS Package Routing System

**Student ID:** 012172824

A comprehensive package routing system implementing a nearest neighbor algorithm with both command-line and web-based interfaces.

## Features

### Core Algorithm
- ✅ Custom hash table implementation (no external data structures)
- ✅ Nearest neighbor greedy algorithm for route optimization
- ✅ Total mileage under 140 miles requirement
- ✅ All package delivery constraints satisfied

### Constraint Handling
- ✅ Package #9 wrong address correction at 10:20 AM
- ✅ "Must be on truck 2" packages properly routed
- ✅ Delayed packages (arrive at 9:05 AM)
- ✅ Early deadline packages prioritized
- ✅ Driver sharing between trucks

### Interfaces
1. **Command Line Interface (CLI)** - Original Python implementation
2. **Web Interface** - Modern React frontend with Flask API backend

## Project Structure

```
wgups/
├── main.py                     # Original CLI application
├── hash_table.py              # Custom hash table implementation
├── app.py                     # Flask API backend
├── WGUPS_Package_File.csv     # Package data
├── WGUPS_Distance_Table.csv   # Distance matrix
├── WGUPS_Address_File.csv     # Address mappings
└── wgups-frontend/           # React web application
    ├── src/
    │   ├── App.js
    │   ├── components/
    │   │   ├── TotalMileage.js
    │   │   ├── PackageTracker.js
    │   │   ├── TimeStatusView.js
    │   │   └── FileUpload.js
    │   └── index.js
    └── package.json
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Python Backend Setup
```bash
# Install Python dependencies
pip install flask flask-cors

# Verify CSV files are present
# - WGUPS_Package_File.csv
# - WGUPS_Distance_Table.csv  
# - WGUPS_Address_File.csv
```

### React Frontend Setup
```bash
# Navigate to frontend directory
cd wgups-frontend

# Install dependencies (already done if following this guide)
npm install

# Verify all dependencies installed
npm list
```

## Running the Applications

### Option 1: Command Line Interface (CLI)
```bash
# Run the original Python CLI
python main.py

# Follow prompts to:
# 1. Look up individual packages
# 2. View all packages at specific times
# 3. Exit
```

### Option 2: Web Interface (Recommended for Screenshots)

**Step 1: Start the Flask API Backend**
```bash
# In the main wgups directory
python app.py

# Should see:
# Initializing WGUPS routing data...
# Data initialized successfully!
# Starting Flask server...
# * Running on http://127.0.0.1:5000
```

**Step 2: Start the React Frontend**
```bash
# In a new terminal, navigate to frontend
cd wgups-frontend

# Start the React development server
npm start

# Should automatically open browser to http://localhost:3000
```

## Web Interface Features

### 1. Total Mileage Summary
- Real-time display of total mileage (117.90 miles)
- Individual truck mileage breakdown
- Success indicator for under-140-mile requirement

### 2. Package Tracker
- Individual package lookup by ID
- Time-based status checking
- Detailed package information display
- Status indicators: At the hub / En route / Delivered

### 3. Time Status View (Perfect for Screenshots)
- View all packages organized by truck at specific times
- Quick select buttons for required screenshot times:
  - **Between 8:35-9:25 AM** (9:00 AM)
  - **Between 9:35-10:25 AM** (10:00 AM)  
  - **Between 12:03-1:12 PM** (12:30 PM)
- Expandable truck sections showing all package details
- Summary statistics

### 4. File Upload Interface
- CSV file upload capability (demonstration)
- Validates file formats
- Shows upload progress
- Ready for production implementation

## Taking Required Screenshots

1. **Start both servers** (Flask backend + React frontend)
2. **Navigate to "Time Status View" tab**
3. **Click the preset time buttons:**
   - "Between 8:35-9:25 AM" button
   - "Between 9:35-10:25 AM" button
   - "Between 12:03-1:12 PM" button
4. **Take screenshots** of each time view showing all trucks and packages

## API Endpoints

The Flask backend provides these REST API endpoints:

- `GET /api/total-mileage` - Total mileage for all trucks
- `GET /api/trucks` - Truck information and package assignments
- `GET /api/package/{id}` - Individual package details
- `GET /api/package/{id}/status?time={HH:MM}` - Package status at specific time
- `GET /api/packages/status?time={HH:MM}` - All packages status at specific time
- `GET /api/initialize` - Reinitialize routing data

## Algorithm Performance

- **Total Distance:** 117.90 miles (✅ Under 140 miles)
- **Truck 1:** 30.50 miles (12 packages, departs 8:00 AM)
- **Truck 2:** 52.40 miles (16 packages, departs 9:05 AM)
- **Truck 3:** 35.00 miles (12 packages, departs 9:41 AM)
- **All packages delivered successfully**

## Technical Implementation

### Hash Table
- Custom implementation using chaining for collision resolution
- O(1) average case lookup and insertion
- No external data structure libraries used

### Routing Algorithm
- Nearest neighbor greedy approach
- Handles all package constraints and special requirements
- Time complexity: O(n²) where n is packages per truck
- Space complexity: O(n) for package storage

### Web Technology Stack
- **Backend:** Flask (Python) with CORS support
- **Frontend:** React with Material-UI components
- **HTTP Client:** Axios for API communication
- **Styling:** Material-UI design system

## Development Notes

This implementation satisfies all C950 course requirements:
- ✅ Self-adjusting data structure (custom hash table)
- ✅ Greedy algorithm implementation
- ✅ All delivery constraints met
- ✅ Under 140 miles total distance
- ✅ Intuitive user interface (both CLI and web)
- ✅ Time-based package status tracking
- ✅ Complete documentation

The web interface enhances the original CLI with a modern, intuitive design perfect for demonstrations and screenshots required for project submission. 