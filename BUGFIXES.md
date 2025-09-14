# Bug Fixes Applied to sgBusLaoBu2021

This document summarizes the bugs that were identified and fixed in the repository.

## Fixed Issues

### 1. SQL Syntax Error ✅
**File:** `sqlcommands.py`  
**Issue:** Missing commas in CREATE TABLE statement causing SQL syntax errors  
**Fix:** Added proper comma separators between constraints in the Bus_Routes table definition

```sql
# Before (broken):
PRIMARY KEY (ServiceNo,Direction,Stopsequence)
FOREIGN KEY(BusStopCode) REFERENCES Bus_Stops(BusStopCode)

# After (fixed):
PRIMARY KEY (ServiceNo,Direction,Stopsequence),
FOREIGN KEY(BusStopCode) REFERENCES Bus_Stops(BusStopCode),
```

### 2. Variable Reference Bugs ✅
**File:** `functions.py`  
**Issue:** Incorrect use of `self.insert` instead of `insert` parameter in json_2_db function  
**Fix:** Replaced `self.insert` with correct `insert` parameter

### 3. Type Checking Logic Bug ✅
**File:** `functions.py`  
**Issue:** Incorrect boolean logic in haversine function type checking  
**Fix:** Replaced faulty type check with proper isinstance validation

```python
# Before (broken):
if type(lat1) and type(lon1) and type(lat2) and type(lon2) is not float:

# After (fixed):
if not all(isinstance(coord, (int, float)) for coord in [lat1, lon1, lat2, lon2]):
```

### 4. Dependency Conflicts ✅
**File:** `requirements.txt`  
**Issue:** Incompatible greenlet version (0.4.15) with gevent 23.9.0  
**Fix:** Updated greenlet to compatible version (>=3.0rc1) and removed duplicate MarkupSafe entry

### 5. Duplicate Function Definition ✅
**File:** `main.py`  
**Issue:** Two `add_header` functions defined, causing the second to override the first  
**Fix:** Merged functionality into single function

### 6. Security Issue - Hardcoded API Key ✅
**File:** `main.py`  
**Issue:** Google Maps API key hardcoded in source code  
**Fix:** Implemented environment variable approach for secure API key management

```python
# Before (insecure):
GoogleMaps(app, key="AIzaSyCCvHi1Jn7gDxjrD1QHRZkPEII3Zy34vgU")

# After (secure):
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY_HERE')
GoogleMaps(app, key=GOOGLE_MAPS_API_KEY)
```

### 7. Incorrect Geographic Coordinates ✅
**File:** `main.py`  
**Issue:** Map initialized with California coordinates instead of Singapore  
**Fix:** Updated to proper Singapore coordinates (1.3521, 103.8198)

### 8. Missing Error Handling ✅
**Files:** `functions.py`, `main.py`  
**Issue:** File operations without error handling could cause crashes  
**Fix:** Added try-except blocks for file I/O operations

### 9. Code Quality Improvements ✅
- Added proper `.gitignore` file to exclude build artifacts
- Improved error handling throughout the codebase
- Better type validation in utility functions

## Security Recommendations

### Environment Variables Setup
To run the application securely, set the Google Maps API key as an environment variable:

```bash
export GOOGLE_MAPS_API_KEY="your_actual_api_key_here"
```

Or create a `.env` file (make sure it's in `.gitignore`):
```
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure config management
- Restrict API key permissions to only necessary services
- Monitor API key usage for unusual activity

## Testing

A validation script `test_bug_fixes.py` has been created to verify all fixes are working correctly. Run it with:

```bash
python3 test_bug_fixes.py
```

All tests should pass, confirming the bugs have been successfully resolved.

## Summary of Changes

- 🔧 Fixed 6 critical bugs across 3 main files
- 🔒 Improved security by removing hardcoded credentials  
- 🧪 Added comprehensive test validation
- 📚 Enhanced error handling and code quality
- 🗂️ Added proper .gitignore for cleaner repository

The codebase is now more secure, stable, and maintainable.