# Capacity Test Debugging Guide

## Current Issue

Users are reporting "WRITE ERROR - size mismatch" on every file during capacity tests. The bash script works fine, so the drive is good.

## Diagnostic Steps

### Step 1: Run with Debug Output

The latest version includes enhanced debug output. Run a small test:

```bash
sudo python3 test_usb.py -c /mnt --size-gb 1
```

Look for output like:
```
Writing file 1/10... 
  Debug: chunks=100, bytes_written=104857600, file_size=104857600
  OK (verified)
```

### Step 2: Check What's Reported

If you see SIZE MISMATCH, note these values:
- **Expected**: Should be 104857600 (100MB)
- **Got**: The actual file size
- **chunks**: How many chunks were generated
- **bytes_written**: How many bytes the code thinks it wrote

### Possible Issues

#### Issue 1: Disk Write Failure
```
Writing file 1/10... WRITE FAILED: [Errno 28] No space left on device
```
**Solution**: Drive is full or has quota limits

#### Issue 2: Size Mismatch
```
Writing file 1/10... SIZE MISMATCH
  Expected: 100.00 MB, Got: 0.00 B
```
**Possible causes**:
- File system issue
- Mount point issue
- Permissions problem

#### Issue 3: Partial Writes
```
Debug: chunks=100, bytes_written=104857600, file_size=52428800
```
**Possible causes**:
- Disk error during write
- Controller issue
- Bad USB cable/port

### Step 3: Compare with Bash Script

Run the same test with the working bash script:

```bash
# Create a test directory
mkdir /mnt/bash_test
cd /mnt/bash_test

# Write a single f3 file
python3 -c "
data = b'test' * 262144  # 1MB
with open('test.dat', 'wb') as f:
    for i in range(100):  # 100MB
        f.write(data)
    f.flush()
    import os
    os.fsync(f.fileno())

import os.path
print(f'File size: {os.path.getsize(\"test.dat\")} bytes')
print(f'Expected: {100 * 1024 * 1024} bytes')
"

# Clean up
rm test.dat
cd /
rmdir /mnt/bash_test
```

### Step 4: Check Filesystem

```bash
# Check filesystem type
df -T /mnt

# Check for errors
dmesg | tail -20

# Check mount options
mount | grep /mnt
```

## Known Working Configuration

**From the bash script that works:**
- Tool: f3write/f3read  
- Files: *.h2w files (1GB each typically)
- Method: Sequential writes with periodic syncs
- Verification: Pattern-based checking

## What the Python Script Does Differently

**test_usb.py approach:**
- Files: 100MB each in subdirectory
- Method: SHA-256 checksums
- Verification: Hash comparison
- Sync: After each file with fsync()

## Potential Root Cause

The issue might be:
1. **Generator pattern size** - Fixed in latest version with exact 1MB chunks
2. **Missing fsync()** - Fixed by adding fsync() after each write
3. **Buffering issues** - Need to investigate further
4. **File system limitations** - Some FS have issues with many small files

## Recommended Fix: Match f3 Behavior More Closely

Instead of 100MB files, use larger 1GB files like f3:

```python
file_size_mb = 1024  # 1GB per file (like f3)
num_files = test_size_gb  # 1 file per GB
```

Benefits:
- Fewer files to manage
- Less filesystem overhead
- Closer to proven f3 approach
- Faster with fewer fsync() calls

## Debug Commands

### Check if files are actually being created:
```bash
ls -lh /mnt/capacity_test_*/
```

### Check actual file sizes:
```bash
du -sh /mnt/capacity_test_*/*
```

### Monitor disk writes in real-time:
```bash
# In another terminal
watch -n 1 'df -h /mnt; ls -lh /mnt/capacity_test_*/ | tail -5'
```

## Next Steps

1. Run test with 1-2 GB first (not 931 GB!)
2. Check debug output
3. Verify files are actually created
4. Compare with bash script behavior
5. Report findings

---

**Status**: Under Investigation  
**Date**: January 19, 2026
