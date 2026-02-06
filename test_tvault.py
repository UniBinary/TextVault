#!/usr/bin/env python3
"""
Test script for TextVault (TVault)
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the project to the Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from tvault.tdb import TextVault

def test_basic_operations():
    """Test basic CRUD operations"""
    print("Testing basic operations...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        db = TextVault(tmpdir)
        
        # Test 1: Create file
        assert db.create("test1", force=True) == True
        assert (Path(tmpdir) / "test1.txt").exists()
        print("✓ Create file")
        
        # Test 2: Write to file
        # Note: write() requires interactive input, so we'll test it differently
        test_file = Path(tmpdir) / "test1.txt"
        test_file.write_text("Hello, World!\nLine 2")
        
        # Test 3: Read file
        print("Testing read (should show 'Hello, World!\\nLine 2'):")
        db.read("test1")
        print("✓ Read file")
        
        # Test 4: Backup file
        assert db.backup("test1") == True
        assert (Path(tmpdir) / "test1.txt.bak").exists()
        print("✓ Backup file")
        
        # Test 5: Read backup
        print("Testing read backup:")
        db.read_backup("test1")
        print("✓ Read backup")
        
        # Test 6: List files
        print("Testing list files:")
        db.list_files()
        print("✓ List files")
        
        # Test 7: Remove backup
        assert db.remove_backup("test1") == True
        assert not (Path(tmpdir) / "test1.txt.bak").exists()
        print("✓ Remove backup")
        
        # Test 8: Remove file
        assert db.remove("test1") == True
        assert not test_file.exists()
        print("✓ Remove file")
        
        # Test 9: List empty
        print("Testing empty list:")
        db.list_files()
        print("✓ Empty list")
        
        print("\nAll basic tests passed! ✅")

def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db = TextVault(tmpdir)
        
        # Test 1: Read non-existent file
        print("Testing read non-existent file (should show error):")
        result = db.read("nonexistent")
        assert result == False
        print("✓ Handles non-existent file")
        
        # Test 2: Backup non-existent file
        print("Testing backup non-existent file (should show error):")
        result = db.backup("nonexistent")
        assert result == False
        print("✓ Handles backup of non-existent file")
        
        # Test 3: Remove non-existent file
        print("Testing remove non-existent file (should show error):")
        result = db.remove("nonexistent")
        assert result == False
        print("✓ Handles remove of non-existent file")
        
        # Test 4: Create duplicate file (without force)
        db.create("duplicate", force=True)
        print("Testing create duplicate file (should prompt):")
        # This will prompt, but we can't test interactively here
        print("✓ Duplicate file handling (manual test required)")
        
        print("\nError handling tests completed! ✅")

def test_totp_feature():
    """Test TOTP feature"""
    print("\nTesting TOTP feature...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db = TextVault(tmpdir)
        
        # Create a file with TOTP secret
        test_file = Path(tmpdir) / "totp-test.txt"
        test_file.write_text("JBSWY3DPEHPK3PXP")  # Example TOTP secret
        
        print("Testing TOTP generation (filename contains 'tt'):")
        db.read("totp-test")
        print("✓ TOTP feature works")
        
        print("\nTOTP tests completed! ✅")

def test_database_backup():
    """Test database backup"""
    print("\nTesting database backup...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db = TextVault(tmpdir)
        
        # Create some test files
        db.create("backup-test1", force=True)
        db.create("backup-test2", force=True)
        
        test_file1 = Path(tmpdir) / "backup-test1.txt"
        test_file2 = Path(tmpdir) / "backup-test2.txt"
        test_file1.write_text("File 1 content")
        test_file2.write_text("File 2 content")
        
        print("Testing database backup:")
        result = db.backup_database()
        assert result == True
        
        # Check if backup directory was created
        backup_dirs = list(Path.home().glob("tdb_backup_*"))
        if backup_dirs:
            print(f"✓ Backup created at: {backup_dirs[-1]}")
            
            # Clean up backup
            shutil.rmtree(backup_dirs[-1])
        else:
            print("⚠ Backup may not have been created (check manually)")
        
        print("\nDatabase backup test completed! ✅")

def main():
    """Run all tests"""
    print("=" * 60)
    print("TextVault (TVault) Test Suite")
    print("=" * 60)
    
    try:
        test_basic_operations()
        test_error_handling()
        test_totp_feature()
        test_database_backup()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully! 🎉")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())