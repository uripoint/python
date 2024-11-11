import pytest
from uripoint import process_video
import os

def test_process_video_input_exists():
    """Test that process_video handles existing input file."""
    # Create a mock video file for testing
    test_video_path = "test_video.mp4"
    try:
        # In a real scenario, you'd create or use an actual test video
        with open(test_video_path, 'wb') as f:
            f.write(b'Mock video content')
        
        # Test processing
        result = process_video(test_video_path)
        assert result is not None, "process_video should return a result"
    finally:
        # Clean up test file
        if os.path.exists(test_video_path):
            os.remove(test_video_path)

def test_process_video_nonexistent_file():
    """Test that process_video handles non-existent files."""
    with pytest.raises(FileNotFoundError):
        process_video("nonexistent_video.mp4")

def test_process_video_invalid_input():
    """Test that process_video handles invalid input types."""
    with pytest.raises(TypeError):
        process_video(None)
