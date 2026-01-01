"""
Quick test to verify warning suppression works
"""
import sys
import io
from contextlib import redirect_stderr

# Test the FilteredStderr class logic
class FilteredStderr:
    def __init__(self, original):
        self.original = original
    def write(self, message):
        msg_lower = message.lower()
        if 'development server' not in msg_lower and 'wsgi' not in msg_lower and 'production deployment' not in msg_lower:
            self.original.write(message)
    def flush(self):
        self.original.flush()
    def __getattr__(self, name):
        return getattr(self.original, name)

# Test messages
test_warning = "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead."
test_normal = "Server starting on http://localhost:5000\n"

print("Testing warning filter...")
print("="*50)

original_stderr = sys.stderr
sys.stderr = FilteredStderr(original_stderr)

print("\n1. Writing warning message (should be filtered):")
sys.stderr.write(test_warning)
sys.stderr.flush()

print("\n2. Writing normal message (should pass through):")
sys.stderr.write(test_normal)
sys.stderr.flush()

sys.stderr = original_stderr

print("\n" + "="*50)
print("Test complete! If you only see '2. Writing normal message' above,")
print("then the filter is working correctly.")

