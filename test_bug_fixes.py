#!/usr/bin/env python3
"""
Bug fix validation tests for sgBusLaoBu2021

This script validates that the identified bugs have been fixed.
"""

import sys
import os
import sqlite3

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_sql_syntax():
    """Test that SQL commands are syntactically correct"""
    try:
        from sqlcommands import commands
        
        # Test that we can create a connection and execute the CREATE statement
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # This should not raise a syntax error anymore
        cursor.execute(commands["createbusroutestable"])
        print("✓ SQL syntax fixed: CREATE TABLE statement executes without syntax errors")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ SQL syntax test failed: {e}")
        return False

def test_functions_variables():
    """Test that variable references in functions.py are correct"""
    try:
        import functions
        
        # Test haversine function with correct type checking
        result = functions.haversine(1.0, 2.0, 3.0, 4.0)
        assert result is not None and isinstance(result, float)
        print("✓ Haversine function type checking fixed")
        
        # Test with invalid types - should return None and print error
        result = functions.haversine('invalid', 2.0, 3.0, 4.0)
        assert result is None
        print("✓ Haversine function properly handles invalid input types")
        
        return True
    except Exception as e:
        print(f"✗ Functions test failed: {e}")
        return False

def test_import_syntax():
    """Test that all modules can be imported without syntax errors"""
    try:
        import main  # This will fail due to missing dependencies, but should not have syntax errors
        print("✓ Main module has no syntax errors")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in main module: {e}")
        return False
    except ImportError:
        print("✓ Main module has no syntax errors (import dependencies missing as expected)")
        return True
    except Exception as e:
        print(f"✗ Unexpected error in main module: {e}")
        return False

def test_requirements_compatibility():
    """Test that requirements.txt has been fixed for compatibility"""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Check that incompatible greenlet version has been removed
        assert 'greenlet==0.4.15' not in content
        assert 'greenlet>=3.0rc1' in content or 'greenlet' not in content
        print("✓ Requirements.txt dependency conflict fixed")
        
        # Check that duplicate MarkupSafe has been removed
        markup_count = content.count('MarkupSafe')
        assert markup_count <= 1
        print("✓ Duplicate MarkupSafe dependency removed")
        
        return True
    except Exception as e:
        print(f"✗ Requirements test failed: {e}")
        return False

def test_security_improvements():
    """Test that security issues have been addressed"""
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check that hardcoded API key has been removed
        assert 'AIzaSyCCvHi1Jn7gDxjrD1QHRZkPEII3Zy34vgU' not in content
        print("✓ Hardcoded Google API key removed")
        
        # Check that environment variable approach is used
        assert 'os.environ.get' in content
        print("✓ Environment variable approach implemented for API key")
        
        return True
    except Exception as e:
        print(f"✗ Security test failed: {e}")
        return False

def test_code_quality_improvements():
    """Test that code quality issues have been fixed"""
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check that duplicate add_header function has been removed
        add_header_count = content.count('def add_header(')
        assert add_header_count == 1
        print("✓ Duplicate add_header function removed")
        
        # Check that Singapore coordinates are used instead of hardcoded US coordinates
        assert '37.4419' not in content and '122.1419' not in content
        assert '1.3521' in content and '103.8198' in content
        print("✓ Hardcoded US coordinates replaced with Singapore coordinates")
        
        return True
    except Exception as e:
        print(f"✗ Code quality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running bug fix validation tests...\n")
    
    tests = [
        test_sql_syntax,
        test_functions_variables,
        test_import_syntax,
        test_requirements_compatibility,
        test_security_improvements,
        test_code_quality_improvements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All bug fixes validated successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please review the fixes.")
        sys.exit(1)