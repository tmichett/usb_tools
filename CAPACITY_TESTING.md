# Capacity Testing Guide 📦

## Understanding USB Capacity Tests

### Important Clarification ✅

**f3write and f3read are ALREADY non-destructive to existing files!**

They write test files to FREE SPACE only and do NOT delete or overwrite your existing files. This was the original design of the f3 tools.

---

## How f3 Tools Work

### f3write
- Writes test files (*.h2w) to **FREE SPACE** only
- Does NOT touch existing files
- Fills all available free space
- Creates numbered test files (1.h2w, 2.h2w, etc.)

### f3read
- Reads back the *.h2w test files
- Verifies data integrity
- Detects fake/counterfeit drives
- Reports actual capacity vs claimed capacity

### Cleanup
- Both scripts automatically delete *.h2w files after testing
- Your original files remain untouched

---

## Testing Options

### Bash Script (usb_test.sh)

Simple and straightforward - ONE capacity test option:

```bash
sudo ./usb_test.sh -c /mnt
```

**What it does:**
- ✅ Preserves all existing files
- ✅ Fills all free space with test data
- ✅ Verifies drive capacity
- ✅ Cleans up automatically
- ⏱️ Takes time proportional to free space

---

### Python Script (usb_test.py)

Offers TWO capacity test options for flexibility:

#### 1. Quick Capacity Test (`-q`)

```bash
sudo python3 usb_test.py -q /mnt
# or custom size
sudo python3 usb_test.py -q /mnt --size 10
```

**What it does:**
- ✅ Preserves all existing files
- ✅ Writes limited data (default: 5 GB)
- ✅ Fast basic capacity check
- ✅ Detects obvious fraud
- ⚡ Completes in ~10-20 minutes

**Best for:**
- Quick verification
- Drives you're actively using
- When time is limited
- Initial screening

**Limitations:**
- Only tests a portion of the drive
- May miss issues in untested areas
- Less thorough than full test

#### 2. Full Capacity Test (`-c`)

```bash
sudo python3 usb_test.py -c /mnt
```

**What it does:**
- ✅ Preserves all existing files
- ✅ Fills ALL free space (uses f3write/f3read)
- ✅ Most thorough validation
- ✅ Detects subtle capacity fraud
- ⏱️ Takes hours on large drives

**Best for:**
- New USB drives
- Suspected counterfeits
- Maximum thoroughness
- Pre-deployment validation

---

## Common Misconceptions Addressed

### ❌ Myth: "f3 tests are destructive"

**✅ Reality:** f3write/f3read do NOT delete existing files. They only use free space.

### ❌ Myth: "I need to backup before testing"

**✅ Reality:** Your existing files are safe. However, the drive will be full during testing, so you can't save new files until the test completes.

### ❌ Myth: "The test will format my drive"

**✅ Reality:** No formatting occurs. Test files are written to free space and deleted after testing.

---

## What Capacity Tests Actually Check

### 1. Fake Capacity Detection
Some counterfeit drives report (e.g.) 256GB but actually only have 32GB. The extra "capacity" is fake - data written there is lost.

**How f3 detects this:**
- Writes known patterns across the drive
- Reads them back
- If data is corrupted or missing → fake capacity detected

### 2. Data Integrity
Tests that data written to the drive can be read back correctly.

### 3. Actual vs. Reported Size
Verifies the drive actually has the capacity it claims.

---

## When to Use Each Test

### Use Quick Test (-q) When:
- ✅ Time is limited (10-20 min vs hours)
- ✅ Drive is in active use with data
- ✅ Doing a preliminary check
- ✅ Regular health monitoring
- ✅ Drive seems normal

### Use Full Test (-c) When:
- ✅ Testing brand new drives
- ✅ Drive behavior is suspicious
- ✅ Maximum confidence needed
- ✅ You have time to spare
- ✅ Preparing for important use

---

## Typical Results

### Genuine Drive
```
Free space: 14.90 GB
Creating file 1.h2w ... OK!
Creating file 2.h2w ... OK!
...
Data OK: 14.90 GB (31242240 sectors)
Data LOST: 0.00 Byte (0 sectors)
```

### Fake Drive Example
```
Free space: 256.00 GB  (CLAIMED)
Creating file 1.h2w ... OK!
...
Creating file 248.h2w ... OK!
...
Data OK: 32.00 GB (67108864 sectors)
Data LOST: 224.00 GB (469762048 sectors)  ⚠️
WARNING: The drive claims 256GB but only 32GB is real!
```

---

## Technical Details

### Test File Format
- Files named: 1.h2w, 2.h2w, 3.h2w, etc.
- Each file is approximately 1 GB
- Contains a known test pattern
- Extension: .h2w (stands for "hex to write")

### Drive States During Testing

#### Before Test:
```
Drive: [Existing Files] [Free Space →→→→→→→]
```

#### During Test:
```
Drive: [Existing Files] [Test Files .h2w →→→]
```

#### After Test (Cleanup):
```
Drive: [Existing Files] [Free Space →→→→→→→]
```

---

## Performance Expectations

### Quick Test (5 GB):
- **Write**: ~5 minutes
- **Read/Verify**: ~5 minutes
- **Total**: ~10-15 minutes

### Full Test (varies by free space):
- **16 GB free**: ~30-40 minutes
- **64 GB free**: ~2 hours
- **256 GB free**: ~8 hours
- **500 GB free**: ~16 hours

*Times are approximate and depend on drive speed and USB version*

---

## Troubleshooting

### "Not enough space for quick test"
- Quick test needs at least 1.5 GB free
- Solution: Free up space or use smaller `--size 2`

### "Test is taking forever"
- Full tests on large drives take hours
- This is normal - the test is thorough
- Can safely interrupt with Ctrl+C (cleanup happens automatically)

### "Test files still present"
- Scripts clean up automatically
- If interrupted, manually remove: `rm /mnt/*.h2w`

### "Can't save files during test"
- Drive is full during testing
- Wait for test to complete
- Or interrupt test to free space

---

## Best Practices

### 1. Test New Drives Immediately
Run a full capacity test on any new USB drive before trusting it with important data.

### 2. Quick Tests for Regular Checks
Use quick tests for monthly or quarterly health checks.

### 3. Full Test Before Important Use
Run a full test before using a drive for critical backups or data transfer.

### 4. Watch for Warnings
Pay attention to f3 output - any "Data LOST" warnings indicate problems.

### 5. Know Your USB Port Speed
- USB 2.0: Slower tests (~20-40 MB/s)
- USB 3.0+: Faster tests (~100-300 MB/s)

---

## Safety Guarantees

✅ **Your existing files are never deleted or modified**
✅ **Automatic cleanup of test files**
✅ **Can interrupt safely with Ctrl+C**
✅ **No formatting or partitioning**
✅ **Read-only to existing data**

---

## Summary

### Bash Script
- One simple capacity test option
- Uses f3write + f3read
- Fills all free space
- Preserves existing files

### Python Script  
- **Quick test**: 5 GB default, fast check
- **Full test**: All free space, thorough check
- Both preserve existing files
- Choose based on time vs thoroughness needs

**Remember:** f3 tools are designed to be safe for your data while thoroughly testing your drive's capacity!

---

**Version**: 2.1
**Last Updated**: January 17, 2026
